	.file	"main.c"
	.text
	.comm	a, 4, 2
	.comm	b, 4, 2
	.comm	c, 4, 2
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "%d / %d = %d\12\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
           

main:

	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	leaq	a(%rip), %rax
	movl	$25, (%rax)
	leaq	b(%rip), %rax
	movl	$3, (%rax)
	leaq	a(%rip), %rax
	movl	(%rax), %edx
	leaq	b(%rip), %rax
	movl	(%rax), %eax
	idivl	%eax, %edx
	leaq	c(%rip), %rax
	movl	%edx, (%rax)
	leaq	c(%rip), %rax
	movl	(%rax), %ecx
	leaq	b(%rip), %rax
	movl	(%rax), %edx
	leaq	a(%rip), %rax
	movl	(%rax), %eax
	movl	%ecx, %r9d
	movl	%edx, %r8d
	movl	%eax, %edx
	leaq	.LC0(%rip), %rcx
	call	printf
	movl	$0, %eax
	addq	$32, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 8.1.0"
	.def	printf;	.scl	2;	.type	32;	.endef
