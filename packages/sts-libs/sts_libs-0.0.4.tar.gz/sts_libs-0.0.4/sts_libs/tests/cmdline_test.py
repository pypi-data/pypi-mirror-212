#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import io
import sys
import unittest

from sts.utils.cmdline import run, run_ret_out


class TestCmdline(unittest.TestCase):
    def test_run_verbose(self):
        test_msg = "run test message"
        # write to stderr, the message should be shown in the test
        test_cmd = f"echo {test_msg} >&2"
        running_string = f"Running command: '{test_cmd}'"

        new_callable = io.StringIO()
        sys.stdout = new_callable
        # Default is verbose=True
        assert run(test_cmd).returncode == 0
        sys.stdout = sys.__stdout__
        assert running_string in new_callable.getvalue().split("\n")[0]
        assert test_msg in new_callable.getvalue().split("\n")[1]
        sys.stdout = sys.__stdout__

        # not verbose
        new_callable = io.StringIO()
        sys.stdout = new_callable
        assert run(test_cmd, verbose=False).returncode == 0
        sys.stdout = sys.__stdout__
        assert new_callable.getvalue() == ""
        sys.stdout = sys.__stdout__

    def test_run_return_output(self):
        test_msg = "run test message"
        test_cmd = f"echo {test_msg}"
        ret_out = run(test_cmd, capture_output=True)
        assert ret_out.returncode == 0
        assert ret_out.output == test_msg

    def test_run_return_output_legacy(self):
        test_msg = "run test message"
        test_cmd = f"echo {test_msg}"
        assert run_ret_out(test_cmd, return_output=True) == (0, test_msg)

    def test_run_fail_return_output(self):
        failure_msg = "ls: cannot access 'invalid_file': No such file or directory"
        test_cmd = "ls invalid_file"
        ret_out = run(test_cmd, capture_output=True)
        assert ret_out.returncode == 2
        assert ret_out.output == failure_msg

    def test_run_fail_return_output_legacy(self):
        failure_msg = "ls: cannot access 'invalid_file': No such file or directory"
        test_cmd = "ls invalid_file"
        assert run_ret_out(test_cmd, return_output=True) == (2, failure_msg)

    def test_run_timeout(self):
        test_cmd = "sleep 9"
        expected_retcode = 124
        assert run(test_cmd, timeout=1).returncode == expected_retcode

    def test_run_timeout_legacy(self):
        test_cmd = "sleep 9"
        expected_retcode = 124
        assert run_ret_out(test_cmd, return_output=True, timeout=1) == (expected_retcode, None)
