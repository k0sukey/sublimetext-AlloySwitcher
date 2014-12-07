# coding: utf-8

import os.path
import re
import sublime
import sublime_plugin

class AlloySwitcherCommand(sublime_plugin.WindowCommand):
    def run(self, type, *args, **kwargs):
        settings = sublime.load_settings("AlloySwitcher.sublime-settings")
        private = sublime.active_window().active_view().settings()

        controller_dir = private.get("controller_dir", settings.get("controller_dir"))
        view_dir = private.get("view_dir", settings.get("view_dir"))
        style_dir = private.get("style_dir", settings.get("style_dir"))
        ios_dir = "Resources/iphone/alloy/controllers"
        android_dir = "Resources/android/alloy/controllers"

        controller_ext = private.get("controller_ext", settings.get("controller_ext"))
        view_ext = private.get("view_ext", settings.get("view_ext"))
        style_ext = private.get("style_ext", settings.get("style_ext"))

        _root = self.window.folders()[0]
        _file = self.window.active_view().file_name()
        _type = None
        _path = None

        controllers_regex = re.compile(r"\." + controller_ext + "$")
        views_regex = re.compile(r"\." + view_ext + "$")
        styles_regex = re.compile(r"\." + style_ext + "$")
        ios_regex = re.compile(r"\.js$")
        android_regex = re.compile(r"\.js$")

        if controllers_regex.search(_file) is not None:
            _type = "controllers"
            _path = _file.replace(os.path.join(_root, "app", controller_dir), "")
            _path = controllers_regex.sub("", _path)
        elif views_regex.search(_file) is not None:
            _type = "views"
            _path = _file.replace(os.path.join(_root, "app", view_dir), "")
            _path = views_regex.sub("", _path)
        elif styles_regex.search(_file) is not None:
            _type = "styles"
            _path = _file.replace(os.path.join(_root, "app", style_dir), "")
            _path = styles_regex.sub("", _path)
        else:
            return True

        if type == _type:
            return True
        elif type == "controllers":
            _path = os.path.join(_root, "app", controller_dir) + _path + "." + controller_ext
        elif type == "views":
            _path = os.path.join(_root, "app", view_dir) + _path + "." + view_ext
        elif type == "styles":
            _path = os.path.join(_root, "app", style_dir) + _path + "." + style_ext
        elif type == "ios":
            _path = os.path.join(_root, ios_dir) + _path + ".js"
        elif type == "android":
            _path = os.path.join(_root, android_dir) + _path + ".js"
        else:
            return True

        if os.path.exists(_path):
            self.window.open_file(_path)
