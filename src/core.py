import numpy as np
import jsonschema
from typing import Callable, Dict, Any
from sympy import symbols,Eq,sin,cos,tan,sec,csc,cot,asin,acos,atan,acot,log,exp,ln

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
        f(x) = 0 => x = g(x) 
        :param f: Original function f(x)
        :return: Transformed function g(x)
        """
        x = symbols('x')

        #Note that trigonometric functions lose their domain of definition if the inverse is taken. //Write frontend
        def isolate_x(equation):
            """
            Internal method for symbolically isolating x in an equation
            Handles various types of functions and transformations
            """
            left_side = equation.lhs
            right_side = equation.rhs

            x_terms = [i for i in left_side.as_ordered_terms() if i.has(x) ]  
            right_side = x_terms[0]
            left_side = x_terms[0] - left_side 
            
            inverse_map = {
                sin: asin,
                cos: acos,
                tan: atan,
                cot: acot,
                sec: lambda x: acos(1/x),  # Special handling for sec
                csc: lambda x: asin(1/x),   # Special handling for csc
                asin: sin,
                acos: cos,
                atan: tan,
                acot: cot,
                log: exp,
                exp:log
            }

            patience = 10
            while not right_side.is_Atom :
                patience -=1
                if patience < 0:
                    print("Not Enough Patience for this equation")
                    break

                if right_side.is_Mul: 
                    args = right_side.args
                    if any(arg.is_Rational and arg.denominator == 1 for arg in args): #dividing 
                        left_side = (left_side / right_side.args[0])
                        if left_side != 0:
                            left_side = 1/left_side
                        right_side, _  = right_side.args[1].as_base_exp()

                    else: #multiplication
                        for i in range(1,len(args)):
                            right_side = right_side / args[i] 
                            left_side = left_side / args[i]
                
                elif right_side.is_Pow:
                    base,exponent = right_side.as_base_exp()
                    right_side = base
                    left_side = left_side ** (1 / exponent)
                    
                
                elif right_side.is_Function: #trigh not supported
                    if right_side.func in inverse_map:  
                        inverse_func = inverse_map[right_side.func]
                        right_side = right_side.args[0]
                        left_side = inverse_func(left_side)
                    else:
                        raise NotImplementedError(f"Cannot isolate {right_side}")

                else:
                    raise NotImplementedError(f"Cannot isolate {right_side}")


            return left_side, right_side
        
        def g():
            """Helper function that returns the transformed and final checked function gx to the class"""
            left_side,right_side=isolate_x(Eq(f),0) # f(x) = 0
            if str(right_side) == "x": # g(x) = x 
                g_x = str(left_side)
                return eval(g_x)
            else:
                print("Did not find the g_x")
        
        return g
        
    def solve(self) -> Dict[str, Any]:
        """
        Perform Fixed-Point Iteration
        
        :return: Dictionary with iteration results
        """
        pass
    
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