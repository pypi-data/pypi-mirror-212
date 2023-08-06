"""cmdline.py: Module to execute a command line."""

#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import subprocess
from datetime import datetime, timezone
from shutil import which
from typing import IO, Optional, Tuple, Union


class StsCompletedProcess:
    """A process that has finished running.

    This is returned by run().
    Derived from subprocess.run()

    Attributes:
      returncode: The exit code of the process, negative for signals.
      output: stdout and stderr combined (None if not captured).
    """

    def __init__(self, returncode, output=None):
        self.returncode = returncode
        self.output = output

    def __repr__(self):
        args = [f"{self.returncode=}"]
        if self.output is not None:
            args.append(f"{self.output=}")


def run(
    cmd: str,
    timeout: Optional[int] = None,
    capture_output: bool = False,
    use_popen: bool = False,
    verbose: bool = True,
) -> StsCompletedProcess:
    """Runs a shell command and returns the CompletedProcess object.

    Usage:
        verbose = False, capture_out

    Args:
        cmd (str): The command to run in the shell.
        timeout (int, optional): The maximum amount of time (in seconds) to wait for the command to finish
            (default None; no timeout).
        capture_output (bool): Whether to capture combined stdout and stderr. (default False)
            When verbose=False and capture_output=False, output will be directed to DEVNULL
        use_popen (bool, optional): Whether to use subprocess.Popen() to execute the command and
            fetch output in real-time (default False; use subprocess.run()).
        verbose (bool, optional): Whether to print the command and output. (default True).

    Returns:
        StsCompletedProces
    """
    if not verbose and use_popen:
        print("WARN: Using run() with use_popen=True, verbose=False!")

    if verbose:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"INFO: {timestamp} Running command: '{cmd}'")

    if use_popen:
        output_str = ""
        try:
            # Using Popen to execute command with real-time output
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            stdout: Optional[IO[str]] = process.stdout
            if stdout is not None:
                while True:
                    output_line = stdout.readline()
                    if not output_line and process.poll() is not None:
                        break
                    output_str += output_line
                    if verbose:
                        print(output_line.rstrip())

            process.wait(timeout=timeout)
            retcode = process.poll()
            return StsCompletedProcess(
                returncode=retcode,
                output=output_str.rstrip() if output_str else None,
            )
        except subprocess.TimeoutExpired:
            if verbose:
                print("WARN: Command timed out")
            return StsCompletedProcess(returncode=124, output=output_str if output_str else None)

    stdout_destination = subprocess.PIPE
    if not capture_output and not verbose:
        stdout_destination = subprocess.DEVNULL

    # Using run to execute command, returns CompletedProcess object
    try:
        cp = subprocess.run(
            cmd,
            shell=True,
            text=True,
            stdout=stdout_destination,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        ret_out = StsCompletedProcess(returncode=cp.returncode, output=cp.stdout.rstrip() if cp.stdout else None)

        if not capture_output and verbose and ret_out.output:
            print(ret_out.output)

        return ret_out

    except subprocess.TimeoutExpired as e:
        return StsCompletedProcess(returncode=124, output=e.stdout if e.stdout else None)


def run_ret_out(
    cmd: str,
    timeout: Optional[int] = None,
    return_output: bool = False,
    use_popen: bool = False,
    verbose: bool = True,
) -> Union[int, Tuple[int, str]]:
    """Runs cmd and returns returncode int or returncode int, output str tuple.

    For legacy compatibility only. TODO: remove it an it's usages
    """
    completed_command = run(
        cmd=cmd,
        timeout=timeout,
        use_popen=use_popen,
        verbose=verbose,
        capture_output=bool(return_output),
    )

    if return_output:
        return completed_command.returncode, completed_command.output

    return completed_command.returncode


def exists(cmd):
    if not which(str(cmd)):
        return False
    return True
