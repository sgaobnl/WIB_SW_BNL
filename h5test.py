import h5py

with h5py.File("test_rms.hdf5", "r+") as f:
    #print("Keys:")
    #print(list(f.keys()))
    # try:
        # del f["rms"]
    # except:
        # raise
    # print(list(f.keys()))
    keylist = list(f.keys())
    print (list(f.keys()))
    a = f[keylist[0]]
    print (type(a))
    print (a.name)
    print (a.ndim)
    print (a.size)
    print (len(keylist))
    print (len(a))
    print (len(a[0]))
    print (len(a[0][0]))

#    print (keylist)
#    for dset in keylist:
#        print(f[dset].name)
#        print(f[dset].ndim)
#        print(f[dset].size)
#        print(f[dset].shape)
#        # print(f[dset].dtype)
#        print(f[dset])
#        print(f[dset][::])
#        #del f[dset]
        
    #print(f[keylist[0]])
    
#with h5py.File("testfile_pulser.hdf5", "r+") as f:
#    #print("Keys:")
#    #print(list(f.keys()))
#    # try:
#        # del f["rms"]
#    # except:
#        # raise
#    # print(list(f.keys()))
#    keylist = list(f.keys())
#    for dset in keylist:
#        # print(f[dset].name)
#        # print(f[dset].ndim)
#        # print(f[dset].size)
#        # print(f[dset].shape)
#        # print(f[dset].dtype)
#        print(f[dset])
#        print(f[dset][::])
#        print(f[dset][0,0,0]) #single value within a sample
#        print(f[dset][0,0]) #a single channel's sample
#        #del f[dset]
#    #print(f[keylist[0]])
