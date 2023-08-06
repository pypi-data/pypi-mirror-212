import numpy as np
from scipy.stats import chi2
from pathlib import Path
import re
from enum import Enum
from nmrtoolbox.util import Range, ROI, AxisData, SpectrumData, PeakOutsideOfMaskError, ParsePeakTableError, is_iterable
from nmrtoolbox.mask import Mask


class Peak:
    """
    A container for the values that describe a peak.
    """
    def __init__(self, prop_list, val_list, axis_property):
        """
        Populate a peak

        :param prop_list: parameter names (from VARS line)
        :param val_list: parameter values (line from peak table)
        :param axis_property: AxisData object
        """
        if not (len(prop_list) == len(val_list)):
            raise ValueError('properties and values must be lists of the same length')

        # this is an AxisData object
        if isinstance(axis_property, AxisData):
            self.axis = axis_property
        else:
            raise TypeError('axis_property must be AxisData type')

        # use the character in the format string to convert each value accordingly
        self.prop = dict()
        for p, v in zip(prop_list, val_list):
            # try to convert the value to int or float; then accept it as string
            try:
                self.prop[p] = int(v)
                continue
            except ValueError:
                pass
            try:
                self.prop[p] = float(v)
                continue
            except ValueError:
                pass
            self.prop[p] = v

    def get_par(self, par, axis_dimensions='all'):
        """
        Get value of specified parameter for specified axes.

        :param par: nmrPipe peak table parameter name (e.g. *_PPM, HEIGHT)
                    The * is substituted with axis values for each label requested
        :param axis_dimensions: list of axis identifiers to include (e.g. 'X' or default of 'all')
        :return: singleton value or list of values
        """
        if '*' not in par:
            par_set = [par]
        else:
            par_set = []

            # determine which axes to query
            if axis_dimensions == 'all':
                axis_dimensions = self.axis.dimensions()
            if isinstance(axis_dimensions, str):
                axis_dimensions = [axis_dimensions]

            # perform substitutions of axis names into parameter name as needed
            for axis in axis_dimensions:
                if axis not in self.axis.dimensions():
                    raise KeyError(f'invalid axis: {axis}')
                par_set.append(par.replace('*', axis))

        out = []
        for par in par_set:
            try:
                out.append(self.prop[par])
            except KeyError:
                raise KeyError(f'property not found: {par}')

        if len(out) == 1:
            return out[0]
        else:
            return out

    def get_par_list(self):
        return list(self.prop.keys())

    def set_par(self, par, value):
        """
        Change or create a new parameter

        :param par: parameter name
        :param value: corresponding value
        :return:
        """
        self.prop[par] = value

    def print(self):
        """Print all the key/value pairs that define the peak"""
        for k, v in self.prop.items():
            print(f"{k:8s}: {v:>15}")

    def in_roi(self, roi: ROI):
        """
        Check if current peak is within the given ROI

        :param roi: ROI class object
        :return: bool
        """
        if not isinstance(roi, ROI):
            raise TypeError('region of interest must be provided as ROI class object')

        if roi.keys() != self.axis.keys():
            raise ValueError('the current peak and the given ROI do not have same set of axes')

        for axis in self.axis.keys():
            dimension = self.axis.axis2dimension(axis)
            roi_range = roi.get_field(name='roi', axis=axis)[0]
            peak_ppm = self.get_par(f'{dimension}_PPM')
            if not roi_range.contains(peak_ppm):
                return False
        return True

    def in_mask(self, mask: Mask, box_radius=2, print_outside_error=False):
        """
        determine if the peak position (and some neighborhood around it) is in empty region of mask
        """
        if not isinstance(mask, Mask):
            raise TypeError('empty region of spectrum must be provided as Mask class object')

        if mask.axis.keys() != self.axis.keys():
            raise ValueError('mask and peak have different axes')

        try:
            return mask.peak_in_mask(
                peak=self,
                box_radius=box_radius,
            )
        except PeakOutsideOfMaskError as e:
            if print_outside_error:
                print(e)
            return False


