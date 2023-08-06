import nmrglue as ng
from enum import Enum
from pathlib import Path


class Spectrum:
    class SpectrumReadError(Exception):
        pass

    class dtype(Enum):
        pipe = 'pipe'
        bruker = 'bruker'
        varian = 'varian'
        sparky = 'sparky'
        rnmrtk = 'rnmrtk'

    @classmethod
    def read(
            cls,
            obj,
            dtype,
    ):
        """
        Call this instead of init - it handles input that is either a Spectrum object or a path to spectrum data file
        :param obj: Spectrum object or file path to spectrum data
        :param dtype: type of data (see nmrglue for full list of what is supported)
        :return:
        """
        if isinstance(obj, Spectrum):
            return obj
        else:
            return cls(obj=obj, dtype=dtype)

    def __init__(
            self,
            obj,
            dtype,
    ):
        try:
            self.fpath = Path(obj)
        except Exception as e:
            raise self.SpectrumReadError(f'input must be a path to a data file')

        if dtype not in self.dtype:
            raise self.SpectrumReadError('spectrum data type not supported')
        self.dtype = dtype

        # nmrglue has a module for each supported datatype that includes read and read_lowmem functions
        func = getattr(ng, self.dtype.name).read_lowmem

        # TODO: return to this and confirm if pattern files are acceptable as inputs for strip_plot
        # if '%' in str(self.fpath):
        #     raise self.SpectrumReadError(f'input file: {self.fpath}\ndo not specify file pattern, please provide a single cube file')

        try:
            self.dic, self.data = func(str(self.fpath))
        except FileNotFoundError:
            raise self.SpectrumReadError(f'spectrum file not found: {self.fpath}')
        except PermissionError:
            raise self.SpectrumReadError(f'permission not allowed: {self.fpath}')
        except Exception as e:
            raise self.SpectrumReadError(e)

