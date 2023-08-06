import subprocess

from taskkill import taskkill_force_pid_children

from isa import is_process_alive


def kill_process(p: subprocess.Popen, timeout=1) -> None:
    """
    Terminate and kill a subprocess with the given process handle.

    Args:
        p (subprocess.Popen): The subprocess handle to terminate and kill.
        timeout (int, optional): Timeout value for waiting for process termination. Default is 1 second.

    Raises:
        None

    Returns:
        None
    """
    try:
        # let's try to terminate it gracefully
        try:
            p.stdout.close()
        except Exception:
            pass
        try:
            p.stdin.close()
        except Exception:
            pass
        try:
            p.stderr.close()
        except Exception:
            pass
        try:
            p.wait(timeout=timeout)
        except Exception:
            pass
        try:
            p.terminate()
        except Exception:
            pass
    except Exception:
        pass

    try:
        if is_process_alive(p.pid):
            taskkill_force_pid_children(pids=(p.pid,))
    except Exception:
        pass
