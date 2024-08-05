# Backprop

## Course
Andrej Karpathy "Hero to zero" course on nnet:

- part 1 (backprop) : <https://www.youtube.com/watch?v=VMj-3S1tku0>

## Derivative

### Definition
```math
\frac{df}{dx} = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}
```

### Intuition
```math
\frac{df}{dx} = \text{slope of curve f(x)}
```

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0f/Tangent_to_a_curve.svg" style="height: 150px;" alt="">

small change in x (h) -> small change in f

### Rules
From limit definition -> derivative rules

```math
\begin{align}

\frac{d(k)}{dx} &= 0 \\
\frac{d(x)}{dx} &= 1 \\
\frac{d(x^2)}{dx} &= 2x \\
\frac{d(kx^n)}{dx} &= k \cdot n \cdot x^{n-1} \\
\frac{d(f(x) + g(x))}{dx} &= \frac{df(x)}{dx} + \frac{dg(x)}{dx} \\
\frac{d(f(x) g(x))}{dx} &= f(x) \frac{dg(x)}{dx} + g(x) \frac{df(x)}{dx} \\
\frac{d(e^x)}{dx} &= e^x

\end{align}
```

Ex:
```math
\begin{align}

f(x) &= 3x^2 - 4x + 5 \\
\frac{df}{dx} &= 3 \cdot 2x - 4 + 0 = 6x - 4

\end{align}
```

### Numerical approximation
if h is very small ($`h \approx 0`$):
```math
\frac{df}{dx} \approx \frac{f(x + h) - f(x)}{h}
```

### Multivariable
multiple variables -> partial derivative, assume other variables are constants.

Ex:
```math
\begin{align}

f(x,y,z) &= x * y + z \\
\frac{\partial f}{\partial x} &= y \cdot 1 + 0 = y \\
\frac{\partial f}{\partial y} &= x \cdot 1 + 0 = x \\
\frac{\partial f}{\partial z} &= 0 + 1 = 1

\end{align}
```

$`\frac{\partial f}{\partial y}`$ : how does y influences f ?

small change in y when keep x,z constants -> small change in f

## Autodiff
- Automatic differentiation
- mathematical expression (function) -> graph of nodes (expression graph)
- forward pass = traverse/eval graph = eval math expression
- compute derivative of function by computing df/dV at each node using numerical differentiation

Ex:
```
[a] -> [+] -> [c]
[b] ->

c = a + b
dc/da = ?
dc/da = 1 + 0 = 1
```

impl:
```
Value
    Value children[2]
    operator (+, -, *, /, ^, ...)
    grad = 0 (dL/dV)
```
operations on : scalar (1x1), vector (Nx1), matrix(MxN), tensor(MxNxK)

## Backprop
Backpropagation = wiggle machine to figure out how inputs affect output

```
from end node, reverse
calc dL/dV = grad of each node, L = loss function
dL/dL = 1 (base case)
dL/dV
...
```

### Chain rule
```
[a] -> [b] -> [L]
```

To find the grad of intermediate nodes (local derivative), we need to use the "chain rule":
```math
\frac{dL}{da} = \frac{dL}{db} \cdot \frac{db}{da}
```

Chain rule = product rule, change or variable, convert units

Find dL/da (impact of a on L) knowing dL/b (impact of b on L) and db/da (impact of a on b).

Intuition from wiki:
"If a car travels twice as fast as a bicycle and the bicycle is four times as fast as a walking man, then the car travels 2 × 4 = 8 times as fast as the man."
```
c: car
b: bike
w: walk

dc/db = 2
db/dw = 4

dc/dw = ?
dc/dw = (dc / db) * (db / dw) = 2 * 4 = 8
```

Ex:
```
[a] -> [+] -> [c]
[b] ->

c = a + b
dc/da = ?
dc/da = 1 + 0 = 1

dL/da = (dL / dc) * (dc / da)
dL/da = (dL / dc) * 1 = dL / dc
=> + node transfers the grad backwards, the grad is the same as previous node
```
Ex:
```
[a] -> [*] -> [c]
[b] ->

c = a * b
dc/da = ?
dc/da = a * db/da + b * da/da = b
dc/db = a * db/db + b * da/db = a

dL/da = (dL / dc) * (dc / da) = (dL / dc) * b
dL/db = (dL / dc) * (dc / db) = (dL / dc) * a
=> grad through the * node is previous node grad times the value of the opposite node
```

### Autograd
- backprop using autograd = reverse autodiff
- how to get output from inputs?
    - follow gradient -> chain rule
- indep of nnet

```
reversed topological sort
apply chain rule repetitively
    base case = 1
```

## Neural networks (nnet)
- MLP (Multi Layer Perceptron) = layers of neuron
- neuron (Perceptron) = weighted sum + bias

```
input = input data, weights, biases
output = loss
```

backprop -> iterative improve weights to min loss (train nnet):

- gradient points in direction of increasing value
- to min L, take step in direction opposite to gradient
- known as "gradient descent", optimization problem

## micrograd vs pytorch
- similar API
- much smaller, ~200lines of python!
- scalar vs tensor = optimization

## Python tricks
- `__repr__` vs `__str__` : str is for making it look good, repr is for making it accurate (debug)
- `__rmul__` : 1 * object
- format string
    - `"some {.4f} value".format(var)`
    - `f"some {var} value"`
    - `"%.4f" % var`
- put 2 lines on 1 : `line 1; line 2`

### Includes
```python
import math
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline #  plot immediately after running plt.plot() (jupyter notebook)
```

### Draw graph of nodes
TODO
