.text
.globl main
.type main, @function
main:
    pushl %ebp
    movl %esp, %ebp

    cmp $1,$0
    je AND
    cmp $0,$0
    je AND
    movl $1,%eax
    jmp F-AND
    AND:
    movl $0,%eax
    F-AND:
    movl %eax, a
    movl $4, %eax
    addl $1, %eax
    movl %eax, a
    subl $4, %esp
    movl $2, %eax
    imull a, %eax
    movl %eax,  -4(%ebp)
    movl  -4(%ebp), %eax
    cdq
    movl a, %ecx
    divl %ecx
    movl %ecx, %eax

    movl %ebp, %esp
    popl %ebp
    ret