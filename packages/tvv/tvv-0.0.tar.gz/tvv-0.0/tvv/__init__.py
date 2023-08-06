n1 = '''
#Непрерывные случайные величины номер 1
# Менять функцию и отрезок (все цифры 4 и 7) и квантиль (0,8 на что-то)
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

# Находим квантиль уровня 0.8 распределения X
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

# # Находим квантиль уровня 0.8 распределения Y
# quantile_Y = fsolve(lambda y: quad(lambda x: pdf_X(x) if g(x) <= y else 0, 4, 8)[0] - 0.8, 4)

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
#Нормальные случайные векторы номер 1
from scipy.stats import norm
#вектор N(-8;16;49;1;0,8)
# Parameters of the distributions
mu_X = -8
mu_Y = 16
sigma_X = 7 #корень из 49
sigma_Y = 1 #корень из 1
rho = 0.8

# Transform the points to the standard normal distribution
z1 = (3 - mu_X) / sigma_X
w1 = (7 - mu_Y) / sigma_Y

# Since X and Y are not independent, we need to use their joint distribution
# The events {X < 3} and {Y > 7} are disjoint, so the total probability is the sum of the two individual probabilities
P_X_less_than_3_and_Y_greater_than_7 = norm.cdf(z1) * (1 - norm.cdf(w1))
P_X_greater_than_3_and_Y_less_than_7 = (1 - norm.cdf(z1)) * norm.cdf(w1)

# The total probability is the sum of the two probabilities
total_probability = P_X_less_than_3_and_Y_greater_than_7 + P_X_greater_than_3_and_Y_less_than_7

print(f"The probability P((X−3)(Y−7)<0) is {total_probability}")
'''


def tv(n):
    if n == 1:
        print(n1)
    if n == 2 :
        print(n2)
    if n == 3:
        print(n3)
        
        
