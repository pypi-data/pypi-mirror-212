#! /usr/bin/env python

# the same contour levels are used across all plots, but some plots may not have data at a
# given contour level.  matplotlib throws an annoying error to stdout.
# expecting this to suppress warnings - doesn't work
# import warnings
# warnings.filterwarnings(
#     action="ignore",
#     module=r'matplotlib\..*',
# )

import copy
import argparse
import sys
from pathlib import Path
from collections import defaultdict
# from itertools import combinations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import nmrglue as ng

from nmrtoolbox.spectrum import Spectrum
from nmrtoolbox.peak import PeakTable
from nmrtoolbox.util import calc_rms, check_file_existence
from nmrtoolbox.roc import roc, RocData


class strip_plot:
    """
    A class for generating strip plots.
    The primary purpose is to work with synthetic peaks and spectral reconstructions, so that ROC analysis can be used
    to classify the recovered peaks.  The peaks are then shown in a series of strip plots and highlighted accordingly.
    """

    def __init__(
            self,
            recSpectrum,
            recPeaks=None,
            sumSpectrum=None,
            synPeaks=None,
            empSpectrum=None,
            empPeaks=None,
            roc_obj=None,
            peak_count=20,
            pairs_strips_per_plot=10,
            num_displayed_contours=8,
            force_delete=True,
            output_dir=Path.cwd(),
            max_strip_plot=10,
            file_prefix='',
            recSpectrumType=Spectrum.dtype.pipe,
            sumSpectrumType=Spectrum.dtype.pipe,
            empSpectrumType=Spectrum.dtype.pipe,
    ):
        # required input
        self.recSpectrum = Spectrum.read(obj=recSpectrum, dtype=recSpectrumType)

        # optional inputs
        # start with ROC parsing because if it is provided, then it includes synthetic and recovered peak tables
        if isinstance(roc_obj, roc):
            self.roc = roc_obj
            self.recPeaks = self.roc.recPeaks
            self.synPeaks = self.roc.synPeaks
            if (recPeaks is not None) or (synPeaks is not None):
                raise ValueError('ROC object includes synthetic and recovered peak tables. do not provide them as inputs')
        else:
            if recPeaks is not None:
                self.recPeaks = PeakTable.read(obj=recPeaks, dtype=PeakTable.dtype.pipeRecovered)
            if synPeaks is not None:
                self.synPeaks = PeakTable.read(obj=synPeaks, dtype=PeakTable.dtype.pipeSynthetic, carrier_frequency=self.recPeaks.axis)

        # optional inputs
        if sumSpectrum is not None:
            self.sumSpectrum = Spectrum.read(obj=sumSpectrum, dtype=sumSpectrumType)
        if empSpectrum is not None:
            self.empSpectrum = Spectrum.read(obj=empSpectrum, dtype=empSpectrumType)
        if empPeaks is not None:
            self.empPeaks = PeakTable.read(obj=empPeaks, dtype=PeakTable.dtype.pipeEmpirical)

        # capture input parameters
        self.peak_count = peak_count
        self.pairs_strips_per_plot = pairs_strips_per_plot
        self.num_displayed_contours = num_displayed_contours
        self.force_delete = force_delete
        self.output_dir = output_dir
        self.max_strip_plot = max_strip_plot
        self.file_prefix = file_prefix
        self.peak_count = min(self.peak_count, self.max_strip_plot * self.pairs_strips_per_plot)

        # now try to plot all the possible comparisons and rely on AttributeError to abort when data is not available
        try:
            self._plot_roc()
        except AttributeError:
            pass
        try:
            self._plot_syn_v_rec()
        except AttributeError:
            pass
        try:
            self._plot_rec_v_syn()
        except AttributeError:
            pass
        try:
            self._plot_emp_v_rec()
        except AttributeError:
            pass


        # TODO: Consider additional scenarios of accidental single entry lists provided, etc ...
        if isinstance(recSpectrum, list) and len(recSpectrum) > 1:
            if isinstance(recPeaks, list):
                if len(recSpectrum) != len(recPeaks):
                    raise ValueError(
                        'The number of recovered spectrum must match that of the number of recovered peak tables.')
            self._plot_list_input()

    def _determine_roc_plateau(self):
        rr = [p.RR for p in self.roc.roc_points]
        return rr.index(max(rr))

    def _plot_roc(self):
        # With the roc object, determine the peak table indices for each of the true and false positive peaks.
        # The indices of false negative peaks is determined by taking the differences of sets as follows
        # set(synthetic peaks) - [set(TP) union set(FP)]
        index_true_recovery_peaks = [p.recovered_peak.get_par('INDEX') for p in self.roc.roc_points
                                     if p.category == RocData.Category.true]
        false_negative_indices = list(
            set([peak.get_par('INDEX') for peak in self.roc.synPeaks.peaks]).difference(
                set([p.synthetic_peak.get_par('INDEX') for p in self.roc.roc_points if p.synthetic_peak is not None])))
        false_negative_synthetic_peaks = [p for p in self.roc.synPeaks.peaks
                                         if p.get_par('INDEX') in false_negative_indices]

        # false_negative_reference_peak_table = copy.deepcopy(self.recTable)
        false_negative_reference_peak_table = copy.deepcopy(self.synPeaks)
        false_negative_reference_peak_table.peaks = false_negative_synthetic_peaks
        _false_negative_reference_peak_count = len(false_negative_reference_peak_table.peaks)
        fn_ref_peak_count = min(_false_negative_reference_peak_count, self.max_strip_plot * self.pairs_strips_per_plot)

        # Often, peak tables have thousands of excess peaks especially if peak picking close to the noise.
        # To exclude these peaks at the level of noise, only plot 1 more than the last peak at the maximum
        # recovery rate (RR). Note, poor reconstructions/peak picking can result in numerous false positives before
        # the max(RR). In this case, this upper bound "_precision_peak_count" could be an excessively large number.
        _precision_peak_count = self._determine_roc_plateau() + 1

        # In the aforementioned case of excessive number of FPs, address this by setting the maximum number of
        # strip plots displayed to be either the number of peaks giving rise to the max(RR) + 1 or the maximum
        # number of strip plots * pairs per plot.
        precision_peak_count = min(_precision_peak_count, self.max_strip_plot * self.pairs_strips_per_plot)

        # Plot the strips corresponding to TP and FP recovered peaks as determined by ROC
        # for the reconstructed and empirical + synthetic spectra
        _strip_plot(
            reference_spectrum=self.sumSpectrum,
            candidate_spectrum=self.recSpectrum,
            candidate_peak_table=self.recPeaks,
            output_dir=self.output_dir,
            recovery_indices=index_true_recovery_peaks,
            peak_count=precision_peak_count,
            pairs_strips_per_plot=self.pairs_strips_per_plot,
            num_displayed_contours=self.num_displayed_contours,
            force_delete=self.force_delete,
            plot_filename=f'{self.file_prefix}_strip_ROC_TP_FP',
            strip_plot_legend='Pairs of Strip Plots: \n   L = NUS Reconstructed (Synthetic + Empirical) \n   R = FT (Synthetic + Empirical)',
            plot_title='NUS Reconstructed Peaks Classified by ROC as True Positive or False Positive'
        )

        # If there are no false negative peaks, then do not call strip plotter.
        if len(false_negative_reference_peak_table.peaks) > 0:
            _strip_plot(
                reference_spectrum=self.recSpectrum,
                candidate_spectrum=self.sumSpectrum,
                candidate_peak_table=false_negative_reference_peak_table,
                output_dir=self.output_dir,
                peak_count=fn_ref_peak_count,
                pairs_strips_per_plot=self.pairs_strips_per_plot,
                num_displayed_contours=self.num_displayed_contours,
                force_delete=self.force_delete,
                plot_filename=f'{self.file_prefix}_strip_ROC_FN',
                strip_plot_legend='Pairs of Strip Plots: \n   L = FT (Synthetic + Empirical)\n   R = NUS Reconstructed (Synthetic + Empirical)',
                plot_title='Synthetic Peaks Not Recovered'
            )

    def _plot_rec_v_syn(self):
        # If no ROC objected was passed as an input, plot a qualitative comparison of the most intense
        # recovered peaks in the reconstructed spectrum vs the empirical + synthetic spectrum.
        _strip_plot(
            reference_spectrum=self.sumSpectrum,
            candidate_spectrum=self.recSpectrum,
            candidate_peak_table=self.recPeaks,
            output_dir=self.output_dir,
            peak_count=self.peak_count,
            pairs_strips_per_plot=self.pairs_strips_per_plot,
            num_displayed_contours=self.num_displayed_contours,
            force_delete=self.force_delete,
            plot_filename=f'{self.file_prefix}_strip_reconstructed_largest',
            strip_plot_legend='Pairs of Strip Plots: \n   L = NUS Reconstructed (Synthetic + Empirical) \n   R = FT (Synthetic + Empirical)',
            plot_title='Most Intense Peaks from NUS Reconstruction and Corresponding Positions in FT Spectrum'
        )

    def _plot_syn_v_rec(self):
        # Again, in the absence of a ROC analysis, create a qualitative comparison of
        # reconstructed and empirical + synthetic peaks but this time at the locations of synthetic peaks
        _strip_plot(
            reference_spectrum=self.recSpectrum,
            candidate_spectrum=self.sumSpectrum,
            candidate_peak_table=self.synPeaks,
            output_dir=self.output_dir,
            peak_count=self.peak_count,
            pairs_strips_per_plot=self.pairs_strips_per_plot,
            num_displayed_contours=self.num_displayed_contours,
            force_delete=self.force_delete,
            plot_filename=f'{self.file_prefix}_strip_synthetic_largest',
            strip_plot_legend='Pairs of Strip Plots: \n   L = FT (Synthetic + Empirical)\n   R = NUS Reconstructed (Synthetic + Empirical)',
            plot_title='Most Intense Synthetic Peaks and Corresponding Positions in NUS Reconstructed Spectrum'
        )

    def _plot_emp_v_rec(self):
        _strip_plot(
            reference_spectrum=self.recSpectrum,
            candidate_spectrum=self.empSpectrum,
            candidate_peak_table=self.empPeaks,
            output_dir=self.output_dir,
            peak_count=self.peak_count,
            pairs_strips_per_plot=self.pairs_strips_per_plot,
            num_displayed_contours=self.num_displayed_contours,
            force_delete=self.force_delete,
            plot_filename=f'{self.file_prefix}_strip_empirical_largest',
            strip_plot_legend='Pairs of Strip Plots: \n   L= FT (Empirical)\n   R = NUS Reconstructed (Synthetic + Empirical)',
            plot_title='Most Intense Empirical Peaks and Corresponding Positions in NUS Reconstructed Spectrum'
        )

    def _plot_list_input(self):

        raise ValueError('this has not been integrated into the code yet')
        # self.recPeaks = []
        # for rec_table in recTable:
        #     if isinstance(rec_table, PeakTable):
        #         pass
        #     else:
        #         self.recPeaks.append(PeakTable.read(
        #             obj=rec_table,
        #             dtype=PeakTable.dtype.pipeRecovered,
        #         ))
        # self.recSpectrum = recSpectrum
        #
        # for rec_1, rec_2 in list(combinations(range(len(self.recSpectrum)), 2)):
        #     # Create strip plots comparing two reconstructions at peaks of the 1st reconstruction
        #     strip_plot(
        #         reference_spectrum=self.recSpectrum[rec_2],
        #         candidate_spectrum=self.recSpectrum[rec_1],
        #         candidate_peak_table=self.recPeaks[rec_1],
        #         output_dir=output_dir,
        #         peak_count=self.peak_count,
        #         pairs_strips_per_plot=pairs_strips_per_plot,
        #         num_displayed_contours=num_displayed_contours,
        #         force_delete=force_delete,
        #         plot_filename=f'{file_prefix}_qualitative_comparison_recon{rec_1}_and_recon{rec_2}',
        #         strip_plot_legend=f'Pairs of Strip Plots: \n   L = Reconstructed #{rec_1}\n   R = Reconstructed #{rec_2}',
        #         plot_title=f'Qualitative Assessment Comparing Absolute Most Intense Recovered Peaks of Reconstruction #{rec_1}'
        #     )
        #
        #     # Create strip plots comparing two reconstructions at peaks of the 2nd reconstruction
        #     strip_plot(
        #         reference_spectrum=self.recSpectrum[rec_1],
        #         candidate_spectrum=self.recSpectrum[rec_2],
        #         candidate_peak_table=self.recPeaks[rec_2],
        #         output_dir=output_dir,
        #         peak_count=self.peak_count,
        #         pairs_strips_per_plot=pairs_strips_per_plot,
        #         num_displayed_contours=num_displayed_contours,
        #         force_delete=force_delete,
        #         plot_filename=f'{file_prefix}_qualitative_comparison_recon{rec_2}_and_recon{rec_1}',
        #         strip_plot_legend=f'Pairs of Strip Plots: \n   L = Reconstructed #{rec_2}\n   R = Reconstructed #{rec_1}',
        #         plot_title=f'Qualitative Assessment Comparing Absolute Most Intense Recovered Peaks of Reconstruction #{rec_2}'
        #     )
        #
        # if empSpectrum is not None:
        #     # For each of the reconstructions, compare
        #     # 1) recovered peaks of the reconstructed spectrum to the empirical spectrum
        #     # 2) the most intense peaks in the empirical spectrum against that reconstructed spectrum for artifacts
        #     for idx_rec, rec_spec in enumerate(self.recSpectrum):
        #         strip_plot(
        #             reference_spectrum=self.empSpectrum,
        #             candidate_spectrum=self.recSpectrum[idx_rec],
        #             candidate_peak_table=self.recPeaks[idx_rec],
        #             output_dir=output_dir,
        #             peak_count=self.peak_count,
        #             pairs_strips_per_plot=pairs_strips_per_plot,
        #             num_displayed_contours=num_displayed_contours,
        #             force_delete=force_delete,
        #             plot_filename=f'{file_prefix}_qualitative_comparison_recon{idx_rec}_and_empirical',
        #             strip_plot_legend=f'Pairs of Strip Plots: \n   L = Reconstructed #{idx_rec}\n   R = Empirical',
        #             plot_title=f'Qualitative Assessment of Absolute Most Intense Recovered Peaks of Reconstruction #{idx_rec}'
        #         )
        #
        #         strip_plot(
        #             reference_spectrum=self.recSpectrum[idx_rec],
        #             candidate_spectrum=self.empSpectrum,
        #             candidate_peak_table=self.empPeaks,
        #             output_dir=output_dir,
        #             peak_count=self.peak_count,
        #             pairs_strips_per_plot=pairs_strips_per_plot,
        #             num_displayed_contours=num_displayed_contours,
        #             force_delete=force_delete,
        #             plot_filename=f'{file_prefix}_qualitative_comparison_empirical_and_recon{idx_rec}',
        #             strip_plot_legend='Pairs of Strip Plots: \n   L = Empirical\n   R = Reconstructed',
        #             plot_title='Qualitative Assessment of Artifacts Introduced at Absolute Most Intense Empirical Peaks'
        #         )
        #
        # print('All combinations of reconstruction in provided list and if, provided empirical spectrum their '
        #       'combinations as well, have been generated. If strip plots utilizing ROC data for true positive '
        #       'and false negative peak categorization is desired, then provide a single reconstructed spectrum with'
        #       'its peak table and ROC python object.')
        # sys.exit(0)


