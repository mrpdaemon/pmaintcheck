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

from subprocess import check_output
import re

def compare_versions(version1, version2):
    """Do a version comparison on strings version1 and version2
    Gets rid of any/all unnecessary characters and compares the versions
    """
    # remove preceding strings
    result = re.search("\d", version1)
    if result:
        version1_clean = version1[result.start():].replace('_','.')
    else:
        return 0

    result = re.search("\d", version2)
    if result:
        version2_clean = version2[result.start():].replace('_','.')
    else:
        return 0

    # remove trailing strings
    result = re.search("-", version1_clean)
    if result:
        version1_clean = version1_clean[:result.start()]

    result = re.search("-", version2_clean)
    if result:
        version2_clean = version2_clean[:result.start()]

    # tokenize and compare each version atom
    version1_atoms = version1_clean.split('.')
    version2_atoms = version2_clean.split('.')
    for version1_atom,version2_atom in zip(version1_atoms,version2_atoms):
        if int(version1_atom) > int(version2_atom):
            return -1
        elif int(version2_atom) > int(version1_atom):
            return 1

    # handle cases like 1.0.1 vs. 1.0.1.1
    if len(version1_clean) > len(version2_clean):
        return -1
    elif len(version2_clean) > len(version1_clean):
        return 1

    # versions equal
    return 0

config_file = open('example.cfg', 'r')

for config_line in config_file:
    # ignore comment lines
    if (config_line[0] == '#'):
        continue

    # tokenize the line
    pkg_name, last_version, plugin_name, plugin_arg = config_line.split()

    print pkg_name + ': checking for updates...'

    git_output = check_output(['git', 'ls-remote', '--tags', plugin_arg])

    for git_line in git_output.splitlines():
        sha1, tag = git_line.split()

        # eliminate duplicate tags that end with ^{}
        if tag.endswith('^{}'):
            continue

        # remove /refs/tags/
        version = tag[10:]

        if compare_versions(last_version, version) > 0:
            print 'NEW VERSION: ' + version
