import sublime
import sublime_plugin
import os
import re
import plistlib


class EndLineCommand(sublime_plugin.TextCommand):

    @staticmethod
    def find_key(plist, needle):
        if isinstance(plist, list):
            for item in plist:
                result = EndLineCommand.find_key(item, needle)
                if result is not None:
                    return result
        elif isinstance(plist, dict):
            for key, value in plist.iteritems():
                if isinstance(value, str) and re.match(needle, value):
                    return plist
                else:
                    result = EndLineCommand.find_key(value, needle)
                    if result is not None:
                        return result
        return None

    IGNORE_LINES = ['.*{\s*$', '.*}\s*$', '\s*$', '.*,\s*$']

    def run(self, edit):
        path = os.path.join(os.path.dirname(sublime.packages_path()), self.view.settings().get('syntax'))
        language = plistlib.readPlist(path)
        endliner = EndLineCommand.find_key(language, 'punctuation.terminator')
        print endliner
        if endliner is not None and 'match' in endliner:
            endliner = endliner['match'].replace('\\', '')
            line = self.view.line(self.view.sel()[0])
            line_content = self.view.substr(line)
            if line_content[-1:] != endliner and not EndLineCommand.match_regex(self.IGNORE_LINES, line_content):
                self.view.insert(edit, line.end(), endliner)
                print 'add end'
        self.view.run_command('run_macro_file', {"file": "Packages/Default/Add Line.sublime-macro"})

    @staticmethod
    def match_regex(regexlist, string):
        for regex in regexlist:
            if re.match(regex, string):
                return True
        return False
