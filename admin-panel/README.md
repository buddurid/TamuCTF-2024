first challenge should be fairly ez , use first overflow to create format string vuln , leak libc and canary then use second overflow to rop into libc **system("/bin/sh")**.
i dont know why the offset to libc a lil bit different than the libc file they provided but whatever. 
look up the solver in sol.py if you wanna . 