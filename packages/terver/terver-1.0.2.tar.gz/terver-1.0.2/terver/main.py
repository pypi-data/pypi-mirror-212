import pyperclip
def n1():
    s = r'''
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
    print(X.ppf(0.9))'''
    return pyperclip.copy(s)
def n2():
    s=r'''
    a=4
    b=8
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
    Xq = a + 0.8 * (b - a)
    print(f(Xq))'''
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