class PeakTable:

    class dtype(Enum):
        # define the types of peak tables that are valid inputs
        pipeRecovered = 'pipeRecovered'
        pipeSynthetic = 'pipeSynthetic'
        pipeEmpirical = 'pipeEmpirical'

    @classmethod
    def read(
            cls,
            obj,
            dtype,
            carrier_frequency=None,
    ):
        """
        Call this instead of init - it handles input that is either a PeakTable object or a path to peak table file
        :param obj: PeakTable object or file path to peak table data
        :param dtype: type of peak table data
        :return:
        """
        if isinstance(obj, PeakTable):
            return obj
        else:
            try:
                if dtype in (PeakTable.dtype.pipeRecovered, PeakTable.dtype.pipeEmpirical):
                    return PeakTablePipeRec(file=str(obj))
                elif dtype == PeakTable.dtype.pipeSynthetic:
                    return PeakTablePipeSyn(
                        file=str(obj),
                        carrier_frequency=carrier_frequency,
                    )
                else:
                    raise ValueError('unsupported type of peak table')
            except ParsePeakTableError as e:
                raise ParsePeakTableError(str(e))

    """
    A class for containing a collection of peaks (e.g. from a peak picker or synthetic peak generator)
    Sub-classes are defined for each peak table file format.
    """
    def __init__(self, file, **kwargs):
        """
        Populate a peak list.  Each type of peak list file is sub-classed from PeakTable.  The subclasses should have
        an __init__ that defines "pre" operations, calls super.__init__, defines "post" operations.  The __init__ here
        includes pre operations for ALL PeakTable subclasses and it includes a call to _parse_file (which should be
        defined within each subclass).  The subclass __init__ should then call _post to run operations that are defined
        for ALL PeakTable subclasses.  By creating an instance of a subclass, the following operations are performed:
            "pre" operations in subclass __init__
            "pre" operations in PeakTable __init__
            _parse_file (defined by subclass)
            "post" operations in PeakTable __init__
            "post" operations in subclass __init__
            _post (defined by PeakTable)

        Here is a template for subclass definition

        class SomeNewSubclass(PeakTable):
            def __init__(self, file):
                # pre
                <define instance variables used specifically by this subclass>

                # call PeakTable.__init__ which includes:
                #   (1) "pre" operations for all subclasses
                #   (2) _parse_file method, which is defined by the subclass
                super().__init__(file, **kwargs)

                # post
                <perform operations after table file is parsed that are specific to this subclass>
                self._post() <- perform operations after the table file is parsed that are for ALL subclasses

        :param file: peak table file
        """
        self.file = Path(file)
        if not self.file.is_file():
            raise FileNotFoundError('peak table does not exist: {}'.format(self.file))

        # list of Peak objects
        self.peaks = []

        # metadata for each axis (e.g. keys are X, Y, Z) - captured in an AxisData object:
        #   - labels (e.g.H1, N15)
        #   - num_pts
        #   - ppm_range (from ppm_high, ppm_low)
        self.axis = AxisData()

        # global properties that describe the collection of peaks
        self.table_property = SpectrumData()

        # subclasses will each call _parse_file() to populate self.peaks and self.axis_property
        # subclasses can optionally include "pre" and "post" tasks in their __init__ to perform before/after parsing

        try:
            self._parse_file()
        except NotImplementedError as e:
            raise ParsePeakTableError(e)
        except ValueError as e:
            raise ParsePeakTableError(f'failed to read peak table: {self.file}\n{e}')
        except Exception as e:
            raise ParsePeakTableError(f'failed to read peak table: {self.file}\n{e}')

        try:
            self._set_carrier_frequency(**kwargs)
        except (AttributeError, ValueError):
            raise
        except Exception as e:
            raise ParsePeakTableError(f'failed to set carrier frequency: {self.file}\n{e}')

        # chi2prob has to be the last filter applied to peak table so set the state here and all PeakTable.reduce
        # commands can check this state before applying other filters
        self.chi2prob_already_applied = False

    def _parse_file(self):
        """stub - subclasses must define this and populate self.peaks and self.axis"""
        raise NotImplementedError('sub-class must define a _parse_file() function')

    def _post(self):
        """operations to run after an instance of any subclass has been created"""
        try:
            self.get_par(par='*_HZ')
        except KeyError:
            try:
                self._set_peak_positions_hz()
            except KeyError:
                print('not able to compute peaks positions in Hz automatically')
                pass

    def _set_carrier_frequency(
            self, carrier_frequency=None, **kwargs):
        """
        Set the carrier frequency of the peak table.   Several types of input data are supported.
        :param carrier_frequency:
            If the input is omitted, then auto-determine CF from peak positions using ppm and hz values.
            If the input is an AxisData object (e.g. from another PeakTable) - then extract the CF values.
            Else - CF data can be given as a list of lists: [key, label, cf, cf_units]
        :param kwargs:
        :return:
        """

        if carrier_frequency is None:
            # try to auto-determine carrier frequency from ppm and Hz values
            try:
                self._set_carrier_frequency_from_ppm_hz()
            except KeyError as e:
                raise KeyError(e)

        elif isinstance(carrier_frequency, AxisData):
            if carrier_frequency.keys() != self.axis.keys():
                raise AttributeError('The axes for the given carrier frequency data do not match those of the peak table')
            # extract ONLY the carrier frequency values from the carrier_frequency AxisData object
            # this object could contain other properties that we don't want
            self.axis.set_data(carrier_frequency.get('carrier_frequency'))

        else:
            msg = 'define carrier frequency by providing a list of lists: [axis, cf, cf_units]'
            if not is_iterable(carrier_frequency):
                raise ValueError(msg)

            axis_labels_table = set(self.axis.keys())
            axis_labels_input = set([cf[0] for cf in carrier_frequency])
            if axis_labels_table != axis_labels_input:
                raise ValueError(f'the axis labels you used to define carrier frequencies {axis_labels_input} do not match the labels defined in the peak table {axis_labels_table}')

            for info in carrier_frequency:
                try:
                    axis, cf, cf_units = info
                except ValueError:
                    raise ValueError(msg)

                if cf_units.lower() == 'hz':
                    cf_hz = cf
                elif cf_units.lower() == 'mhz':
                    cf_hz = cf * 1e6
                else:
                    raise ValueError(f'do not recognize units for carrier frequency: {cf_units}.  must use "Hz" or "MHz"')

                self.axis.set(
                    axis=axis,
                    name='carrier_frequency',
                    value=cf_hz,
                    unit='Hz',
                )

    def _set_carrier_frequency_from_ppm_hz(self):
        """Determine carrier frequency from the ratio between peak positions in Hz and ppm"""
        # get average hz/ppm ratio across all peaks for each dimension
        # NOTE: peak tables from genSimTab do not have Hz values, so catch missing data
        try:
            ppm = self.get_par(par='*_PPM')
            hz = self.get_par(par='*_HZ')

            # minimum ppm magnitude to use for computing carrier (avoid divide by 0 or even divide by small value)
            ppm_min = 1

            carrier = 1e6 * np.mean(
                np.asarray([hz_row/ppm_row for hz_row, ppm_row in zip(hz, ppm) if (np.abs(ppm_row) > ppm_min).all()]),
                axis=0,
            )
        except KeyError as e:
            raise KeyError(e)

        for axis, cf in zip(self.axis.keys(), carrier):
            self.axis.set(
                axis=axis,
                name='carrier_frequency',
                value=cf,
                unit='Hz',
            )

    def _set_peak_positions_hz(self):
        """Use ppm peak positions and provided carrier frequencies to determine peak positions in Hz"""

        for axis in self.axis.keys():
            dimension = self.axis.axis2dimension(axis)

            try:
                peak_ppm = self.get_par(par=f'{dimension}_PPM')
            except KeyError:
                raise KeyError(f'missing peak PPM data for axis: {axis}')
            try:
                unit = self.axis.get_field(name='carrier_frequency', axis=axis, field='unit')[0]
                value = self.axis.get_field(name='carrier_frequency', axis=axis, field='value')[0]
                if unit.lower() == 'hz':
                    cf_mhz = value / 1e6
                elif unit.lower() == 'mhz':
                    cf_mhz = value
                else:
                    raise ValueError(f'do not recognize unit for carrier frequency: {unit}')
                peak_hz = peak_ppm * cf_mhz
            except KeyError:
                raise KeyError(f'missing carrier frequency for axis: {axis}')
            for idx, peak in enumerate(self.peaks):
                peak.set_par(par=f'{dimension}_HZ', value=peak_hz[idx])

    class chi2probAbort(Exception):
        """
        Custom exception to be raised when a filter is applied to peak table AFTER chi2prob filter already applied
        """
        pass

    def _chi2prob_must_be_last(self):
        # check if state allows filter to run
        # raise custom error if needed
        if self.chi2prob_already_applied:
            raise self.chi2probAbort('The chi2prob filtering must be last filtering operation on PeakTable.')
            SystemExit()

    def num_peaks(self):
        """
        Count the peaks in a peak list

        :return: count
        """
        return len(self.peaks)

    def get_peak(self, index):
        """
        Get a peak, specified by index

        :param index: index within PeakTable (not necessarily same as "index" in the tab file)
        :return: PipePeak
        """
        try:
            return self.peaks[index]
        except IndexError:
            raise IndexError('asking for index = {:d}, max index = {:d}'.format(index, len(self.peaks)))

    def get_par(self, par, axis_dimensions='all'):
        """
        Get all values for specified parameter for all peaks for specified axes.

        :param par: nmrPipe peak table parameter name (e.g. *_PPM, HEIGHT)
                    The * is substituted with axis values for each label requested
        :param axis_dimensions: list of axis identifiers to include (e.g. 'X' or default of 'all')
        :return: numpy array
        """
        out = []
        for peak in self.peaks:
            out.append(peak.get_par(
                par=par,
                axis_dimensions=axis_dimensions,
            ))
        return np.array(out)

    def get_par_list(self):
        return self.peaks[0].get_par_list()

    def reduce(
            self,
            number=None,
            height=None,
            abs_height=None,
            roi=None,
            index=None,
            cluster_type=None,
            mask=None,
            box_radius=2,
            chi2prob=None,
            outlier=None,
            vol_height_mismatch=False,
            maxLW_percent_SW=None,
    ):
        """
        reduce the peak list using filter criteria

        :param number: number of peaks to keep according to absolute value of peak HEIGHT
        :param height: keep all peaks with at least this HEIGHT
        :param abs_height: keep all peaks with absolute value at least this HEIGHT
        :param roi: keep peaks within the given ROI
        :param index: keep only peaks with given index values
        :param cluster_type: keep only peaks with given cluster type index
            NMRPipe currently uses: 1 = Peak, 2 = Random Noise, 3 = Truncation artifact
        :param mask: mask of True/False values on indel grid (e.g. use empirical peak table to set empty region)
        :param box_radius: defines size of box around peak position when querying it against empty mask
        :param chi2prob: remove peaks whose widths are outliers along any of the dimensions using chi2 probability
            expressed as p-value on [0,1] interval
        :param outlier: +/- percentage of the mode LW of peaks along each dimension to exclude
        :param vol_height_mismatch: type boolean: keep only peaks that have a nonzero height and volume
            and whose sign(HEIGHT) and sign(VOL) are in agreement.
        :param maxLW_percent_SW: threshold for the maximum linewidth along each dimensions defined as a percentage of
            the spectral window; input given on range [0,1]
        :return:
        """
        if number is not None:
            self.order_by_height()
            try:
                self.peaks = self.peaks[:number]
            except IndexError:
                # if the number of requested peaks is larger than number of actual peaks, just ignore and keep all
                pass

        elif height is not None:
            self.peaks = [p for p in self.peaks if p.get_par('HEIGHT') >= height]

        elif abs_height is not None:
            self.peaks = [p for p in self.peaks if abs(p.get_par('HEIGHT')) >= abs_height]

        elif roi is not None:
            if not isinstance(roi, ROI):
                raise TypeError('when reducing PeakTable by ROI, you must provide ROI class object')
            self.peaks = [p for p in self.peaks if p.in_roi(roi)]

        elif index is not None:
            if not isinstance(index, (list, tuple)):
                index = [index]
            try:
                self.peaks = [self.peaks[idx] for idx in index]
            except IndexError:
                raise IndexError('invalid index values for peak list')

        elif cluster_type is not None:
            self._chi2prob_must_be_last()
            if cluster_type not in [1, 2, 3]:
                print('NMRPipe peaks are categorized as:')
                print('  1 = Peak, 2 = Random Noise, 3 = Truncation artifact')
                raise TypeError('NMRPipe cluster_type must be one of the values above')
            self.peaks = [p for p in self.peaks if p.get_par('TYPE') == cluster_type]

        elif mask is not None:
            if not isinstance(mask, Mask):
                raise ValueError(f'provided mask should be of type nmrtoolbox.Mask (you provided {type(mask)}')
            self.peaks = [p for p in self.peaks if p.in_mask(mask=mask, box_radius=box_radius)]

        elif chi2prob is not None:
            idx_keep, idx_outlier = self.determine_outliers(chi2prob)
            self.reduce(index=idx_keep)

        elif vol_height_mismatch:
            self.peaks = [p for p in self.peaks
                          if p.get_par("VOL") != 0
                          and p.get_par("HEIGHT") != 0
                          and np.sign(p.get_par("VOL")) == np.sign(p.get_par("HEIGHT"))]

        elif maxLW_percent_SW is not None:
            if (maxLW_percent_SW > 1) or (maxLW_percent_SW < 0):
                raise ParsePeakTableError('invalid value for filtering by peak LW')
            lw_cutoff = np.asarray(self.axis.get_field('num_pts')) * maxLW_percent_SW
            self.peaks = [p for p in self.peaks if all(np.asarray(p.get_par("*W")) < lw_cutoff)]

        elif outlier is not None:
            self._chi2prob_must_be_last()
            # compute the relative LW of each peak on each dimension against the median LW on that dimension
            LW = self.get_par('*W')
            LW_median = np.median(LW, axis=0)
            LW_median_relative = np.absolute(LW - LW_median) / LW_median

            # keep just the peaks that are within the cutoff on ALL dimensions
            good_peak = [(lw <= outlier).all() for lw in LW_median_relative]
            self.peaks = [p for p, is_valid in zip(self.peaks, good_peak) if is_valid]

    def order_by_height(self):
        """Reorder the peak list by HEIGHT (most intense to least intense)"""
        self.peaks = sorted(self.peaks, key=lambda x: np.absolute(x.prop['HEIGHT']), reverse=True)

    def determine_outliers(self, chi2prob):
        # get full width of each recovered peak in points along each of its dimensions
        w = self.get_par('*W')

        # Covariance matrix
        covariance = np.cov(w, rowvar=False)

        # Covariance matrix power of -1
        covariance_pm1 = np.linalg.matrix_power(covariance, -1)

        # Center point
        centerpoint = np.mean(w, axis=0)

        # the width of each peak along each dimension is compared to the mean width of all peaks along the dimension
        # the covariance matrix is used to normalize
        distances = (np.matmul(w - centerpoint, covariance_pm1) * (w - centerpoint)).sum(axis=1)

        # Cutoff (threshold) value from Chi-Square Distribution for detecting outliers
        cutoff = chi2.ppf(chi2prob, w.shape[1])

        # TODO
        #  stupid [0] needed to get ndarray out of tuple
        #  for now: put ndarray into list because PeakTable.reduce() seems to fail when index is provided as ndarray
        idx_keep = [x for x in np.where(distances <= cutoff)[0]]
        idx_outlier = [x for x in np.where(distances > cutoff)[0]]

        # return these lists so that other downstream analysis can be performed
        return idx_keep, idx_outlier


