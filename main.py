import re
import os
from pathlib import Path

import sublime, sublime_plugin

class SublimeGoToFileCommand(sublime_plugin.TextCommand):
    # in the future get pattern from settings?
    # aka multi languages support???
    pattern = re.compile(r"[\'|\"](.*?)[\'|\"]")

    def run(self, edit):
        current_match = self.match[0]
        opened_file = Path(self.view.file_name())
        possible_full_path = Path(opened_file.parent, current_match)
        possible_file_path = self.possible_file_path(str(possible_full_path))

        if possible_file_path:
            print('File exists @ {} opening...'.format(possible_file_path))
            self.view.window().open_file(possible_file_path)
        else:
            print('trying somethng else...')
            print('basename', os.path.basename(current_match))
            print('dirname', os.path.dirname(current_match))

            for i in opened_file.parents:
                possible_file_path = self.possible_file_path(str(i.joinpath(current_match)))
                if possible_file_path:
                    break

            print('done walking', current_match)
            print('done walking :: possible_file_path', possible_file_path)

            if possible_file_path:
                self.view.window().open_file(possible_file_path)

    def is_visible(self):
        self.current_line = self.view.line(self.view.sel()[0])
        self.text = self.view.substr(self.current_line)
        self.match = self.pattern.findall(self.text.strip())

        return len(self.match) > 0

    # only works for relative paths
    def possible_file_path(self, path):
        from glob import glob

        print('suffixes', Path(path).suffixes)

        (_, ext) = os.path.splitext(self.view.file_name())
        (file_name, _) = os.path.splitext(path)

        print('file_name', file_name)

        if len(Path(path).suffixes) == 0:
            pattern = path + '*'
        else:
            # pattern = '*' + ''.join(Path(path).suffixes) + '*'
            full = Path(os.path.join(file_name) + ext)

            if full.exists():
                return str(full)

        print('pattern', pattern)

        path_lists = glob(pattern)

        print('path_lists', path_lists)

        # print('1', Path(path).joinpath('*.old').resolve())

        if len(path_lists) > 0:
            return path_lists[0]
        else:
            return False
