import numpy as np

def read_spec ( filename ):
    with open(filename) as f:
        rec = '!'
        while rec[0] == '!': rec = f.readline()
        flds = rec.split()
        npts = abs ( int(flds[0]) )
        wno1 = float(flds[1])
        wnod = float(flds[2])
        if wnod > 0:         # regular grid
            spc = np.fromfile(f,sep=" ")
            wno = wno1 + np.arange(npts)*wnod
        else:                # irregular grid
            dat = np.fromfile(f,sep=" ").reshape(npts,2)
            wno = dat[:,0]
            spc = dat[:,1]
    return wno, spc