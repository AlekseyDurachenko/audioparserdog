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
import sqlite3
import os


class AudioWebPageDb:
    """This class used for access the database. The database structure:

--------------------------------------------------------------|
| TProperty (the property table)                              |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| name      | string   | unique         | property name       |
| value     | string   |                | property value      |
--------------------------------------------------------------|

--------------------------------------------------------------|
| TPage (the page with audio files)                           |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| link      | string   | unique         | link to page        |
| subdir    | string   |                | subdir for files    |
| active    | integer  |                | 0 - inactive        |
| comment   | string   |                | description         |
--------------------------------------------------------------|

--------------------------------------------------------------|
| TAudioFile (the downloaded audio files)                     |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| TPageId   | integer  | unique         |                     |
| link      | integer  | unique         | link to audio file  |
--------------------------------------------------------------|
    """
    __conn = None

    def __init__(self):
        path = os.path.expanduser("~")          \
                + os.path.sep + ".config"       \
                + os.path.sep + "audiowebpagedog"
        if not os.path.exists(path):
            os.makedirs(path)
        self.__conn = sqlite3.connect(os.path.join(path, 'audiowebpagedog.db'))
        self.__conn.text_factory = str

    def create_tables(self):
        cursor = self.__conn.cursor();
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TProperty(
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL);""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TPage(
                id INTEGER PRIMARY KEY NOT NULL,
                link TEXT NOT NULL,
                subdir TEXT NOT NULL,
                active INTEGER NOT NULL,
                comment TEXT NOT NULL,
                UNIQUE(link));""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TAudioFile(
                id INTEGER PRIMARY KEY NOT NULL,
                TPageId INTEGER NOT NULL,
                link TEXT NOT NULL,
                UNIQUE(TPageId, link));""")
        self.__conn.commit()

    def set_property(self, name, value):
        cursor = self.__conn.cursor()
        try:
            cursor.execute("INSERT INTO TProperty(name, value) VALUES(?, ?)",
                           (name, value))
        except sqlite3.IntegrityError:
            cursor.execute("UPDATE TProperty SET value = ? WHERE name = ?",
                           (value, name))
        self.__conn.commit()

    def get_property(self, name):
        cursor = self.__conn.cursor()
        for row in cursor.execute(
                "SELECT value FROM TProperty WHERE name = ?", (name,)):
            return row[0]
        return None

    def add_page(self, link, subdir, comment=""):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(
                "INSERT INTO TPage(link, subdir, active, comment) "
                "VALUES(?, ?, ?, ?)", (link, subdir, 1, comment))
            self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def edit_page(self, link, subdir, comment=""):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(
                "UPDATE TPage SET subdir = ? "
                "WHERE link = ?", (subdir, link))
            self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def remove_page(self, link):
        cursor = self.__conn.cursor()
        cursor.execute("DELETE FROM TPage WHERE link = ?", (link,))
        self.__conn.commit()

    def add_audio_file(self, channel_link, podcast_link):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO TAudioFile(TPageId, link) "
                           "VALUES((SELECT id FROM TPage WHERE link = ?),"
                           "?)", (channel_link, podcast_link))
            self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def remove_audio_file(self, channel_link, podcast_link):
        cursor = self.__conn.cursor()
        cursor.execute("DELETE FROM TAudioFile WHERE "
                       "TPageId = (SELECT id FROM TPage WHERE link = ?) "
                       "AND link = ?", (channel_link, podcast_link))
        self.__conn.commit()

    def get_audio_files(self, channel_link):
        cursor = self.__conn.cursor()
        return [row[0] for row in cursor.execute(
                "SELECT link FROM TAudioFile WHERE TPageId = "
                "(SELECT id FROM TPage WHERE link = ?)", (channel_link,))]

    def get_pages(self):
        cursor = self.__conn.cursor()
        return [{"link": row[0], "subdir": row[1], "active": row[2]}
                for row in cursor.execute("SELECT link, subdir, active "
                                          "FROM TPage")]
