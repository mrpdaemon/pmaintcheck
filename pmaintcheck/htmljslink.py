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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

import re, urllib2, sys

class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

def get_version_list(plugin_arg):
    """ Plugin arguments: URL|Template
        where Template is of the form http://some.url/folder/%v-.*\.tar\.gz
        using regex syntax and %v denotes the location of the version string
    """
    version_list = []

    url, template = plugin_arg.split('|')

    result = unicode(Render(url).frame.toHtml()).encode('utf-8')
    soup = BeautifulSoup(result)

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
