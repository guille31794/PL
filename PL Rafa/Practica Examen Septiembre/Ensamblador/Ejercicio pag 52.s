.text
.globl media
.type media, @function

media:
    pushl %ebp
    movl %esp,%ebp     //Guardar valor anterior de %ebp


    subl $4,%esp       //Reservar 1 variable local
                       //int temp;

    movl 8(%ebp),%eax  //Metemos "n" en la pila
    addl 12(%ebp),%eax //n+m

    movl %eax,-4(%ebp) //temp = n+m;

    movl -4(%ebp),%eax //temp = temp/2;
    cdq
    movl $2,%ebx
    divl %ebx
    movl %eax,-4(%ebp) 

    movl -4(%ebp),%eax //return temp;

    movl %ebp,%esp     //Borrar var locales y temporales de la pila
    popl %ebp          //Restaura macro activacion anterior 
    ret                //Devuelve el control al main 


.text
.globl main
.type main, @function
main:
    pushl %ebp
    movl %esp,%ebp

    subl $8,%esp    //Reservamos espacio var locales ("b" y "resultado")

    movl $35,p      //p = 35;
    movl $12,q      //q = 12;

    pushl q         //printf("p=.....)
    pushl p
    pushl $s0
    call printf
    addl $12,%esp   //quitamos parametros

    pushl $s1       //print("teclea dos...")
    call printf
    addl $4,%esp

    pushl $a         //scanf("%d%d",&a,&b);
    leal -4(%ebp),%eax
    pushl %eax
    pushl $s2
    call scanf
    addl $12,%esp

    pushl a         //resultado = media(a,b);
    pushl -4(%ebp)  
    call media
    addl $8,%esp
    movl %eax,-8(%ebp)

    pushl $s3       //printf("La media...")
    pushl a
    pushl -4(%ebp)
    pushl -8(%ebp)
    call printf
    addl $16,%esp

    movl $0,%eax
    popl %ebp
    movl %ebp,%esp
    ret



