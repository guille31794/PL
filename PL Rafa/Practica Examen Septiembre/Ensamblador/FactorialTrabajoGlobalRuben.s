# ==============================================================================
# MARCOS DE ACTIVACIÓN
# ==============================================================================
# -> Función Fact:
#    param n = EBP + 8
#    eIP     = EBP + 4
#    eBP     = EBP
#    
# -> Función main:
#    eIP     = EBP + 4
#    eBP     = EBP
# ==============================================================================
.section
.rodata
.LC0:
    .string "Enter a number: "

.LC1:
    .string "%d"

.LC2:
    .string "Factorial = %d\n"

.text
.globl main
.type main, @function
main:
    # PRÓLOGO
    pushl %ebp
    movl %esp, %ebp
    
    # CUERPO
    movl $.LC0, %eax        # printf(LC0)
    pushl %eax
    call printf
    addl $4, %esp

    pushl $numb             # scanf(LC1)
    movl $.LC1, %eax
    pushl %eax
    call scanf 
    addl $8, %esp

    pushl $numb             # fact(numb)
    call fact
    addl $4, %esp

    pushl %eax              # printf(LC2)
    movl $.LC1, %eax
    pushl %eax
    call printf
    addl $8, %esp
    
    movl $0, %eax

    # EPÍLOGO
    movl %ebp, %esp
    popl %ebp
    ret

.text
.globl fact
.type fact, @function
fact:
    # PRÓLOGO
    pushl %ebp
    movl %esp, %ebp
    
    # CUERPO
    movl $8(%ebp), %ebx     
    cmpl $1, %ebx           # if(n <= 1)
    jle cuerpo_if

    subl $1, %ebx           # CUERPO DEL ELSE
    pushl %ebx              # (n - 1)
    call fact               
    addl $4, %esp               
    imull %ebx, %eax        # n * fact(n - 1)
    jmp fin_fact            

cuerpo_if:
    movl $1, %eax           # CUERPO DEL IF

fin_fact:
    # EPÍLOGO
    popl %ebp
    movl %ebp, %esp
    ret