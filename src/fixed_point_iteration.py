import numpy as np
import jsonschema
from sympy import symbols,Eq,sin,cos,tan,sec,csc,cot,asin,acos,atan,acot,log,exp,ln,sqrt,lambdify,sympify

class FixedPointIteration:
    """
    Fixed-Point Iteration class for root finding
    """
    def __init__(self, 
                 f: str,
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
        self.x = symbols('x')
        self.f_x = f
        self.g_x = self.__transform_to_g(f)
        self.__f = lambdify(self.x,f)
        self.__g = self.__g_function(self.g_x)
        self.__x0 = x0
        self.__tol = tol
        self.__max_iter = max_iter

    def __transform_to_g(self,f: str):
        """
        Transform f(x) to g(x) for Fixed-Point Iteration
        f(x) = 0 => x = g(x) 
        :param f: Original function f(x)
        :return: Transformed function g(x)
        """

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

            while not right_side.is_Atom :

                if right_side.is_Mul: 
                    args = right_side.args
                    if any(arg.is_Rational and arg.denominator == 1 for arg in args): #dividing 
                        left_side = (right_side.args[0] / left_side )**-1
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
            
        x = self.x
        left_side,right_side=isolate_x(equation=Eq(eval(self.f_x),0)) # f(x) = 0

        if str(right_side) == "x": # g(x) = x 
            return str(left_side)
        else:
            return ValueError("The function is not convertable to g(x) = x")
    
    def __g_function(self,g_x:str):
        """
        Create a function for g(x) using the transformed expression
        
        :param g_x: Transformed function g(x)
        :return: Function for g(x)
        """
        try:
            x = self.x
            return lambdify(x, g_x, modules=['numpy'])
        except RuntimeError as e:
            return ValueError(f"Error creating g(x) function: {str(e)}")
        
    def solve(self):
        """
        Perform Fixed-Point Iteration with NaN and Inf checks
        
        :return: Dictionary with iteration results
        """
        x_now = self.__x0
        iterations = [
            {
                "n": 0,
                "x_n": x_now,
                "f(x_n)": self.__f(x_now),
                "g_x_function": str(self.g_x)
            }
        ]
        best_error = np.inf
        patience = 10
        for n in range(1, self.__max_iter + 1):
            try:
                # NaN/Inf check before computation
                if np.isnan(x_now) or np.isinf(x_now):
                    return {
                        "success": False,
                        "message": "Invalid initial value: NaN or Infinity detected",
                        "x_0": x_now
                    }

                x_next = self.__g(x_now)

                # NaN/Inf check after g(x) computation
                if np.isnan(x_next) or np.isinf(x_next):
                    return {
                        "success": False,
                        "message": "Computation resulted in NaN or Infinity",
                        "iteration": n,
                        "previous_x": x_now,
                        "problematic_x": x_next,
                        "iterations": iterations
                    }

                f_x = self.__f(x_next)
                error = abs(x_next - x_now)

                if error < best_error:
                    best_error = error
                else:
                    patience -= 1

                # Additional NaN check for function value
                if np.isnan(f_x):
                    return {
                        "success": False,
                        "message": "Function evaluation resulted in NaN",
                        "iteration": n,
                        "x_n": x_next,
                        "f(x_n)": f_x,
                        "iterations": iterations
                    }

                iteration_info = {
                    "n": n,
                    "x_n": x_next,
                    "f(x_n)": f_x,
                    "error": error
                }
                iterations.append(iteration_info)

                if error < self.__tol or abs(f_x) < self.__tol:
                    return {
                        "success": True,
                        "message": "Convergence achieved",
                        "n": n,
                        "x": x_next,
                        "f(x)": f_x,
                        "error": error,
                        "iterations": iterations
                    }
                
                if patience == 0:
                    return {
                        "success": True,
                        "message": "Patience limit reached",
                        "n": n,
                        "x": x_next,
                        "f(x)": f_x,
                        "error": best_error,
                        "iterations": iterations
                    }
            
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Computational error: {str(e)}",
                    "iteration": n,
                    "x_n": x_now,
                    "iterations": iterations
                }
            
            x_now = x_next

        return {
            "success": False,
            "message": "Maximum iterations reached without convergence",
            "error": best_error,
            "n": self.__max_iter,
            "x": x_now,
            "f(x)": self.__f(x_now),
            "iterations": iterations
        }

            
    
    @staticmethod
    def validate_input(input_json) -> bool:
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
        

if __name__ == "__main__":
    fpi=FixedPointIteration(f="sin(cos(x)) +3*x + x", x0=-4, tol=1e-1, max_iter=10000)
    print(fpi.g_x)
    print(fpi.solve())