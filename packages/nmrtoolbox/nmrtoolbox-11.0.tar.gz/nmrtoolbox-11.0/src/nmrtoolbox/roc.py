#!/usr/bin/env python3
import copy
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.spatial import distance_matrix
from itertools import combinations

from nmrtoolbox.peak import Peak, PeakTable
from nmrtoolbox.util import ROI
from nmrtoolbox.mask import Mask


class RocData:
    """Define a single ROC data point"""

    class Category:
        """allowed types of ROC data points"""
        true = 'true positive'
        false = 'false positive'
        corner = 'corner'

        def allowed(self):
            return self.true, self.false, self.corner

    def __init__(
            self,
            category: str,
            RR: float,
            FDR: float,
            recovered_peak=None,
            synthetic_peak=None,
    ):

        self.category = category
        if category not in self.Category().allowed():
            raise ValueError('invalid category type for ROC data point')

        self.RR = RR
        self.FDR = FDR
        if not (0 <= RR <= 1):
            raise ValueError('RR must be in range [0,1]')
        if not (0 <= FDR <= 1):
            raise ValueError('FDR must be in range [0,1]')

        # validation for inputs on RECOVERED peak
        #   required for category: true, false
        #   must be none for category: corner
        self.recovered_peak = recovered_peak
        if category in (RocData.Category.true, RocData.Category.false):
            if recovered_peak is None:
                raise ValueError('must provide recovered_peak')
            if not isinstance(recovered_peak, Peak):
                raise TypeError("recovered_peak must be of type Peak")
        elif category == RocData.Category.corner:
            if recovered_peak is not None:
                raise ValueError('cannot provide recovered_peak')

        # validation for inputs on SYNTHETIC peak
        #   required for category: true
        #   must be none for category: corner, false
        self.synthetic_peak = synthetic_peak
        if category == RocData.Category.true:
            if synthetic_peak is None:
                raise ValueError('must provide synthetic_peak')
            if not isinstance(synthetic_peak, Peak):
                raise TypeError("synthetic_peak must be of type Peak")
        elif category in (RocData.Category.false, RocData.Category.corner):
            if synthetic_peak is not None:
                raise ValueError('cannot provide synthetic_peak')


