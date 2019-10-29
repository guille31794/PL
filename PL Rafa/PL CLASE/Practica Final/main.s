.section .rodata.text
.globl main
.type main, @function
main:
    pushl %ebp
    movl %esp, %ebp

    cmpl $1,$1
    je EQ
    movl $0,%eax
    jmp F-EQ
EQ:
    movl $1,%eax
F-EQ:
    cmpl $0, %eax
    je final
start:
    cmpl a,$1
    jne NE
    movl $0,%eax
    jmp F-NE
NE:
    movl $1,%eax
F-NE:
    cmpl $0, %eax
    je final
    movl $1, %eax
    addl a, %eax
    movl %eax, a
    jmp start:
final:
final:
    movl $0, %eax

    movl %ebp, %esp
    popl %ebp
    ret