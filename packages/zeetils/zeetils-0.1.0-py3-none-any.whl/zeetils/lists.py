"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

def listify(v):
    if isinstance(v, (tuple, set)):
        v = list(v)
    else:
        v = v if isinstance(v, list) else [v]

    return v