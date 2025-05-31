# Proyecto Integrador - Mini IDE Web

**Estudiante:** JOSE FERNANDO DOMINGUEZ BAUTISTA  
**Matrícula:** 22230686  
**Materia:** Lenguajes Autómatas I  
**Profesor:** Kevin David Molina Gomez  
**Fecha de entrega:** 30 de mayo de 2025 


## Estructura del proyecto

![image](https://github.com/user-attachments/assets/2e76b2a5-fe77-4151-ae9e-ef8b7a8b92d8)


##  Instrucciones para ejecutar el proyecto

1. Requisitos previos
   - Python 3.x instalado
   - PIP para gestión de paquetes

2. Instalación
   ```bash
   pip install flask

3. Ejecución
   - python app.py

4. Acceso
   -Abrir en navegador : http://127.0.0.1:5000

 ##  Lenguaje personalizado

|  **Tokens reconocidos**   |    **Tipo**   |          **Descripción**                  |
| ------------------------- | ------------- | ----------------------------------------- |
|    KEYWORD                | Palabra clave | Palabras reservadas del lenguaje          |
|    OPERATOR               | Operador      | Operadores matemáticos y lógicos          |
|    NUMBER                 | Número        | Valores numéricos                         |
|    STRING                 | Cadena        | Texto entre comillas                      |
|    SYMBOL                 | Símbolo       | Símbolos especiales usados en la sintaxis |
|    IDENT                  | Identificador | Nombres de variables o identificadores    |

##  Diccionario de operadores

1. Operadores Aritméticos
   
|  **Operador**  | **Descripción**         | 
| -------------- | ----------------------- | 
|     +          | Suma                    |  
|     -          | Resta                   |  
|     *          | Multiplicación          |  
|     /          | División                |  
|     ()         | Paréntesis (agrupación) |        

3. Operadores Relacionales

|  **Operador**   | **Descripción** | 
| ----------------| --------------- | 
|      ==         | Igualdad        |  
|     !=          | Desigualdad     |  
|     <           | Menor que       |  
|     >           | Mayor que       |  
|     <=          | Menor o igual   |  
|     >=          | Mayor o igual   |  

5. Operadores de Asignación
   
| **Operador** | **Descripción**   | 
| ------------ | ----------------- | 
|  =           | Asignación básica | 

7. Operadores Especiales
   
| **Operador** | **Descripción**     |
| ------------ | ------------------- | 
|  ;           | Fin de declaración  |  
|  {}          | Bloques de código   |  


##  Manejo de errores

**Léxicos**

1. Caracteres no válidos:
Ejemplo: x = ##5;
Error: Carácter no válido: '#'
Corrección: Remover carácter no válido
2. Strings no cerrados:
Ejemplo: materia = "Automatas;
Error: Carácter no válido: ';' (dentro del string no cerrado)
Corrección: Usar comillas: "texto"
3. Identificadores inválidos:
Ejemplo: 123.var = 5;
Error: Carácter no válido: '.' (al final del numero)
Corrección: Los numeros deben ser decimales o remover el punto

**Sintácticos**

1. Falta de punto y coma: 
Ejemplo: v  5;
Error: Falta '=' al final de la expresión
Corrección: v = 5;
2. Condicionales mal formados:
Ejemplo: si x > 5 entonces { ... }
Error: Falta '(' después de 'si'
Corrección: si (x > 5) entonces { ... }
3. Operador lógico mal usado:
Ejemplo: si (x > 5 & y < 10) entonces {
    z = 0;
}
Error: Operador '&' no válido. Use '&&' para AND lógico.
Corrección:si (x > 5 && y < 10) entonces {
    z = 0;
}
4. Asignaciones incorrectas:
Ejemplo: x == 5;
Error: Falta '=' en la asignación
Corrección: x = 5;
5. Expresión aritmética incompleta:
Ejemplo: x = 5 + ;
Error: xpresión incompleta después del operador '+'
Corrección: x = 5 + 3;

**Máquina de Turing**
1. Caracteres no válidos:
Ejemplo: abc
Error: Error: no se reconocio 'c'
Corrección: La cadena debe contener solo 'a' y 'b'
2. No comienza con 'a':
Ejemplo: bab
Error: Error: debe comenzar con 'a'
Corrección: La cadena debe comenzar con 'a'
4. Símbolos repetidos:
Ejemplo: aab
Error: Error: dos 'a' seguidos
Corrección: Debe alternar perfectamente entre 'a' y 'b'
5. No termina con 'b':
Ejemplo: aba
Error: Error: cadena incompleta
Corrección: La cadena debe terminar con 'b'
6. Transición no definida:
Ejemplo: a (cadena incompleta)
Error: Error: 'b' sin procesar
Corrección: La cadena debe tener igual cantidad de 'a' y 'b'


## Ejemplos válidos

**Lexico** 
1. x = 10;
2. resultado = (5 + 3) * 2 - 1;
3. y = (5 + 3) * 2;

   ![image](https://github.com/user-attachments/assets/c150b8d6-296b-4768-83ce-43b6f49e3660)


**Sintactico** 
1. mientras (contador < 5) hacer {
    contador = contador + 1;
    si (!terminado) entonces {
        continuar= avanzar;
        }
}fin
2. si (x != 0)entonces { y = 10 / x; }
3. (a + b) * (c - d);

   ![image](https://github.com/user-attachments/assets/49f4f971-4e85-4dd2-84d7-886c64ab37aa)


**Maquina de Turing** 
1. ababab
2. abab
3. abababab

   ![image](https://github.com/user-attachments/assets/78c772eb-5e26-41c3-94e5-3f7d84228480)


## Ejemplos inválidos

**Lexico** 
1. x = 5%;
2. precio = $100; 
3. z = a ^ b;

   ![image](https://github.com/user-attachments/assets/7c85e80f-02c6-41c1-8fa9-00a834bb418f)
   

**Sintactico** 
1. y = 10  
2. mientras (x < 10 hacer { x++; } 
3. z = a + * b;

   ![image](https://github.com/user-attachments/assets/d74195ce-3717-4ba5-a642-b448360409ea)


**Maquina de Turing** 
1. aabb  
2. aaa
3. ababaa

   ![image](https://github.com/user-attachments/assets/7d77c379-c5c2-4183-8d8e-89042b149564)




