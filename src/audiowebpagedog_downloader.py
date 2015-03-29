#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2015, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
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
from _operator import sub
import feedparser
import urllib.parse
import urllib.request
import shutil
import sys
import re
import notify2
from audiowebpagedog_db import *


class AudioWebPageDownloader:
    __db = None

    def __init__(self, db):
        self.__db = db

    def download_directory(self):
        return self.__db.get_property("download_directory")

    def parse_url(self, url):
        return urllib.parse.urlparse(url).path.split('/')[-1]


    def dst_filename(self, url, subdir):
        return os.path.join(
            self.download_directory(), subdir, self.parse_url(url))

    def download_url(self, url, dst_filename):
        dir = os.path.dirname(dst_filename)
        if not os.path.exists(dir):
            os.makedirs(dir)

        try:
            print("Download url: %s" % (url,))
            tmp_filename, h = urllib.request.urlretrieve(url)
            print("Download complete! Temporary filename: %s" % (tmp_filename,))
            if os.path.getsize(tmp_filename) < 1024*128:
                print("The size of a file is less than 128k")
                return False
            shutil.move(tmp_filename, dst_filename)
            print("Moving complete! Permanent filename: %s" % (dst_filename,))
            return True
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            return False

    def create_description(self, link):
        return "<center><b>%s</b> downloaded</center>" % (link,)


    def parse_page(self, link):
        response = urllib.request.urlopen(link)
        html = response.read()
        codec = response.info().get_param('charset', 'utf8')
        html = html.decode(codec)
        url_list = []
        for url in re.finditer('https://([0-9a-zA-Z\.\-\_\/\+]{1,}).mp3', html):
            url_list.append(url.group(0))
        for url in re.finditer('http://([0-9a-zA-Z\.\-\_\/\+]{1,}).mp3', html):
            url_list.append(url.group(0))
        return url_list


    def download_page(self, link, subdir):
        audiofiles = self.parse_page(link)
        exists_audiofiles = set(self.__db.get_audio_files(link))
        for audiofile in audiofiles:
            # http or https links are mixed in the rss,
            # we should to prevent this situation
            http_audiofile_url = audiofile
            if http_audiofile_url[0:5] == "https":
                http_audiofile_url = "http" + http_audiofile_url[5:]
            if http_audiofile_url not in exists_audiofiles:
                if self.download_url(audiofile,
                                     self.dst_filename(audiofile, subdir)):
                    self.__db.add_audio_file(link, audiofile)
                    try:
                        notify2.init("audiowebpagedog")
                        notify = notify2.Notification(
                            "New audiofile is available",
                            self.create_description(audiofile))
                        notify.show()
                    except:
                        pass


    def download_pages(self):
        for page in self.__db.get_pages():
            if page["active"]:
                self.download_page(page["link"], page["subdir"])
