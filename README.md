# FormulaBasedMaterials
Generate Formula-Based Materials into Voxel, STL files

# Usage:
import matplotlib.pyplot as plt
%matplotlib inline
import FormulaBasedMaterials as FBM

test_SingleFM=FBM.SingleFormulaBasedMaterials(formula='sin(x)*cos(y)+sin(y)*cos(z)+sin(z)*cos(x)+1', l=10, r=[1,1,1], a=[1,1,1], eps=0.2, res=0.2, png=True, smooth=True)
test_SingleFM=FBM.SingleFormulaBasedMaterials(unit='random', l=10, r=[1,1,1], a=[1,1,1], eps=0.2, res=0.2, png=True, smooth=True)
test_SingleFM=FBM.SingleFormulaBasedMaterials(unit='SchD', l=10, r=[1,1,1], a=[1,1,1], eps=0.2, res=0.2, png=True, smooth=True)
test_SingleFM=FBM.SingleFormulaBasedMaterials(unit='gyroid', l=10, r=[1,1,1], a=[1,1,1], eps=0.2, res=0.2, png=True, smooth=True)
test_SingleFM.save2stl()
