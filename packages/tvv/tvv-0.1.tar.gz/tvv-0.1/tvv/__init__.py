n1 = '''
#Непрерывные случайные величины номер 1
# Менять функцию и отрезок (все цифры 4 и 9) и квантиль (0,9 на что-то)

import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve
from scipy import stats
import scipy

# Определяем функцию плотности вероятности
def pdf(x, C):
    return C*(1 + 7 * x**0.5 + 8 * x**0.7 + 4 * x**0.9)**1.3

# Находим константу C
C, error = quad(pdf, 4, 9, args=(1,))
C = 1 / C

# Находим математическое ожидание E(X)
EX, error = quad(lambda x: x*pdf(x, C), 4, 9)

# Находим стандартное отклонение σX
VarX, error = quad(lambda x: (x-EX)**2*pdf(x, C), 4, 9)
sigmaX = np.sqrt(VarX)

# Находим квантиль уровня 0.9 распределения X
quantile_09 = fsolve(lambda x: quad(pdf, 4, x, args=(C))[0] - 0.9, 4)

print(f"C = {C}")
print(f"E(X) = {EX}")
print(f"σX = {sigmaX}")
print(f"Квантиль уровня 0.9: {quantile_09[0]}")

'''

n2 = '''
#Непрерывные случайные величины номер 2
#Менять функцию, края отрезков, квантиль и в функции pdf_X
#поменять return, он рассчитывается так:
# 1/(b-a) = 1/(8-4) = 1/4, где b, a - края отрезка

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
from scipy.optimize import fsolve

# Определяем функцию g(x)
def g(x):
    return (1 + 6*x**0.5 + 4*x**0.7 + 5*x**0.9)**1.3

# Определяем функцию плотности вероятности X
def pdf_X(x):
    if 4 <= x <= 8:
        return 1/4
    else:
        return 0

# Находим математическое ожидание E(Y)
EY, _ = quad(lambda x: g(x)*pdf_X(x), 4, 8)

# Находим дисперсию D(Y) и стандартное отклонение σY
EY2, _ = quad(lambda x: (g(x)**2)*pdf_X(x), 4, 8)
DY = EY2 - EY**2
sigma_Y = np.sqrt(DY)

# Находим асимметрию As(Y)
AsY, _ = quad(lambda x: ((g(x)-EY)/sigma_Y)**3*pdf_X(x), 4, 8)

# Построим функцию распределения F(y) для Y с использованием численного интегрирования и интерполяции
x_values = np.linspace(4, 8, 1000)
y_values = g(x_values)
F_values = np.array([quad(lambda x: pdf_X(x), 4, x)[0] for x in x_values])
F_Y = interp1d(y_values, F_values, fill_value="extrapolate")

# Находим квантиль уровня 0.8 распределения Y
min_y = g(4)
quantile_Y = fsolve(lambda y: F_Y(y) - 0.8, min_y)

print(f"E(Y) = {EY}")
print(f"σY = {sigma_Y}")
print(f"As(Y) = {AsY}")
print(f"Квантиль уровня 0.8: {quantile_Y[0]}")
'''

n3 = '''
#Нормальные случайные векторы номер 1.1
from scipy.stats import norm
#вектор N(−8;16;49;1;0,8)
#Параметры распределения
EX = -8
EY = 16
stdOX = 7 #корень из 49
stdOY = 1 #корень из 1
korel_koef = 0.8

#Преобразуем значения точек в стандартное нормальное распределение
z1 = (3 - EX) / stdOX #Значение z-статистики для X=3
w1 = (7 - EY) / stdOY #Значение z-статистики для Y=7

#Так как X и Y не являются независимыми, нам нужно использовать их совместное распределение
#События несовместны, поэтому общая вероятность равна сумме двух индивидуальных вероятностей
P_X_less_than_3_and_Y_greater_than_7 = norm.cdf(z1) * (1 - norm.cdf(w1)) #Вероятность P(X < 3) ∩ P(Y > 7)
P_X_greater_than_3_and_Y_less_than_7 = (1 - norm.cdf(z1)) * norm.cdf(w1) #Вероятность P(X > 3) ∩ P(Y < 7)

#Общая вероятность равна сумме двух индивидуальных вероятностей
P = P_X_less_than_3_and_Y_greater_than_7 + P_X_greater_than_3_and_Y_less_than_7

print(f"Вероятность P((X−3)(Y−7)<0) is {P}")
'''


