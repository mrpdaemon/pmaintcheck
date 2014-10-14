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

from BeautifulSoup import BeautifulSoup

import re, urllib2

def get_version_list(plugin_arg):
    """ Plugin arguments: URL|Template
        where Template is of the form http://some.url/folder/%v-.*\.tar\.gz
        using regex syntax and %v denotes the location of the version string
    """
    version_list = []

    url, template = plugin_arg.split('|')

    soup = BeautifulSoup(urllib2.urlopen(url).read())

    for link in soup.findAll('a', href=True):

        # replace %v with .* for the regex
        regex_pattern = template.replace('%v', '.*')

        if re.search(regex_pattern, link['href']) is None:
            continue

        # split template to the stuff before/after %v
        template_pre, template_post = template.split('%v')

        # throw away template_pre from the link
        result = link['href'][len(template_pre):]

        # search for template_post in the link
        link_post = re.search(template_post, link['href'][len(template_pre):])
        if link_post is None:
            continue

        # remove template_post from the link
        version = result[:-len(link_post.group(0))]

        if version not in version_list:
            version_list.append(version)

    return version_list