class roc:
    """
    A class for performing receiver operator characteristic (ROC) analysis on NMR peak lists
    """

    def __init__(
            self,
            recPeaks,
            synPeaks,
            lw_scalar=1,
            number=None,
            height=None,
            abs_height=None,
            roi_list: list = None,
            index=None,
            cluster_type=None,
            mask=None,
            mask_file=None,
            box_radius=2,
            chi2prob=None,
            outlier=None,
            vol_height_mismatch=False,
            maxLW_percent_SW=None,
    ):
        """
        :param recPeaks: table (file) of recovered peaks from NMRPipe->pkDetect3D.tcl
        :param synPeaks: table (file) of synthetic peaks from NMRPipe->genSimTab.tcl
        :param lw_scalar: scalar of a synthetic peak's linewidth to define a region in which a recovered peak is valid
        :param number: number of peaks to keep according to absolute value of peak HEIGHT
        :param height: keep all peaks with at least this HEIGHT
        :param abs_height: keep all peaks with absolute value at least this HEIGHT
        :param roi_list: region of interest to filter the recovered_peaklist
            specified as a list of lists: [key, dimension, ppm1, ppm2]
            example: [['HN', 'X', 10.297, 5.798], ['15N', 'Y', 129.088, 107.113]]
        :param index: keep only peaks with given index values
        :param cluster_type: keep only peaks with given cluster type index
            NMRPipe currently uses: 1 = Peak, 2 = Random Noise, 3 = Truncation artifact
        :param mask: nmrtoolbox.Mask object defining the empty region of a spectrum.  used to isolate regions where
            synthetic peaks may be inserted
        :param mask_file: mask data in the tabular file format from ConnjurST
        :param box_radius: defines size of box around peak position when querying it against empty mask
        :param chi2prob: remove peaks whose widths are outliers along any of the dimensions using chi2 probability
            expressed as p-value on [0,1] interval
        :param outlier: +/- percentage of the mode LW of peaks along each dimension to exclude
        :param vol_height_mismatch: type boolean: keep only peaks that have a nonzero height and volume
            and whose sign(HEIGHT) and sign(VOL) are in agreement.
        :param maxLW_percent_SW: threshold for the maximum linewidth along each dimensions defined as a percentage of
            the spectral window; input given on range [0,1]
        """
        # This ROC class accepts filtering criteria as a convenience to users so they do not have to read in peak tables
        # and call filtering functions before running roc.  So process the inputs for the peak table files and the roi
        # and then call the peak.reduce command to handle the rest.

        # ================================================
        self.recPeaks = PeakTable.read(
            obj=recPeaks,
            dtype=PeakTable.dtype.pipeRecovered,
        )
        self.synPeaks = PeakTable.read(
            obj=synPeaks,
            dtype=PeakTable.dtype.pipeSynthetic,
            carrier_frequency=self.recPeaks.axis,
        )
        # ================================================
        # validate some aspects of the peak table metadata and then move on to filtering operations
        self._validate_input()

        # ================================================
        self.roi = None
        if roi_list is not None:

            try:
                # capture the roi as temp object in case it is not good
                roi_object = ROI(key_dimension_range=roi_list)
            except ValueError as e:
                raise ValueError(f'failed to read ROI - {e}')

            if roi_object.keys() != self.recPeaks.axis.keys():
                raise ValueError('ROI axes do not match those of recovered peak table')

            # after validation - capture the roi
            self.roi = roi_object

        # ================================================
        self.mask = None
        if mask is not None:
            if isinstance(mask, Mask):
                self.mask = mask
            else:
                raise TypeError('mask provided, but type is invalid')
        elif mask_file is not None:
            print('Reading mask file.  This may take a while...')

            self.mask_file = mask_file
            self.mask = Mask(file=self.mask_file)

        # ================================================
        # Get the max LW values used by genSimTab and then expand by a lw_scalar to define the distance along each axis
        # used to define if a recovered peak is within the accepted range of a synthetic peak to be considered a match.
        self.lw_scalar = lw_scalar
        self.peak_range_hz = np.array(self.synPeaks.axis.get_field('maxLW')) * self.lw_scalar

        # ================================================
        # run the reduce commands (if any parameters are not given to roc, then they are None and reduce skips them)
        self.recPeaks.reduce(number=number)
        self.recPeaks.reduce(height=height)
        self.recPeaks.reduce(abs_height=abs_height)
        self.recPeaks.reduce(roi=self.roi)
        self.recPeaks.reduce(index=index)
        self.recPeaks.reduce(cluster_type=cluster_type)
        self.recPeaks.reduce(
            mask=self.mask,
            box_radius=box_radius,
        )
        self.recPeaks.reduce(outlier=outlier)
        self.recPeaks.reduce(vol_height_mismatch=vol_height_mismatch)
        self.recPeaks.reduce(maxLW_percent_SW=maxLW_percent_SW)

        # ================================================
        if chi2prob is not None:
            # could do this directly with: self.recovered_peaks.reduce(chi2prob=chi2prob)
            # BUT: the commands of reduce are reproduced here so that intermediate data can be captured
            # and used for outlier plotting

            # save instances of ALL peaks before removing the outlier peaks
            self.recovered_peaks_all = copy.deepcopy(self.recPeaks)
            self.recovered_peaks_outliers = copy.deepcopy(self.recPeaks)

            # partition all peaks into outliers and not outliers
            idx_keep, idx_outlier = self.recPeaks.determine_outliers(chi2prob=chi2prob)
            self.recovered_peaks_outliers.reduce(index=idx_outlier)
            self.recPeaks.reduce(index=idx_keep)

        # ================================================
        # create a list of RocData objects (initialize to include the origin)
        self.roc_points = [
            RocData(
                category=RocData.Category.corner,
                RR=0,
                FDR=0,
            )
        ]
        self._recovery_rate()

        # compute metrics from ROC data
        self.AUC = self._AUC()
        self.DPC, self.DPC_index = self._DPC()
        self.MRMF = self._MRMF()

    def _validate_input(self):
        if self.synPeaks.axis.keys() != self.recPeaks.axis.keys():
            raise ValueError('The synthetic and recovered peak tables have different axis labels.')

        if hasattr(self, 'roi'):
            if self.synPeaks.axis.keys() != self.roi.keys():
                raise ValueError(
                    'The ROI definition does not have the same axis labels as the synthetic and recovered peak tables.')

        if self.synPeaks.num_peaks() == 0:
            raise ValueError('No recorded peaks in synthetic peak table')

        if self.recPeaks.num_peaks() == 0:
            raise ValueError('No peaks recovered by peak picker')

    def _recovery_rate(self):
        # ordering of peaks matters
        # sort the recovered peaks by height
        #   => the most intense recovered peaks have priority in being matched to closest synthetic peaks
        self.recPeaks.order_by_height()

        synthetic_peaks_hz = self.synPeaks.get_par(par="*_HZ")
        recovered_peaks_hz = self.recPeaks.get_par(par="*_HZ")

        # compute pairwise distances between recovered and synthetic peaks - to be used for defining matches
        #  Currently finding closest synthetic peak to each recovered peak with unweighted L2, but at least it is in
        #  Hz and not ppm.  Eventually, the closest match identified here is more accurately assessed below by taking
        #  the distance along each axis and comparing to a cutoff distance defined as multiple of linewidth.
        #  Q: Is it possible that unweighted L2 matches incorrect synthetic peak to a recovered peak?
        #  A: Maybe.  But...
        #       - it's probably a recovered peak that isn't even near a synthetic peak
        #       - running several recovered peak tables through this shows that both methods yield same result
        #       - compute times are roughly 100:1 ratio (weighted vs unweighted) but on the order of 5s vs .05s
        #  Conclusion: just use unweighted L2 for now - can always toggle over to weighted L2, but must define weights
        pairwise_dist = distance_matrix(recovered_peaks_hz, synthetic_peaks_hz)
        # pairwise_dist = pairwise_weighted_norm(
        #     A=recovered_peaks_hz,
        #     B=synthetic_peaks_hz,
        #     w=np.array([1] * self.recovered_peaks.num_dims()),
        # )

        # for each recovered peak find the closest synthetic peak
        idx_recovered2synthetic = np.argmin(pairwise_dist, axis=1)

        # running tallies used to compute the recovery rate and false discovery rate
        count_true = 0
        count_false = 0

        # start with all synthetic peaks and remove them as they are matched to a recovered peak
        idx_synthetic_peak_available = set(range(self.synPeaks.num_peaks()))

        for idx_recovered_peak, idx_synthetic_peak in enumerate(idx_recovered2synthetic):
            # distance along each axis from synthetic to nearest recovered peak
            distance_hz = np.abs(recovered_peaks_hz[idx_recovered_peak] - synthetic_peaks_hz[idx_synthetic_peak])

            # check if the closest synthetic peak is still available AND if it's inside the allowable neighborhood
            if (idx_synthetic_peak in idx_synthetic_peak_available) and (distance_hz <= self.peak_range_hz).all():
                count_true += 1
                category = RocData.Category.true
                synthetic_peak = self.synPeaks.get_peak(idx_synthetic_peak)

                # remove the synthetic peak from the pool (can't use it again!)
                idx_synthetic_peak_available.remove(idx_synthetic_peak)
            else:
                count_false += 1
                category = RocData.Category.false
                synthetic_peak = None

            self.roc_points.append(RocData(
                category=category,
                RR=count_true / self.synPeaks.num_peaks(),
                FDR=count_false / (count_false + count_true),
                recovered_peak=self.recPeaks.get_peak(idx_recovered_peak),
                synthetic_peak=synthetic_peak,
            ))

        # Appending the top right corner (extending the "plateau" of the ROC curve to reach the right edge)
        self.roc_points.append(RocData(
            category=RocData.Category.corner,
            RR=max([p.RR for p in self.roc_points]),
            FDR=1,
        ))

        # Appending the bottom right corner
        self.roc_points.append(RocData(
            category=RocData.Category.corner,
            RR=0,
            FDR=1,
        ))

    def RR(self):
        return np.asarray([p.RR for p in self.roc_points])

    def FDR(self):
        return np.asarray([p.FDR for p in self.roc_points])

    def _DPC(self):
        corner = np.array([[0, 1]])
        roc = np.column_stack((self.FDR(), self.RR()))
        dst = distance_matrix(corner, roc)

        dpc = np.min(dst)
        dpc_index = np.argmin(dst)

        return dpc, dpc_index

    def _AUC(self):
        """Area under the curve"""

        # reference: https://math.stackexchange.com/questions/492407/area-of-an-irregular-polygon
        n = len(self.roc_points)
        RR = self.RR()
        FDR = self.FDR()
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += FDR[i] * RR[j]
            area -= FDR[j] * RR[i]
        area = abs(area) / 2.0

        return area

    def _MRMF(self):
        """Maximum Recovery at Minimum False"""
        # construct an iterator that finds the first false positive and returns the previous index
        # use next() to only evaluate the iterator until the first result is found
        # provide len(self.FDR) as default in case no false positive is found
        idx = next((i - 1 for i, v in enumerate(self.FDR()) if v > 0), len(self.roc_points))

        # if the very first recovered peak is false, that would result in an invalid idx=-1 (catch that case)
        # otherwise return the recovery rate at the index
        if idx >= 0:
            return self.RR()[idx]
        else:
            return 0

    def print_stats(self):
        print(f"AUC: {self.AUC:5.4f}")
        print(f"DPC: {self.DPC:5.4f}")
        print(f"DPC_index: {self.DPC_index:d}")
        print(f"MRMF: {self.MRMF:5.4f}")

    def plot_outliers(self, file_out='outliers.pdf', show_figure=False):
        """Plot histograms of peak widths for all recovered peaks and for outliers vs keepers"""

        try:
            peak_width_all = self.recovered_peaks_all.get_par(par="*W")
            peak_width_keep = self.recPeaks.get_par(par="*W")
            peak_width_out = self.recovered_peaks_outliers.get_par(par="*W")
        except AttributeError:
            print('can only plot outlier data if you use chi2prob outlier filtering')
            return

        fig, axs = plt.subplots(3, 3, sharex='col', sharey='col')
        plt.suptitle('Histograms of recovered peak widths')
        # iterate through dimension indices (columns of the figure)
        for dim in [0, 1, 2]:
            # row 0: peak widths for ALL peaks on dimension
            ax = axs[0, dim]
            n, bins, patches = ax.hist([p[dim] for p in peak_width_all], bins=20)
            ax.set_xlim(.9*np.min(bins), 1.1*np.max(bins))
            ax.set_ylim(-0.1*np.max(n), 1.1*np.max(n))
            ax.set_title(self.recPeaks.axis.keys()[dim])

            # row 1: peak widths for KEEPERS on dimension
            ax = axs[1, dim]
            ax.hist([p[dim] for p in peak_width_keep], bins=bins)

            # row 2: peak widths for OUTLIERS on dimension
            ax = axs[2, dim]
            ax.hist([p[dim] for p in peak_width_out], bins=bins)

        for a in axs[-1, :]:
            a.set_xlabel('peak width\n[points]')
        axs[0, 0].set_ylabel('ALL\n[count]')
        axs[1, 0].set_ylabel('KEEPER\n[count]')
        axs[2, 0].set_ylabel('OUTLIER\n[count]')
        fig.tight_layout()

        Path(file_out).parent.absolute().mkdir(exist_ok=True)
        fig.savefig(file_out, format='pdf', dpi=1200)
        if show_figure:
            plt.show()
        plt.close()

    def plot_roc(self, file_out='ROC.pdf', show_figure=False):
        RR = self.RR()
        FDR = self.FDR()

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        plt.xlabel('False Discovery Rate', fontsize=14)
        plt.ylabel('Recovery Rate', fontsize=14)
        plt.plot(FDR[:-1], RR[:-1],
                 marker='o', mew=0, mfc=(0, 0, 1, .5), ms=6,   # marker properties
                 c='.7', lw=2,                          # line properties
                 label='ROC curve',
                 zorder=1)
        plt.xlim(-0.02, 1.02)
        plt.ylim(-0.02, 1.02)

        # put a big red dot on the point that is closest to perfect classifier
        plt.scatter(FDR[self.DPC_index], RR[self.DPC_index],
                    marker='s', c='red', s=30,
                    label='DPC reference',
                    zorder=2)

        # logic to control legend location so it doesn't overlap ROC data
        if self.AUC > .5:
            plt.legend(loc='lower right')
        else:
            plt.legend(loc='upper left')

        Path(file_out).parent.absolute().mkdir(exist_ok=True)
        fig.savefig(file_out, format='pdf', dpi=1200)
        if show_figure:
            plt.show()
        plt.close()

    def plot_peaks(self, dir_out=os.getcwd(), file_basename='peaks', show_figure=False):

        # TODO: this axis and dimension handling is very confusing
        num_dim = len(self.synPeaks.axis.keys())
        temp_slice_axes = combinations(list(range(1, num_dim + 1)), 2)
        slice_axes = [i for i in temp_slice_axes]

        synthetic_peaks_ppm = self.synPeaks.get_par(par="*_PPM")

        recovered_peaks_true_ppm = [p.recovered_peak.get_par('*_PPM') for p in self.roc_points if p.category == RocData.Category.true]
        recovered_peaks_false_ppm = [p.recovered_peak.get_par('*_PPM') for p in self.roc_points if p.category == RocData.Category.false]

        for dims in slice_axes:
            xdim = int(dims[0]) - 1
            ydim = int(dims[1]) - 1

            syn_xdim_ppm = [p[xdim] for p in synthetic_peaks_ppm]
            syn_ydim_ppm = [p[ydim] for p in synthetic_peaks_ppm]

            trueRecov_xdim_ppm = [p[xdim] for p in recovered_peaks_true_ppm]
            trueRecov_ydim_ppm = [p[ydim] for p in recovered_peaks_true_ppm]

            falseRecov_xdim_ppm = [p[xdim] for p in recovered_peaks_false_ppm]
            falseRecov_ydim_ppm = [p[ydim] for p in recovered_peaks_false_ppm]

            fig, ax = plt.subplots()
            fig.subplots_adjust(right=0.75)
            plt.xlabel(f"{self.recPeaks.axis.keys()[xdim]} Domain [ppm]")
            plt.ylabel(f"{self.recPeaks.axis.keys()[ydim]} Domain [ppm]")
            plt.scatter(trueRecov_xdim_ppm, trueRecov_ydim_ppm,
                        c='#C5C9C7', marker='s', label='True Recovered')
            plt.scatter(falseRecov_xdim_ppm, falseRecov_ydim_ppm,
                        c='k', marker='x', label='Falsely Recovered')
            plt.scatter(syn_xdim_ppm, syn_ydim_ppm,
                        c='g', marker='v', label='synthetic')
            plt.legend(loc=(1.02, 0.15), prop={'size': 8})
            plt.title("Categorization of recovered peaks relative to synthetic peaks",
                         fontsize=10)

            filename = f"{file_basename}_{xdim + 1}_{ydim + 1}.pdf"
            file_out = Path(dir_out) / filename
            Path(file_out).parent.absolute().mkdir(exist_ok=True)

            plt.savefig(file_out, format='pdf', dpi=1200)
            if show_figure:
                plt.show()
            plt.close()