class PeakTablePipe(PeakTable):
    def __init__(self, file, **kwargs):
        """
        This class has subclasses for peak tables coming from SYNTHETIC and RECOVERED peak tables; use those subclasses.
        You probably don't want to create a PeakTablePipe object - it is just a super-class to provide common tasks.
        """
        # pre
        self.REMARK = []
        self.DATA = []
        self.VARS = None
        self.FORMAT = None

        try:
            super().__init__(file, **kwargs)
        except ParsePeakTableError as e:
            # raise ParsePeakTableError(e)
            raise
        except Exception as e:
            # raise ParsePeakTableError(e)
            raise

    def _parse_file(self):
        """
        Parser for peak tables from NMRPipe generated by peak picker (i.e. "REC") OR by genSimTab (i.e. "SYN").
        The PeakTablePipe class is subclassed to handle the differences in data presented in RECOVERED and SYNTHETIC.
        """

        with open(self.file, 'r') as f_in:
            mode = None
            for line in f_in:
                line = line.strip()
                if line in ['', '#']:
                    continue

                if mode is None:
                    # recovered peak table starts with REMARK section
                    # synthetic peak table starts with genSimTab
                    if line.startswith('REMARK'):
                        mode = 'remark'
                    elif re.match('# [a-zA-Z_]*genSimTab.tcl', line):
                        # several variants of genSimTab.tcl are in use, so find all lines that might look like:
                        #   # genSimTab.tcl
                        #   # xzy_genSimTab.tcl
                        #   # new_genSimTab.tcl
                        mode = 'genSimTab'
                    else:
                        continue

                if mode == 'remark':
                    if line.startswith('REMARK'):
                        self.REMARK.append(line)
                        continue
                    else:
                        mode = 'data'

                if mode == 'genSimTab':
                    if line.startswith('#'):
                        self.genSimTab_raw_list.append(line.strip().lstrip('#').rstrip('\\').strip())
                        continue
                    else:
                        mode = 'data'

                if mode == 'data':
                    if line.startswith('DATA'):
                        # axis properties are described like this
                        # example: DATA  X_AXIS HN           1   659   10.297ppm    5.798ppm
                        self.DATA.append(line)
                        info = line.split()
                        try:
                            if info[1] == 'CLUSTER':
                                # some filtered peak tables include CLUSTER info - ignore these lines
                                # example: DATA  CLUSTER X_AXIS +/- 7
                                continue
                            elif info[1].endswith('_AXIS'):
                                axis = info[2]
                                self.axis.set(
                                    axis=axis,
                                    name='dimension',
                                    value=info[1].split('_')[0],
                                )
                                self.axis.set(
                                    axis=axis,
                                    name='num_pts',
                                    value=int(info[4]),
                                    unit='count'
                                )
                                self.axis.set(
                                    axis=axis,
                                    name='range',
                                    value=Range(
                                            min=float(info[5].rstrip('pm')),
                                            max=float(info[6].rstrip('pm')),
                                        ),
                                    unit='ppm',
                                )
                                continue
                            else:
                                raise ValueError(f'unrecognized line in peak table: {line}')
                        except (IndexError, ValueError):
                            raise ValueError('metadata missing from peak table header')
                    else:
                        mode = 'vars'

                if mode == 'vars':
                    if line.startswith('VARS'):
                        self.VARS = line.split()[1:]
                        # this is a single line of data, so get it and move on to next mode
                        mode = 'format'
                        continue

                if mode == 'format':
                    if line.startswith('FORMAT'):
                        self.FORMAT = line.split()[1:]
                        # this is a single line of data, so get it and move on to next mode
                        mode = 'peak'
                        continue

                if mode == 'peak':
                    if line.startswith('#'):
                        # comments are mixed into the synthetic peak lists - just ignore them
                        continue
                    else:
                        self.peaks.append(Peak(
                            prop_list=self.VARS,
                            val_list=line.split(),
                            axis_property=self.axis,
                        ))

    def _build_genSimTab_comment(self):
        """
        convert list of genSimTab lines into a single comment string that can be written into header of peak table
        :return:
        """
        try:
            join_str = ' \\\n#' + ' ' * 15
            return '# ' + join_str.join(self.genSimTab_raw_list)
        except AttributeError:
            raise AttributeError

    def write(self, file):
        """
        write a peak table to file.  include (if available) genSimTab, REMARK, DATA, VARS, FORMAT, and peak table
        :param file:
        :return:
        """
        try:
            with open(file, 'w') as f_out:
                try:
                    f_out.write(self._build_genSimTab_comment())
                    f_out.write('\n\n')
                except AttributeError:
                    pass

                if self.REMARK:
                    for line in self.REMARK:
                        f_out.write(line + '\n')
                    f_out.write('\n')

                if self.DATA:
                    for line in self.DATA:
                        f_out.write(line + '\n')
                    f_out.write('\n')

                # build the FORMAT and VARS lines in the same style as NMRPipe tables
                vars_out   = 'VARS   '
                format_out = 'FORMAT '
                for vars_current, format_current in zip(self.VARS, self.FORMAT):
                    width = max(len(vars_current), len(format_current))
                    vars_out += f' {vars_current:<{width}}'
                    format_out += f' {format_current:<{width}}'
                f_out.write(vars_out + '\n')
                f_out.write(format_out+ '\n')
                f_out.write('\n')

                for p in self.peaks:
                    out = []
                    for vars_name, format_spec in zip(self.VARS, self.FORMAT):
                        val = p.get_par(par=vars_name)
                        out.append(f'{val:{format_spec.lstrip("%")}}')
                    f_out.write(' ' + ' '.join(out) + '\n')
        except FileNotFoundError:
            raise FileNotFoundError(f'bad file: {file}')
        except PermissionError:
            raise PermissionError(f'bad file: {file}')
        except Exception as e:
            raise Exception(e)


