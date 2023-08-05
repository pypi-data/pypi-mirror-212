import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

class Julia:
    def __init__(self,expr):
        self.z = sp.symbols('z')
        self.expr = expr
        self.eval = sp.lambdify(self.z,expr)
        self.fixed_points = [complex(float(sp.re(i)),float(sp.im(i))) for i in sp.solve(expr-self.z,self.z)]
        self.critical_points = [complex(float(sp.re(i)),float(sp.im(i))) for i in sp.solve(expr.diff(),self.z)]

    def grid(a,b,c,d,resx,resy):
        xvals = np.linspace(a,b,resx)
        yvals = np.linspace(c,d,resy)
        points = []
        for i in yvals:
            for j in xvals:
                points.append(complex(j,i))
        return(points)
    
    def orbit(self,seed,depth,bail_out):
        o = [seed]
        for i in range(depth):
            try:
                z = self.eval(o[-1])
                if abs(z)<bail_out:
                    o.append(z)
                else:
                    break
            except Exception:
                pass
        return(o)
    
    def plot(self,a=-1,b=1,c=-1,d=1,resx=300,resy=300,depth=25,bail_out=1000,filled=True,glow=0,cmap='binary',
             scale=1,grid=True,critical_orbit_depth=0,fixed_points=True,
             cols=[(61, 64, 91),(244, 241, 222), (224, 122, 95),(129, 178, 154),(242, 204, 143)]):
        def plot_orbit(orb):
            orb_mod = [[(orb[i].real+b)*(resx/(b-a)),(orb[i].imag+d)*(resy/(d-c))] for i in range(len(orb))]
            for i in range(len(orb_mod)-1):
                ax.add_artist(ConnectionPatch(orb_mod[i],orb_mod[i+1],"data","data",arrowstyle="->"))
        def find_nearest(arr, z):
            arr = np.asarray(arr)
            idx = (np.abs(arr - z)).argmin()
            return(arr[idx])
        points = Julia.grid(a,b,c,d,resx,resy)
        if filled:
            ol = []
            cfp = []
            for i in points:
                o = self.orbit(i,depth,bail_out)
                ol.append(len(o))
                can = find_nearest(self.fixed_points,o[-1])
                if (self.expr.limit(self.z,sp.oo)!=sp.oo) or (self.expr.limit(self.z,sp.oo)==sp.oo and np.abs(can-o[-1])<1):
                    cfp.append(can)
                else:
                    cfp.append(np.inf)
            if self.expr.limit(self.z,sp.oo)==sp.oo:
                self.fixed_points.insert(0, np.inf)
            colors = [ (int(cols[self.fixed_points.index(cfp[i])][0]+(ol[i]*glow*0.299)),
                        int(cols[self.fixed_points.index(cfp[i])][1]+(ol[i]*glow*0.587)),
                        int(cols[self.fixed_points.index(cfp[i])][2]+(ol[i]*glow*0.114) )) for i in range(len(points)) ]
            colors = np.asarray(colors).reshape(resy,resx,-1)
            ydim,xdim = colors.shape[:2]
            plt.imshow(colors,aspect=(d-c)/(b-a))
        else:
            colors = []
            for i in points:
                colors.append(len(self.orbit(i,depth,bail_out)))
            colors = np.asarray(colors).reshape(resy,resx)
            ydim,xdim = colors.shape[:2]
            plt.imshow(colors,aspect=(d-c)/(b-a),cmap=cmap)
            
        ax = plt.gca()
        ax.set_xlim(0,xdim)
        ax.set_ylim(0,ydim)
        ax.set_yticks([0,ydim/2,ydim])
        ax.set_yticklabels([c, (d+c)/2, d])
        ax.set_xticks([0,xdim/2,xdim])
        supress = ax.set_xticklabels([a, (a+b)/2, b])
        fig = plt.gcf()
        fig.set_figheight( scale*10 )
        fig.set_figwidth( scale*10 )
        if grid:
            pass
        else:
            plt.axis('off')
        if critical_orbit_depth<=0:
            pass
        elif critical_orbit_depth==1:
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in self.critical_points],[(z.imag+d)*(resy/(d-c)) for z in self.critical_points],c='Black')
        else:
            orbs = [self.orbit(self.critical_points[i],critical_orbit_depth,1000) for i in range(len(self.critical_points))]
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in self.critical_points],[(z.imag+d)*(resy/(d-c)) for z in self.critical_points],c='Black')
            [plot_orbit(orbs[i]) for i in range(len(orbs))]
        if fixed_points == True:
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in self.fixed_points],[(z.imag+d)*(resy/(d-c)) for z in self.fixed_points],c='Black',marker='x')
