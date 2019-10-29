	.file	"media.c"
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
	.seh_endprologue
	movl	%ecx, 16(%rbp)
	movl	%edx, 24(%rbp)




	nop
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 8.1.0"
