	.file	"assembler.c"
	.text
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "25 * a + 3 / b = %d\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	movl	$5, -4(%rbp)  # asignamos 5 a "a"
	movl	$3, -8(%rbp) # asignamos 10 a "b"

	# OPERACION: 25 * a + 3 / b;

	# MULTIPLICACION (25*a)
	movl	-4(%rbp), %eax 
	imull	$25, %eax
	movl 	%eax,%ebx			# Guardamos el resultado de la multiplicación
	
	# DIVISION (3/b)
	movl $3,%eax
	cdq						# extendemos el bit de signo
	movl -8(%rbp),%edx
	divl %edx
	# pushl %eax				# Guardamos el resultado de la division

	# SUMA ((25*a) + (3/b))
	# popl %eax				# Sacamos el resultado de la división
	# popl %eax				# Sacamos el resultado de la multiplicación
	addl %ebx,%eax			# Sumamos
	
	# ASIGNAMOS EL RESULTADO A "c" Y LO IMPRIMIMOS
	movl	%eax,-12(%rbp)  
	movl	%eax, %edx
	leaq	.LC0(%rip), %rcx
	call	printf
	movl	$0, %eax # limpia las variables locales y temporales
	addq	$48, %rsp 
	popq	%rbp # restaura el marco de activación anterior
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 8.1.0"
	.def	printf;	.scl	2;	.type	32;	.endef
