this challenge is super fun (but at what cost), requires some reading and debugging tho  . 


1. we have 21 arbitrary reads within our binary (even though PIE is enabled) as there is no checks on the **pick** . with this we can leak a libc value from got for example (we leak first lower 32 bits first then the higher 32 bits and we assemble them)
2. the **lucky_numbers** is a total bait , dont even bother looking at it . 
3. there is no chance to write out of bounds so we will need to face the **rand()** face to face . 


### some infos about random : 
before going down the hill , i recommend you read some source code (it aint hard believe me ) * [random_r](https://github.com/lattera/glibc/blob/master/stdlib/random_r.c) .
my first thought was that the seed is saved somewhere in libc and if we leak it its GG . so i had to step through the rand function and see for my self but i got bored so i went reading its source . reading though **srandom_r** which is the real deal , it looked like the seed is at **state[0]** , but at the end of the function it changes (used gdb) so we'll need another way to do predict the value  . one thing to mention is that srand does some calculation based on the seed value and places the results in the array **state**

Reading through _random_r which is the real rand , the return value looked very easy to calculate **ret = (a+b) >> 1** . after some reading and gdb tracing , i found out that these a and b are values from the **state** array in such way : **a=state[i] ; b=state[i+3]** and after doing a 
rand() , **state[i+3]=a+b** . so yes you guesses it right , we will leak the entire **state** array and bingo . 

i never thought the 'unpredictable' random function is this easily implemented tho . never saw it coming .

![flag](/super-lucky/flag.png)

🥲🥲