class PeakTablePipeRec(PeakTablePipe):
    """This subclass is for capturing the peaks "recovered" from an experiment by the NMRPipe peak picker"""
    def __init__(self, file, **kwargs):
        # pre

        try:
            super().__init__(file, **kwargs)
        except:
            raise ParsePeakTableError(f'failed to read peak table as type: PeakTablePipeRec\n{file}')

        # post
        self._get_noise()
        self._get_category_count()
        self._get_LW()

        self._post()

    def _get_LW(self):
        try:
            LW_list = self.get_par('*W').mean(axis=0)
        except KeyError as e:
            raise KeyError(e)

        for axis, LW in zip(self.axis.keys(), LW_list):
            self.axis.set(
                axis=axis,
                name='LW',
                value=LW,
                unit='pts',
            )

    def _get_noise(self):
        for line in self.REMARK:
            if line.startswith('REMARK Noise:'):
                # example: "REMARK Noise: 91905.9, Chi2-Threshold: 1.000000e-04, Local Adjustment: None"
                self.table_property.set(
                    name='noise',
                    value=float(line.split()[2].strip(',')),
                    unit='au',
                )

    def _get_category_count(self):
        for line in self.REMARK:
            if line.startswith('REMARK Total Peaks:'):
                # example: "REMARK Total Peaks: 60425, Good Peaks: 40513, Questionable Peaks: 19912"
                self.table_property.set(
                    name='peak_count_total',
                    value=int(line.split()[3].strip(',')),
                    unit='count'
                )
                self.table_property.set(
                    name='peak_count_good',
                    value=int(line.split()[6].strip(',')),
                    unit='count',
                )
                self.table_property.set(
                    name='peak_count_questionable',
                    value=int(line.split()[9].strip(',')),
                    unit='count',
                )


