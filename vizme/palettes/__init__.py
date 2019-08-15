#!/usr/bin/env python3

import os
import vizme
from importlib import import_module

"""
    Ghetto dynamic pallet system
"""

palettes = {}
for modname in os.listdir(os.path.join(os.path.dirname(vizme.__file__), 'palettes')):
    if modname.startswith('__'):
        continue

    modname = modname.split('.py')[0]
    m = import_module('.palettes.' + modname, package='vizme')

    palettes[m.name] = m.palette
