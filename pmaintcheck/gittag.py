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

def _cleanup_version(version):
    # remove preceding strings
    result = re.search("\d", version)
    if result:
        version_clean = version[result.start():].replace('_','.')
    else:
        return ''

    # remove trailing strings
    result = re.search("-", version_clean)
    if result:
        version_clean = version_clean[:result.start()]

    return version_clean

def get_version_list(plugin_arg):
    """ Plugin arguments: repo-url|ignore-versions
        where ignore-versions is a comma separated list of tags to ignore
    """
    version_list = []

    repo_url, ignore_list = plugin_arg.split('|')
    ignore_versions = ignore_list.split(',')

    git_output = check_output(['git', 'ls-remote', '--tags', repo_url])

    for git_line in git_output.splitlines():
        sha1, tag = git_line.split()

        # eliminate duplicate tags that end with ^{}
        if tag.endswith('^{}'):
            continue

        # remove /refs/tags/ and clean up
        version = _cleanup_version(tag[10:])

        if version not in ignore_versions:
            version_list.append(version)

    return version_list
