import CoolProp.CoolProp as CP
import numpy as np

class Point(object):
    def __init__(self, fluid, T=None, V=None, P=None, Q=None):
        if (not P and not Q) and (T and V):
            self.T = T
            self.V = V
            self.P = CP.PropsSI("P", "T", T, "D",1/V, fluid.name)
            self.D = 1.0/self.V

        elif (not T and not Q) and (P and V):
            self.P = P
            self.V = V
            self.D = 1/self.V
            self.T = CP.PropsSI("T", "P", P, "D", self.D, fluid.name)       
            self.C = CP.PropsSI("C", "P", P, "D", self.D, fluid.name)
            self.Phase = CP.PropsSI("Phase", "P", P, "D", self.D, fluid.name)
            if self.Phase == CP.get_phase_index('phase_twophase'):
                self.Q = CP.PropsSI("Q", "P", P, "D", self.D, fluid.name)
                self.Z = np.nan
            elif self.Phase == CP.get_phase_index('phase_liquid'):
                self.Q = 0
                self.Z = CP.PropsSI("Z", "P", P, "D", self.D, fluid.name)

            elif self.Phase == CP.get_phase_index('phase_supercritical_gas'):
                self.Q = 1
                self.Z = CP.PropsSI("Z", "P", P, "D", self.D, fluid.name)

            elif self.Phase == CP.get_phase_index('phase_gas'):
                self.Q = 1
                self.Z = CP.PropsSI("Z", "P", P, "D", self.D, fluid.name)

            elif self.Phase == CP.get_phase_index('phase_supercritical'):
                self.Q = 1
                self.Z = CP.PropsSI("Z", "P", P, "D", self.D, fluid.name)
            elif self.Phase == CP.get_phase_index('phase_supercritical_liquid'):
                self.Q = 0
                self.Z = CP.PropsSI("Z", "P", P, "D", self.D, fluid.name)

            else:
                raise NotImplementedError
            self.H = CP.PropsSI("H", "P", P, "D", self.D, fluid.name)
            self.S = CP.PropsSI("S", "P", P, "D", self.D, fluid.name)

        elif (V is None and Q is None) and (P and T):
            self.P = P
            self.T = T
            self.D = CP.PropsSI("D", "P", P, "T",T, fluid.name)
            self.V = 1./self.D
        

        elif (not V and not T) and (P and (Q is not None)):            
            self.P = P
            self.T = CP.PropsSI("T", "P", P, "Q", Q, fluid.name)
            self.D = CP.PropsSI("D", "P", P, "Q", Q, fluid.name)
            self.V = 1./self.D
        else:
            raise NotImplementedError
            

    def plot(self, go):

        hovertext='v : {:.3f} [kgm^-3]<br />P: {:.2f} [Pa]<br />T: {:.2f} [K]'.format(self.V, self.P,self.T)
        
        trace = go.Scatter3d(
            x=[self.V],  
            y=[self.T],  
            z=[self.P],  
            name=self.name,
            mode='markers',
            marker = self.markerstyle,
            hoverinfo='name+text',
            hoverlabel = dict(namelength = -1),
            
            text=[hovertext]
        )
        return trace
        
class TriplePoint(Point):
    def __init__(self, fluid):
        self.T = CP.PropsSI("T_TRIPLE", fluid.name)
        self.P = CP.PropsSI("P_TRIPLE", fluid.name)
        try:
            self.D = CP.PropsSI("D", "P",self.P+0.01,"T", self.T,fluid.name)
        except:
            try:
                self.D = CP.PropsSI("D", "P",self.P,"T", self.T+1e-5,fluid.name)
            except:
                self.D = CP.PropsSI("D", "P",self.P*1.01,"T", self.T+0.1,fluid.name)
        self.V = 1./self.D
        self.markerstyle =  dict( size=6, color='darkblue')
        self.name = "Triple Point"
        
class CriticalPoint(Point):
    def __init__(self, fluid):
        self.T = CP.PropsSI("T_CRITICAL", fluid.name)
        self.P = CP.PropsSI("P_CRITICAL", fluid.name)
        self.D = CP.PropsSI("D","P",self.P, "T", self.T, fluid.name)
        self.V = 1.0/self.D
        self.markerstyle =  dict( size=6, color='green')
        self.name = "Critical Point"
        
