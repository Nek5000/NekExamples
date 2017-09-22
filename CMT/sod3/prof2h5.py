import numpy as np
import os
import tables

def profcat(prefix,ncol,nx1,nfiles):
   ntmp=0
   ipad=int(np.ceil(np.log10(nfiles)))
   for p in range(nfiles):
      zefile=prefix+str(p).zfill(ipad)
      if os.access(zefile,os.F_OK):
         if (os.stat(zefile).st_size>0):
            tmp=np.loadtxt(zefile)
            ntmp=ntmp+1
            if ntmp==1:
               fullprof=tmp
            else:
               fullprof=np.vstack((fullprof,tmp))
   fullprof=fullprof.reshape((-1,nx1,ncol))
   vertices=fullprof[:,0,0]
   fullprof=fullprof[vertices.argsort(),:,:].reshape((-1,ncol))
   return fullprof

Np=9
numtasks=8

fid=tables.open_file("prof10001.h5",'w')
profiles=fid.create_group('/','profiles')
profiles._v_attrs.nx1=Np
profiles._v_attrs.dt=2.0e-5
profiles._v_attrs.time=0.2
profiles._v_attrs.eos="CPG"
profiles._v_attrs.case="Sod"
profiles._v_attrs.gamma=1.4
profiles._v_attrs.rgas=1.0


cmtdata=fid.create_group(profiles,'cmt')
cmtdata._v_attrs.isc=0.75
cmtdata._v_attrs.cmax=0.3
cmtdata._v_attrs.ce=40.0
cmtdata._v_attrs.nxd=12

exact=fid.create_group(profiles,'exact')
exact._v_attrs.solver="e1rpex"

tmp=profcat('profiles/uprof10001p',3,Np,numtasks)

x=tmp[:,0]
fid.create_array('/','x',x)

fid.create_array(cmtdata,'u',tmp[:,1])
fid.create_array(exact,'u',tmp[:,-1])

tmp=profcat('profiles/Tprof10001p',3,Np,numtasks)
print np.amax(x-tmp[:,0])
fid.create_array(cmtdata,'T',tmp[:,1])
fid.create_array(exact,'T',tmp[:,-1])

tmp=profcat('profiles/rhoprof10001p',3,Np,numtasks)
print np.amax(x-tmp[:,0])
fid.create_array(cmtdata,'d',tmp[:,1])
fid.create_array(exact,'d',tmp[:,-1])

tmp=profcat('profiles/viscprof10001p',4,Np,numtasks)
print np.amax(x-tmp[:,0])
fid.create_array(cmtdata,'artdiff',tmp[:,1])
fid.create_array(cmtdata,'mumax',tmp[:,2])
fid.create_array(cmtdata,'resid',tmp[:,-1])

fid.close()
