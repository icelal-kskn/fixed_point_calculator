function solveFixedPoint() {
    const functionInput = document.getElementById('function').value;
    const x0Input = parseFloat(document.getElementById('x0').value);
    const toleranceInput = parseFloat(document.getElementById('tolerance').value);
    const maxIterationsInput = parseInt(document.getElementById('maxIterations').value);

    console.log('Function:', functionInput);
    console.log('x0:', x0Input);
    console.log('Tolerance:', toleranceInput);
    console.log('Max Iterations:', maxIterationsInput);
    
    const payload = {
        function: functionInput,
        x0: x0Input,
        tolerance: toleranceInput,
        max_iterations: maxIterationsInput
    };

    fetch('http://localhost:5000/fixed-point-iteration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            if (data.success) {
                resultDiv.innerHTML = `
                    <strong>Convergence achieved!</strong><br>
                    x = ${data.x}<br>
                    f(x) = ${data["f(x)"]}<br>
                    Iterations: ${data.n}<br>
                    Error: ${data.error}
                `;
            } else {
                resultDiv.innerHTML = `
                    <strong>Error:</strong> ${data.message}<br>
                    Iterations: ${data.iteration || 0}
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').textContent = 'Failed to fetch results. Check the API server.';
        });
}
