# coding: utf-8

import os.path
import re
import sublime
import sublime_plugin

class AlloySwitcherCommand(sublime_plugin.WindowCommand):
    def run(self, type, *args, **kwargs):
        _root = self.window.folders()[0]
        _file = self.window.active_view().file_name()
        _type = None
        _path = None

        controllers_regex = re.compile(r"\.js$")
        views_regex = re.compile(r"\.xml$")
        styles_regex = re.compile(r"\.tss$")

        if controllers_regex.search(_file) is not None:
            _type = "controllers"
            _path = _file.replace(os.path.join(_root, "app", "controllers"), "")
            _path = controllers_regex.sub("", _path)
        elif views_regex.search(_file) is not None:
            _type = "views"
            _path = _file.replace(os.path.join(_root, "app", "views"), "")
            _path = views_regex.sub("", _path)
        elif styles_regex.search(_file) is not None:
            _type = "styles"
            _path = _file.replace(os.path.join(_root, "app", "styles"), "")
            _path = styles_regex.sub("", _path)
        else:
            return True

        if type == _type:
            return True
        elif type == "controllers":
            _path = os.path.join(_root, "app", "controllers") + _path + ".js"
        elif type == "views":
            _path = os.path.join(_root, "app", "views") + _path + ".xml"
        elif type == "styles":
            _path = os.path.join(_root, "app", "styles") + _path + ".tss"
        else:
            return True

        if os.path.exists(_path):
            self.window.open_file(_path)
