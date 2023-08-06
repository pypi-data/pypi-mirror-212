from dataclasses import dataclass
from collections import defaultdict, namedtuple
import numpy as np
from pathlib import Path


class PeakOutsideOfMaskError(Exception):
    # use this when the position of a Peak is outside of the ppm ranges covered by a Mask
    pass


class ParsePeakTableError(Exception):
    pass


@dataclass
class Range:
    """
    Store a min and max value to define a range
    """
    min: float
    max: float

    def contains(self, val):
        """
        Check if value is in range
        :param val: value to check (float or int)
        :return: bool
        """
        if not isinstance(val, (float, int)):
            raise TypeError('must enter a float or int')
        return self.min <= val <= self.max


class Data:
    def __init__(self, name, value, unit):
        # NOT using @dataclass because it requires explicit typing; want to allow value to be int, float, str, etc.
        self.name = name
        self.value = value
        self.unit = unit

    def get(self, field):
        try:
            return self.__getattribute__(field)
        except AttributeError:
            raise AttributeError(f'invalid field: {field}')

    def print(self):
        print(f"{self.name} = {str(self.value)} [{self.unit}]")


class DND:
    """Dictionary of Named Data (DND)"""
    def __init__(self):
        self.data = {}

    def set(self, name, value, unit=None):
        self.data[name] = Data(name=name, value=value, unit=unit)

    def get(self, name):
        try:
            return self.data[name]
        except KeyError as e:
            raise KeyError(e)

    def get_field(self, name, field='value'):
        # extract out just the desired field and return value
        try:
            return self.get(name=name).get(field=field)
        except KeyError as e:
            raise KeyError(e)

    def print(self):
        [d.print() for d in self.data.values()]


class DDND:
    def __init__(self):
        """Dictionary of Dictionary of Named Data (DDND)"""
        self.data = defaultdict(DND)

        # self.data[key][name] = Data(name, value, unit)
        #   "key" : nucleus of the axis (HN, N15, CA, etc.)
        #   "name" : property that gets recorded
        #       for "name" = "dimension", the values should be: X, Y, Z, A (correspond to NMRPipe data)

    def keys(self):
        return list(self.data.keys())

    def set(self, axis, name, value, unit=None):
        axis = axis.upper()
        self.data[axis].set(name=name, value=value, unit=unit)

    def set_list(self, name, value_list, unit=None, axis_list=None):
        if axis_list is None:
            axis_list = self.keys()

        for axis, value in zip(axis_list, value_list):
            self.set(axis=axis, name=name, value=value, unit=unit)

    def set_data(self, data):
        if not isinstance(data, DDND):
            raise TypeError(f'input must be of type AxisData, not: {type(data)}')
        for ax in data.keys():
            self.data[ax].data = {**self.data[ax].data, **data.data[ax].data}

    def get(self, name, axis=None):
        """
        Return an AxisData object that only contains data for the desired "name" and "axis"
        name: property name
        axis: name of axis (str) or list of axis names
        """
        if axis is None:
            ax_list = self.keys()
        else:
            if not isinstance(axis, list):
                axis = [axis]
            try:
                ax_list = [ax.upper() for ax in axis]
            except AttributeError:
                raise AttributeError(f"axis should probably be 'X', 'Y', 'Z' or similar. unable to use: {str(axis)}")

        out = DDND()
        try:
            for ax in ax_list:
                if not isinstance(self.data[ax], DND):
                    print('debugging test')
                out.data[ax].data[name] = self.data[ax].get(name=name)
        except KeyError as e:
            raise KeyError(e)
        return out

    def get_field(self, name, axis=None, field='value'):
        # get the AxisData object containing just the desired "name"
        # extract out just the desired field and return values in a list
        data_out = self.get(axis=axis, name=name)
        try:
            return [data_out.data[ax].get(name=name).get(field=field) for ax in data_out.keys()]
        except KeyError as e:
            raise KeyError(e)

    def print(self):
        for axis in self.keys():
            print(f"axis = {axis}")
            [d.print() for d in self.data[axis].values()]