z1 = '''
#Непрерывные случайные величины номер 1

import numpy as np
from scipy.stats import *
from sympy import *
from scipy.integrate import quad, dblquad

def f(x):
  return (1 + 7 * x**0.5 + 8 * x**0.7 + 4 * x**0.9)**1.3

def f_c(x):
  return C * (1 + 7 * x**0.5 + 8 * x**0.7 + 4 * x**0.9)**1.3

C, _ = quad(f, 4, 9)
C = 1/C
print("Константа C:", C)
print(quad(f_c, 4, 9)[0])

def E(x):
  return x* f_c(x)

mean, _ = quad(E, 4, 9)
print("Мат. ожидание E(X):", mean)

def E2(x):
  return x**2 * f_c(x)

mean, _ = quad(E, 4, 9)
mean2, _ = quad(E2, 4, 9)
std = (mean2- mean**2) ** 0.5
print("Стандартное отклонение sigma X:", std)

class my_distribution(rv_continuous):
  def _pdf(self,x):
    return C * (1 + 7 * x**0.5 + 8 * x**0.7 + 4 * x**0.9)**1.3
rv = my_distribution(a=4, b=9, name = 'my_distribution')
q = rv.ppf(0.9)
print("Квантиль уровня 0,9 распределения X:", q)
'''

z2 = '''
#Непрерывные случайные величины номер 2

from scipy.stats import *
import numpy as np
from sympy import *
from scipy.integrate import quad, dblquad

def Y(X):
  return (1+6*X**0.5 + 4*X**0.7 + 5*X**0.9) ** 1.3

a = 4
b = 8
X = uniform(loc = a, scale = b - a)

def E_f(x):
    return Y(x) / (b-a)

def Var_f(x):
    return (Y(x) - quad(E_f, a, b)[0]) ** 2 / (b-a)

def As_f(x):
    return (Y(x) - quad(E_f, a, b)[0]) ** 3 / (b-a)

E, _ = quad(E_f, a, b)
std = quad(Var_f, a, b)[0] ** 0.5
As = (quad(As_f, a, b)[0]) / (std ** 3)
q = Y(X.ppf(.8))
print(E)
print(std)
print(As)
print(q)
'''


z3 = '''
#Нормальные случайные векторы номер 1

from scipy.stats import *
import numpy as np
from sympy import *
from scipy.integrate import quad, dblquad

#менять значения вектора
e1 = -8
e2 = 16
var1 = 49
var2 = 1
corr = 0.8

mu = np.array([e1, e2])
cov = np.array([[var1, var1**0.5 * var2 ** 0.5 * corr],
                [var1**0.5 * var2**0.5 * corr, var2]])
X_Y = multivariate_normal(mu, cov)

X = norm(e1, var1**0.5)
Y = norm(e2, var2**0.5)

Q1 = X.cdf(3) - X_Y.cdf([3,7]) #менять все 3 и 7
#print(Q1)

Q2 = Y.cdf(7) - X_Y.cdf([3,7]) #менять все 3 и 7
#print(Q2)

res = Q1 + Q2
print(res)
'''

z4 = '''
#Нормальные случайные векторы номер 2

from scipy.stats import *
import numpy as np
from sympy import *
from scipy.integrate import quad, dblquad

#менять значения вектора
e1 = -4
e2 = 4
var1 = 64
var2 = 81
corr = -0.31

mu = np.array([e1, e2])
cov = np.array([[var1, var1**0.5 * var2 ** 0.5 * corr],
                [var1**0.5 * var2**0.5 * corr, var2]])
X_Y = multivariate_normal(mu, cov)

X = norm(e1, var1**0.5)
Y = norm(e2, var2**0.5)

#Менять все 8,10,1 по логике исходя из этого P((X−8)(X−10)(Y−1)<0)

Q1 = X_Y.cdf([8, 1])
#print(Q1)

Q2 = X.cdf(10) - X.cdf(8) - (X_Y.cdf([10, 1]) - X_Y.cdf([8, 1]))
#print(Q2)

Q3 = Y.cdf(1) - X_Y.cdf([10, 1])

res = Q1 + Q2 + Q3
print(res)
'''

z5 = '''
#Нормальные случайные векторы номер 5
#Менять функцию и матрицу C

from scipy.stats import *
import numpy as np
from sympy import *
from scipy.integrate import quad, dblquad
from sympy.solvers.solveset import linsolve
from fractions import Fraction

x, y = symbols('x y')
q = 12 * (-51/2 * x ** 2 - 45*x*y - 9*x - 51/2 * y ** 2 - 7*y - 5/6)
C = Matrix([[51,45], [45,51]])
C = C**(-1)

s1 = diff(q, x)
s2 = diff(q, y)

lst = []
for i in linsolve([s1,s2], (x,y)):
    for j in i:
        lst.append(Fraction(str(j)).limit_denominator())
print("Мат ожидание X:", lst[0])
print("Мат ожидание Y:", lst[1])

varX, varY = C[0], C[3]
cov = C[1]
print("Дисперсия X:", varX)
print("Дисперсия Y:", varY)
print("Ковариация:", cov)

p = str(cov / (varX ** 0.5 * varY ** 0.5))
print("Коэффициент корреляции:", Fraction(p).limit_denominator())
'''


def tv(n):
    if n == 1:
        print(n1)
    if n == 2 :
        print(n2)
    if n == 3:
        print(n3)
    if n == 6:
        print(z1)
    if n == 7:
        print(z2)
    if n == 8:
        print(z3)
    if n == 9:
        print(z4)
    if n == 10:
        print(z5)
        
        
