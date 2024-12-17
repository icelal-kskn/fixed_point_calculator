from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from fixed_point_iteration import FixedPointIteration

app = Flask(__name__)
CORS(app)

@app.route('/fixed-point-iteration', methods=['POST'])
def fixed_point_iteration():
    try:
        # Get JSON input
        input_data = request.json
        
        # Validate input
        if not FixedPointIteration.validate_input(input_data):
            return jsonify({
                "error": "Invalid input",
                "message": "Input does not match required schema"
            }), 400
        
        # Create FixedPointIteration instance
        fpi = FixedPointIteration(
            f=input_data["function"],
            x0=input_data["x0"],
            tol=input_data["tolerance"],
            max_iter=input_data["max_iterations"]
        )
        
        # Solve and return results
        result = fpi.solve()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": "Computation failed",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)