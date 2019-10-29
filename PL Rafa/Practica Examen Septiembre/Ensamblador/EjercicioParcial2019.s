.text
.globl despl
.type despl,@function
despl:

    pushl %ebp
    movl %esp,%ebp

    subl $4,%esp    //int e;

    movl $12(%ebp),%eax //(v0 * t)
    imull $16(%ebp),%eax
    pushl %eax

    movl  16(%ebp), %eax      # mueve t al registro eax
    imull 16(%ebp), %eax      # t * t --> eax
    imull 20(%ebp), %eax      # a * t * t --> eax
    movl  $2, %ebx
    cdq
    idivl %ebx
    pushl %eax                # almacena resultado intermedio en la pila (1/2 * a * t * t)


    popl %ebx           //e = e0 + (v0 * t) + (1/2 * a * t * t);
    popl %eax
    addl %ebx,%eax
    addl 8(%ebp),%eax
    movl %eax,-4(%ebp)

    movl -4(%ebp),%eax  //return e;

    movl %ebp,%esp
    popl %ebp  
    ret


.text
.globl main
.type main,@function
main:

    pushl %ebp
    movl %esp,%ebp

    subl $12,%esp   //int e,t,a;

    pushl $s0       //printf("Introduce...");
    call printf
    addl $4,%esp

    pushl v0       //scanf("%d%d"....);
    pushl e0
    pushl $s1
    call scanf
    addl $12,%esp

    pushl $s2       //printf("Introduce la...");
    call printf
    addl $4,%esp

    leal -12(%ebp),%eax //scanf("%d",&a)
    pushl %eax
    pushl $s3
    call scanf
    addl $8,%esp

    pushl $s4       //printf("Introduce el tiempo...");
    call printf
    addl $4,%esp

    leal -8(%ebp),%eax  //scanf("%d",&t);
    pushl %eax
    pushl $s5
    call scanf
    addl $8,%esp

    pushl -12(%ebp)  //e = despl(e0,v0,t,a);
    pushl -8(%ebp)
    pushl v0
    pushl e0
    call despl
    addl $16,%esp
    movl %eax,-4(%ebp)

    pushl -4(%ebp)    //printf("El desplazamiento del...");
    pushl $s6
    call printf
    addl $8,%esp

    movl $0,%eax      //return 0;

    movl %ebp,%esp
    popl %ebp
    ret