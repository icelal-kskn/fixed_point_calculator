let currentChart = null;

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
            console.log('Success:', data);
            const resultDiv = document.getElementById('result');
            if (data) {
                resultDiv.innerHTML = `
                    <strong>Convergence achieved!</strong><br>
                    x = ${data.x}<br>
                    f(x) = ${data["f(x)"]}<br>
                    Iterations: ${data.n}<br>
                    Error: ${data.error}
                `;
                // Render chart if iterations data is available
                if (data.iterations) {
                    const xValues = data.iterations.map(iter => iter.x_n);
                    renderChart(xValues);
                }
            } else {
                resultDiv.innerHTML = `
                    <strong>Error:</strong> ${data.message}<br>
                    Iterations: ${data.iteration || 0}
                `;
                // Clear the chart if there's an error
                if (currentChart) {
                    currentChart.destroy();
                    currentChart = null;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').textContent = 'Failed to fetch results. Check the API server.';
            // Clear the chart on error
            if (currentChart) {
                currentChart.destroy();
                currentChart = null;
            }
        });
}

function renderChart(dataPoints) {
    const ctx = document.getElementById('resultChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (currentChart) {
        currentChart.destroy();
    }

    // Create new chart
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataPoints.map((_, i) => `Iteration ${i}`),
            datasets: [{
                label: 'x Values Over Iterations',
                data: dataPoints,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    display: true,
                    text: 'Fixed Point Iteration Convergence'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'x value'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Iteration'
                    }
                }
            }
        }
    });
}