import os.path


class rv:
    def discrete(number):
        sklad = {1:\
"import numpy as np\n\
from scipy.stats import *\n\
from tqdm import tqdm\n\
from sympy import *\n\
import matplotlib.pyplot as plt\n\
import itertools as it\n\
from scipy import integrate\n\
from scipy.special import *\n\
import random",
                2: "\
a,b = 4,7\n\
def f(x):\n\
    if a <= x <= b:\n\
        return (1+5*x**0.5+7*x**0.7+4*x**0.9)**0.4\n\
    return 0\n\
C = 1/integrate.quad(f,a,b)[0]\n\
print(C)\n\
#матожидание:\n\
def f_C(x):\n\
    if 4 <= x <= 7:\n\
        return x*C*((1+5*x**0.5+7*x**0.7+4*x**0.9)**0.4)\n\
    return 0\n\
Ex = integrate.quad(f_C,a,b)[0]\n\
print(Ex)\n\
def f_C_sq(x):\n\
    if 4 <= x <= 7:\n\
        return (x)**2 * C *((1+5*x**0.5+7*x**0.7+4*x**0.9)**0.4)\n\
    return 0\n\
print((integrate.quad(f_C_sq,a,b)[0] - Ex**2)**0.5)\n\
class distrbution(rv_continuous):\n\
    def _pdf(self, x):\n\
        return C * f(x)\n\
d = distrbution()\n\
quant = 0.8\n\
print(d.ppf(quant))\n",
                3:"\
def Y(x):\n\
#сюда вставляем функцию\n\
    return (1+5*x**0.5+7*x**0.7+4*x**0.9)**1.1\n\
a,b = 4,8\n\
dlin = b-a\n\
def f(x):\n\
    if a <= x <= b:\n\
        return Y(x)\n\
    return 0\n\
Ex = integrate.quad(f,a,b)[0] * 1/dlin\n\
print(Ex)\n\
def f_s(x):\n\
    if a <= x <= b:\n\
        return (Y(x))**2\n\
    return 0\n\
std = (integrate.quad(f_s,a,b)[0] * 1/dlin - (Ex)**2)**0.5\n\
print(std)\n\
#асимметрия:\n\
def f_sk(x):\n\
    if a <= x <= b:\n\
        return ((Y(x) - Ex)/std)**3\n\
    return 0\n\
skew = integrate.quad(f_sk,a,b)[0] * 1/dlin\n\
print(skew)\n\
#квантиль:\n\
quant = 0.8\n\
q = a + quant * dlin\n\
print(Y(q))\n",
                4: "\
from scipy.stats import multivariate_normal, norm\n\
# для нормального (-7; 17; 81; 16; 0.6) найдите\n\
# P((x - 4)(y - 3) < 0)\n\
# ЗНАК МЕНЬШЕ\n\
a = -7; b = 17; c = 81; d = 16; e = 0.6\n\
mu = np.array([a, b])\n\
Cov = np.array([[c, e * np.sqrt(c) * np.sqrt(d)], [e * np.sqrt(c) * np.sqrt(d), d]])\n\
\n\
W = multivariate_normal(mu, Cov)\n\
X = norm(a, np.sqrt(c))\n\
Y = norm(b, np.sqrt(d))\n\
x = 4; y = 3\n\
print(X.cdf(x) - W.cdf([x, y]))\n",
                
                5: "\
from scipy.stats import multivariate_normal, norm\n\
# для нормального (-4; 4; 64; 81; -0.31) найдите\n\
# P((x - 8)(x - 10)(y - 1) < 0)\n\
# ЗНАК МЕНЬШЕ\n\
a = -4; b = 4; c = 64; d = 81; e = -0.31\n\
mu = np.array([a, b])\n\
Cov = np.array([[c, e * np.sqrt(c) * np.sqrt(d)], [e * np.sqrt(c) * np.sqrt(d), d]])\n\
W = multivariate_normal(mu, Cov)\n\
X = norm(a, np.sqrt(c))\n\
Y = norm(b, np.sqrt(d))\n\
x1 = 8; x2 = 10; y = 1\n\
Pa = W.cdf([x1, y])\n\
Pb = X.cdf(x2) - X.cdf(x1) - (W.cdf([x2, y]) - W.cdf([x1, y]))\n\
Pc = Y.cdf(y) - W.cdf([x2, y])\n\
print(Pa + Pb + Pc)\n",
                
                6: "\
from sympy import *\n\
import numpy as np\n\
init_printing()\n\
from fractions import Fraction\n\
def dr(x):\n\
    return Fraction(x).limit_denominator()\n\
# выражение 18 / pi * E**(-30*x**2 - 48*x*y + 8*x - 30*y**2 - 5*y - 85/24)\n\
x, y = symbols('x y')\n\
prim = 18 / pi * E**(-30*x**2 - 48*x*y + 8*x - 30*y**2 - 5*y - 85/24)\n\
integ_y = simplify(integrate(prim, (x, -np.inf, np.inf)))\n\
integ_x = simplify(integrate(prim, (y, -np.inf, np.inf)))\n\
Ey = float(simplify(integrate(integ_y * y, (y, -np.inf, np.inf))))\n\
Ex = float(simplify(integrate(integ_x * x, (x, -np.inf, np.inf))))\n\
print(dr(Ex), dr(Ey))\n\
Varx = float(simplify(integrate(x**2 *integ_x, (x, -np.inf, np.inf))) - Ex ** 2)\n\
Vary = float(simplify(integrate(y ** 2 *integ_y, (y, -np.inf, np.inf))) - Ey ** 2)\n\
print(dr(Varx), dr(Vary))\n\
Cov = float(simplify(integrate(simplify(integrate((x - Ex) * (y - Ey) * prim, (x, -np.inf, np.inf))), (y, -np.inf, np.inf))))\n\
print(dr(Cov))\n\
p = Cov / (np.sqrt(Varx) * np.sqrt(Vary))\n\
print(dr(p))\n"}
        print(sklad[number])
    
    def cont(number):
        sklad = {1:'imports', 
                2:"Абсолютно непрерывная случайная величина X\
может принимать значения только в отрезке [5,10]\
. На этом отрезке плотность распределения случайной величины X\
имеет вид: f(x)=C(1+5x0,5+7x0,7+4x0,9)0,4\
, где C\
– положительная константа. Найдите: 1) константу C\
; 2) математическое ожидание E(X)\
; 3) стандартное отклонение σX\
; 4) квантиль уровня 0,8\
распределения X. " ,
                3: "\
Случайная величина X\
равномерно распределена на отрезке [5,10]\
. Случайная величина Y\
выражается через X\
следующим образом: Y=(1+5X0,5+7X0,7+4X0,9)1,1\
. Найдите: 1) математическое ожидание E(Y)\
; 2) стандартное отклонение σY\
; 3) асимметрию As(Y)\
; 4) квантиль уровня 0,8\
распределения Y",
                4: "\
Для нормального случайного вектора (X,Y)∼N(0;0;1;1;0)\
найдите вероятность P((X−1)(Y−2)<0)\
                    ",
                5: "\
Для нормального случайного вектора (X,Y)∼N(0;0;1;1;0)\
найдите вероятность P((X−1)(X−2)(Y−3)<0)",
                6: "\
Случайный вектор (X,Y)\
имеет плотность распределения\
f X,Y(x,y)= 18e**(−30x**2−48xy+8x−30y**2−5y−85/24)/π\
Найдите: 1) математическое ожидание E(X)\
; 2) математическое ожидание E(Y)\
; 3) дисперсию Var(X)\
; 4) дисперсию Var(Y)\
; 5) ковариацию Cov(X,Y)\
; 6) коэффициент корреляции ρ(X,Y)"

                
        }
        print(sklad[number])