class _strip_plot:
    """
    A helper class for creating strip plots, comparing reference and contestant reconstructions
    You shouldn't call this helper class directly.
    You should call strip_plot(), which will call this helper to generate all possible figures for the data you provide.
    """

    def __init__(
            self,
            reference_spectrum: Spectrum,
            candidate_spectrum: Spectrum,
            candidate_peak_table: PeakTable,
            output_dir,
            strip_plot_legend,
            plot_title,
            plot_filename='strip_plot_',
            recovery_indices=None,
            peak_count=20,
            pairs_strips_per_plot=10,
            num_displayed_contours=8,
            force_delete=True,
    ):
        """
        :param reference_spectrum: spectrum being compared to at the locations of peaks in the candidate_peak_table
        :param candidate_spectrum: spectrum whose peak table is defining the location of strip plots for comparison
        :param candidate_peak_table: peak table whose peaks will define the location of strips
        :param output_dir: location to save strip plots
        :param strip_plot_legend: string input to define what spectrum is to the L/R in each of the strips
        :param plot_title: title for each of the strip plots
        :param plot_filename: filename_{increment} used to save each of the strip plots
                up until ceil(peak_count/pairs_strips_per_plot)
        :param recovery_indices: indices of peaks in the candidate_peak_table.
                If provided, a peak with index in recovery_indices is labeled on the strip plot as being a true positive,
                otherwise it is labeled as a false positive.
        :param peak_count: maximum number of peaks in the candidate_spectrum to create strip plots
        :param pairs_strips_per_plot: number of pairs of strips to plot in a figure
        :param num_displayed_contours: number of contours to display for each the positive and negative intensities
        :param force_delete: if the same plot_filename_{increment} is found in the output_dir,
                then it will be overwritten
        """
        if isinstance(reference_spectrum, Spectrum):
            self.reference_spectrum = reference_spectrum
        else:
            raise TypeError(f'reference_spectrum must be Spectrum data type, not {type(reference_spectrum)}')
        if isinstance(candidate_spectrum, Spectrum):
            self.candidate_spectrum = candidate_spectrum
        else:
            raise TypeError(f'candidate_spectrum must be Spectrum data type, not {type(candidate_spectrum)}')
        if isinstance(candidate_peak_table, PeakTable):
            self.candidate_peak_table = candidate_peak_table
        else:
            raise TypeError(f'candidate_peak_table must be PeakTable data type, not {type(candidate_peak_table)}')

        self.outdir = Path(output_dir)
        self.filename = plot_filename
        self.force_delete = force_delete
        self.pspp = pairs_strips_per_plot
        self._legend_add_on = strip_plot_legend
        self.plot_title = plot_title

        # Peak count is used to define reduce the size of peak table as well as
        # to capture the last of the peaks to plot and save the figure.
        self.peak_count = peak_count

        self.recovery_indices = recovery_indices

        # # Note: When nmrglue reads in a spectrum, internally it does the following to the axes (X, Y, Z) --> (Z, Y, X)
        # self.candidate_dic, self.candidate_data = ng.pipe.read_lowmem(candidate_spectrum)
        # self.reference_dic, self.reference_data = ng.pipe.read_lowmem(reference_spectrum)

        # Create a dictionary of unit conversions.
        # This will be later used in plotting the two spectra at the same peak location
        self.ref_uc = {x: ng.pipe.make_uc(self.reference_spectrum.dic,
                                          self.reference_spectrum.data,
                                          x)
                       for x in range(len(self.candidate_peak_table.axis.dimensions()))}

        self.cand_uc = {x: ng.pipe.make_uc(self.candidate_spectrum.dic,
                                           self.candidate_spectrum.data,
                                           x)
                        for x in range(len(self.candidate_peak_table.axis.dimensions()))}

        # TODO:
        #   PeakTable has an AxisData attribute.  Since the PeakTable is not provided for reference spectrum,
        #   we can just create an AxisData object to contain metadata we can derive.
        #   Here's what AxisData usually contains
        #       - dimension
        #       - num_pts
        #       - range <-- this should contain the upfield/downfield limits of each axis
        #       - carrier_frequency
        #       - LW
        self.ref_upfield = {k: self.ref_uc[k]._first + self.ref_uc[k]._delta *  self.ref_uc[k]._size
                            for k in self.ref_uc.keys()}
        self.ref_downfield = {k: self.ref_uc[k]._first for k in self.ref_uc.keys()}

        # Determine the axes mapping between spectral data and peak tables
        self.axis_order = self._determine_axis_ordering()

        self._determine_contour(num_displayed_contours)
        self.candidate_peak_table.reduce(number=self.peak_count)

        self.strip_xwidths = self.calcXWidth()
        self.create_strips()


    def _determine_axis_ordering(self):
        """
        Because the ordering of axes cannot be assumed equivalent between candidate and reference spectra
        as well as their peak tables, their relative ordering must be determined.
        :return: a dictionary of dictionaries whose outermost keys are 'ref' or 'cand'.
                The innermost keys are the 0-indexed dimensions/axes (i.e., 0 -> X, 1 -> Y, and 2 -> Z)
                whose values are the 0-indexed dimensions of the respective spectrum.
        """

        dct = defaultdict(lambda: defaultdict(int))
        unassigned_cand_keys = []

        # Luckily, candidate_peak_table is a nmrtoolbox object that has a peaktable class.
        # This peaktable class carries its axes information as an AxisData class object.
        # Using AxisData, we will attempt to populate our lookup table by checking for unique pairs of spectral range
        # and number of increments between the candidate peaktable and spectra.
        for i, (pts, ppm_bounds) in enumerate(
                zip(self.candidate_peak_table.axis.get_field('num_pts'),
                    self.candidate_peak_table.axis.get_field('range'))):
            ii = [cand_key for cand_key, cand_val in self.cand_uc.items() if pts == cand_val._size]
            jj = [cand_key for cand_key, cand_val in self.cand_uc.items() if
                  abs(ppm_bounds.min - cand_val._first) / cand_val._first < 0.001]
            try:
                unique_axis_idx = list(set(ii) & set(jj))[0]
                dct['cand'][i] = unique_axis_idx
            except IndexError:
                unassigned_cand_keys.append(i)

        # If our nifty trick is unsuccessful in creating a complete lookup table,
        # then we will attempt to match any unassigned axes by checking for matching carrier frequencies.
        # If this does not fully assign the lookup table, exit with an error message.
        if len(unassigned_cand_keys) > 0:
            kk = [cand_key for cand_key, cand_val in self.cand_uc.items() if np.abs((self.candidate_peak_table.axis.get_field('carrier_frequency')[0] - 10**6 * cand_val._obs) / self.candidate_peak_table.axis.get_field('carrier_frequency')[0]) < 0.001]
            ll = list(dct['cand'].values())
            if len(kk) == 1 and set(self.cand_uc.keys()).difference(set(ll)) == set(kk):
                dct['cand'][unassigned_cand_keys[0]] = kk[0]
            else:
                raise SystemExit('The look up table between axes of the provided candidate peak table and spectrum cannot'
                                 'be completed as of this code"s current automated method.')

        # With the easier task of creating a lookup table for the candidate spectrum, we now compare spectral properties
        # between the candidate and reference spectrum to utilize the candidate lookup table.
        inverted_cand_dct = {v: k for k, v in dct['cand'].items()}
        unassigned_ref_keys = []
        for ref_key, ref_val in self.ref_uc.items():
            ii = [cand_key for cand_key, cand_val in self.cand_uc.items() if
                  all(np.asarray([np.abs(ref_val._car - cand_val._car)/ref_val._car, np.abs(ref_val._first - cand_val._first)/ref_val._first]) < 0.001)]
            try:
                dct['ref'][inverted_cand_dct[ii[0]]] = ref_key
            except IndexError:
                unassigned_ref_keys.append(ref_key)

        # If comparing spectral carrier frequencies and ppm/increment did not fully assign the reference spectrum's
        # lookup table, then in the event that there is a single dimension unassigned give it the last remaining
        # possible assignment.
        # I have not encounter a case where there were more than 1 unassigned dimensions.
        # If this is the case, exit with an error message.
        if len(set(self.cand_uc.keys()) - set(list(dct['ref'].values()))) == 1 and len(unassigned_ref_keys) == 1:
            dct['ref'][inverted_cand_dct[list(set(self.cand_uc.keys()) - set(list(dct['ref'].values())))[0]]] = unassigned_ref_keys[0]

        # Ensure that each of the dimensions have been assigned in the reference lookup table
        if any([x != len(self.candidate_peak_table.axis.data) for x in [len(set(dct['ref'].keys())), len(set(dct['ref'].values()))]]):
            raise SystemExit('The lookup table for the reference spectrum could not be completed by comparing'
                             'the spectral properties of it and the candidate spectrum.')
        return dct


    def _determine_contour(self, contour_count):
        """
        A function to determine the separate positive and negative intensity contours
        :param contour_count: the number of contours for each the positive and negative contours
        :return: list of two
        """

        # Calculate the RMS from the FID at the longest evolution time point in the Nyquist grid.
        self.ref_noise = calc_rms(self.reference_spectrum.data[:][-1][-1])
        self.cand_noise = calc_rms(self.candidate_spectrum.data[:][-1][-1])

        # Find the maximum (positive) intensity in the two spectra
        # TODO: Discuss with Adam whether to also find the maximum (negative) intensity to use as the stop
        #  of the negative contours. Drawback would be that the positive and negative contours
        #  in the strip plot would be of differing intensities.
        ref_contour_stop = np.nanmax(self.reference_spectrum.data[:, :, :])
        cand_contour_stop = np.nanmax(self.candidate_spectrum.data[:, :, :])

        # Determine the intensities of the contours to display using logspacing from the estimated noise
        # to the maximum intensity. Do the same for the negative contours.
        # Number of logspacings is 1 + requested contour count, because the last logspacing is forced
        # to be the maximum provided and is subsequently excluded.
        self.cand_contour_levels = [np.logspace(start=np.log(self.cand_noise),
                                               stop=np.log(cand_contour_stop),
                                               num=contour_count+1, endpoint=True, base=np.e)[1:],
                                    np.logspace(start=np.log(1),
                                                stop=np.log(cand_contour_stop),
                                                num=contour_count+1,
                                                endpoint=True, base=np.e)[1:] * -1]
        self.ref_contour_levels = [np.logspace(start=np.log(self.ref_noise),
                                              stop=np.log(ref_contour_stop),
                                              num=contour_count+1, endpoint=True, base=np.e)[1:],
                                    np.logspace(start=np.log(1),
                                                stop=np.log(ref_contour_stop),
                                                num=contour_count+1,
                                                endpoint=True, base=np.e)[1:] * -1]


    def calcXWidth(self):
        # TODO: Future iterations might want to generalize this to be the average along any arbitrary dimension
        """
        Create chunks of peak parameters for the linewidth along the x-dimension.
        Chunk sizes are determined by self.pssp, i.e., the number of strip pairs per plot.
        :return: list of average peak widths for the x-dimension
        """

        # If the peak of interest has its full width at half height in points along X accessible, if so then use it.
        # Otherwise, peak width is determined using coordinates of the bounding region
        # surrounding the peak or its cluster in points.
        if 'XW' in self.candidate_peak_table.peaks[0].prop:
            peak_widths = [p.get_par('XW') for p in self.candidate_peak_table.peaks]
            scaled_xw = [np.abs(3.0 * p * self.cand_uc[self.axis_order['cand'][0]]._delta) for p in peak_widths]
        else:
            peak_widths = [p.get_par('X1') - p.get_par('X3') for p in self.candidate_peak_table.peaks]
            # TODO: Verify that this should be 'cand' and not 'ref'
            scaled_xw = [np.abs(1.0 * p * self.cand_uc[self.axis_order['cand'][0]]._delta) for p in peak_widths]

        peak_chunks = list(_chunk(scaled_xw, self.pspp))
        return list(map(np.mean, zip(*peak_chunks)))


    def create_strips(self):
        # Turn interactive plotting off
        plt.ioff()

        plot_number = 1
        # fig = plt.figure()
        # fig.suptitle(self.plot_title, fontsize=16)

        # min should be upfield value, but compute min/max on both upfield and downfield in case values are reversed
        min_ref_a2 = 0
        max_ref_a2 = self.ref_uc[self.axis_order['ref'][2]]._size - 1

        min_cand_a2 = 0
        max_cand_a2 = self.candidate_peak_table.axis.get_field('num_pts')[2] - 1

        cand_order = (self.axis_order['cand'][2], self.axis_order['cand'][1], self.axis_order['cand'][0])
        ref_order = (self.axis_order['ref'][2], self.axis_order['ref'][1], self.axis_order['ref'][0])


        # TODO: Adjust width of pairs of strip plots based on number of pairs to be displayed.
        #  E.g., for FN plotting when there is only a few pairs of strips to be plotted.
        for idx, peak in enumerate(self.candidate_peak_table.peaks):
            # Recall transposed axes in nmrglue, i.e., (Z, Y, X)

            if idx % self.pspp == 0:
                fig = plt.figure()
                fig.suptitle(self.plot_title, fontsize=16)

            # TODO: Discuss with Adam, fixing the strip plot widths
            # Determine what chunk this peak belongs in
            chunk_idx = int(np.floor(idx / (len(self.candidate_peak_table.peaks)) / self.pspp))
            x_width = self.strip_xwidths[chunk_idx]

            ### Reference spectrum ###
            # Recall, self.axis_order nested dictionaries is a lookup table
            # with key-value pairs are (dimension desired, dimension in the spectrum).

            # Suffixes are indicative of the desired dimension; e.g., idx_ref_a1 is the index of the peak in the
            # 1st dimension (O-indexed), namely the y-axis.

            # Here, we ue the lookup table in self.axis_order to correctly use the spectrum's "uc" (unit conversion)
            # for the desired dimension. These series of variable definitions are converting
            # the peak parameter from index (coordinates) to ppm.
            idx_ref_a1 = self.ref_uc[self.axis_order['ref'][1]](peak.get_par('Y_PPM'), "ppm")
            min_ref_a0 = self.ref_uc[self.axis_order['ref'][0]](peak.get_par('X_PPM') + x_width, "ppm")
            max_ref_a0 = self.ref_uc[self.axis_order['ref'][0]](peak.get_par('X_PPM') - x_width, "ppm")

            # Ensures width of strip plot does not exceed spectral bounds
            # TODO: Discussion with Mike; require understanding of how data was acquired (STATES, TPPI, STATE-TPPI)
            #  in order to determine folding pattern
            if min_ref_a0 < 0:
                min_ref_a0 = 0

            if max_ref_a0 > self.ref_uc[self.axis_order['ref'][0]]._size:
                max_ref_a0 = self.ref_uc[self.axis_order['ref'][0]]._size

            # extract strip
            # TODO: Option to sum across planes above and below
            strip_ref = self.reference_spectrum.data.transpose(ref_order)[min_ref_a2:max_ref_a2 + 1,
                        idx_ref_a1, min_ref_a0:max_ref_a0 + 1]

            # determine ppm limits of contour plot; x, y - axes of generated figure
            strip_ppm_x = self.ref_uc[self.axis_order['ref'][0]].ppm_scale()[min_ref_a0:max_ref_a0 + 1]
            strip_ppm_y = self.ref_uc[self.axis_order['ref'][2]].ppm_scale()[min_ref_a2:max_ref_a2 + 1]
            strip_x, strip_y = np.meshgrid(strip_ppm_x, strip_ppm_y)

            # define axes for left and right strips
            axL = fig.add_subplot(1, 2 * self.pspp + 1, 2 * idx + 1 - (plot_number - 1) * (2 * self.pspp))
            axR = fig.add_subplot(1, 2 * self.pspp + 1, 2 * idx + 2 - (plot_number - 1) * (2 * self.pspp))

            # move the right strip, so it has a lower left corner where the left strip has its lower right corner
            boxL = axL.get_position()
            boxR = axR.get_position()
            axR.set_position([boxL.x0 + boxL.width, boxR.y0, boxR.width, boxR.height])

            c1 = axR.contour(strip_x,
                        strip_y,
                        strip_ref,
                        self.ref_contour_levels[0],
                        colors='black',
                        linewidths=0.5,
                        linestyles='-')
            c2 = axR.contour(strip_x,
                        strip_y,
                        strip_ref,
                        self.ref_contour_levels[1][::-1],
                        colors='red',
                        linewidths=0.5,
                        linestyles='-')

            # If the peak of interest has its full width at half height in points along Z accessible, if so then use it.
            # Otherwise, peak width is determined using coordinates of the bounding region
            # surrounding the peak or its cluster in points.
            if 'ZW' in peak.prop:
                peak_width_a2_upfield = peak.get_par('Z_PPM') - 1.0 * abs(
                    (peak.get_par('ZW') * self.cand_uc[self.axis_order['cand'][2]]._delta))
                peak_width_a2_downfield = peak.get_par('Z_PPM') + 1.0 * abs(
                    (peak.get_par('ZW') * self.cand_uc[self.axis_order['cand'][2]]._delta))
            else:
                peak_width_a2_upfield = peak.get_par('Z_PPM') - 1.0 * abs(
                    ((peak.get_par('Z1') - peak.get_par('Z3')) * self.cand_uc[self.axis_order['cand'][2]]._delta))
                peak_width_a2_downfield = peak.get_par('Z_PPM') + 1.0 * abs(
                    ((peak.get_par('Z1') - peak.get_par('Z3')) * self.cand_uc[self.axis_order['cand'][2]]._delta))

            # This could be of use to identify artifacts with spectral widths exceeding that of the spectral window
            # TODO: If ever triggered, may be the case that aesthetically needs adjusted.
            #  Concern is that for spectrum with the larger spectral window there may be a gap,
            #  i.e., difference of their spectral windows, that is not shaded.
            # Note: nmrtoolbox.peak.axis Range class's "max" value is the upfield value,
            # though numerically it is the min ppm value
            if peak_width_a2_upfield < min(self.ref_upfield[self.axis_order['ref'][2]],
                                           self.candidate_peak_table.axis.get_field('range')[2].max):
                peak_width_a2_upfield = min(self.ref_upfield[self.axis_order['ref'][2]],
                                            self.candidate_peak_table.axis.get_field('range')[2].max)

            if peak_width_a2_downfield > max(self.ref_downfield[self.axis_order['ref'][2]],
                                             self.candidate_peak_table.axis.get_field('range')[2].min):
                peak_width_a2_downfield = max(self.ref_downfield[self.axis_order['ref'][2]],
                                              self.candidate_peak_table.axis.get_field('range')[2].min)

            # Use contour x-axis limits to define width of peak demarcation.
            # This use of existing contour boundaries ensures that there is no white space padding created.
            c4 = axR.fill_between(
                c2.axes.dataLim.intervalx,
                peak_width_a2_upfield,
                peak_width_a2_downfield,
                facecolor='silver',
                alpha=.5,
            )
            axR.invert_yaxis()
            axR.invert_xaxis()

            # turn off ticks and labels, add labels
            axR.tick_params(axis='y', labelbottom=False, bottom=False, top=False,
                            labelleft=False, left=False, right=False)

            # put a single tick at the center of the slice
            axR.set_xticks([peak.get_par('X_PPM')], labels=[''])

            ### Candidate spectrum ###
            idx_cand_a1 = self.cand_uc[self.axis_order['cand'][1]](peak.get_par('Y_PPM'), "ppm")
            min_cand_a0 = self.cand_uc[self.axis_order['cand'][0]](peak.get_par('X_PPM') + x_width, "ppm")
            max_cand_a0 = self.cand_uc[self.axis_order['cand'][0]](peak.get_par('X_PPM') - x_width, "ppm")

            # Ensures width of strip plot does not exceed spectral bounds
            # TODO: Discuss with Mike of how to handle this case wih wrapped spectral windows in mind
            # TODO: verify wanted min
            if min_cand_a0 < self.cand_uc[self.axis_order['cand'][0]](self.candidate_peak_table.axis.get_field('range')[0].min, "ppm"):
                min_cand_a0 = self.cand_uc[self.axis_order['cand'][0]](self.candidate_peak_table.axis.get_field('range')[0].min, "ppm")

            if max_cand_a0 > self.cand_uc[self.axis_order['cand'][0]](self.candidate_peak_table.axis.get_field('range')[0].max, "ppm"):
                max_cand_a0 = self.cand_uc[self.axis_order['cand'][0]](self.candidate_peak_table.axis.get_field('range')[0].max, "ppm")

            strip_cand = self.candidate_spectrum.data.transpose(cand_order)[min_cand_a2:max_cand_a2 + 1,
                         idx_cand_a1, min_cand_a0:max_cand_a0 + 1]

            # determine ppm limits of contour plot; x, y - axes of generated figure
            # x-axis -> direct dim (0-th index); y-axis -> 2nd-indirect dimension (n-th index)
            strip_ppm_x = self.cand_uc[self.axis_order['cand'][0]].ppm_scale()[min_cand_a0:max_cand_a0 + 1]
            strip_ppm_y = self.cand_uc[self.axis_order['cand'][2]].ppm_scale()[min_cand_a2:max_cand_a2 + 1]
            strip_x, strip_y = np.meshgrid(strip_ppm_x, strip_ppm_y)

            c3 = axL.contour(strip_x,
                        strip_y,
                        strip_cand,
                        self.cand_contour_levels[0],
                        colors='black',
                        linewidths=0.5,
                        linestyles='-')

            # No need to assign a legend for these contours as negative contours have already been assigned within the
            # ref strip plots
            axL.contour(strip_x,
                        strip_y,
                        strip_cand,
                        self.cand_contour_levels[1][::-1],
                        colors='red',
                        linewidths=0.5,
                        linestyles='-')

            # If provided with indices of candidate's peaktable that correspond to successfully recovered
            # peaks from the reference spectrum, assign the appropriate color shading
            if self.recovery_indices is not None:
                if peak.get_par('INDEX') in self.recovery_indices:
                    c5 = axL.fill_between(
                        c3.axes.dataLim.intervalx,
                        peak_width_a2_upfield,
                        peak_width_a2_downfield,
                        facecolor='green',
                        alpha=.5,
                    )
                else:
                    c6 = axL.fill_between(
                        c3.axes.dataLim.intervalx,
                        peak_width_a2_upfield,
                        peak_width_a2_downfield,
                        facecolor='red',
                        alpha=.5,
                    )
            else:
                c7 = axL.fill_between(
                    c3.axes.dataLim.intervalx,
                    peak_width_a2_upfield,
                    peak_width_a2_downfield,
                    facecolor='silver',
                    alpha=.5,
                )

            # Display the bounds and center of the x-axis and invert
            axL.set_xticks(
                [peak.get_par('X_PPM') - x_width, peak.get_par('X_PPM'), peak.get_par('X_PPM') + x_width])
            axL.invert_yaxis()
            axL.invert_xaxis()

            # turn off y-ticks and labels, add labels and assignment
            axL.tick_params(axis='y', labelbottom=False, bottom=False, top=False,
                            labelleft=False, left=False, right=False)

            # label chemical shift of the strip along second dimension - put at the top of the strip
            axL.set_title(
                label=f'{self.candidate_peak_table.axis.keys()[1]} [PPM] = {peak.get_par("Y_PPM")}',
                loc='left',
            )

            # label and put ticks on first strip plot
            if idx % self.pspp == 0:
                axL.set_ylabel(f"{self.candidate_peak_table.axis.keys()[2]} [PPM]")
                axL.tick_params(axis='y', labelleft=True, left=True, direction='out', labelsize=6)

            if (idx + 1) % self.pspp == 0 or idx == self.peak_count - 1:
                # fig.text(0.45, 0.05, f"{self.candidate_peak_table.axis.keys()[0]} [PPM]")
                fig.supxlabel(f"{self.candidate_peak_table.axis.keys()[0]} [PPM]")
                # TODO: Consider adding label to dimension being sliced, perhaps located above strips

                # Use contour plot handles to build out the legend
                h1, l1 = c1.legend_elements('')
                h2, l2 = c2.legend_elements('')

                # Create an empty space legend key whose value will be provided as input to strip_plot
                # for describing the ordered pairs of strips.
                extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)

                # consideration would need to be taken to make this more dynamic,
                # potentially for use in the case of handing nD spectra
                _labels = [self._legend_add_on, 'Positive Intensity', 'Negative Intensity', 'Reference Peak']
                _legend_handles = [extra, h1[0], h2[0], c4]
                if 'c5' in locals():
                    _legend_handles.append(c5)
                    _labels.append('True Recovery')
                if 'c6' in locals():
                    _legend_handles.append(c6)
                    _labels.append('False Recovery')

                fig.legend(_legend_handles, _labels)
                # In the event that you have all of one classification of TP/FP in a strip plot and the other
                # classification existed in the prior strip plot figure, its handle will point to an old figure
                # which will trigger a RuntimeError.
                if 'c5' in locals():
                    del c5
                if 'c6' in locals():
                    del c6

                fFormat = "pdf"
                fOut = f"{self.outdir}/{self.filename}_{plot_number}.{fFormat}"
                if check_file_existence(fOut):
                    if self.force_delete:
                        Path(fOut).unlink()
                        fig.set_size_inches(25.6, 12.4)
                        fig.savefig(fOut, format=fFormat, dpi=1200)
                    else:
                        print(f'No figure was saved because there is an existing figure saved as {fOut} ')
                else:
                    fig.set_size_inches(25.6, 12.4)
                    fig.savefig(fOut, format=fFormat, dpi=1200)

                plt.close(fig)
                plot_number += 1


def _chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def parse_args():
    # TODO: you are missing parameters here
    parser = argparse.ArgumentParser(description='You can add a description here')
    parser.add_argument('--reference_spectrum', required=True)
    parser.add_argument('--candidate_spectrum', required=True)
    parser.add_argument('--candidate_peak_table', required=True)
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('--true_recovery_indices', required=False)
    return parser.parse_args()


def main():
    # TODO:
    #   1) replace this with a call to screening_study_strip_plots (and update arg_parse accordingly)
    #   2) add --help flag and print useful info

    # parse the arguments from command line input and execute
    args = parse_args()

    try:
        my_strip_plot = _strip_plot(
            reference_spectrum=args.reference_spectrum,
            candidate_spectrum=args.candidate_spectrum,
            candidate_peak_table=args.candidate_peak_table,
            output_dir=args.output_dir,
            peak_count=20,
            pairs_strips_per_plot=10,
            num_displayed_contours=8,
            plot_title='test comparison',
            strip_plot_legend='Pairs of Strip Plots: \n   L = Candidate\n   R = Reference',
        )
    except (SystemExit, EnvironmentError, OSError) as e:
        print(e)
        sys.exit()
