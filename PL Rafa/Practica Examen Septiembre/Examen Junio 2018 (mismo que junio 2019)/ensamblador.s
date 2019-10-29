.text
.type mcd,@function
.globl mcd
mcd:
    pushl %ebp
    movl %esp,%ebp

    subl $4,%esp    # int resto;


    movl -4(%esp),%eax # while(b!=0)
    start:
    cmpl $0,%eax
    je final
   
    cdq                # resto = a%b; 
    movl 8(%esp),%eax
    divl %ebx
    movl %edx,-4(%esp)

    movl 12(%esp),8(%esp) # a = b;
    movl -4(%esp),12(%esp) # b = resto;
    jmp start
    final:


    movl 8(%esp),%eax   # return a;
    popl %ebp
    movl %ebp,%esp
    ret

main:
    pushl %ebp
    movl %esp,%ebp

    subl $4,%esp    # int x;

    pushl $s0       # printf("introduce dos enteros: ");
    call printf
    addl $4,%esp

    pushl $y        # scanf("%d%d",&x,&y)
    leal -4(%esp),%eax
    pushl %eax
    pushl $s1
    call scanf
    addl $12,%esp

    pushl y         # mcd(c,y)
    pushl -4(%esp)
    call mcd
    addl $8,%esp

    pushl %eax      # printf(....)
    pushl y
    pushl -4(%esp)
    pushl $s2
    call printf
    addl $16,%esp

    movl $0,%eax    # return 0;
    popl %ebp
    movl %ebp,%esp

    ret