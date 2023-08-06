
class rv:
    def discrete(number):
        sklad = {1: "\
import numpy as np\n\
from scipy.stats import *\n\
from tqdm import tqdm\n\
from sympy import *\n\
import matplotlib.pyplot as plt\n\
import itertools as it\n\
from scipy import integrate\n\
from scipy.special import *\n\
import random",
                 2: "\
a = 4\n\
b = 9\n\
q = 0.9\n\
def f(x):\n\
    if a <= x <= b:\n\
        return (1 + 7 * x ** 0.5 + 8 * x ** 0.7 + 4 * x ** 0.9) ** 1.3\n\
    return 0\n\
# константа\n\
C = 1/integrate.quad(f, a, b)[0]\n\
# объект, представляющий непрерывное случайное распределение\n\
class distr(rv_continuous):\n\
    def _pdf(self, x):\n\
        return C * f(x)\n\
X = distr()\n\
Ex = X.expect() # мат ожидание\n\
VarX = X.expect(lambda x: (x - Ex) ** 2, lb = a, ub = b) # дисперсия\n\
StdX = np.sqrt(VarX) # стандартное отклонение\n\
Qx = X.ppf(q) # квантиль\n\
C, Ex, StdX, Qx\n",

                 3: "\
a = 4\n\
b = 8\n\
q = 0.8\n\
def f(x):\n\
    if (a <= x <= b):\n\
        return (1 + 6 * x ** 0.5 + 4 * x ** 0.7 + 5 * x ** 0.9) ** 1.3\n\
    return 0\n\
fx = 1 / (b - a) #  коэффициент нормировки плотности вероятности для случайной величины Y.\n\
Ey = integrate.quad(f, a, b)[0] * fx # мат ожидание\n\
VarY = integrate.quad(lambda x: f(x) ** 2, a, b)[0] * fx - Ey ** 2 # дисперсия\n\
StdY = np.sqrt(VarY) # стандартное отклонение\n\
AsY = integrate.quad(lambda x: (f(x) - Ey) ** 3, a, b)[0] / (StdY ** 3) * fx # асимметрия\n\
Xq = a + q * (b - a)\n\
Qy = f(Xq)\n\
Ey, StdY, AsY, Qy\n\
\n",



                 4: "\
# для нормального случайного вектора (X, Y)\n\
Ex = -8\n\
Ey = 16\n\
VarX = 49\n\
VarY = 1\n\
r = 0.8 # коэф корр\n\
        \n\
# вероятность (X-3)*(Y-7)<0\n\
x1 = 3\n\
y1 = 7\n\
        \n\
StdX = np.sqrt(VarX)\n\
StdY = np.sqrt(VarY)\n\
        \n\
Exy = [Ex, Ey]\n\
Cov = [[VarX, r * StdX * StdY], [r * StdX * StdY, VarY]] #ковариц матрица\n\
        \n\
#  объекты нормального распределения\n\
X = norm(Ex, StdX)\n\
Y = norm(Ey, StdY)\n\
W = multivariate_normal(Exy, Cov)\n\
        \n\
Pa = X.cdf(x1) - W.cdf([x1, y1])\n\
Pb = Y.cdf(y1) - W.cdf([x1, y1])\n\
        \n\
P = Pa + Pb\n\
P\n",

                 5: "\
# норм случ вектор (,,,,)\n\
Ex = -4\n\
Ey = 4\n\
VarX = 64\n\
VarY = 81\n\
r = -0.31\n\
\n\
#(x-8)(x-10)(y-1)\n\
x1 = 8\n\
x2 = 10\n\
y1 = 1\n\
\n\
StdX = np.sqrt(VarX)\n\
StdY = np.sqrt(VarY)\n\
\n\
Exy = [Ex, Ey]\n\
Cov = [[VarX, r * StdX * StdY], [r * StdX * StdY, VarY]]\n\
\n\
X = norm(Ex, StdX)\n\
Y = norm(Ey, StdY)\n\
W = multivariate_normal(Exy, Cov)\n\
\n\
Pa = W.cdf([x1, y1])\n\
Pb = X.cdf(x2) - X.cdf(x1) - W.cdf([x2, y1]) + W.cdf([x1, y1])\n\
Pc = Y.cdf(y1) - W.cdf([x2, y1])\n\
\n\
P = Pa + Pb + Pc\n\
P\n",

                 6: "\
x, y = sp.symbols('x y')\n\
# -(x2 + xy + y2) / 2\n\
f = 60 * x ** 2 + 96 * x * y + 60 * y ** 2 - 16 * x + 10 * y\n\
\n\
C = sp.Matrix(2, 2, [60, sp.Rational(96, 2), sp.Rational(96, 2), 60])\n\
C = C ** -1\n\
\n\
VarX = C[0, 0]\n\
VarY = C[1, 1]\n\
CovXY = C[0, 1]\n\
\n\
r = CovXY / sp.sqrt(VarX * VarY)\n\
\n\
res = sp.solve([f.diff(x), f.diff(y)], [x, y])\n\
\n\
Ex = res[x]\n\
Ey = res[y]\n\
Ex, Ey, VarX, VarY, CovXY, r\n"}
        print(sklad[number])

    def cont(number):
        sklad = {1: 'imports',
                 2: "Абсолютно непрерывная случайная величина X\
может принимать значения только в отрезке [5,10]\
. На этом отрезке плотность распределения случайной величины X\
имеет вид: f(x)=C(1+5x0,5+7x0,7+4x0,9)0,4\
, где C\
– положительная константа. Найдите: 1) константу C\
; 2) математическое ожидание E(X)\
; 3) стандартное отклонение σX\
; 4) квантиль уровня 0,8\
распределения X. ",
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



