"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""
import types 
import re


# is variable a class?
def is_class(cls):
    return str(type(cls)).startswith("<class") and hasattr(cls, "__weakref__")

# check if a class is initialized
def is_initialized(cls):
    new_cls = types.new_class("_")
    return is_class(cls) and type(cls) != type(new_cls)


# get properties of this class
def get_props(cls, filter_callable=False, with_meta=False):
    default_props = dir(types.new_class("_"))

    resp = {} if with_meta else set()
    
    for p in dir(cls):
        if p not in default_props and (
            getattr(cls, p) if not filter_callable else callable(getattr(cls, p))
        ):
            if with_meta:
                resp[p] = {
                    "type": re.match(r"<class\s+'([^>']+)", str(type(getattr(cls, p))))[
                        1
                    ],
                    "value" : getattr(cls, p) if not callable(getattr(cls, p)) else 'N/A'
                }

            else:
                resp.add(p)

    return resp
