from distribution import *
from point import *
class Surface(object):
    def __init__(self,fluid):
        self.fluid = fluid      
        
    def set_points(self):
        self.pts = [[Point(P=p, 
                           V=self.V[i][j],
                           fluid=self.fluid) for j, p in enumerate(P)] 
                    for i, P in enumerate(self.P)]
        self.T = [[j.T for j in i] for i in self.pts]
        self.Phase = [[j.Phase for j in i] for i in self.pts]
        self.Q = [[j.Q for j in i] for i in self.pts]
        self.Z = [[j.Z for j in i] for i in self.pts]
        self.S = [[j.S for j in i] for i in self.pts]
        self.H = [[j.H for j in i] for i in self.pts]
        self.Z = [[j.Z for j in i] for i in self.pts]
    
    def plot(self,go, variable,title):
        hovertext = list()
        for xi, xx in enumerate(self.P):
            hovertext.append(list())
            for yi, yy in enumerate(xx):
                hovertext[-1].append('v: {:.3f} [kgm^-3]<br />P: {:.2f} [Pa]<br />T: {:.2f} [K]'.format(self.V[xi][yi], self.P[xi][yi], self.T[xi][yi]))
        
        if variable in ['S','H']:
            scale =1e-3
        elif variable == 'P':
            scale=1e-5
        else:
            scale =1.
        if variable != "P":
            data = [[j*scale for j in i] for i in self.__getattribute__(variable)]
        else:
            data = [[np.log(j*scale) for j in i] for i in self.__getattribute__(variable)]
        trace = go.Surface(
            x=self.V, 
            y=self.T, 
            z=self.P,
            hidesurface=False,
	    contours=go.surface.Contours(
            	z=go.surface.contours.Z(
              	show=True,
	        usecolormap=False,
        	highlightcolor="darkblue",
              	project=dict(z=True)),
            	y=go.surface.contours.Y(
              	show=True,
	        usecolormap=False,
        	highlightcolor="darkgreen",
              	project=dict(y=True)),
                ),
            colorscale= 'Jet',
            surfacecolor=data,
            hoverinfo="text",
            colorbar =dict(title = title),
            text=np.array(hovertext),
            )
        return trace

class AllPhaseSurface(Surface):
    def __init__(self, fluid, npointsP1,npointsP2, npointsV1, npointsV2, npointsV3):
        Surface.__init__(self,fluid)
        self.P_dis = self.get_pressure_discretization( npointsP1, npointsP2)
        self.construct_grid(npointsV1, npointsV2, npointsV3)
        self.set_points()
    
    def construct_grid(self, npointsV1, npointsV2, npointsV3):
        self.P = []
        self.V = []
        for p in self.P_dis:
            if p < self.fluid.crit_point.P:
                v1 = DiscretizedLine(xmin=self.fluid.trip_point.V, 
                                           xmax=self.fluid.getLiquidLinePoint(p).V, 
                                           npoints=npointsV1, 
                                           factor=1,
                                           distribution='tanh', log=True)

                v2 =  DiscretizedLine(xmin=self.fluid.getLiquidLinePoint(p).V, 
                                           xmax=self.fluid.getVapourLinePoint(p).V, 
                                           npoints=npointsV2, 
                                           factor=4,
                                           distribution='atan', log=True)

                v3 =  DiscretizedLine(xmax=self.fluid.getVapourLinePoint(p).V,
                                           xmin = Point(P=p, T=self.fluid.Tmax, fluid=self.fluid).V,  
                                           npoints=npointsV3, 
                                           factor=1,
                                           distribution='tanh', log=True, reverse=True)

                v1.append(v2, last=False, first=False)
                v1.append(v3, last=True, first=True)

            else:
                v1 = DiscretizedLine(xmin=self.fluid.trip_point.V, 
                               xmax= Point(P=p, T=self.fluid.Tmax, fluid=self.fluid).V, 
                                   npoints=npointsV1+npointsV2+npointsV3-2, 
                                   factor=1,
                                   distribution='atan', log=True,reverse=False)

            tmpP = [p for v in v1.x ]
            tmpV = v1.x.tolist()
            if abs(p-self.fluid.crit_point.P)>=1e-8:
                self.P.append(tmpP)
                self.V.append(tmpV)
        
        
    def get_pressure_discretization(self, npointsP1, npointsP2):
        pressure1 = DiscretizedLine(xmin=self.fluid.trip_point.P, 
                                   xmax=self.fluid.crit_point.P*0.99999, 
                                   npoints=npointsP1, 
                                   factor=3,
                                   distribution='tanh', log=True)
        pressure2 = DiscretizedLine(xmin=self.fluid.Pmax, 
                           xmax= self.fluid.crit_point.P*1.00001, 
                           npoints=npointsP2, 
                           factor=3,
                           distribution='tanh', log=True, reverse=True)

        pressure1.append(pressure2, first=False, last=True)
        return pressure1.x
    
    
