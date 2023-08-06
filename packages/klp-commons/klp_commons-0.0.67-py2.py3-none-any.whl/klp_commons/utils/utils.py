from numpy import ndarray
from numpy import floating
from numpy import integer
from json import JSONEncoder

def divide_chunks(l: list = None, n: int = 100) -> list:

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_full_class_name(obj):
    """
    get full class name error 
    """
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__

class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, integer):
            return int(obj)
        elif isinstance(obj, floating):
            return float(obj)
        elif isinstance(obj, ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)

