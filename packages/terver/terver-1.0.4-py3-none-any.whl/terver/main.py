import pyperclip
def n0():
    s=r'''
    from scipy import integrate
    import numpy as np
    import sympy as sp
    import scipy.stats as sps'''
    return pyperclip.copy(s)
def n1():
    s = r'''
    a=4
    b=9
    q=0.9
    def f(x):
        if a<=x<=b:
            return (1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3
        return 0
    class Distr(sps.rv_continuous):
        def _pdf(self,x):
            return c*f(x)
    X=Distr()
    c=1/integrate.quad(f,a,b)[0]
    print(c)
    def e_f(x):
        if a<=x<=b:
            return c*x*(1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3
        return 0
    Ex=integrate.quad(e_f,a,b)[0]
    print(Ex)
    def var_f(x):
        if a<=x<=b:
            return c*(x-Ex)**2*(1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3
        return 0
    Vx=integrate.quad(var_f,a,b)[0]
    print(np.sqrt(Vx))
    print(X.ppf(q))'''
    return pyperclip.copy(s)
def n1_2():
    s=r'''
    a = 4
    b = 9
    q = 0.9
    def f(x):
        if a <= x <= b:
            return (1 + 7 * x ** 0.5 + 8 * x ** 0.7 + 4 * x ** 0.9) ** 1.3
        return 0
    C = 1 / integrate.quad(f, a, b)[0]
    class distr(rv_continuous):
        def _pdf(self, x):
            return C * f(x)
    X = distr()
    Ex = X.expect()
    VarX = X.expect(lambda x: (x - Ex) ** 2, lb=a, ub=b)
    StdX = np.sqrt(VarX)
    Qx = X.ppf(q)
    C, Ex, StdX, Qx'''
    return pyperclip.copy(s)
def n1_3():
    s=r'''
    import numpy as np
    import scipy.stats as sps
    import sympy as sp
    from scipy import integrate
    a=4
    b=9
    def f(x):
        if a<=x<=b:
            return (1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3
        return 0
    class Distr(sps.rv_continuous):
        def _pdf(self,x):
            return c*f(x)
    X=Distr()
    c=1/integrate.quad(f,a,b)[0]
    print(c)
    Ex=X.expect()
    print(Ex)
    def var_f(x):
        if a<=x<=b:
            return c*(x-Ex)**2*(1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3
        return 0
    Vx=integrate.quad(var_f,a,b)[0]
    print(np.sqrt(Vx))
    print(sps.distributions.rv_continuous.ppf(X, 0.9))'''
    return pyperclip.copy(s)
def n2():
    s=r'''
    a=4
    b=8
    q=0.8
    def f(x):
        if (a<=x<=b):
            return (1 + 6 * x ** 0.5 + 4 * x ** 0.7 + 5 * x ** 0.9) ** 1.3
        return 0
    fx = 1 / (b - a)
    EY = integrate.quad(f, a, b)[0] * fx
    print(EY)
    def f2(x):
        if (a <= x <= b):
            return ((1 + 6 * x ** 0.5 + 4 * x ** 0.7 + 5 * x ** 0.9) ** 1.3) ** 2
        return 0
    Var = integrate.quad(f2, a, b)[0] * fx - EY ** 2
    print(Var ** 0.5)
    def f3(x):
        if (a <= x <= b):
            return ((1 + 6 * x ** 0.5 + 4 * x ** 0.7 + 5 * x ** 0.9) ** 1.3 - EY) ** 3
        return 0
    As = integrate.quad(f3, a, b)[0] / ((Var ** 0.5) ** 3) * fx
    print(As)
    Xq = a + q * (b - a)
    print(f(Xq))'''
    return pyperclip.copy(s)
def n2_2():
    s=r'''
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
    Ey, StdY, AsY, Qy'''
    return pyperclip.copy(s)
