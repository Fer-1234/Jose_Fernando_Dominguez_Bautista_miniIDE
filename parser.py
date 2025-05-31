class Parser:
    def __init__(self):
        self.current_token = 0
        self.tokens = []
        self.errors = []
        
    def parse(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.errors = []
        
        try:
            self.program()
            
            if self.errors:
                return {
                    "status": "error",
                    "errors": sorted(self.errors, key=lambda x: x['line'])
                }
            return {
                "status": "success",
                "message": "Análisis sintáctico completado correctamente"
            }
        except Exception as e:
            return {
                "status": "error",
                "errors": sorted(self.errors + [{
                    "message": f"Error crítico: {str(e)}",
                    "line": self.get_current_line(),
                    "correction": "Revise la estructura del programa"
                }], key=lambda x: x['line'])
            }
    
    def program(self):
        while self.current_token < len(self.tokens) and self.peek()[0] != 'EOF':
            self.statement()
    
    def statement(self):
        token = self.peek()
        
        if token[0] == 'KEYWORD':
            if token[1] == 'si':
                self.if_statement()
            elif token[1] == 'mientras':
                self.while_statement()
            elif token[1] == 'fin':
                self.consume()
        elif token[0] == 'IDENT':
            self.assignment()
        elif token[0] in ('NUMBER', 'STRING', '(') or (token[0] == 'SYMBOL' and token[1] == '('):
            self.expression()
            self.match('SYMBOL', ';', "Falta ';' al final de la expresión")
        else:
            self.error(f"Declaración no válida: '{token[1]}'", 
                      "Ejemplos válidos:\nx = 5 + 5;\n5 + 5;\nsi (x > 5) entonces { ... }")
            self.consume()
    
    def if_statement(self):
        self.match('KEYWORD', 'si', "Use 'si (condición) entonces'")
        self.match('SYMBOL', '(', "Falta '(' después de 'si'")
        self.expression()
        self.match('SYMBOL', ')', "Falta ')' después de la condición")
        self.match('KEYWORD', 'entonces', "Falta 'entonces' después del if")
        self.match('SYMBOL', '{', "Falta '{' después de 'entonces'")
        
        while not (self.peek()[0] == 'SYMBOL' and self.peek()[1] == '}'):
            if self.peek()[0] == 'EOF':
                self.error("Bloque 'entonces' no cerrado", "Agregue '}' para cerrar el bloque")
                break
            self.statement()
        
        self.match('SYMBOL', '}', "Falta '}' para cerrar el bloque")
        
        if self.peek()[1] == 'sino':
            self.match('KEYWORD', 'sino', None)
            self.match('SYMBOL', '{', "Falta '{' después de 'sino'")
            
            while not (self.peek()[0] == 'SYMBOL' and self.peek()[1] == '}'):
                if self.peek()[0] == 'EOF':
                    self.error("Bloque 'sino' no cerrado", "Agregue '}' para cerrar el bloque")
                    break
                self.statement()
            
            self.match('SYMBOL', '}', "Falta '}' para cerrar el bloque else")
    
    def while_statement(self):
        self.match('KEYWORD', 'mientras', "Use 'mientras (condición) hacer'")
        self.match('SYMBOL', '(', "Falta '(' después de 'mientras'")
        self.expression()
        self.match('SYMBOL', ')', "Falta ')' después de la condición")
        self.match('KEYWORD', 'hacer', "Falta 'hacer' después del while")
        self.match('SYMBOL', '{', "Falta '{' después de 'hacer'")
        
        while not (self.peek()[0] == 'SYMBOL' and self.peek()[1] == '}'):
            if self.peek()[0] == 'EOF':
                self.error("Bloque 'mientras' no cerrado", "Agregue '}' para cerrar el bloque")
                break
            self.statement()
        
        self.match('SYMBOL', '}', "Falta '}' para cerrar el bloque")
        self.match('KEYWORD', 'fin', "Falta 'fin' para terminar el bucle")
    
    def assignment(self):
        ident = self.peek()
        self.match('IDENT', None, None)
        if not self.match('OPERATOR', '=', "Falta '=' en la asignación"):
            return
        self.expression()
        self.match('SYMBOL', ';', "Falta ';' al final de la asignación")
    
    def expression(self):
        self.logical_expression()
    
    def logical_expression(self):
        self.comparison()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in ['&&', '!']:
            op = self.peek()[1]
            self.consume()
            self.comparison()
    
    def comparison(self):
        self.term()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in ['==', '!=', '<', '>', '<=', '>=']:
            op = self.peek()[1]
            self.consume()
            self.term()
    
    def term(self):
        self.factor()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in '+-*/':
            op = self.peek()[1]
            self.consume()
            self.factor()
    
    def factor(self):
        token = self.peek()
        if token[0] in ('NUMBER', 'STRING', 'IDENT'):
            self.consume()
        elif token[1] == '(':
            self.match('SYMBOL', '(', None)
            self.expression()
            self.match('SYMBOL', ')', "Falta ')' para cerrar la expresión")
        elif token[1] == '!':
            self.match('OPERATOR', '!', None)
            self.factor()
        else:
            self.error(f"Factor no válido: '{token[1]}'", 
                      "Use un número, cadena, variable o expresión entre paréntesis")
            self.consume()
    
    def peek(self):
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return ('EOF', '', self.get_current_line())
    
    def consume(self):
        if self.current_token < len(self.tokens):
            self.current_token += 1
    
    def match(self, expected_type, expected_value=None, correction_msg=None):
        token = self.peek()
        line = self.get_current_line()
        
        if token[0] == expected_type and (expected_value is None or token[1] == expected_value):
            self.consume()
            return True
        
        if expected_value:
            msg = f'Línea {line}: Se esperaba "{expected_value}" pero se encontró "{token[1]}"'
            correction = correction_msg or f'Falta "{expected_value}"'
        else:
            msg = f"Línea {line}: Se esperaba {expected_type} pero se encontró {token[0]} ('{token[1]}')"
            correction = correction_msg or f"Se esperaba un {expected_type}"
        
        self.error(msg, correction)
        return False
    
    def error(self, message, correction=None):
        line = self.get_current_line()
        self.errors.append({
            "message": message,
            "line": line,
            "correction": correction
        })
    
    def get_current_line(self):
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token][2] if len(self.tokens[self.current_token]) > 2 else 1
        if self.tokens and len(self.tokens[-1]) > 2:
            return self.tokens[-1][2]
        return 1