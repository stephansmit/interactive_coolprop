from distribution import *
import CoolProp.CoolProp as CP
from point import *
class Line(object):
    def __init(self):
        pass
    
    def plot(self,go):
        hovertext=list()
        for i, v in enumerate(self.V):
                hovertext.append('V: {:.3f} [kgm^-3]<br />P: {:.2f} [Pa]<br />T: {:.2f} [K]'
                                .format(v, self.P[i], self.T[i]))
        
        trace = go.Scatter3d(
            x=self.V,
            y=self.T,
            z=self.P,
            mode='lines',
            name = self.name,
            hoverinfo='name+text',
            hoverlabel = dict(namelength = -1),
            text=np.array(hovertext),
            line = self.linestyle 
        )
        return trace
    


        
class Isobar(Line):
    def __init__(self, fluid, P, n, linestyle=None, color="green", name=None):
        Line.__init__(self)
        V_min = fluid.trip_point.V
        V_max = 1/CP.PropsSI("D",'P', P, "T", fluid.Tmax, fluid.name)
        self.V = np.geomspace(V_min, V_max, n)
        self.P=[P for i in self.V]
        self.T=[Point(P=P,V=v, fluid=fluid).T for v in self.V]
        if name:
            self.name = name
        else:
            self.name = "Isobar at %2.1f [Bar]" % (P/1.e5)
        self.linestyle = dict(
                    color = color,
                    width = 10,
                    dash= linestyle)

class IsobarReverse(Line):
    def __init__(self, fluid, P, n, linestyle=None, color='green',name=None):
        Line.__init__(self)
        V_min = fluid.getLiquidLinePoint(fluid.trip_point.P).V
        V_max = 1/CP.PropsSI("D",'P', P, "T", fluid.Tmax, fluid.name)
        self.V = np.geomspace(V_min, V_max, n)
        self.P=[P for i in self.V]
        self.T=[Point(P=P,V=v, fluid=fluid).T for v in self.V]
        if name:
            self.name = name
        else:
            self.name = "Isobar at %2.1f [Bar]" % (P/1.e5)
            
        self.linestyle = dict(
                    color =color,
                    width = 10,
                    dash= linestyle)


class Isotherm(Line):
    def __init__(self, fluid,T, n, linestyle=None,color='orange',name=None):
        Line.__init__(self)
        P_min = fluid.trip_point.P
        P_max = fluid.Pmax
        self.P = np.geomspace(P_min, P_max, n)
        self.T=[T for i in self.P]
        self.V=[Point(T=T,P=p, fluid=fluid).V for p in self.P]
        if name:
            self.name = name
        else:
            self.name = "Isotherm at %2.1f [K]" % (T)
        self.linestyle = dict(
                    color = color,
                    width = 10,
                    dash= linestyle)


class LiquidLine(Line):
    def __init__(self,fluid, npoints):
        Line.__init__(self)
        self.P = DiscretizedLine(xmin=fluid.trip_point.P, 
                           xmax=fluid.crit_point.P, 
                           npoints=npoints, 
                           factor=2,
                           distribution='tanh', log=True).x
        pts = [fluid.getLiquidLinePoint(p) for p in self.P]
        self.V = [pt.V for pt in pts]
        self.T = [pt.T for pt in pts]
        self.name = "Liquid Saturation Curve"

        self.linestyle = dict(
                    color = 'blue',
                    width = 8,)
        
        
class VapourLine(Line):
    def __init__(self,fluid,npoints):
        Line.__init__(self)
        
        self.P = DiscretizedLine(xmin=fluid.trip_point.P, 
                       xmax=fluid.crit_point.P, 
                       npoints=npoints, 
                       factor=2,
                       distribution='tanh', log=True).x
        pts = [fluid.getVapourLinePoint(p) for p in self.P]
        self.V = [pt.V for pt in pts]
        self.T = [pt.T for pt in pts]
        self.linestyle = dict(
                    color = 'red',
                    width = 8,)
        self.name = "Vapour Saturation Curve"

        
class WidomLine(object):
    def __init__(self, fluid):
        self.fluid = fluid
        
    def initialize_line(npoints):
        self.P = DiscretizedLine(xmin=self.fluid.crit_point.P*2.0, 
               xmax=self.fluid.crit_point.P, 
               npoints=npoints, 
               factor=1,
               distribution='tanh', log=True, reverse=True).x
        self.V = []
        self.V.append(fluid.crit_point.V)
        for i, p in enumerate(self.P[1:]):
            value = minimize(self.evaluate,[self.V[i]], 
                             args =(p,),
                            method='Nelder-Mead', tol=-1000000,options={'disp': False, 'maxiter':1000})
            self.V.append(value.x[0])
        pts = [Point(V=V, P=self.P[i]) for i,V  in enumerate(self.V)]
        self.T = [pt.T for pt in pts]
    def evaluate(self,V,P):
        try:
            value = -CP.PropsSI("C","D", 1/V, "P", P, self.fluid.name)
        except:
            value =1000
        return value
    
    def evaluate_log(self,V,P):
        try:
            value = -CP.PropsSI("Z","D", 1/np.power(10,V), "P", P, self.fluid.name)
        except:
            value =1000
        return value    
    
    def get_point(self, P, fluid, v0):
        return minimize(self.evaluate,[v0], 
                             args =(P,),
                            method='Nelder-Mead', tol=-1000000,options={'disp': False, 'maxiter':5000}).x[0]
 
    

