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

def compare_versions(version1, version2):
    """Do a version comparison on strings version1 and version2"""
    # handle empty version strings
    if (len(version2) == 0):
        if (len(version1) == 0):
            return 0
        else:
            return -1
    elif (len(version1) == 0):
        return 1

    # tokenize and compare each version atom
    for version1_atom,version2_atom in zip(version1.split('.'),
                                           version2.split('.')):
        if int(version1_atom) > int(version2_atom):
            return -1
        elif int(version2_atom) > int(version1_atom):
            return 1

    # handle cases like 1.0.1 vs. 1.0.1.1
    if len(version1) > len(version2):
        return -1
    elif len(version2) > len(version1):
        return 1

    # versions equal
    return 0

