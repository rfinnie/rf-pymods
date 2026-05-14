# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2018 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT

import sys
import os
import shlex
import subprocess


class AutoPager:
    # SPDX-SnippetComment: Originally from https://forge.colobox.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: © 2018 Ryan Finnie <ryan@finnie.org>
    # SPDX-LicenseInfoInSnippet: MIT

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __init__(self):
        self.closed = False
        self.pager = None
        if sys.stdout.isatty():
            pager_cmd = ["pager"]
            if os.environ.get("PAGER"):
                pager_cmd = shlex.split(os.environ.get("PAGER"))
            env = os.environ.copy()
            if not os.environ.get("LESS"):
                env.update({"LESS": "FRX"})
            try:
                self.pager = subprocess.Popen(
                    pager_cmd,
                    stdin=subprocess.PIPE,
                    stdout=sys.stdout,
                    encoding="UTF-8",
                    env=env,
                )
            except FileNotFoundError:
                pass

    def write(self, line):
        if self.closed:
            return

        fh = self.pager.stdin if self.pager else sys.stdout
        try:
            fh.write(line)
        except KeyboardInterrupt:
            self.close()
        except BrokenPipeError:
            self.close()

    def close(self):
        if self.closed:
            return

        if self.pager:
            try:
                self.pager.stdin.close()
            except BrokenPipeError:
                pass
            ret = None
            while ret is None:
                try:
                    ret = self.pager.wait()
                except KeyboardInterrupt:
                    pass

        self.closed = True
