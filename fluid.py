from point import *
from line import *
from distribution import *
from surface import *
class Fluid(object):
    def __init__(self,name):
        self.name = name
        self.trip_point = self.getTriplePoint()
        self.crit_point = self.getCriticalPoint()
        self.Tmax = self.crit_point.T*1.2
        self.Pmax = self.crit_point.P*10

        self.ll = self.getLiquidLine(100)
        self.vl = self.getVapourLine(100)
        self.ps = self.getPhaseSurface()
        
        
        p = np.power(10,
                      1./3.*(np.log10(self.crit_point.P)-np.log10(self.trip_point.P))+
                      np.log10(self.trip_point.P))
        self.ib1 = self.getIsoBar(P=p, linestyle=None,color='black')


        p = np.power(10,
                      2./3.*(np.log10(self.crit_point.P)-np.log10(self.trip_point.P))+
                      np.log10(self.trip_point.P))
        self.ib2 = self.getIsoBar(P=p, linestyle=None,color='black')
        
        
        self.cib = self.getIsoBar(P=self.crit_point.P*1.00001, 
                      linestyle=None,color='black',
                  name = "Critical Isobar at %2.1f [Bar]" % (self.crit_point.P/1e5))
        
        
        self.ib3 = self.getIsoBar(P=self.crit_point.P*2.,linestyle=None,color='black')



        self.it1 = self.getIsoTherm(T=1./3.*(self.crit_point.T-self.trip_point.T)+self.trip_point.T, 
                                    linestyle='dash')
        self.it2 = self.getIsoTherm(T=2./3.*(self.crit_point.T-self.trip_point.T)+self.trip_point.T,
                                       linestyle='dot')
        self.cit = self.getIsoTherm(T=self.crit_point.T*1.00001, 
                                    linestyle='dash',color='white',
                                    name = "Critical Isotherm at %2.1f [K]" % (self.crit_point.T))
        
        self.it2 = self.getIsoTherm(T=4./3.*(self.crit_point.T-self.trip_point.T)+self.trip_point.T,
                                       linestyle=None)

    
    def getPhaseSurface(self):
        if self.trip_point.V > self.crit_point.V:
            return AllPhaseSurfaceReverse(self, 50,10,20,21, 40)
        else:
            return AllPhaseSurface(self, 50,10,20,21, 40)
    
    
    def getIsoBar(self,P, linestyle,color='green',name=None):
        if self.trip_point.V > self.crit_point.V:
            return IsobarReverse(fluid=self,linestyle=linestyle,color=color,P=P, n=100,name=name )
        else:
            return IsobarReverse(fluid=self,linestyle=linestyle,color=color,P=P, n=100,name=name )
    
    def getIsoTherm(self,T,linestyle,color='orange',name=None):
        return Isotherm(fluid=self, linestyle=linestyle,color=color, T=T, n=100, name=name)
            
    def getPoint(self,T=None,V=None, P=None):
        return Point(self, T=T,V=V, P=P)
    
    def getLiquidLinePoint(self, P):
        return Point(self, P=P, Q=0.0)
    
    def getVapourLinePoint(self, P):
        return Point(self, P=P, Q=1.0)
    
    def getCriticalPoint(self):
        return CriticalPoint(self)
    
    def getTriplePoint(self):
        return  TriplePoint(self)
    
    def getLiquidLine(self, npoints):
        return LiquidLine(self, npoints)
    
    def getVapourLine(self,npoints):
        return VapourLine(self, npoints)    
    
    def getWidomLine(self):
        return WidomLine(self)
    
    
    def getPhaseData(self,go):
        return [    self.trip_point.plot(go),
                    self.crit_point.plot(go),
                    self.ll.plot(go),
                    self.vl.plot(go)
                    ]
                    #self.ib1.plot(go),
                    #self.ib2.plot(go),
                    #self.cib.plot(go),
                    #self.ib3.plot(go),
                    #self.it1.plot(go),
                    #self.it2.plot(go),
                    #self.cit.plot(go)]
    
    def getSurfaceData(self,go, variable):
        if variable == "S":
            return self.ps.plot(go,'S', "Entropy [KJ/kgK]")
        elif variable == "H":
            return self.ps.plot(go,'H', "Enthalpy [KJ/kg]")
        elif variable == "Q":
            return self.ps.plot(go,'Q', "Vapour Fraction [-]")
        elif variable == "Z":
            return self.ps.plot(go,'Z', "Compressibility Factor [-]")
        elif variable == "P":
            return self.ps.plot(go,'P', "Log Pressure [bar]")
        
        
    def getData(self,go):
        entry = dict()
        entry['phase'] = self.getPhaseData(go)
        entry['surface'] = {"Q":self.getSurfaceData(go,"Q"),
                        "H":self.getSurfaceData(go,"H"),
                        "S":self.getSurfaceData(go,"S"),
                        "Z":self.getSurfaceData(go,"Z"),
                        "P":self.getSurfaceData(go,"P"),
                        }
        return entry
