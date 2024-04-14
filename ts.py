import numpy as np
import yfinance as yf # now irrelivent and will be pruned
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools
class ts():
    def __init__(self,raw):
        self.raw = raw
        self.data = np.array(raw)
        self.acfr =[]
        self.acfData =[]
        self.pacfr =[]
        self.pacfData=[]
        self.model = [0,0]
        self.consts = [0.45,0.25,0.15,0.6]
        
        
    ###DATA FEAUTRES
    def ACF(self,k): #sample acf calculated
        d = self.acfData
        mea = d.mean()
        b= 0
        for i in range(len(d)-1): #maybe another -1
            b+=(d[i]-mea)**2
        u=0  
        for i in range(len(d)-k-1): #maybe another -1
            u+=(d[i+k]-mea) * (d[i]-mea)
        return u/b
    

    def PACF(self,k): ##using k for kk rather than considering different pairs
        return statsmodels.tsa.stattools.pacf(self.pacfData,k,method="ols")
        
    #    return
    
    ####Transformations
    
    
    ###MODELS --- models initatlise the variables to then be optimised to create a good forecasting system
    def MA(self,a,l):
        noise = [10,10]
        x=0
        c=self.consts
        for i in range(l):
            x=0
            noise.append(np.random.normal())
            for j in range(a):
                x+=noise[i-j-1]*c[j]
                print(c[j])
            x+= np.random.normal()
            self.model.append(x)
        
        plt.plot(self.model)
        plt.show()
        self.data = np.array(self.model)
        self.display()
        return
    
    def AR(self,a,l):
        x=0
        c=self.consts
        for i in range(l):
            x=0
            for j in range(a):
                x+=self.model[i-j]*c[j] #-1 for AR to not get self then first value is counted
                print(c[j])
            x+= np.random.normal()
            self.model.append(x)
        
        plt.plot(self.model)
        plt.show()
        self.data = np.array(self.model)
        self.display()
        return
    
    def ARMA(self,a,b,l):
        noise = [0]
        x=0
        c=[0.2,0.4]
        k =[0.6,-0.2,-0.5]
        for i in range(l):
            x=0
            noise.append(np.random.normal())
            for j in range(b-1):
                x+=noise[i-j-1]*c[j]
            for j in range(a-1):
                x+=self.model[i-j-1]*k[j] 
            x+= np.random.normal()
            self.model.append(x)
        
        plt.plot(self.model)
        plt.show()
        self.data = np.array(self.model)
        self.display()
        return
    
    def ARIMA(self,a,b,c):
        return
    
    def SARIMA(self,a,b):
        return
    
    def error(self):
        m = self.model
        d = self.raw
        r = len(m)-2
        err = 0
        for i in range(r):
            err+=d[-abs(i-r)] - m[-abs(i-r)]
        return err
    
    def optModel(self):
        vals=[]
        for i in range(1000):
            for j in [1,-1]:
                self.consts[0] = np.random.uniform()
                self.AR(1, 100)
                vals.append([self.consts[0],self.error()])
        print(vals)
        return
    
    
    ####PLOTS
    def fillACF(self):
        r = []
        self.acfData = self.data
        for i in range(20):
            r.append(self.ACF(i+1))
        self.acfr = r
        return
    
    def fillPACF(self):
        self.pacfData = self.data
        self.pacfr = self.PACF(20)
        return
    
    def plotACF(self): 
        end=range(len(self.acfr))
        plt.bar(end,self.acfr,)
        plt.ylim(-1,1)
        plt.ylabel("ACF")
        plt.xlabel("k")
        plt.show()
        return
    
    def plotPACF(self):
        end=range(len(self.pacfr))
        plt.bar(end,self.pacfr,)
        plt.ylabel("PACF")
        plt.xlabel("k")
        plt.show()
        
    def display(self):
        plt.plot(self.data)
        plt.show()
        self.fillACF()
        self.plotACF()
        self.fillPACF()
        self.plotPACF()

d = yf.download("AAPL",start="2010-01-01",end="2020-01-01",interval="1d")
df = d["Close"]

# data from https://www.statista.com/statistics/584914/monthly-rainfall-in-uk/
rainfall = [187,167.80,
79.80,
67.50,
99.40,
54.50,
64.30,
137.90,
22.50,
157.40,
123.30,
131.40,
153.50,
79.90,
94.90,
45.50,
56.20,
107.60,
104.70,
52.10,
72.10,
172,
216.90,
178.70,
110.10,
83.80,
77.30,
61.40,
96.10,
78.50,
85.10,
96.30,
47,
104.90,
77.30,
76,
93.40,
97.70,
33.20,
57.20,
110.40,
101.30,
102.30,
117.20,
101.40,
107.70,
120.60,
132.40,
68.60,
103.90,
83.90,
47.70,
34.70,
54.20,
83,
101.40,
104.20,
121.70,
117.70,
64.60,
71.10,
128.90,
48.60,
63.60,
109,
89.10,
132.60,
126.10,
139.80,
119.10,
139.60,
121.30,
213.70,
78.50,
30,
32.80,
107.60,
96,
122.20,
77.40,
182.70,
104.90,
167,
139.60,
105.40,
87,
20.50,
121,
44.70,
74.50,
66.60,
82.30,
167.80,
80.60,
114.20,
62.90,
151.30,
50.70,
49.80,
77.50,
61.80,
48.40,
51.90,
105.20,
147.50,
167.20,
116,
125.70,
43.40,
132,
69.80,
39.10,
52.20,
140.10,
89.10,
119.40,
171.50,
118.90,
188.60,
]
#data from https://www.statista.com/statistics/1299082/northern-hemisphere-sea-ice-extent/
ice = [[
14.86,
15.96,
16.04,
15.43,
13.79,
12.21,
10.10,
7.98,
7.67,
9.18,
11.38,
13.59,
],[
14.73,
15.47,
15.89,
15.36,
14.07,
12.22,
9.74,
7.40,
6.70,
8.55,
11.03,
13.05,
],[
14.78,
15.58,
15.87,
14.65,
13.23,
11.64,
9.25,
6.80,
6.14,
8.49,
11.08,
13.11,
],[
14.59,
15.23,
15.26,
14.45,
12.97,
11.44,
8.99,
6.74,
6.08,
7.83,
10.76,
12.92,
],[
14.22,
15.14,
15.23,
14.56,
13.15,
11.67,
9.51,
7.17,
6.25,
8.38,
10.32,
12.64,
],[
13.66,
14.37,
14.69,
14.09,
12.91,
11.16,
8.65,
6.30,
5.50,
7.35,
10.22,
12.23,
],[
13.74,
14.58,
15.14,
14.66,
12.87,
10.59,
8.08,
5.88,
4.87,
6.98,
9.61,
11.83,
],[
13.60,
14.40,
14.37,
13.89,
12.47,
10.88,
8.38,
5.60,
4.62,
6.97,
9.85,
12.05,
],[
13.64,
14.64,
14.73,
13.62,
12.34,
10.59,
7.29,
5.07,
4,
5.33,
8.99,
11.73,
]]

x=[]
var= ts(rainfall)
var.optModel()
#var.display()
#var.MA(2,100)
#var.AR(2,100)
#var.ARMA(3,2,100)
#for i in ice:
#    for j in i:
#        x.append(j)
#var = ts(x)
#var.display()
#d=[]
#for i in range(len(df)-1):
#    d.append(df[i+1] - df[i])
#var= ts(d)
#var.display()