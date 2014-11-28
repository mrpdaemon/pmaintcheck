#! /usr/bin/env python2

# Copyright (C) 2014 Mark Pariente <markpariente@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pmaintcheck import util

import sys

config_file = open('example.cfg', 'r')

for config_line in config_file:
    # ignore comment lines
    if (config_line[0] == '#'):
        continue

    # tokenize the line
    pkg_name, last_version, plugin_name, plugin_arg = config_line.split()

    print pkg_name + ': checking for updates...'

    # load the right plugin
    try:
        plugin = __import__('pmaintcheck.%s' % plugin_name, fromlist=['pmaintcheck'])
    except ImportError as ie:
        print 'Plugin %s could not be loaded: %s' % (plugin_name, ie)
        sys.exit(1)

    version_list = plugin.get_version_list(plugin_arg)

    if not version_list:
        print 'WARNING: No versions found!'

    for version in version_list:
        if util.compare_versions(last_version, version) > 0:
            print 'NEW VERSION: ' + version