class PeakTablePipeSyn(PeakTablePipe):
    """This subclass is for capturing the synthetic peaks generated by the NMRPipe genSimTab.tcl tool"""
    def __init__(self, file, carrier_frequency, **kwargs):
        """
        :param carrier_frequency: either a list of values in MHz or an AxisData object (e.g. from another PeakTable)
        """

        # could get carrier_frequency from kwargs input, but it wouldn't be a required input or autocomplete
        # want to put carrier_frequency back into kwargs, so that kwargs can be passed up to super
        kwargs['carrier_frequency'] = carrier_frequency

        # pre
        # capture the lines of genSimTab command as they are formatted so they can be written to file if needed
        self.genSimTab_raw_list = []

        try:
            super().__init__(file, **kwargs)
        except (ParsePeakTableError, Exception) as e:
            raise ParsePeakTableError(f'failed to read peak table as type: PeakTablePipeSyn\n  table = {file}\n  error = {e}')

        # post
        self.genSimTab = ' '.join(self.genSimTab_raw_list)
        self._set_maxLW()
        self._post()

    def _set_maxLW(self):
        """
        #1. read LW params from genSimTab command (indirect)
        #2. compute LW from synthetic peak table using X1/X3 (in pts) and converting to hz
        :return:
        """

        # parse through the tokens to find maxLW values for each axis
        tokens = self.genSimTab.split()
        for axis in self.axis.keys():
            dimension = self.axis.axis2dimension(axis)
            try:
                idx = tokens.index(f'-{dimension.lower()}wMax')
                self.axis.set(
                    axis=axis,
                    name='maxLW-genSimTab',
                    value=float(tokens[idx + 1]),
                    unit='Hz',
                )
            except (ValueError, IndexError):
                pass

        indel_width = np.asarray([self.get_par(f"{dim}3") - self.get_par(f"{dim}1") for dim in self.axis.dimensions()]).max(axis=1)
        axis_ppm_range = np.asarray([abs(r.min-r.max) for r in self.axis.get_field('range')])
        num_pts = np.asarray(self.axis.get_field('num_pts'))
        ppm_per_indel = axis_ppm_range / num_pts
        peak_width_ppm = indel_width * ppm_per_indel

        cf_unit = self.axis.get_field(name='carrier_frequency', field='unit')
        cf_value = self.axis.get_field(name='carrier_frequency', field='value')
        cf_mhz = []
        for unit, value in zip(cf_unit, cf_value):
            if unit.lower() == 'hz':
                cf_mhz.append(value / 1e6)
            elif unit.lower() == 'mhz':
                cf_mhz.append(cf_value)
            else:
                raise ValueError

        peak_width_hz = peak_width_ppm * cf_mhz

        self.axis.set_list(
            axis_list=self.axis.keys(),
            name='maxLW',
            value_list=peak_width_hz,
            unit='Hz',
        )
