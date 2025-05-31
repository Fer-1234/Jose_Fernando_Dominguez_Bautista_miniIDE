class TuringMachine:
    def __init__(self):
        self.transitions = {
            ('q0', 'a'): ('q1', 'X', 'R'),
            ('q0', 'b'): ('qr', 'b', 'R', "Error: debe comenzar con 'a'"),
            ('q0', 'X'): ('q3', 'X', 'R'),
            ('q0', '_'): ('qa', '_', 'R'),
            
            ('q1', 'a'): ('qr', 'a', 'R', "Error: dos 'a' seguidos"),
            ('q1', 'b'): ('q2', 'X', 'R'),
            ('q1', 'X'): ('qr', 'X', 'R', "Error: falta 'b'"),
            ('q1', '_'): ('qr', '_', 'R', "Error: cadena incompleta"),
            
            ('q2', 'a'): ('q1', 'X', 'R'),
            ('q2', 'b'): ('qr', 'b', 'R', "Error: dos 'b' seguidos"),
            ('q2', 'X'): ('q0', 'X', 'R'),
            ('q2', '_'): ('qa', '_', 'R'),
            
            ('q3', 'X'): ('q3', 'X', 'R'),
            ('q3', '_'): ('qa', '_', 'R'),
            ('q3', 'a'): ('qr', 'a', 'R', "Error: 'a' sin procesar"),
            ('q3', 'b'): ('qr', 'b', 'R', "Error: 'b' sin procesar")
        }
        self.accept_state = 'qa'
        self.reject_state = 'qr'
    
    def run(self, input_str):
        tape = list(input_str + '_')
        head = 0
        state = 'q0'
        path = []
        rejection_reason = None
        
        while state != self.accept_state and state != self.reject_state:
            current_symbol = tape[head] if head < len(tape) else '_'
            
            path.append({
                'state': state,
                'head': head,
                'tape': ''.join(tape).replace('_', ' ').strip(),
                'symbol': current_symbol
            })
            
            key = (state, current_symbol)
            if key in self.transitions:
                transition = self.transitions[key]
                new_state = transition[0]
                write = transition[1]
                move = transition[2]
                
                if len(transition) > 3 and new_state == self.reject_state:
                    rejection_reason = transition[3]
                
                if head < len(tape):
                    tape[head] = write
                else:
                    tape.append(write)
                
                if move == 'R':
                    head += 1
                elif move == 'L':
                    head = max(0, head - 1)
                
                state = new_state
            else:
                state = self.reject_state
                rejection_reason = f"Transición no definida para estado '{state}' y símbolo '{current_symbol}'"
        
        path.append({
            'state': state,
            'head': head,
            'tape': ''.join(tape).replace('_', ' ').strip(),
            'symbol': tape[head] if head < len(tape) else '_'
        })
        
        accepted = state == self.accept_state
        
        if accepted:
            for i in range(len(input_str)-1):
                if input_str[i] == input_str[i+1]:
                    accepted = False
                    rejection_reason = f"Los símbolos {i+1} y {i+2} son iguales ({input_str[i]})"
                    break
            
            if accepted and input_str and input_str[-1] != 'b':
                accepted = False
                rejection_reason = "La cadena debe terminar con 'b'"
        
        return {
            'accepted': accepted,
            'path': path,
            'final_tape': ''.join(tape).replace('_', ''),
            'message': "VÁLIDO" if accepted else "NO VÁLIDO",
            'reason': rejection_reason
        }