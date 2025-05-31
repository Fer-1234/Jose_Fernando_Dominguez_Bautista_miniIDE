import re

class Lexer:
    def __init__(self):
        self.keywords = ['si', 'entonces', 'sino', 'mientras', 'hacer', 'fin']
        self.operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '!']
        self.symbols = ['(', ')', '{', '}', ';']
        
    def tokenize(self, code):
        tokens = []
        errors = []
        line_number = 1
        line_start = 0
        
        token_specs = [
            ('NUMBER', r'\d+(\.\d+)?'),
            ('OPERATOR', r'(\+|-|\*|/|==?|!=|<=?|>=?|&&|\!)'),
            ('STRING', r'"[^"]*"'),
            ('KEYWORD', r'\b(si|entonces|sino|mientras|hacer|fin)\b'),
            ('SYMBOL', r'[(){};]'),
            ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.')
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'NEWLINE':
                line_number += 1
                line_start = mo.end()
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                errors.append({
                    'message': f"Carácter no válido: '{value}'",
                    'line': line_number,
                    'correction': "Remover carácter no válido"
                })
                continue
            
            if kind == 'IDENT' and value in self.keywords:
                kind = 'KEYWORD'
            
            tokens.append((kind, value, line_number))
        
        return tokens, errors
    
    def suggest_correction(self, char, line, code):
        if char == '"':
            return 'Usar comillas: "texto"'
        return "Revisar sintaxis"