from .SingleFormulaBasedMaterials import *

class MixFormulaBasedMaterials(SingleFormulaBasedMaterials):
            
    def __init__(self, mix=SingleFormulaBasedMaterials(unit='random').get_vox(), rule='OR', unit=None, formula=None, l=10, r=[1,1,1], a=[1,1,1], eps=0.1, res=0.1, png=True, smooth=True):
        
        super().__init__(unit, formula, l, r, a, eps, res, png, smooth)
        
        print('Initial porosity: {}'.format(self.get_porosity()))

        if rule is 'OR':
            self._vox = np.logical_or(self._vox, mix)
        elif rule is 'XOR':
            self._vox = np.logical_xor(self._vox, mix)
        elif rule is 'SUB':
            self._vox = np.logical_xor(np.logical_or(self._vox, mix), mix)
        elif rule is 'AND':
            self._vox = np.logical_and(self._vox, mix)
        else:
            raise NameError('No such rule! Only ''OR'', ''XOR'', ''SUB'' and ''AND'' are supported.')
        print('Final porosity: {}'.format(self.get_porosity()))
        self._model+='_{}'.format(rule)

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
        MixFormulaBasedMaterials(unit, l, r, eps, res, png, smooth).save2stl()

    except:
        pass