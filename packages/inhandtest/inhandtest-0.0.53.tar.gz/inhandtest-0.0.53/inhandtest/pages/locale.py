# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 15:37:51
# @Author  : Pane Li
# @File    : locale.py
"""
locale

"""

import dynaconf
import os

os.path.dirname(__file__),

in_setting = dynaconf.Dynaconf(settings_files=[os.path.join(os.path.dirname(__file__), 'ingateway', 'locale.yml')])
