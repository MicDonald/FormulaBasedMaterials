from .SingleFormulaBasedMaterials import *

class HierarchicalFormulaBasedMaterials(SingleFormulaBasedMaterials):
            
    def __init__(self, unit=None, formula = None, l=10, r=[1,1,1], a=[1,1,1], eps=0.1, res=0.1, png=True, smooth=True):

        super().__init__(unit, formula, l, r, a, eps, res, png, smooth)
        

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
        RFBM=ReducedFormulaBasedMaterials(unit, l, r, a, eps, res, png, smooth)
        RFBM.save2stl()
    except:
        pass