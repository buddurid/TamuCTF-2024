this might be my first time in a format string challenge that i wanna break out of the infinite loop . to sum up the problems we have : 
1. our buffer that we write into isnt on the stack so we cant write an address then read to it (like a typical fs challenge), but we can still write into buffers that are on the stack . 
2. full relro so overwriting got of printf with system wont give us a shell
3. infinite loop so we cant execute neither leave (for pivoting) nor ret (for rop) , but we will solve this later 

the upside is everything is leaked so if we find a way to abitrary write its GG . the idea is to find a value on the stack that points to a stack value , so if we write using %hhn or %hn into that value , we can obtain in the second value a stack value that we can control hover we want . for example : 5th value on the stack is 0x7ffffffa20 . in the address 0x7ffffffa20 , there is another stack value 0x7ffffffb50 . this way we can write 0x80 into it and it becomes 0x7ffffffb0 . then we can write into it . in some ASLR extreme cases , some stack missalignements might happen (i put an assertion in my script) . but the idea is create the return address for the **Vuln** function then write a one gadget to it (you can write a full rop to it as well) then we write the create the address of **always_true** and write 0 to it , so it we quit the loop and ret . 
Was a good challenge thanks for author . 

