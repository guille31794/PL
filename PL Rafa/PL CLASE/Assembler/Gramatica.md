###  **PL Grammar**

**entrada** &rarr; instruccion entrada | Epsilon
<br/>
**instruccion** &rarr; funcion | asignacion ';' | condicional | inicializacion ';' 

<br/>

**funcion** &rarr; TIPO ID '(' inicializacion ')' '{' contenido '}'
<br/>
**condicional** &rarr; IF '(' operacionLog ')' '{' contenido '}' |  IF '(' operacionLog ')' '{' contenido '}' ELSE '{' contenido '}' | WHILE '(' operacionLog ')' '{' contenido '}'
<br/>
**contenido** &rarr; asignacion ';' contenido | inicializacion ';' contenido | condicional contenido | retorno ';' contenido | Epsilon
<br/>
**retorno** &rarr; RETU devuelve 
<br/>
**devuelve** &rarr;  operacion | Epsilon
<br/>
**asignacion** &rarr; ID ASSIGN operacion

<br/>

**operacion** &rarr; operacionAri | operacionLog
<br/>
**operacionLog** &rarr; exprLog
<br/>
**exprLog** &rarr;  factor AND exprLog | factor EQ exprLog | factor (EQ, LT, LE, GT, GE, NE, AND, OR, NOT) exprLog | factor | Epsilon
<br/>
**operacionAri** &rarr; sum PLUS operacionAri | sum MINUS operacionAri | sum
<br/>
**sum** &rarr; exprAri TIMES exprAri | exprAri DIVIDE exprAri | factor
<br/>
**exprAri** &rarr; '(' exprAri ')' | factor PLUS factor | factor DIVIDE factor | factor TIMES factor | factor MINUS factor | factor
<br/>
**factor** &rarr; MINUS NUMBER | NUMBER | ID


*Creamos otra "inicialización" que se adecúe a las funciones*

**inicializacion_cabecera** &rarr; TIPO ID Resto_cabecera | Epsilon
<br/>
**resto_cabecera** &rarr; ',' TIPO ID Resto_cabecera | Epsilon
<br/>

**inicializacion** &rarr; TIPO ID resto | TIPO asignacion resto 
<br/>
**TIPO** &rarr; INT 
<br/>
**resto** &rarr; ',' ID resto | ',' ID asignacion resto | Epsilon
