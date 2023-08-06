"""Save any object to a pickled object that can be converted"""
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

    def single_save(self, item):
        """Save a single item"""
        try:
            return json.dumps(item)
        except TypeError:
            try:
                return marshal.dumps(item)
            except TypeError:
                try:
                    return marshal.dumps(item.__code__)
                except AttributeError:
                    try:
                        return pickle.dumps(item)
                    except pickle.PicklingError:
                        messaging.error(
                            #pylint: disable-next=line-too-long
                            f"Sorry, we found an {item.__class__.__name__} with the name/signature {item} that is an invalid object for the world storage system. This means that you aren't basing it on an Object, an Item, a Player, a Room, or an Entity. Please make it be based on one of those.\n",
                            sys.stdout)
                        return bytes()

    def __call__(self, item):
        copy = {}
        for ite in item.__class__.save.append("__class__"):
            copy[ite] = self.single_save(item.__getitem__(ite))
        copy["__VERSION__"] = txtadv.__version__
        #pylint: disable-next=consider-using-with
        pickle.dump(copy,open(savepath+"/"+item.__name__,'wb'))
        return pickle.dumps(copy)

    def save_to_file(self, item):
        """Save to a file"""
        data = self(item)
        with open(item.__name__ + '.' + item.__class__.__name__, 'wb') as file:
            file.write(data)


sys.modules[__name__] = Call()
