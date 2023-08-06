# Terminates a subprocess gracefully, if it doesn't work, it will be killed (Windows only)

## pip install gracefully_kill

#### Tested against Windows 10 / Python 3.10 / Anaconda


The function attempts to terminate the subprocess gracefully by closing its standard input, output, and error streams, waiting for a specified timeout, 
and finally terminating the process. 
This allows the subprocess to clean up its resources and exit properly.
The function checks if the process is still alive after termination attempts. 
If it is, it uses the taskkill_force_pid_children function from the taskkill module to forcibly terminate 
any child processes associated with the given process ID. 
This ensures that the entire process hierarchy is terminated if necessary.


```python
pro=subprocess.Popen('ping -t 8.8.8.8')
kill_process(pro, timeout=1)
```

