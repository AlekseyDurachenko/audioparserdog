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
from audiowebpagedog_downloader import *


def init(db):
    db.create_tables()
    sys.exit(0)


def get_prop_download_directory(db):
    print("property[download_directory] = %s" %
          (db.get_property("download_directory",)))
    sys.exit(0)


def set_prop_download_directory(db, download_directory):
    db.set_property("download_directory", download_directory)
    sys.exit(0)


def page_list(db):
    dl_dir = db.get_property("download_directory",)
    for channel in db.get_pages():
        print("* %s (%s) -> %s" % (channel['link'],
                                   channel['subdir'],
                                   os.path.join(dl_dir, channel['subdir'])))
    sys.exit(0)


def page_add(db, link, subdir):
    if not db.add_page(link, subdir):
        print("the channel is already exists")
    sys.exit(0)


def page_edit(db, link, subdir):
    if not db.edit_page(link, subdir):
        print("the channel is not exists")
    sys.exit(0)


def page_remove(db, link):
    db.remove_page(link)
    sys.exit(0)


def print_usage():
    print("""=== audio web page control v.0.1.0 ===
Usage:
    audiowebpagedog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                            -- init the database
    set download_directory <path>   -- set the download directory
    get download_directory          -- show the download directory
    page add <page_url> <subdir>    -- add the page
    page edit <page_url> <subdir>   -- change the page directory
    page remove <page_url>          -- remove the page
    page list                       -- show the page list
""")
    sys.exit(-1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        audioParserDb = AudioWebPageDb()

        # init
        if sys.argv[1] == "init":
            init(audioParserDb)
        # get <property>
        elif sys.argv[1] == "get" and len(sys.argv) > 2:
            # get download_directory
            if sys.argv[2] == "download_directory":
                get_prop_download_directory(audioParserDb)
        # set <property>
        elif sys.argv[1] == "set" and len(sys.argv) > 2:
            # set download_directory
            if sys.argv[2] == "download_directory" and len(sys.argv) == 4:
                set_prop_download_directory(audioParserDb, sys.argv[3])
        # podcast <command>
        elif sys.argv[1] == "page" and len(sys.argv) > 2:
            # podcast add <rss_url> <subdir>
            if sys.argv[2] == "add" and len(sys.argv) == 5:
                page_add(audioParserDb, sys.argv[3], sys.argv[4])
            # podcast edit <rss_url> <subdir>
            if sys.argv[2] == "edit" and len(sys.argv) == 5:
                page_edit(audioParserDb, sys.argv[3], sys.argv[4])
            # podcast remove <rss_url>
            elif sys.argv[2] == "remove" and len(sys.argv) == 4:
                page_remove(audioParserDb, sys.argv[3])
            # podcast list
            elif sys.argv[2] == "list":
                page_list(audioParserDb)
    # invalid
    print_usage()
