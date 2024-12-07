import numpy as np
import jsonschema
from typing import Callable, Dict, Any

class FixedPointIteration:
    """
    Fixed-Point Iteration class for root finding
    """
    def __init__(self, 
                 f: Callable[[float], float],
                 x0: float,
                 tol: float = 1e-6,
                 max_iter: int = 100):
        """
        Initialize Fixed-Point Iteration solver
        
        :param f: Original function f(x)
        :param x0: Initial guess
        :param tol: Tolerance for convergence
        :param max_iter: Maximum number of iterations
        """
        self.__f = f
        self.__g = self.__transform_to_g(f)
        self.__x0 = x0
        self.__tol = tol
        self.__max_iter = max_iter

    def __transform_to_g(self,f: Callable[[float], float]) -> Callable[[float], float]:
        """
        Transform f(x) to g(x) for Fixed-Point Iteration
        
        :param f: Original function f(x)
        :return: Transformed function g(x)
        """
        def g(x:float)->float:
            return x - f(x)
        
        return g
        
    def solve(self) -> Dict[str, Any]:
        """
        Perform Fixed-Point Iteration
        
        :return: Dictionary with iteration results
        """
        x_prev = self.__x0
        iterations = [{'n': 0, 'x': x_prev, 'f_x': self.__f(x_prev)}]
        
        for n in range(1, self.__max_iter + 1):
            try:
                x_curr = self.__g(x_prev)
                
                # Store iteration details
                iterations.append({
                    'n': n, 
                    'x': x_curr, 
                    'f_x': self.__f(x_curr),
                })
                
                # Convergence checks
                if abs(self.__f(x_curr)) < self.__tol:
                    return {
                        'success': True,
                        'root': x_curr,
                        'iterations': iterations,
                        'message': 'Converged by f(x) tolerance'
                    }
                
                if abs(x_curr - x_prev) < self.__tol:
                    return {
                        'success': True,
                        'root': x_curr,
                        'iterations': iterations,
                        'message': 'Converged by x difference tolerance'
                    }
                
                x_prev = x_curr
            except Exception as e:
                    return {
                        'success': False,
                        'root': None,
                        'iterations': iterations,
                        'message': f'Computation error: {str(e)}'
                    }
        
        # If maximum iterations reached
        return {
            'success': False,
            'root': x_curr,
            'iterations': iterations,
            'message': 'Maximum iterations reached'
        }
    
    @staticmethod
    def validate_input(input_json: Dict[str, Any]) -> bool:
        """
        Validate input JSON schema
        
        :param input_json: Input configuration
        :return: Boolean indicating valid input
        """
        
        schema = {
            "type": "object",
            "properties": {
                "function": {"type": "string"},
                "x0": {"type": "number"},
                "tolerance": {"type": "number"},
                "max_iterations": {"type": "integer"}
            },
            "required": ["function", "x0", "tolerance", "max_iterations"],
            "additionalProperties": False
        }
        
        try:
            jsonschema.validate(instance=input_json, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False