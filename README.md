# Fixed-Point Iteration Root Finder
CSE 3121 Numerical Analysis course Homework

## Overview
A Python-based application for solving root-finding problems using the Fixed-Point Iteration method. This project includes a **core library**, a **REST API**, and a **graphical user interface (GUI)**.

## Features
- **Core Solver:** Root finding using Fixed-Point Iteration Method
- **API:** RESTful API endpoint for numerical computation
- **GUI:** Interactive GUI with `tkinter`
- **Custom Validation:** Ensures proper input schema for API requests.
- **Visualization:** Detailed convergence plots using `matplotlib`.

## Requirements
- Python 3.10+
- Dependencies:
  - Flask
  - Flask-CORS
  - NumPy
  - Matplotlib
  - Tkinter
  - Requests
  - jsonschema

## Installation
1. Clone the this project
```bash
   git clone https://github.com/icelal-kskn/fixed_point_iteration.git
```
2. Setup the project
```bash
pip install e .
```

3. Starting Flask Based API
```bash 
python -m fixed_point_iteration.api
```

4. Starting Tkinter Based GUI
```bash
python -m fixed_point_iteration.gui
```

## Project Structure
```bash
fixed_point_calculator/
│
├── src/
│   ├── fixed_point_iteration/
│   │   ├── core.py        # Core solver logic
│   │   ├── api.py         # Flask API implementation
│   │   ├── gui.py         # GUI application
│   │   ├── __init__.py    # Package initialization
│
├── requirements.txt       # Dependencies
├── setup.py               # Installation script
├── README.md              # Project documentation
```


## Usage

### GUI Application
Run the GUI interface to input the function, initial guess, tolerance, and maximum iterations.
```bash
python -m fixed_point_iteration.gui
```
### API Endpoint
Run the Flask API Server
```bash
python -m fixed_point_iteration.api
```

Send a POST request to `/fixed-point-iteration` with JSON payload:
```bash
curl -X POST http://localhost:5000/fixed-point-iteration \
-H "Content-Type: application/json" \
-d '{
  "function": "sin(x) + x + 1",
  "x0": 2,
  "tolerance": 1e-6,
  "max_iterations": 100
}'
```
## Contributing
1. Fork the repository.
2. Create your feature branch (git checkout -b feature/AmazingNewFeature).
3. Commit your changes (git commit -m 'Add AmazingNewFeature').
4. Push to the branch (git push origin feature/AmazingNewFeature).
5. Open a pull request.

## Contact
School Email: 200316059@ogr.cbu.edu.tr
Github: @icelal-kskn

## Homework Assessment
- Finds root of any function using Fixed-Point Iteration
- Uses input parameters: f(x), x_0, tolerance, max iterations
- Transforms function f(x)=0 to x=g(x)
- Converges using x_(n+1)=g(x_n)
- Stops when |f(x_n)|<tol or |x_n-x_(n-1)|<tol
- Stops if iterations exceed max_iter
- Provides visual plot representation
- Implements JSON-based API
- Includes independent GUI