def n2_3():
    s=r'''
    a = 4
    b = 8
    
    def f(x):
        if a <= x <= b:
            return (1 + 6 * x**0.5 + 4 * x**0.7 + 5 * x**0.9)**1.3
        return 0
    class Distr(sps.rv_continuous):
        def _pdf(self,x):
            return c*f(x)
    X=Distr()
    # Вычисление математического ожидания E(Y)
    EY = np.mean([f(x) for x in np.linspace(a, b, 1000)])
    
    print("Математическое ожидание E(Y):", EY)
    
    variance = np.var([f(x) for x in np.linspace(a, b, 10000)])
    std_deviation = np.sqrt(variance)
    
    print("Стандартное отклонение σY:", std_deviation)
    
    skewness = sps.skew([f(x) for x in np.linspace(a, b, 10000)])
    
    print("Асимметрия As(Y):", skewness)
    
    # Нахождение квантили уровня 0,8 распределения Y
    quantile_08 = np.quantile([f(x) for x in np.linspace(a, b, 10000)], 0.8)
    
    print("Квантиль уровня 0,8 распределения Y:", quantile_08)'''
    return pyperclip.copy(s)
def n3():
    s=r'''
    mu1=-8
    mu2=16
    var1=49
    var2=1
    po=0.8
    x1=3
    y1=7
    si1=np.sqrt(var1)
    si2=np.sqrt(var2)
    mu = np.array([mu1,mu2])
    Cov= np.array([[var1,po*si1*si2],[po*si1*si2,var2]])
    W = sps.multivariate_normal(mu,Cov)
    X = sps.norm(mu1,si1)
    Y = sps.norm(mu2,si2)
    Pa=X.cdf(x1)-W.cdf([x1,y1])
    Pb=Y.cdf(y1)-W.cdf([x1,y1])
    Pall = Pa + Pb
    print(Pall)'''
    return pyperclip.copy(s)
def n3_3():
    s=r'''
    import numpy as np
    import scipy.stats as sps
    
    # Задание параметров нормального случайного вектора
    mu = [-8, 16]
    cov = [[49, 1], [1, 0.8]]
    
    # Создание объекта многомерного нормального распределения
    multivariate_normal = sps.multivariate_normal(mu, cov)
    
    # Вычисление вероятности P((X-3)(Y-7) < 0)
    probability = multivariate_normal.cdf([3, np.inf]) - multivariate_normal.cdf([3, 7]) - multivariate_normal.cdf([np.inf, 7]) + multivariate_normal.cdf([3, 7])
    
    # Вывод результата
    print("Вероятность P((X-3)(Y-7) < 0):", probability)'''
    return pyperclip.copy(s)
def n4():
    s=r'''
    mu1=-4
    mu2=4
    var1=64
    var2=81
    po=-0.31
    x1=8
    x2=10
    y1=1
    si1=np.sqrt(var1)
    si2=np.sqrt(var2)
    mu = np.array([mu1,mu2])
    Cov= np.array([[var1,po*si1*si2],[po*si1*si2,var2]])
    W = sps.multivariate_normal(mu,Cov)
    X = sps.norm(mu1,si1)
    Y = sps.norm(mu2,si2)
    Pa1 = W.cdf([x1,y1])
    Pb1 = X.cdf(x2) - X.cdf(x1) - (W.cdf([x2,y1])-W.cdf([x1,y1]))
    Pc1 = Y.cdf(y1) - W.cdf([x2,y1])
    Pall2 = Pa1+Pb1+Pc1
    Pall2'''
    return pyperclip.copy(s)
