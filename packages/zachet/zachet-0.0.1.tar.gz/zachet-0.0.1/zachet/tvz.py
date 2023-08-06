def help_():
    print('''
    Для импорта перечня используемых библиотек libs()
    Для задач первого типа one()
    Для задач второго типа two()
    Для задач третьего типа three()
    ''')
def libs():
    print('''
from scipy.stats import *
from scipy import integrate
import numpy as np
import sympy as sp
    ''')
def one():
    print('''
Усл: абс. непр. велич. Х может принимать значения [4,9] 
     распр. Х имеет вид f(x) = C(1 + 7x^0.5 + 8x^0.7 + 4x^0.9)^1.3
     C - конст. 
     Найти: C, E(X), стандарт.откл., квантиль уровня 0,9 распр. Х

a = 4
b = 9
q = 0.9

def f(x):
    if a <= x <= b:
        return (1 + 7 * x ** 0.5 + 8 * x ** 0.7 + 4 * x ** 0.9) ** 1.3
    return 0

C = 1/integrate.quad(f, a, b)[0]

class distr(rv_continuous):
    def _pdf(self, x):
        return C * f(x)
    
X = distr()
Ex = X.expect()

VarX = X.expect(lambda x: (x - Ex) ** 2, lb = a, ub = b)
StdX = np.sqrt(VarX)

Qx = X.ppf(q)

print(C, Ex, StdX, Qx)
_______________________________________________________
Усл: абс. непр. велич. Х может принимать значения [4,7] 
     распр. Х имеет вид f(x) = C(1 + 3x^0.5 + 6x^0.7 + 9x^0.9)^1.5
     C - конст. 
     Найти: C, E(X), стандарт.откл., квантиль уровня 0,8 распр. Х
a = 4
b = 7
q = 0.8

def f(x):
    if a <= x <= b:
        return (1 + 3 * x ** 0.5 + 6 * x ** 0.7 + 9 * x ** 0.9) ** 1.5
    return 0

C = 1/integrate.quad(f, a, b)[0]

class distr(rv_continuous):
    def _pdf(self, x):
        return C * f(x)
    
X = distr()
Ex = X.expect()

VarX = X.expect(lambda x: (x - Ex) ** 2, lb = a, ub = b)
StdX = np.sqrt(VarX)

Qx = X.ppf(q)
print(C, Ex, StdX, Qx)
_______________________________________________________
Усл: случ. велич. Х равн. распр. на [4,8]. Случ. велич. Y выраж.
     через Х след. образом 
     распр. Y = C(1 + 6x^0.5 + 4x^0.7 + 5x^0.9)^1.3 
     Найти: E(Y), стандарт.откл., As(Y), квантиль уровня 0,8 распр. Х
a = 4
b = 8
q = 0.8

def f(x):
    if (a <= x <= b):
        return (1 + 6 * x ** 0.5 + 4 * x ** 0.7 + 5 * x ** 0.9) ** 1.3
    return 0

fx = 1 / (b - a)

Ey = integrate.quad(f, a, b)[0] * fx

VarY = integrate.quad(lambda x: f(x) ** 2, a, b)[0] * fx - Ey ** 2
StdY = np.sqrt(VarY)

AsY = integrate.quad(lambda x: (f(x) - Ey) ** 3, a, b)[0] / (StdY ** 3) * fx

Xq = a + q * (b - a)
Qy = f(Xq)
print(Ey, StdY, AsY, Qy)
_______________________________________________________
Усл: случ. велич. Х равн. распр. на [4,7]. Случ. велич. Y выраж.
     через Х след. образом 
     распр. Y = C(1 + 3x^0.5 + 4x^0.7 + 9x^0.9)^1.1 
     Найти: E(Y), стандарт.откл., As(Y), квантиль уровня 0,9 распр. Х
a = 4
b = 7
q = 0.9

def f(x):
    if (a <= x <= b):
        return (1 + 3 * x ** 0.5 + 4 * x ** 0.7 + 9 * x ** 0.9) ** 1.1
    return 0

fx = 1 / (b - a)

Ey = integrate.quad(f, a, b)[0] * fx

VarY = integrate.quad(lambda x: f(x) ** 2, a, b)[0] * fx - Ey ** 2
StdY = np.sqrt(VarY)

AsY = integrate.quad(lambda x: (f(x) - Ey) ** 3, a, b)[0] / (StdY ** 3) * fx

Xq = a + q * (b - a)
Qy = f(Xq)
print(Ey, StdY, AsY, Qy)
    ''')
