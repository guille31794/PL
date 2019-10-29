/*

    int h2;

    int pitagoras(int c1,int c2)
    {
        int temp,temp1,temp2;
        temp1 = c1 * c1;
        temp2 = c2 * c2;
        temp = temp1 + temp2;

        return temp;
    }

    int main()
    {
        int a,b;

        printf("teclea dos numeros: ");
        scanf("%d%d",&a,&b);
        h2 = pitagoras(a,b);
        printf("La hipotenusa es %d \n",hs);

        return 0;
    }

*/


.text
.globl pitagoras
.type pitagoras, @function
pitagoras:

    pushl %ebp      //Guardamos el estado anterior del programa
    movl %esp,%ebp  //Puntero actual de la funcion
    subl $12,%esp   //int temp,temp1,temp2;

    movl 8(%ebp),%eax   //temp1 = c1*c1;   
    imull 8(%ebx),%eax
    movl %eax,-8(%ebp)

    movl 12(%ebp),%eax  //temp2 = c2*c2;
    imull 12(%ebp),%eax
    movl %eax,-12(%ebp)

    movl -8(%ebp),%eax  //temp = temp1 + temp2;
    addl -12(%ebp),%eax
    movl %eax,-4(%ebp)

    movl -4(%ebp),%eax  //return temp

    movl %ebp,%esp
    popl %ebp
    ret


.text
.globl main
.type main,@function
main:

    pushl %ebp      //Guardamos enlace dinamico
    movl %esp,%ebp  

    subl $8,%esp    //int a,b;

    pushl $s0       //printf("teclea dos numeros: ");
    call printf
    addl $4,%esp

    leal -8(%ebp),%eax  //scanf("%d%d",&a,&b);
    pushl %eax
    leal -4(%ebp),%eax
    pushl %eax
    pushl $s1
    call scanf
    addl $12,%esp

    pushl -8(%ebp)  //h2 = pitagoras(a,b);
    pushl -4(%ebp)
    call pitagoras
    addl $8,%esp
    movl %eax,h2

    pushl h2       //printf("La hipotenusa...");
    pushl $s2
    call printf
    addl $8,%esp

    movl $0,%eax    //return 0;

    movl %ebp,%esp
    popl %ebp
    ret





