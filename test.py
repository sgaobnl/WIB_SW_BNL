from ROOT import TFile, TTree, addressof
import numpy as np
from array import array

f = TFile('example.root', 'recreate')
t = TTree('mytree', 'example tree')

x = np.zeros((2,3),dtype=int)
t.Branch('myarray', addressof(x), 'myarray[2][3]/I')

nentries = 25
for i in range(nentries):
   #x = [[1+i, 2.+i, 3.+i], [4.+i, 5.+i, 6.+i]]
   x = [(1+i, 2+i, 3+i), (4+i, 5+i, 6+i)]
   #x[0] = [1+i, 2.+i, 3.+i]
   #x[1] = [4.+i, 5.+i, 6.+i]
   x = np.array(x)
   #print(x)
   t.Fill()

f.Write()
f.Close()