def parse_args():
    parser = argparse.ArgumentParser(description='You can add a description here')
    parser.add_argument('--recovered_table', required=True)
    parser.add_argument('--synthetic_table', required=True)
    parser.add_argument('--lw_scalar', type=float,
                        help='scalar multiple of linewidth for synthetic peak to define valid region for recovered peak')
    parser.add_argument('--number', type=int,
                        help='number of peaks to keep (starting from most intense)')
    parser.add_argument('--height', type=float,
                        help='')
    parser.add_argument('--abs_height', type=float,
                        help='')
    parser.add_argument('--roi_list', nargs='*', type=float,
                        help='min and max values in ppm for each dimension (min1 max1 min2 max2 ...)')
    parser.add_argument('--index', nargs='*', type=int,
                        help='peak indices to keep (indexing by position in peak list, NOT by indexing embedded in peak file)')
    parser.add_argument('--cluster_type', choices=[1, 2, 3],
                        help='keep only peaks with given cluster type index. NMRPipe currently uses: 1 = Peak, 2 = Random Noise, 3 = Truncation artifact')
    parser.add_argument('--mask_file', type=str,
                        help='path to file containing the mask of the empty region (tabular format from ConnjurST')
    parser.add_argument('--box_radius', type=int,
                        help='size of box around peak position when querying it against empty mask')
    parser.add_argument('--chi2prob', type=float,
                        help='chi square probability [0-1] used to remove peaks with outlier width')
    parser.add_argument('--print_stats', action='store_true',
                        help='print all ROC metric values to stdout')
    parser.add_argument('--plot_roc', action='store_true',
                        help='generate the roc plot and save to file')
    parser.add_argument('--plot_outliers', action='store_true',
                        help='generate histogram of outlier peaks if chi2prob is used for outlier removal')
    parser.add_argument('--plot_peaks', action='store_true',
                        help='generate projections of synthetic and recovered peak positions and save to file')
    return parser.parse_args()


def main():
    # parse the arguments from command line input and execute the nuscon workflow
    args = parse_args()

    try:
        my_roc = roc(
            recPeaks=args.recovered_table,
            synPeaks=args.synthetic_table,
            lw_scalar=args.lw_scalar,
            number=args.number,
            height=args.height,
            abs_height=args.abs_height,
            roi_list=args.roi_list,
            index=args.index,
            cluster_type=args.cluster_type,
            mask_file=args.mask_file,
            box_radius=args.box_radius,
            chi2prob=args.chi2prob,
        )
        if args.print_stats:
            my_roc.print_stats()
        if args.plot_roc:
            my_roc.plot_roc()
        if args.plot_outlier:
            my_roc.plot_outliers()
        if args.plot_peaks:
            my_roc.plot_peaks()

    except (SystemExit, EnvironmentError, OSError) as e:
        print(e)
        sys.exit()
