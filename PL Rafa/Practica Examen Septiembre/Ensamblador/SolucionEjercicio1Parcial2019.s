.text
.globl Desplazamiento
.type Desplazamiento, @function

Desplazamiento:               # PRÓLOGO
    pushl %ebp                # salvar enlace dinámico
    movl  %esp, %ebp          # establecer nuevo enlace dinámico
    subl  $4, %esp            # reservar espacio para variables locales (int e;)

    movl  16(%ebp), %eax      # mueve t al registro eax
    imull 16(%ebp), %eax      # t * t --> eax
    imull 20(%ebp), %eax      # a * t * t --> eax
    movl  $2, %ebx
    cdq
    idivl %ebx
    pushl %eax                # almacena resultado intermedio en la pila (1/2 * a * t * t)

    movl  12(%ebp), %eax      # mueve v0 al registro eax
    imull 16(%ebp), %eax      # v0 * t --> eax
    popl  %ebx                # (1/2 * a * t * t) --> ebx
    addl  %ebx, %eax          # (v0 * t) + (1/2 * a * t * t) --> eax
    addl  8(%ebp), %eax       # e0 + (v0 * t) + (1/2 * a * t * t) --> eax
    movl  %eax, -4(%ebp)
    movl  -4(%ebp), %eax      # return e
                              # EPÍLOGO
    movl  %ebp, %esp          # borra variables locales y temporales
    popl  %ebp                # restaura el marco de activación
    ret                       # devuelve el control

.text
.globl main
.type main, @function

main:                         #PRÓLOGO
    pushl %ebp                # salvar enlace dinámico
    movl  %esp, %ebp          # establecer nuevo enlace dinámico
    subl  $12, %esp           # reservar espacio para variables locales (int e, t, a;)

    pushl $S0                 # S0 = "Introduce la posicióm y la velocidad iniciales:"
    call  printf
    addl  $4, %esp            # Quita parámetros

    pushl v0
    pushl e0
    pushl $S1                 # S1 = "%d%d"
    call  scanf
    addl  $12, %esp           # Quita parámetros

    pushl $S2                 # S2 = "Introduce la aceleración"
    call  printf
    addl  $4, %esp            # Quita parámetros

    leal  -12(%ebp), %eax
    pushl %eax
    pushl $S3                 # S3 = "%d"
    call  scanf
    addl  $8, %esp            # Quita parámetros

    pushl $S4                 # S4 = "Introduce el tiempo transcurrido"
    call  printf
    addl  $4, %esp            #Quita parámetros

    leal  -8(%ebp), %eax
    pushl %eax
    pushl $S3
    call  scanf
    addl  $8, %esp

    pushl -12(%ebp)
    pushl -8(%ebp)
    pushl v0
    pushl e0
    call  Desplazamiento
    addl  $16, %esp
    movl  %eax, -4(%ebp)
    pushl -4(%ebp)
    pushl $S4                 # S4 = "El desplazamiento del móvil es de %d\n"
    call  printf
    addl  $8, %esp

    movl $0, %esp             # return 0;
                              # EPÍLOGO
    movl  %ebp, %esp          # borra variables locales y temporales
    popl  %ebp                # restaura el marco de activación
    ret                       # devuelve el control