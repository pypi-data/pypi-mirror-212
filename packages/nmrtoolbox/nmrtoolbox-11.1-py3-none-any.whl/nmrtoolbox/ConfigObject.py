import configparser
import os
from collections import OrderedDict


# TODO: convert paths as strings to pathlib (more complicated here than other upgrades)
class ConfigObject:
    """
    Read a configparser file into a 'dot-able' object
    This class supports nested config files, value mapping, and lists.
    """

    def __init__(self, file=None, list_delimiter=',', nested_section_name='configs', unpack_section_name='configs-unpack', parseVal=True, splitList=True, unpack=False):

        """
        Using the dot to access fields and nested fields only works for class objects that have self.__dict__

        In order to use this feature all the way through nested ConfigObjects, fill the top level of __dict__
        with OrderedDict (replaces default of regular dict) and fill all nested levels with ConfigObjects.

        Note: the keys put in __dict__ will appear as properties of ConfigObject, just like self.list_delimiter,
        but ConfigObject.keys() can be used to only return the keys from __dict__

            file                    config file
            parseVal                controls if values in cfg file are converted to bool, int, float where possible
            splitList               controls if values in cfg file are split on list_delimiter
            list_delimiter          character that separates items in a list value
            nested_section_name     section name where all keys are taken as nested cfg files and parsed/inserted

        """
        self.__dict__ = OrderedDict()
        self.list_delimiter = list_delimiter
        self.parseVal = parseVal
        self.splitList = splitList

        if not file:
            # allow constructor to be called with no file so that empty ConfigObject is created and can be populated
            return

        if not os.path.isfile(file):
            raise FileNotFoundError('config file not found: {:s}'.format(str(file)))

        # read master config file
        cparser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(),
            empty_lines_in_values=False,
        )
        cparser.optionxform = str
        try:
            cparser.read(file)
        except configparser.DuplicateSectionError:
            raise configparser.DuplicateSectionError('duplicate sections found in: {:s}'.format(file))

        for sec in cparser.sections():
            if sec in (nested_section_name, unpack_section_name):
                # found the keyword that indicates this section contains config files that should be parsed
                for param in cparser.options(sec):
                    # get the filename and perform system variable substitution (i.e. allow $HOME in config file)
                    config_file = os.path.expandvars(cparser.get(sec, param))
                    if not config_file.endswith('.cfg'):
                        # probably tried to interpret value as a nested config file, but it's just a value from DEFAULT
                        continue
                    if not config_file.startswith('/'):
                        # if filename is not absolute => assume filename is relative to location of main config file
                        config_file = os.path.join(os.path.dirname(file), config_file)
                    if not os.path.isfile(config_file):
                        raise FileExistsError('config file not found: {:s}'.format(config_file))
                    try:
                        obj = ConfigObject(
                            file=config_file,
                            list_delimiter=self.list_delimiter,
                            nested_section_name=nested_section_name,
                            unpack_section_name=unpack_section_name,
                            parseVal=parseVal,
                            splitList=splitList,
                        )
                    except:
                        raise EnvironmentError('failed to read config file: {:s}'.format(config_file))

                    if sec == unpack_section_name:
                        self.__dict__.update(obj.__dict__)
                    elif sec == nested_section_name:
                        # parse the config file and insert ConfigObject into self
                        self.__dict__[param] = obj
            else:
                # create a new section as an empty ConfigObject
                self.__dict__[sec] = ConfigObject(
                    file=None,
                    list_delimiter=list_delimiter,
                    nested_section_name=nested_section_name,
                    unpack_section_name=unpack_section_name,
                    parseVal=parseVal,
                    splitList=splitList,
                )
                # fill this new section with key/value pairs
                for param in cparser.options(sec):
                    self.__dict__[sec].__dict__[param] = self.format_val(cparser.get(sec, param))

    def get(self, sec, param=None):
        """
        Return the portion of the object rooted at the given key
        """
        if param:
            try:
                return self.__dict__[sec].__dict__[param]
            except KeyError:
                raise KeyError('parameter not found: {:s}/{:s}'.format(sec, param))
        else:
            try:
                return self.__dict__[sec]
            except KeyError:
                raise KeyError('section not found: {:s}'.format(sec))

    def set(self, sec, param=None, value=None):
        """
        Set the value for the given key
        """
        if param:
            try:
                self.__dict__[sec].__dict__[param] = value
            except KeyError:
                raise KeyError('parameter not found: {:s}/{:s}'.format(sec, param))
        else:
            try:
                self.__dict__[sec] = value
            except KeyError:
                raise KeyError('section not found: {:s}'.format(sec))

    def dictionary(self):
        """
        Recursively unpack nested ConfigObject into nested dictionary
        :return: dictionary
        """
        d = dict()
        for key in self.__dict__:
            if isinstance(self.__dict__[key], ConfigObject):
                d[key] = self.__dict__[key].dictionary()
            else:
                d[key] = self.__dict__[key]
        return d

    def keys(self):
        """
        Return all keys at top level of ConfigObject
        :return: list
        """
        return list(self.__dict__.keys())

    def format_val(self, val):
        """
        Convert a value (given as str) into correct data type and store as list, if applicable
        :param val: str input
        :return: list
        """
        if self.splitList:
            # convert value to a list
            if isinstance(val, str):
                val_list = val.split(self.list_delimiter)
                val_list = [v.strip() for v in val_list]
            else:
                if not isinstance(val, list):
                    val_list = [val]
                else:
                    val_list = val
        else:
            # don't split, just pass along the full value
            val_list = val

        if self.parseVal:
            num_val_in = len(val_list)
            val_out = []

            for v in val_list:
                if v in ['true', 'True']:
                    val_out.append(True)
                elif v in ['false', 'False']:
                    val_out.append(False)
                else:
                    for t in [int, float, str]:
                        try:
                            val_out.append(list(map(t, [v]))[0])
                            break
                        except ValueError:
                            pass  # try next format option

            if len(val_out) != num_val_in:
                raise ValueError('failed to convert cfg value: {:s}'.format(val))
        else:
            val_out = val_list

        if isinstance(val_out, list):
            if len(val_out) == 1:
                return val_out[0]
        return val_out

    def print(self, OBJ=None, level=0, param_length=25):
        """
        Print the sections, parameters, and values.  Use indenting to indicate nesting.
        :param OBJ: object to print (used to accept recursive call for nested configs)
        :param level: current nesting level - used to control indentation
        :param param_length: field width to use when printing parameter names
        :return:
        """
        # indent the keys progressively with nested sections
        pad = '    ' * level
        # indent multiline values (the last 2 spaces account for "= " and ensure that trailing lines are at same depth)
        multiline_pad = ' ' * param_length + pad + '  '

        if OBJ is None:
            OBJ = self.__dict__

        for k in OBJ.keys():
            if isinstance(OBJ.get(k), ConfigObject):
                print('-' * 40 + '\n' + pad + '[{}]'.format(k))
                self.print(OBJ=OBJ.get(k), level=level + 1, param_length=param_length)
            else:
                val = OBJ.get(k)
                if isinstance(val, str):
                    val = val.replace('\n', '\n' + multiline_pad)

                print(pad + '{key:{key_length}s}= {val:}'.format(
                    key=k, key_length=param_length, val=val))
