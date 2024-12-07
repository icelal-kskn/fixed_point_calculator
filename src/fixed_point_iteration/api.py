from .core import FixedPointIteration
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/fixed-point-iteration', methods=['POST'])
def fixed_point_iteration():
    """
    API endpoint for Fixed-Point Iteration
    
    Expects JSON with:
    - function: Original function as a string
    - x0: Initial guess
    - tolerance: Convergence tolerance
    - max_iterations: Maximum iteration count
    """
    try:
        data = request.json
        
        # Validate input
        if not FixedPointIteration.validate_input(data):
            return jsonify({
                'error': 'Invalid input schema',
                'status': 400
            }), 400
        
        def f(x):
            return eval(data['function']) # pylint: disable=eval-used # Must be checked in frontend 
        
        solver = FixedPointIteration(
            f=f, 
            x0=data['x0'], 
            tol=data['tolerance'], 
            max_iter=data['max_iterations']
        )
        
        result = solver.solve()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 500
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)