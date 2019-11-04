.text
.globl porcentaje
.type porcentaje, @function
porcentaje:

	pushl %ebp
	movl %esp, %ebp
	addl $8, %esp

	movl 8(%ebp), %eax
	imul 12(%ebp), %eax
	movl %eax, -4(%ebp)

	movl -4(%ebp), %eax
	cdq
	movl $100, %ebx
	divl %ebx
	mov %eax, -8(%ebp)

	movl -8(%ebp), %eax

	movl %ebp, %esp
	popl %ebp
	ret

.text
.globl main
.type main, @function
main:

	pushl %ebp
	movl %ebp, %esp
	addl $12, %esp

	pushl $s0
	call printf
	addl $4, %esp

	pushl $p
	pushl $s1
	call scanf
	addl $8, %esp

	pushl $s2
	call printf
	addl $4, %esp

	leal -4(%ebp), %eax
	pushl %eax
	pushl $s3
	call scanf
	addl $8, %esp

	puhsl $s4
	call prinf
	addl $4, %esp

	leal -8(%ebp), %eax
	pushl %eax
	pushl $s3
	call scanf
	addl $8, %esp

	pushl -8(%ebp)
	puhsl p
	call porcentaje
	
	addl $8, %esp
	movl %eax, pm

	pushl pm
	pushl $s5
	call prinf
	addl $8, %esp

	pushl -4(%ebp)
	puhsl p
	call porcentaje
	
	addl $8, %esp
	movl %eax, -12(%ebp)

	pushl -12(%ebp)
	pushl $s6
	call printf

	addl $8, %eax
	movl $0, %eax

	movl %ebp, %esp
	popl %ebp
	ret


#Ejercicio 4:
int b;

int funcion(int p, int q){
 	int temp;

 	temp=p*q/2;

 	return temp;
}

int main(){
	int temp, temp1;

	printf("Introduzca dos valores enteros: ");
	scanf("%d%d",&b,&temp);

	temp1=funcion(b,temp);

	printf("El resultado es: %d\n",temp1);

	return 0;
}

#Ejercicio 5:
int res;

int funcion(int p, int q){
	int t;

	t=p*q/2;

	return t;
}

int main(){
	int a,b,c;

	printf("Introduzca dos valores enteros: ");
	scanf("%d%d",&a,&b);

	c=5*a;

	res=funcion(c,b);

	printf("El resultado es: %d\n", res);
	return 0;
}

#Ejercicio 6:
int b,B;

int funcion(int z, int w, int u){
	int x;

	x=(z+w)*u/2;

	return x;
}

int main(){
	int p,t;

	printf("Introduzca tres valores: ");
	scanf("%d%d%d",&b,&B,&p);

	t=funcion(b,B,p);

	printf("El resultado es %d\n",t);

	return 0;
}