"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from .lists import listify
from .classes import is_initialized, is_class

# pick values from list/dict/tuple/class or set
def pick(obj, keys, sort_keys=True):
    if not isinstance(obj, (dict, list, tuple, set)) and not is_initialized(obj):
        raise KeyError(f"obj must be a dict, list, tuple, set or an initialized class object")
    if not isinstance(keys, (tuple, set, list, str, int)):
        raise KeyError(f"keys to pick must be a string, integer, set, tuple or list")

    keys = listify(keys)

    if sort_keys:
        keys = sorted(keys)

    if isinstance(obj, dict):
        return {k: obj[k] for k in keys if k in obj}

    elif isinstance(obj, tuple):
        l = len(obj)
        return tuple([obj[k] for k in keys if k <= l - 1])

    elif isinstance(obj, set):
        return {k for k in keys if k in obj}

    elif is_class(obj):
        return {k: getattr(obj, k) for k in keys if hasattr(obj, str(k))}

    else:
        l = len(obj)
        return [obj[k] for k in keys if k <= l - 1]
