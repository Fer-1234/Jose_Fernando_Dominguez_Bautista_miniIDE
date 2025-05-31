from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser
from turing_machine import TuringMachine

app = Flask(__name__)

STUDENT_INFO = {
    "Nombre": "JOSE FERNANDO DOMINGUEZ BAUTISTA",
    "Matricula": "22230686",
    "Materia": "Lenguaje Autómatas I",
    "Profesor": "Kevin David Molina Gomez"
}

@app.route('/')
def index():
    return render_template('index.html', student_info=STUDENT_INFO)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    code = data['code']
    action = data['action']
    
    try:
        if action == "lexical":
            lexer = Lexer()
            tokens, errors = lexer.tokenize(code)
            return jsonify({"tokens": tokens, "errors": errors})
        
        elif action == "syntax":
            lexer = Lexer()
            parser = Parser()
            tokens, lex_errors = lexer.tokenize(code)
            
            if lex_errors:
                return jsonify({"status": "error", "errors": lex_errors})
            
            parse_result = parser.parse(tokens)
            return jsonify(parse_result)
        
        elif action == "turing":
            tm = TuringMachine()
            result = tm.run(code)
            return jsonify(result)
        
        return jsonify({"error": "Acción no válida"}), 400
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "errors": [{
                "message": f"Error interno: {str(e)}",
                "line": 1,
                "correction": "Revise la sintaxis del código"
            }]
        }), 500

if __name__ == '__main__':
    app.run(debug=True)