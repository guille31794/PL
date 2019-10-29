.text
.globl fact
.type fact,@function
fact:

    pushl %ebp
    movl %esp,%ebp

    cmpl 8(%esp),$1 # if(n<=1)
    jge true
    movl $8(%esp),%eax # return n*fact(n-1)
    subl $1,%eax
    pushl %eax
    call fact
    addl $4,%esp
    imull 8(%esp),%eax
    jmp final
    true:
    movl $1,%eax    # return 1
    final:
    movl %ebp,%esp
    popl %ebp
    ret

.text
.globl main
.type main,@function
main:
    
    pushl %ebp
    movl %esp,%ebp

    pushl $s0   # printf("Dame...")
    call printf
    addl $4,%esp

    pushl $numero # scanf("%d"....)
    pushl $s1
    call scanf
    addl $8,%esp

    pushl numero
    call fact
    addl $4,%esp
    
    pushl %eax # printf("El factorial...")
    pushl $s2
    call printf
    addl $8,%esp

    movl $0,%eax # return 0;
    movl %ebp,%esp
    popl %ebp
    ret