def n4_3():
    s = r'''
    import numpy as np
    from scipy.stats import norm, multivariate_normal
    
    mu1 = -4
    mu2 = 4
    var1 = 64
    var2 = 81
    correlation = -0.31
    x1 = 8
    x2 = 10
    y1 = 1
    
    sigma1 = np.sqrt(var1)
    sigma2 = np.sqrt(var2)
    
    mean = np.array([mu1, mu2])
    covariance = np.array([[var1, correlation * sigma1 * sigma2], [correlation * sigma1 * sigma2, var2]])
    
    multivariate_dist = multivariate_normal(mean, covariance)
    
    prob_a = multivariate_dist.cdf([x1, y1])
    prob_b = norm.cdf(x2, mu1, sigma1) - norm.cdf(x1, mu1, sigma1) - (multivariate_dist.cdf([x2, y1]) - multivariate_dist.cdf([x1, y1]))
    prob_c = norm.cdf(y1, mu2, sigma2) - multivariate_dist.cdf([x2, y1])
    
    total_prob = prob_a + prob_b + prob_c
    print("Total Probability:", total_prob)'''
    return pyperclip.copy(s)
def n5():
    s=r'''
    # f(x,y)=18/pi*e**(-(60x**2+96xy-16x+60y**2+10y+85/24)/2)
    # 60x**2+96xy+60y**2
    c_inv=sp.Matrix([[60,96/2],
                     [96/2,60]])
    #det=60**2-48**2=3600-2304 = 1296
    # c=1/1296 * [[60,-48],
    #            [-48,60]]
    #varx=c[0,0]=5/108
    #vary=c[1,1]=5/108
    #cov=c[0,1]=-1/27
    #po=cov/(varx*vary)**0.5=-(108)/(27*5)=-4/5
    #f'x=120*x+96*y-16
    #f'y=120*y+96*x+10
    #x=5/9
    #y=-19/36'''
    return pyperclip.copy(s)
def n5_2():
    s=r'''
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
    Ex, Ey, VarX, VarY, CovXY, r'''
    return pyperclip.copy(s)
def n5_3():
    s = r'''
    import numpy as np
    from scipy import integrate
    from fractions import Fraction
    
    # Определение функции плотности распределения fX,Y(x,y)
    def fxy(x, y):
        return 18 * np.exp(-30*x**2 - 48*x*y + 8*x - 30*y**2 - 5*y - 85/24) / np.pi
    
    # Функция для преобразования десятичного значения в несократимую дробь
    def to_fraction(decimal):
        return Fraction(decimal).limit_denominator()
    
    # 1) Математическое ожидание E(X)
    ex_num, _ = integrate.dblquad(lambda x, y: x * fxy(x, y), -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)
    ex = to_fraction(ex_num)
    
    # 2) Математическое ожидание E(Y)
    ey_num, _ = integrate.dblquad(lambda x, y: y * fxy(x, y), -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)
    ey = to_fraction(ey_num)
    
    # 3) Дисперсия Var(X)
    varx_num, _ = integrate.dblquad(lambda x, y: (x - ex_num)**2 * fxy(x, y), -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)
    varx = to_fraction(varx_num)
    
    # 4) Дисперсия Var(Y)
    vary_num, _ = integrate.dblquad(lambda x, y: (y - ey_num)**2 * fxy(x, y), -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)
    vary = to_fraction(vary_num)
    
    # 5) Ковариация Cov(X,Y)
    covxy_num, _ = integrate.dblquad(lambda x, y: (x - ex_num) * (y - ey_num) * fxy(x, y), -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)
    covxy = to_fraction(covxy_num)
    
    # 6) Коэффициент корреляции ρ(X,Y)
    corr_xy_num = covxy_num / np.sqrt(varx_num * vary_num)
    corr_xy = to_fraction(corr_xy_num)
    
    # Вывод результатов
    print("1) Математическое ожидание E(X):", ex)
    print("2) Математическое ожидание E(Y):", ey)
    print("3) Дисперсия Var(X):", varx)
    print("4) Дисперсия Var(Y):", vary)
    print("5) Ковариация Cov(X,Y):", covxy)
    print("6) Коэффициент корреляции ρ(X,Y):", corr_xy)'''
    return pyperclip.copy(s)