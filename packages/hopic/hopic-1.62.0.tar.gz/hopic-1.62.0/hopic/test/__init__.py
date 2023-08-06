# Copyright (c) 2020 - 2021 TomTom N.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from io import StringIO

from ..compat import metadata

PACKAGE : str = __package__.split('.')[0]

# Converting to frozenset because this returns two duplicate entries since importlib_metadata 4.3.0.
# Specifically it seems that the f"{PACKAGE}.egg-info" directory created by setup.py in the repository's root directory gets selected along with the
# f"{PACKAGE}-{VERSION}.dist-info" directory in Tox' virtualenv.
(_hopic_ep,) = frozenset(metadata.entry_points(group="console_scripts", name=PACKAGE))
hopic_cli = _hopic_ep.load()
source_date_epoch = 7 * 24 * 3600

sgr_re = re.compile(r"\x1B\[.*?m")


def config_file(name: str, content: str):
    f = StringIO(content)
    f.name = name
    return f
