"""
Module globals.

SPDX-License-Identifier: GPL-3.0-or-later
"""

import logging
import re

log = logging.getLogger("sextant")
DEPFILE = "package.json"
RE_VERSION = re.compile(r"^(version:[\s\"']*)([\d.]+)", re.MULTILINE)
