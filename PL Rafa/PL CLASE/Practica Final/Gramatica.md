###  **PL Grammar**

**entrada** &rarr; instruccion entrada | Epsilon
<br/>
**instruccion** &rarr; funcion | asignacion ';' | condicional | inicializacion ';' 

<br/>

**funcion** &rarr; TIPO ID '(' inicializacion_cabecera ')' '{' contenido '}'
<br/>
**condicional** &rarr; IF '(' operacionLog ')' '{' contenido '}' ELSE '{' contenido '}' | WHILE '(' operacionLog ')' '{' contenido '}'
<br/>
**contenido** &rarr; asignacion ';' contenido | inicializacion ';' contenido | condicional contenido | retorno ';' contenido | leer ';' contenido | imprimir ';' contenido | Epsilon
<br/>
**leer** &rarr; SCANF '(' STRING ',' '&' ID leer_opc ')'
<br/>
**leer_opc** &rarr; ',' '&' ID leer_opc | Epsilon 
<br/>
**imprimir** &rarr; PRINTF '(' STRING imprimir_opc ')'
<br/>
**imprimir_opc** &rarr; ',' '&' ID imprimir_opc | ',' ID imprimir_opc | Epsilon
<br/>
**retorno** &rarr; RETURN devuelve 
<br/>
**devuelve** &rarr;  operacion | Epsilon
<br/>
**asignacion** &rarr; ID ASSIGN operacion

<br/>

**operacion** &rarr; operacionAri | operacionLog
<br/>
**operacionLog** &rarr; exprLog
<br/>
**exprLog** &rarr;  factor AND exprLog | factor EQ exprLog | factor (EQ, LT, LE, GT, GE, NE, AND, OR, NOT) exprLog | factor
<br/>
**operacionAri** &rarr; sum PLUS operacionAri | sum MINUS operacionAri | sum
<br/>
**sum** &rarr; exprAri | exprAri TIMES exprAri | exprAri DIVIDE exprAri
<br/>
**exprAri** &rarr; '(' operacionAri ')' | factor
<br/>
**factor** &rarr; MINUS NUMBER | NUMBER | ID


*Creamos otra "inicialización" que se adecúe a las funciones*

**inicializacion_cabecera** &rarr; TIPO ID Resto_cabecera | Epsilon
<br/>
**resto_cabecera** &rarr; ',' TIPO ID Resto_cabecera | Epsilon
<br/>

**inicializacion** &rarr; TIPO ID resto | TIPO ID asignacion_ini resto 
<br/>
**asignacion_ini** &rarr; ASSIGN operacion
<br/>
**TIPO** &rarr; INT 
<br/>
**resto** &rarr; ',' ID resto | ',' ID asignacion resto | Epsilon
