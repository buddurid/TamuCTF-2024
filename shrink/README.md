i dont know how and why does my script work , but here we go . the vulnerability i remarqued is the address of the string address in our username instance is swapped with a stack value that is the **&username+0x10** if you write input with len<14 .(for some reasons i obviously dont know but maybe due to shrink_to_fit() ). this sometimes doesnt work but i kept playing with it . when we obtain this pointer we write into it to overwrite the len variable with a bigger value so when we do the same thing again we reach the ret value and ret2win . 

i totally dont recommend this writeup for this challenge . but a flag is flag i guess .  