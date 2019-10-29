	.def	__main;	.scl	2;	.type	32;	.endef
	.text
	.seh_proc	main
main:
	.seh_pushreg	%rbp
	.seh_setframe	%rbp, 0
	.seh_endprologue
	call	__main
	movl	$0, %eax
	addq	$32, %rsp
	popq	%rbp

	.ident	"GCC: (GNU) 6.4.0"