def two():
    print('''
Усл: Для норм. случ. вектора (X,Y) ~ N(-8;16;49;1;0;8)
Найти: P((X-3)(Y-7)<0)
Ex = -8
Ey = 16
VarX = 49
VarY = 1
r = 0.8

x1 = 3
y1 = 7

StdX = np.sqrt(VarX)
StdY = np.sqrt(VarY)

Exy = [Ex, Ey]
Cov = [[VarX, r * StdX * StdY], [r * StdX * StdY, VarY]]

X = norm(Ex, StdX)
Y = norm(Ey, StdY)
W = multivariate_normal(Exy, Cov)

Pa = X.cdf(x1) - W.cdf([x1, y1])
Pb = Y.cdf(y1) - W.cdf([x1, y1])

P = Pa + Pb
print(P)
_______________________________________________________
Усл: Для норм. случ. вектора (X,Y) ~ N(-7;17;81;16;0;6)
Найти: P((X-4)(Y-3)<0)
Ex = -7
Ey = 17
VarX = 81
VarY = 16
r = 0.6

x1 = 4
y1 = 3

StdX = np.sqrt(VarX)
StdY = np.sqrt(VarY)

Exy = [Ex, Ey]
Cov = [[VarX, r * StdX * StdY], [r * StdX * StdY, VarY]]

X = norm(Ex, StdX)
Y = norm(Ey, StdY)
W = multivariate_normal(Exy, Cov)

Pa = X.cdf(x1) - W.cdf([x1, y1])
Pb = Y.cdf(y1) - W.cdf([x1, y1])

P = Pa + Pb
print(P)
_______________________________________________________
Усл: Для норм. случ. вектора (X,Y) ~ N(-4;4;64;81;-0,31)
Найти: P((X-8)(X-10)(Y-1)<0)
Ex = -4
Ey = 4
VarX = 64
VarY = 81
r = -0.31

x1 = 8
x2 = 10
y1 = 1

StdX = np.sqrt(VarX)
StdY = np.sqrt(VarY)

Exy = [Ex, Ey]
Cov = [[VarX, r * StdX * StdY], [r * StdX * StdY, VarY]]

X = norm(Ex, StdX)
Y = norm(Ey, StdY)
W = multivariate_normal(Exy, Cov)

Pa = W.cdf([x1, y1])
Pb = X.cdf(x2) - X.cdf(x1) - W.cdf([x2, y1]) + W.cdf([x1, y1])
Pc = Y.cdf(y1) - W.cdf([x2, y1])

P = Pa + Pb + Pc
print(P)
_______________________________________________________
Усл: Для норм. случ. вектора (X,Y) ~ N(-1;2;49;25;-0,20)
Найти: P((X-5)(X-13)(Y-1)<0)
Ex = -1
Ey = 2
VarX = 49
VarY = 25
r = -0.2

x1 = 5
x2 = 13
y1 = 1

StdX = np.sqrt(VarX)
StdY = np.sqrt(VarY)

Exy = [Ex, Ey]
Cov = [[VarX, r * StdX * StdY], [r * StdX * StdY, VarY]]

X = norm(Ex, StdX)
Y = norm(Ey, StdY)
W = multivariate_normal(Exy, Cov)

Pa = W.cdf([x1, y1])
Pb = X.cdf(x2) - X.cdf(x1) - W.cdf([x2, y1]) + W.cdf([x1, y1])
Pc = Y.cdf(y1) - W.cdf([x2, y1])

P = Pa + Pb + Pc
print(P)
_______________________________________________________
''')
def three():
    print('''
Усл: Случ. вектор (X, Y) имеет плотность распр.
     fx,y(x,y) = 18e^(-30^2 - 48xy + 8x - 30y^2 - 5y - 85/24)/ Pi
Найти:E(X), E(Y), Var(x), Var(Y), Cov(X, Y), коэф. корреляц ро от (X, Y)
x, y = sp.symbols('x y')
f = 60 * x ** 2 + 96 * x * y + 60 * y ** 2 - 16 * x + 10 * y

C = sp.Matrix(2, 2, [60, sp.Rational(96, 2), sp.Rational(96, 2), 60])
C = C ** -1

VarX = C[0, 0]
VarY = C[1, 1]
CovXY = C[0, 1]

r = CovXY / sp.sqrt(VarX * VarY)

res = sp.solve([f.diff(x), f.diff(y)], [x, y])

Ex = res[x]
Ey = res[y]
print( Ey, VarX, VarY, CovXY, r)
_______________________________________________________\
Усл: Случ. вектор (X, Y) имеет плотность распр.
     fx,y(x,y) = 12e^(-51^2/2 - 45xy - 9x - 51y^2/2 - 7y - 5/6)/ Pi
Найти:E(X), E(Y), Var(x), Var(Y), Cov(X, Y), коэф. корреляц ро от (X, Y)
x, y = sp.symbols('x y')
f = 51 * x ** 2 + 90 * x * y + 51 * y ** 2 + 18 * x + 14 * y

C = sp.Matrix(2, 2, [51, sp.Rational(90, 2), sp.Rational(90, 2), 51])
C = C ** -1

VarX = C[0, 0]
VarY = C[1, 1]
CovXY = C[0, 1]

r = CovXY / sp.sqrt(VarX * VarY)

res = sp.solve([f.diff(x), f.diff(y)], [x, y])

Ex = res[x]
Ey = res[y]
print( Ey, VarX, VarY, CovXY, r)
''')

help_()