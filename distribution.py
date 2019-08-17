import numpy as np

class Distribution(object):
    def __init__(self, npoints):
        self.i = np.linspace(0,1,npoints)
        self.dis = self.i

class TanHyperbolicDistribution(Distribution):
    def __init__(self, npoints, factor):
        Distribution.__init__(self, npoints)
        self.dis = np.tanh(factor*self.i)
        self.dis /= self.dis[-1]

        
class ArcTanDistribution(Distribution):
    def __init__(self, npoints, factor):
        Distribution.__init__(self, npoints)
        self.dis = np.arctan(2*factor*(self.i-1./2.))
        self.dis -= self.dis[0]
        self.dis /= self.dis[-1]


class DiscretizedLine(object):
    def __init__(self, xmin, xmax, npoints, factor, distribution='arctan', log=False, reverse=False):
        self.log = log
        if distribution == 'lin':
            dis = Distribution(npoints).dis
        elif distribution == 'atan':
            dis = ArcTanDistribution(npoints, factor).dis
        elif distribution == 'tanh':
            dis = TanHyperbolicDistribution(npoints,factor).dis
        else:
            raise NotImplementedError
        if not log:
            self.x = xmin + (dis)*(xmax-xmin)
        else:
            self.x = np.log10(xmin)+dis*(np.log10(xmax)-np.log10(xmin))
            self.x = np.power(10,self.x)
        if reverse:
            self.x = self.x[::-1]
            
    def append(self, discretized_line, first=True, last=True):
        tmp1 = self.x.tolist()
        tmp2 = discretized_line.x.tolist()
        if (first and last):
            tmp1.extend(tmp2)
        elif (not first and last):
            tmp1.extend(tmp2[1:])
        elif (not last and first):
            tmp1.extend(tmp2[:-1])
        elif (not first and not last):
            tmp1.extend(tmp2[1:-1])
        else:
            raise NotImplementedError
        self.x = np.array(tmp1)

    def plot(self,ax, yvalue=1, marker='x',log=False):
        ax.plot(self.x, np.ones(np.shape(self.x))*yvalue, marker=marker)
        if self.log:
            ax.set_xscale('log')
        if log:
            ax.set_yscale('log')
