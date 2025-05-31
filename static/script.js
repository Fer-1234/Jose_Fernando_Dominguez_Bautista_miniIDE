document.addEventListener('DOMContentLoaded', function () {
    const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: 'text/x-csrc',
        theme: 'neon',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true,
        matchBrackets: true,
        extraKeys: {
            "Ctrl-Space": "autocomplete",
            "Ctrl-Enter": runLexicalAnalysis,
            "Shift-Enter": runSyntaxAnalysis
        }
    });

    let errorMarkers = [];

    document.getElementById('lexical-btn').addEventListener('click', runLexicalAnalysis);
    document.getElementById('syntax-btn').addEventListener('click', runSyntaxAnalysis);
    document.getElementById('run-turing-btn').addEventListener('click', runTuringValidation);
    document.getElementById('clear-btn').addEventListener('click', clearAll);

    function runLexicalAnalysis() {
        clearErrorMarkers();
        const code = editor.getValue();

        document.getElementById('tokens-container').style.display = 'block';
        document.getElementById('error-container').style.display = 'none';

        fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, action: "lexical" })
        })
            .then(handleResponse)
            .then(data => {
                updateTokensTable(data.tokens);
                if (data.errors && data.errors.length > 0) {
                    document.getElementById('error-container').style.display = 'block';
                    showErrors(data.errors);
                }
            })
            .catch(handleError);
    }

    function runSyntaxAnalysis() {
        clearErrorMarkers();
        const code = editor.getValue();

        document.getElementById('tokens-container').style.display = 'none';
        document.getElementById('error-container').style.display = 'block';

        fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, action: "syntax" })
        })
            .then(handleResponse)
            .then(data => {
                if (data.status === 'error') {
                    showErrors(data.errors);
                } else {
                    showSuccessMessage();
                }
            })
            .catch(handleError);
    }

    function runTuringValidation() {
        const input = document.getElementById('turing-input').value.trim();

        if (!/^[ab]+$/.test(input)) {
            showTuringError("Por favor ingresa solo 'a' y 'b'");
            return;
        }

        fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: input, action: "turing" })
        })
            .then(handleResponse)
            .then(data => {
                updateTuringResult(data);
            })
            .catch(handleError);
    }

    function clearAll() {
        editor.setValue('');
        clearErrorMarkers();
        resetTuringPanel();

        document.getElementById('tokens-container').style.display = 'none';
        document.getElementById('error-container').style.display = 'none';

        document.querySelector('#tokens-table tbody').innerHTML = '';
        document.getElementById('errors-content').innerHTML = '';
    }

    function clearErrorMarkers() {
        errorMarkers.forEach(marker => marker.clear());
        errorMarkers = [];
    }

    function resetTuringPanel() {
        document.getElementById('turing-input').value = 'abab';
        document.querySelector('.result-icon').textContent = '❌';
        document.querySelector('.result-text').textContent = 'NO VÁLIDO';
        document.getElementById('path-content').innerHTML = '<p class="path-msg">Ingresa una secuencia y haz clic en Validar</p>';
    }

    function updateTokensTable(tokens) {
        const tbody = document.querySelector('#tokens-table tbody');
        tbody.innerHTML = '';

        if (tokens.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="empty-msg">No se encontraron tokens</td></tr>';
            return;
        }

        tokens.forEach(token => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${token[0]}</td>
                <td>${escapeHtml(token[1])}</td>
                <td>${token[2]}</td>
            `;
            tbody.appendChild(row);
        });
    }

    function showErrors(errors) {
        const errorContent = document.getElementById('errors-content');
        errorContent.innerHTML = '';

        if (errors.length === 0) {
            errorContent.innerHTML = `
                <div class="error-message success">
                    ✅ No se encontraron errores léxicos
                </div>
            `;
            return;
        }

        errors.forEach(error => {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.innerHTML = `
                <strong>Línea ${error.line}:</strong> ${error.message}
                ${error.correction ? `<div class="correction">Solución: ${error.correction}</div>` : ''}
            `;
            errorContent.appendChild(errorDiv);

            if (error.line && error.line > 0) {
                const marker = editor.markText(
                    { line: error.line - 1, ch: 0 },
                    { line: error.line - 1 },
                    {
                        className: 'error-line',
                        attributes: { title: error.message }
                    }
                );
                errorMarkers.push(marker);
            }
        });
    }

    function showSuccessMessage() {
        const errorContent = document.getElementById('errors-content');
        errorContent.innerHTML = `
            <div class="error-message success">
                ✅ Análisis sintáctico completado sin errores
            </div>
        `;
    }

    function updateTuringResult(data) {
        const resultBox = document.getElementById('turing-result');
        const resultIcon = resultBox.querySelector('.result-icon');
        const resultText = resultBox.querySelector('.result-text');
        const pathContent = document.getElementById('path-content');

        resultIcon.textContent = data.accepted ? '✓' : '❌';
        resultText.textContent = data.message;

        resultBox.className = data.accepted ? 'result-box accepted' : 'result-box rejected';

        pathContent.innerHTML = '';
        if (data.path.length === 0) {
            pathContent.innerHTML = '<p class="path-msg">No se ejecutaron pasos</p>';
        } else {
            data.path.forEach((step, index) => {
                const stepDiv = document.createElement('div');
                stepDiv.className = 'path-step';
                stepDiv.innerHTML = `
                    <strong>Paso ${index + 1}:</strong> 
                    <span class="state">Estado ${step.state}</span> | 
                    <span class="symbol">Símbolo '${step.symbol}'</span> | 
                    <span class="tape">Cinta: ${step.tape}</span> | 
                    <span class="head">Cabezal: posición ${step.head}</span>
                `;
                pathContent.appendChild(stepDiv);
            });
        }

        if (!data.accepted && data.reason) {
            const reasonDiv = document.createElement('div');
            reasonDiv.className = 'path-step rejection-reason';
            reasonDiv.innerHTML = `<strong>Razón:</strong> ${data.reason}`;
            pathContent.appendChild(reasonDiv);
        }
    }

    function showTuringError(message) {
        const resultBox = document.getElementById('turing-result');
        const resultIcon = resultBox.querySelector('.result-icon');
        const resultText = resultBox.querySelector('.result-text');

        resultIcon.textContent = '⚠️';
        resultText.textContent = message;
        resultBox.className = 'result-box rejected';
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
            .toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function handleResponse(response) {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    }

    function handleError(error) {
        console.error('Error:', error);
        showTuringError("Error al conectar con el servidor");
    }

    let analysisTimeout;
    editor.on('change', function () {
        clearTimeout(analysisTimeout);
        analysisTimeout = setTimeout(function () {
            const code = editor.getValue();
            if (code.trim() === '') {
                clearErrorMarkers();
                return;
            }

            fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code, action: "lexical" })
            })
                .then(handleResponse)
                .then(data => {
                    clearErrorMarkers();
                    showErrors(data.errors);
                })
                .catch(console.error);
        }, 1000);
    });

    clearAll();
});