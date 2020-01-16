.text
globl main
.type main, @function
main:

pushl %ebp
movl %esp, %ebp
movl $2 ,None(%ebp)
subl $4, %esp
subl $4, %esp
subl $4, %esp
subl $4, %esp
movl %eax,None(%ebp)
