""" Coldsnap Filesystem Walkers

Provides filesystem-walking classes to iterate files.
"""

import fnmatch
import os

class BaseWalker(object):
    """
    """

    def __init__(self, top_dir):
        self._top_dir = top_dir

    def walk(self):
        for (base_path, directories, files) in os.walk(self._top_dir,
                onerror=self._handle_walk_error, followlinks=False):
            #this and the files line probably wont work, probably need to make
            # our own walk implementation, with blackjack and callbacks!
            directories = self._filter_directories(base_path, directories)
            for full_path in (os.path.join(base_path, d) for d in directories):
                yield full_path
            files = self._filter_files(base_path, files)
            for full_path in (os.path.join(base_path, f) for f in files):
                yield full_path

    def _filter_directories(self, base_path, directories):
        return directories

    def _filter_files(self, base_path, files):
        return files

    def _handle_walk_error(self, error):
        raise error


class SimpleFilteringWalker(BaseWalker):
    """
    """

    def __init__(self, top_dir, allow_patterns=None, deny_patterns=None):
        super(SimpleFilteringWalker, self).__init__(top_dir)
        self._allow = allow_patterns if allow_patterns is not None else []
        self._deny = deny_patterns if deny_patterns is not None else []

    def _filter_directories(self, base_path, directories):
        full_paths = [os.path.join(base_path, d) for d in directories]
        denied = set(fnmatch.filter(full_paths, p) for p in self._deny)
        exp_allowed = set(fnmatch.filter(denied, p) for p in self._allow)
        allowed = [d for d in full_paths if d not in denied or d in exp_allowed]
        return allowed

    def _filter_files(self, base_path, files):
        full_paths = [os.path.join(base_path, f) for f in files]
        denied = set(fnmatch.filter(full_paths, p) for p in self._deny)
        exp_allowed = set(fnmatch.filter(denied, p) for p in self._allow)
        allowed = [f for f in full_paths if f not in denied or f in exp_allowed]
        return allowed
