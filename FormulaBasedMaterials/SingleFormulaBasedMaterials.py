import numpy as np
import matplotlib.pyplot as plt
import os
import trimesh  
from mpl_toolkits.mplot3d import axes3d
import os, time, warnings
from skimage import measure
import random
from sympy import sympify

warnings.filterwarnings("ignore")

class SingleFormulaBasedMaterials:
            
    def __gyroid(self):
        return 'sin(x)*cos(y)+sin(y)*cos(z)+sin(z)*cos(x)'

    def __SchD(self):
        return 'sin(x)*sin(y)*sin(z)+sin(x)*cos(y)*cos(z)+cos(x)*sin(y)*cos(z)+cos(x)*cos(y)*sin(z)'

    def __randomFormulaString(self,n_terms=5):

        formula='{:.2f}'.format(random.random())

        for i in range(n_terms):
            ch_digit = '{:.2f}'.format(random.random())
            ch_X = random.choice(['sin(x)', 'cos(x)', '1'])
            ch_Y = random.choice(['sin(y)', 'cos(y)', '1'])
            ch_Z = random.choice(['sin(z)', 'cos(z)', '1'])
            formula+='+'+ch_digit+'*'+ch_X+'*'+ch_Y+'*'+ch_Z

        return formula

    def __formula_string(self):
        f = sympify(self.__formula)
        from sympy.abc import x, y, z
        from sympy.utilities.lambdify import lambdify
        f = lambdify([x,y,z], f, 'numpy')

        return f(self.__x*np.pi*2/self.__a[0],self.__y*np.pi*2/self.__a[1],self.__z*np.pi*2/self.__a[2])
    
    def __init__(self, unit=None, formula = None, l=10, r=[1,1,1], a=[1,1,1], eps=0.1, res=0.1, png=True, smooth=True):
        
        self.__l = l
        self.__r = r
        self.__a = a
        self.__eps = eps
        self.__res = res 
        self.__png = png
        self.__smooth = smooth

        if unit == 'gyroid':
            self.__formula = self.__gyroid()
        elif unit == 'SchD':
            self.__formula = self.__SchD()
        elif unit == 'random':
            self.__formula = self.__randomFormulaString()
        elif formula:
            self.__formula = formula
            unit = 'user-defined'
        else:
            raise NameError('Please input user-defined formula')
        print('Using formula:', self.__formula)
        rx,ry,rz = self.__r
        _res=int(self.__l/self.__res)
        self.__x=np.array([i for i in range(_res*rx)])
        self.__y=np.array([i for i in range(_res*ry)])
        self.__z=np.array([i for i in range(_res*rz)])

        lx=len(self.__x)
        ly=len(self.__y)
        lz=len(self.__z)
        
        if type(self.__eps)==float:
 
            self._model = unit+'_'+str(rx)+'x'+str(ry)+'x'+str(rz)+'_r'+str(round(res,2))
        elif np.sum(eps/np.max(eps)-np.ones(eps.shape))==0:

            self._model = unit+'_'+str(rx)+'x'+str(ry)+'x'+str(rz)+'_r'+str(round(res,2))
        else:
            self._model = unit+'_'+str(rx)+'x'+str(ry)+'x'+str(rz)+'_r'+str(round(res,2))+'_custom_eps'

        self.__x, self.__y, self.__z = np.meshgrid(self.__x/_res, self.__y/_res, self.__z/_res, indexing='ij')
        self._vox = self._buildvox()

        while self.get_porosity() > 0.99:
            self.__eps+=0.001
            self.update_eps(self.__eps)
            print('Finding matched material, but porosity: {} is too high. Update eps with {}'.format(self.get_porosity(), self.__eps))

    def _buildvox(self):
        return np.fabs(self.__formula_string())<=self.__eps

    def update_eps(self, eps):

        self.__eps=eps
        rx,ry,rz = self.__r
        _res=int(self.__l/self.__res)
        self.__x=np.array([i for i in range(_res*rx)])
        self.__y=np.array([i for i in range(_res*ry)])
        self.__z=np.array([i for i in range(_res*rz)])

        lx=len(self.__x)
        ly=len(self.__y)
        lz=len(self.__z)

        self.__x, self.__y, self.__z = np.meshgrid(self.__x/_res, self.__y/_res, self.__z/_res, indexing='ij')
        self._vox = self._buildvox()
        if self.get_porosity() == 0:
            raise NameError('Didn\'t find matched material with {}'.format(self.__formula))
    #======================================================================================================================

    def get_porosity(self):
        return 1-(np.sum(self._vox)/self._vox.size)
    def get_vox(self):
        return self._vox
    def get_formula(self):
        return self.__formula
    
    def save2stl(self):
            #%matplotlib inline
        os.makedirs(self._model, exist_ok=True)
        with open(self._model+"/info.txt",'w') as f:
            print('Formula: {}'.format(self.__formula), file=f)
            print('Porosity: {}'.format(self.get_porosity()), file=f)
            print('L: {}'.format(self.__l), file=f)   
            print('a: {}'.format(self.__a), file=f)
            print('eps: {}'.format(self.__eps), file=f)
        for i in range(self._vox.shape[0]):
            temp_img=self._vox[i]
            plt.imsave(self._model+'/'+str(i)+'.png', temp_img, cmap='gray')
            if self.__png:
                from IPython import display
                display.clear_output(wait=True)
                plt.imshow(temp_img, cmap='gray')    
                plt.axis('off')
                plt.title(str(i))
                plt.show()

        mesh = trimesh.voxel.ops.matrix_to_marching_cubes(self._vox, pitch=self.__res)

        if self.__smooth:
            mesh = trimesh.smoothing.filter_humphrey(mesh)

        mesh.rezero()
        mesh.export(self._model+'/'+self._model+'.stl')            
        print('save stl model to {}'.format(self._model))

if __name__=='__main__':
    
    try:
        import argparse
        parser = argparse.ArgumentParser(description='generate stl by function')
        parser.add_argument('--r', nargs=3, type=int, default=[1,1,1])
        parser.add_argument('--res', type=float, default=1.0)
        parser.add_argument('--l', type=float, default=10)
        parser.add_argument('--eps', type=float, default=0.5)
        parser.add_argument('--unit', type=str, default='gyroid')
        parser.add_argument('--smooth', type=bool, default=True)
        parser.add_argument('--png', type=bool, default=False)
        args = parser.parse_args()
    
        res=args.res # mm/pixel
        l=args.l # 1 unit => 10*10*10mm
        r=args.r # [2,7,7]
        unit=args.unit #'gyroid'
        eps=args.eps
        smooth=args.smooth
        png=args.png
        SingleFormulaBasedMaterials(unit, l, r, eps, res, png, smooth).save2stl()

    except:
        pass