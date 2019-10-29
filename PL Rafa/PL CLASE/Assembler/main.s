	.file	"main.c"
	.text
	.comm	a, 4, 2
	.comm	p, 4, 2
	.comm	q, 4, 2
	.globl	media
	.def	media;	.scl	2;	.type	32;	.endef
	.seh_proc	media
media:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$16, %rsp
	.seh_stackalloc	16
	.seh_endprologue
	movl	%ecx, 16(%rbp)
	movl	%edx, 24(%rbp)
	# movl	$0, -4(%rbp)

	# Suma: temp = n+m;
	movl    8(%rbp),%eax
	addl    12(%rbp),%eax
	movl	%eax,-4(%rbp)

	# Division: temp = temp/2
	movl 	-4(%rbp),%eax
	cdq
	movl 	$2,%ebx
	divl	%ebx
	movl	%eax,-4(%rbp)
	movl	-4(%rbp), %eax

	addq	$16, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "Resultado: %d\12\0"
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
	movl	$10, -12(%rbp)
	movl	$50, -16(%rbp)

	movl 	-12(%rbp),%eax
	movl 	%eax,-4(%rbp)	 # b = n
	movl 	-16(%rbp),%eax
	movl 	%eax,a 		 # a = m

	# Asignar media(a,b) a resultado
	pushq 	-4(%rbp)
	pushq 	a
	call 	media
	addq	$8,%rsp
	movl	%eax,-8(%rbp)

	# printf
	movl	-8(%rbp), %eax
	movl	%eax, %edx
	leaq	.LC0(%rip), %rcx
	call	printf
	movl	$0, %eax
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 8.1.0"
	.def	printf;	.scl	2;	.type	32;	.endef
