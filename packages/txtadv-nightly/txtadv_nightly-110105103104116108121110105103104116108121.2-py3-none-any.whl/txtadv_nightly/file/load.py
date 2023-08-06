"""Load any object from a pickled object"""
import os
import inspect
import sys
import marshal
import pickle
import json
from .. import messaging
from .. import __init__ as txtadv

savepath = os.path.dirname(inspect.getfile(txtadv)) + "/saves"


class Call:
    """The class that's used to make this module callable"""

    def single_load(self, item):
        """Load a single item"""
        try:
            return json.loads(item)
        except json.decoder.JSONDecodeError:
            try:
                return marshal.loads(item)
            except (EOFError, TypeError, ValueError):
                try:
                    return pickle.loads(item)
                #pylint: disable-next=duplicate-code
                except (TypeError, pickle.UnpicklingError):
                    messaging.error(
                        #pylint: disable-next=line-too-long
                        "Sorry, while trying to load an item, it wasn't stored as json data, marshal data, or pickle data\n",
                        sys.stdout)
                    return bytes()

    def __call__(self, filename):
        try:
            #pylint: disable-next=consider-using-with
            file = pickle.load(open(filename + ".save", 'rb'))
        except (FileNotFoundError, IsADirectoryError, TypeError,
                pickle.UnpicklingError):
            #pylint: disable-next=line-too-long
            messaging.error(
                f"Attempted load of invalid save/nonexistant save {filename}!\n",
                sys.stdout)
            return
        if file.__class__.__name__ != "dict":
            messaging.error(f"Attempted load of invalid save {filename}!\n",
                            sys.stdout)
            return
        if file["__VERSION__"] != txtadv.__version__:
            #pylint: disable-next=line-too-long
            file_version = file[
                "__VERSION__"]  # I do this instead of putting it in the f-string directly because for some reason if I do, pylint and python get VERY mad
            #pylint: disable-next=line-too-long
            messaging.error(
                f"Attempted load of save {filename} which has a file version of {file_version}, but this copy of txtadv is still on version {txtadv.__VERSION__}!\n",
                sys.stdout)
        copy = {}
        for ite in file.items():
            copy[ite] = self.single_load(ite)


sys.modules[__name__] = Call()