class AllPhaseSurfaceReverse(AllPhaseSurface):
    def __init__(self, fluid, npointsP1,npointsP2, npointsV1, npointsV2, npointsV3):
        AllPhaseSurface.__init__(self, fluid, npointsP1,npointsP2, npointsV1, npointsV2, npointsV3)
    
    
    def construct_grid(self, npointsV1, npointsV2, npointsV3):
        self.P = []
        self.V = []
        for p in self.P_dis:
            if p < self.fluid.crit_point.P:
                v1 = DiscretizedLine(xmin=self.fluid.getLiquidLinePoint(self.fluid.trip_point.P).V, 
                                           xmax=self.fluid.getLiquidLinePoint(p).V, 
                                           npoints=npointsV1, 
                                           factor=1,
                                           distribution='tanh', log=True)

                v2 =  DiscretizedLine(xmin=self.fluid.getLiquidLinePoint(p).V, 
                                           xmax=self.fluid.getVapourLinePoint(p).V, 
                                           npoints=npointsV2, 
                                           factor=4,
                                           distribution='atan', log=True)

                v3 =  DiscretizedLine(xmax=self.fluid.getVapourLinePoint(p).V,
                                           xmin = Point(P=p, T=self.fluid.Tmax, fluid=self.fluid).V,  
                                           npoints=npointsV3, 
                                           factor=1,
                                           distribution='tanh', log=True, reverse=True)

                v1.append(v2, last=False, first=False)
                v1.append(v3, last=True, first=True)

            else:
                v1 = DiscretizedLine(xmin=self.fluid.getLiquidLinePoint(self.fluid.trip_point.P).V, 
                               xmax= Point(P=p, T=self.fluid.Tmax, fluid=self.fluid).V, 
                                   npoints=npointsV1+npointsV2+npointsV3-2, 
                                   factor=1,
                                   distribution='atan', log=True,reverse=False)
                
            tmpP = [p for v in v1.x ]
            tmpV = v1.x.tolist()
            if abs(p-self.fluid.crit_point.P)>=1e-8:
                self.P.append(tmpP)
                self.V.append(tmpV)
    def get_pressure_discretization(self, npointsP1, npointsP2):
        pressure1 = DiscretizedLine(xmin=self.fluid.trip_point.P, 
                                   xmax=self.fluid.crit_point.P*0.99999, 
                                   npoints=npointsP1, 
                                   factor=3,
                                   distribution='tanh', log=True)
        pressure2 = DiscretizedLine(xmin=self.fluid.Pmax, 
                           xmax= self.fluid.crit_point.P*1.00001, 
                           npoints=npointsP2, 
                           factor=3,
                           distribution='tanh', log=True, reverse=True)

        pressure1.append(pressure2, first=False, last=True)
        return pressure1.x
      


            
class TwoPhaseSurface(Surface):
    def __init__(self, fluid, npointsP, npointsV):
        Surface.__init__(self,fluid)
        self.P_dis = self.get_pressure_discretization(npointsP)
        self.construct_grid(npointsV)
        self.set_points()
    
    def construct_grid(self, npointsV):
        vmax = self.fluid.getVapourLinePoint(P=self.fluid.trip_point.P).V
        self.P = []
        self.V = []
        for p in self.P_dis:
            v =  DiscretizedLine(xmin=self.fluid.getLiquidLinePoint(p).V, 
                                       xmax=self.fluid.getVapourLinePoint(p).V, 
                                       npoints=npointsV, 
                                       factor=3,
                                       distribution='atan', log=True)

            tmpP = [p for v in v.x ]
            tmpV = v.x.tolist()
            tmpP.reverse()
            tmpV.reverse()
            self.P.append(tmpP)
            self.V.append(tmpV)
        
        
    def get_pressure_discretization(self, npointsP):
        pressure1 = DiscretizedLine(xmin=self.fluid.trip_point.P, 
                                   xmax=self.fluid.crit_point.P, 
                                   npoints=npointsP, 
                                   factor=3,
                                   distribution='tanh', log=True)
        return pressure1.x