class AxisData(DDND):
    """Subclass from DDND and provide a couple helper functions specific to NMR usage"""
    # def num_dims(self):
    #     """Number of dimensions"""
    #     return len(self.keys())

    def dimensions(self):
        """Get the axis dimensions"""
        return self.get_field(name='dimension')

    def axis2dimension(self, axis):
        """Convert an axis (e.g. 'HN') to a dimension (e.g. 'X')"""
        try:
            return self.get_field(name='dimension', axis=axis)[0]
        except KeyError as e:
            raise KeyError(e)


class SpectrumData(DND):
    """Subclass from DND and provide a couple helper functions specific to NMR usage"""
    pass


class ROI(DDND):
    def __init__(self, key_dimension_range):
        """
        Define a region of interest (ROI) by giving the min/max values along each axis
        :param key_dimension_range: iterable of (key, dimension, ppm1, ppm2)
        """
        super().__init__()

        msg = 'define ROI by providing a list of lists: [key, label, ppm1, ppm2]'

        if not is_iterable(key_dimension_range):
            raise ValueError(msg)

        for info in key_dimension_range:
            try:
                key, dimension, ppm1, ppm2 = info
                ppm_range = Range(
                    min=min(float(ppm1), float(ppm2)),
                    max=max(float(ppm1), float(ppm2)),
                )
            except ValueError:
                raise ValueError(msg)

            self.set(
                axis=key,
                name='dimension',
                value=dimension,
            )
            self.set(
                axis=key,
                name='roi',
                value=ppm_range,
            )


def weightedL2(a, b, w):
    """weighted norm of vectors a and b using weighting coefficients from w"""
    q = a - b
    return np.sqrt((w * q * q).sum())


def pairwise_weighted_norm(A, B, w=None):
    """
    A and B are matrices where each row is a vector of n dimensions.
    w is a vector of length n containing weighting factors for an L2 norm
    """
    if not (isinstance(A, np.ndarray) and isinstance(B, np.ndarray)):
        raise TypeError('must provide inputs as numpy.array')
    rowA, colA = A.shape
    rowB, colB = B.shape
    if colA != colB:
        raise ValueError('A and B must have same number dimensions in each column vector')

    if w is not None:
        try:
            w = np.asarray(w)
        except:
            raise TypeError('weights must be provided as data type that can be converted to numpy.array')
    else:
        w = np.ones(colA)
    numW = len(w)

    if numW != colA:
        raise ValueError('w must have the same number of weighting factors as A and B have dimensions')

    N = np.zeros((rowA, rowB))
    for indexA, a in enumerate(A):
        for indexB, b in enumerate(B):
            N[indexA][indexB] = weightedL2(a, b, w)
    return N


def pairwise_weighted_norm2(A, B, w=None):
    """
    A and B are matrices where each row is a vector of n dimensions.
    w is a vector of length n containing weighting factors for an L2 norm
    """
    if not (isinstance(A, np.ndarray) and isinstance(B, np.ndarray)):
        raise TypeError('must provide inputs as numpy.array')
    rowA, colA = A.shape
    rowB, colB = B.shape
    if colA != colB:
        raise ValueError('A and B must have same number dimensions in each column vector')

    if w is not None:
        try:
            w = np.asarray(w)
        except:
            raise TypeError('weights must be provided as data type that can be converted to numpy.array')
    else:
        w = np.ones(colA)
    numW = len(w)

    if numW != colA:
        raise ValueError('w must have the same number of weighting factors as A and B have dimensions')

    N = np.zeros((rowA, rowB))
    for indexA, a in enumerate(A):

        Q = B - a
        N[indexA] = np.sqrt((w * np.matmul(Q, Q.T)).sum())

    return N

def is_iterable(obj):
    try:
        iterator = iter(obj)
        return True
    except TypeError:
        return False


def calc_rms(data):
    return np.sqrt(np.mean(np.square(data)))


def check_file_existence(str_file_path):
    my_file = Path(str_file_path)
    if my_file.is_file():
        return True
    else:
        return False
