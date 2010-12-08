#! /usr/bin/python
# Python module to run top-down tests for Nek

import sys
import os

###############################################################################################
def Test(name, logfile,listOfValue)  :
    """A Test function which look in the log file and compare the value to the target value 

        --Variable :
            name (string): name of the test
            logfile (string) : path of the log file
            listOfValue (list) : list of the different ['name',target,tolerance] we want to check
         --Function :
           Test will read the logfile and for all the set of ['name',target,tolerance,position] in listOfValue
           will catch the value of 'name', compare it to target according to tolerance and return
           success or failure.
           Position is the number of the row (starting from the right in which the information is."""
           
    global num_test
    global num_success
    
    test_result = False
    numTest = len(listOfValue)                             #Number of tests to do
    success = 0
    num_test += numTest
    #Test that the input file are here       
    try :
        olog = open(logfile, 'r')
        olog.close()
        inputisgood = True
    except IOError :
        print("[%s]...Sorry, I must skip this test."%name)
        print("[%s]...The logfile is missing or doesn't have the correct name..."%name)
        inputisgood = False

    #If we could find the log file, then we run the test    
    if inputisgood :        
        log = open(logfile,'r')
        for line in log :                                               #we read the log file line by line  
            for set in listOfValue :                                    #for each line we loof if the value we want are there
                if set[0] in line :                                     #set[0] is the name of the value
                    testvalue = float(line.split()[-set[3]])                 #the value is on the set[3]th column from the right of the line 
                    print("[%s] %s : %s"%(name,set[0],testvalue))
                    if (abs(testvalue - set[1]) < set[2]) :             #set[1] is the target value / set[2] is the tolerance
                        success += 1
                        num_success +=1
                    listOfValue.remove(set)                             #The value was found so we remove it from the search
        log.close()
    if success == numTest :
        test_result = True
    elif (len(listOfValue) > 0) :
        print("[%s]...I couldn't find all the requested value in the log file..."%name)
        slist = ""
        for set in listOfValue :
            slist = slist + set[0] + ", "
        print("[%s]...%s were not found..."%(name,slist))

    return test_result
    
###############################################################################################
def Run(name, logfile,listOfValue)  :
    """A Run function which runs the test and prints out the result
        --Variable :
            name (string): name of the test
            logfile (string) : path of the log file
            listOfValue (list) : list of the different ['name',target,tolerance] we want to check"""
           
    Result = Test(name,logfile, listOfValue)   
    if Result :
        print("%s : ."%name)
    else :
        print("%s : F "%name)
###############################################################################################
def FindPhrase(name, logfile, keyword) :
    """A  Test to search the logfile for a specific word or phrase
        --Variable :
            name (string): name of the test
            logfile (string): path of the logfile
            keyword (string): word or phrase searching for
        --Function :
            Tests to find a phrase or word in the logfile"""

    global num_test
    global num_success

    num_test += 1
    result    = False

    #Test that the input file is here
    try :
        olog = open(logfile, 'r')
        olog.close()
        inputisgood = True
    except IOError :
        print("[%s]...Sorry, I must skip this test."%name)
        print("[%s]...The logfile is missing or doesn't have the correct name..."%name)
        inputisgood = False

    #If we could find the log file, then we run the test
    if inputisgood :
        openlog  = open(logfile,'r')
        for line in openlog :
            if keyword in line :
                num_success += 1
                result       = True
                print("[%s] : %s"%(name,keyword))
        openlog.close()

        if result :
            print("%s : ."%name)                 #prints the result
        else :
            print("[%s]...I couldn't find '%s' in the logfile..."%(name,keyword))
            print("%s : F "%name)

    return result
###############################################################################################
def DFdPhrase(name, logfile, keyword) :
    """A  Test to search the logfile for a specific word or phrase, returns True, if not found
        --Variable :
            name (string): name of the test
            logfile (string): path of the logfile
            keyword (string): word or phrase searching for
        --Function :
            Tests to find that a phrase or word is not the logfile"""

    global num_test
    global num_success

    num_test += 1
    result    = False

    #Test that the input file is here
    try :
        olog = open(logfile, 'r')
        olog.close()
        inputisgood = True
    except IOError :
        print("[%s]...Sorry, I must skip this test."%name)
        print("[%s]...The logfile is missing or doesn't have the correct name..."%name)
        inputisgood = False

    #If we could find the log file, then we run the test
    if inputisgood :
        openlog  = open(logfile,'r')
        for line in openlog :
            if keyword in line :
                result       = True
                print("[%s] : %s"%(name,keyword))
        openlog.close()

        if result :
            print("%s : F"%name)                 #prints the result
        else :
            num_success += 1
            print("%s : . "%name)

    return result
###############################################################################################
num_test = 0 
num_success = 0
print("Beginning of top-down testing\n\n")
print("    . : successful test, F : failed test\n\n")
###############################################################################################
#---------------------Tools-------------------------------------------------------
#---------------------Tests-----------------------------------------------------
print("\nBEGIN TESTING TOOLS")  
#PGI Compiler
log = "./pgitools.out"
value = "Error "
DFdPhrase("Tools/PGI",log,value)

#GNU Compiler
log = "./gnutools.out"
value = "Error "
DFdPhrase("Tools/GNU",log,value)

#INT Compiler
log = "./inttools.out"
value = "Error "
DFdPhrase("Tools/INT",log,value)
###############################################################################################
#---------------------MPI-------------------------------------------------------
#---------------------Pn-Pn-----------------------------------------------------
print("\nBEGIN Pn-Pn TESTING")  
#Test0001 
log = "./mpiLog/test0001.log.1"
value = [['total solver time',0.01,400,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/MPI: Serial",log,value)

log = "./mpiLog/test0001.log.4"
value = [['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/MPI: Parallel-error",log,value)


#axi 
log = "./mpiLog/axi.log.1"
value = [['total solver time',0.01,2,2]]
Run("Example axi/MPI: Serial-time",log,value)


#benard 
log = "./mpiLog/ray_9.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_9/MPI: Serial-time",log,value)

log = "./mpiLog/ray_dd.log.1"
value = [['total solver time',0.01,34,2]]
Run("Example benard/ray_dd/MPI: Serial-time",log,value)

log = "./mpiLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/MPI: Serial-error",log,value)

log = "./mpiLog/ray_dn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_dn/MPI: Serial-time",log,value)

log = "./mpiLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/MPI: Serial-error",log,value)

log = "./mpiLog/ray_nn.log.1"
value = [['total solver time',0.01,50,2]]
Run("Example benard/ray_nn/MPI: Serial-time",log,value)

log = "./mpiLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/MPI: Serial-error",log,value)


#conj_ht
log = "./mpiLog/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/MPI: Serial-time",log,value)

log = "./mpiLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI: Serial-error",log,value)

log = "./mpiLog/conj_ht.err.4"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI: Parallel-error",log,value)


#eddy
log = "./mpiLog/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/MPI: Serial-time",log,value)

log = "./mpiLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/MPI: Serial-error",log,value)

log = "./mpiLog/eddy_uv.err.4"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/MPI: Parallel-error",log,value)


#vortex 
log = "./mpiLog/r1854a.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example vortex/MPI: Serial-time",log,value)

log = "./mpiLog/vortex.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/MPI: Serial-error",log,value)

log = "./mpiLog/vortex.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/MPI: Parallel-error",log,value)


#fs_2 
log = "./mpiLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/MPI: Serial",log,value)

log = "./mpiLog/st1.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/MPI: Parallel",log,value)

log = "./mpiLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/MPI: Serial",log,value)

log = "./mpiLog/st2.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/MPI: Parallel",log,value)

log = "./mpiLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/MPI: Serial",log,value)

log = "./mpiLog/std_wv.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/MPI: Parallel",log,value)


#fs_hydro 
log = "./mpiLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/MPI: Serial",log,value)

log = "./mpiLog/fs_hydro.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/MPI: Parallel",log,value)


#kovasznay
log = "./mpiLog/kov.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example kov/MPI: Serial-time",log,value)

log = "./mpiLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/MPI: Serial-error",log,value)

log = "./mpiLog/kov.err.4"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/MPI: Parallel-error",log,value)


#lowMach_test 
log = "./mpiLog/lowMach_test.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example lowMach_test/MPI: Serial-time",log,value)

log = "./mpiLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/MPI: Serial-error",log,value)

log = "./mpiLog/lowMach_test.err.4"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/MPI: Parallel-error",log,value)


#peris
log = "./mpiLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/MPI: Serial",log,value)

log = "./mpiLog/peris.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/MPI: Parallel",log,value)


#pipe 
log = "./mpiLog/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/MPI: Serial-time",log,value)

log = "./mpiLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/MPI: Serial-error",log,value)

log = "./mpiLog/helix.err.4"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/MPI: Serial-error",log,value)

log = "./mpiLog/stenosis.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example stenosis/MPI: Serial-time",log,value)


#rayleigh 
log = "./mpiLog/ray1.log.1"
value = [['total solver time',0.01,5,2]]
Run("Example ray1/MPI: Serial-time",log,value)

log = "./mpiLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/MPI: Serial-error",log,value)

log = "./mpiLog/ray1.err.4"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/MPI: Parallel-error",log,value)

log = "./mpiLog/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/MPI: Serial-time",log,value)

log = "./mpiLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/MPI: Serial-error",log,value)

log = "./mpiLog/ray2.err.4"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/MPI: Parallel-error",log,value)


#shear4 
log = "./mpiLog/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/MPI: Serial-time",log,value)

log = "./mpiLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI: Serial-error",log,value)

log = "./mpiLog/shear4.err.4"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI: Parallel-error",log,value)

log = "./mpiLog/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/MPI: Serial-time",log,value)

log = "./mpiLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/MPI: Serial-error",log,value)

log = "./mpiLog/thin.err.4"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/MPI: Parallel-error",log,value)


#turbChannel 
log = "./mpiLog/turbChannel.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example turbChannel/MPI: Serial-time",log,value)

######################################################################
#---------------------PGI----------------------------------------------
#---------------------Pn-Pn--------------------------------------------
#axi
log = "./pgiLog/axi.log.1"
value = [['total solver time',0.01,2,2]]
Run("Example axi/PGI: Serial-time",log,value)


#benard 
log = "./pgiLog/ray_9.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_9/PGI: Serial-time",log,value)

log = "./pgiLog/ray_dd.log.1"
value = [['total solver time',0.01,24,2]]
Run("Example benard/ray_dd/PGI: Serial-time",log,value)

log = "./pgiLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/PGI: Serial-error",log,value)

log = "./pgiLog/ray_dn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_dn/PGI: Serial-time",log,value)

log = "./pgiLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/PGI: Serial-error",log,value)

log = "./pgiLog/ray_nn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_nn/PGI: Serial-time",log,value)

log = "./pgiLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/PGI: Serial-error",log,value)


#conj_ht 
log = "./pgiLog/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/PGI: Serial-time",log,value)

log = "./pgiLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/PGI: Serial-error",log,value)


#eddy 
log = "./pgiLog/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/PGI: Serial-time",log,value)

log = "./pgiLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/PGI: Serial-error",log,value)


#vortex
log = "./pgiLog/r1854a.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example vortext/PGI: Serial-time",log,value)

log = "./pgiLog/vortex.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/PGI: Serial-error",log,value)


#fs_2 
log = "./pgiLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/PGI: Serial",log,value)

log = "./pgiLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/PGI: Serial",log,value)

log = "./pgiLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/PGI: Serial",log,value)


#fs_hydro 
log = "./pgiLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/PGI: Serial",log,value)


#kovaszany 
log = "./pgiLog/kov.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example kov/PGI: Serial-time",log,value)

log = "./pgiLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/PGI: Serial-error",log,value)


#lowMach_test
log = "./pgiLog/lowMach_test.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example lowMach_test/PGI: Serial-time",log,value)

log = "./pgiLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/PGI: Serial-error",log,value)


#peris 
log = "./pgiLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/PGI: Serial",log,value)


#pipe
log = "./pgiLog/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/PGI: Serial-time",log,value)

log = "./pgiLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/PGI: Serial-error",log,value)


#rayleigh
log = "./pgiLog/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/PGI: Serial-time",log,value)

log = "./pgiLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/PGI: Serial-error",log,value)

log = "./pgiLog/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/PGI: Serial-time",log,value)

log = "./pgiLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/PGI: Serial-error",log,value)


#shear4 
log = "./pgiLog/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/PGI: Serial-time",log,value)

log = "./pgiLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/PGI: Serial-error",log,value)

log = "./pgiLog/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/PGI: Serial-time",log,value)

log = "./pgiLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/PGI: Serial-error",log,value)

#turbChannel 
log = "./pgiLog/turbChannel.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example turbChannel/PGI: Serial-time",log,value)

######################################################################
#---------------------GNU----------------------------------------------
#---------------------Pn-Pn--------------------------------------------
#axi 
log = "./gnuLog/axi.log.1"
value = [['total solver time',0.01,2,2]]
Run("Example axi/GNU: Serial-time",log,value)


#benard
log = "./gnuLog/ray_9.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_9/GNU: Serial-time",log,value)

log = "./gnuLog/ray_dd.log.1"
value = [['total solver time',0.01,24,2]]
Run("Example benard/ray_dd/GNU: Serial-time",log,value)

log = "./gnuLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/GNU: Serial-error",log,value)

log = "./gnuLog/ray_dn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_dn/GNU: Serial-time",log,value)

log = "./gnuLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/GNU: Serial-error",log,value)

log = "./gnuLog/ray_nn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_nn/GNU: Serial-time",log,value)

log = "./gnuLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/GNU: Serial-error",log,value)


#conj_ht 
log = "./gnuLog/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/GNU: Serial-time",log,value)

log = "./gnuLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/GNU: Serial-error",log,value)


#eddy 
log = "./gnuLog/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/GNU: Serial-time",log,value)

log = "./gnuLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/GNU: Serial-error",log,value)


#vortex
log = "./gnuLog/r1854a.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example vortex/GNU: Serial-time",log,value)

log = "./gnuLog/vortex.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/GNU: Serial-error",log,value)


#fs_2 
log = "./gnuLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/GNU: Serial",log,value)

log = "./gnuLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/GNU: Serial",log,value)

log = "./gnuLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/GNU: Serial",log,value)


#fs_hydro
log = "./gnuLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/GNU: Serial",log,value)


#kovaszany 
log = "./gnuLog/kov.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example kov/GNU: Serial-time",log,value)

log = "./gnuLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/GNU: Serial-error",log,value)


#lowMach_test
log = "./gnuLog/lowMach_test.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example lowMach_test/GNU: Serial-time",log,value)

log = "./gnuLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/GNU: Serial-error",log,value)


#peris 
log = "./gnuLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/GNU: Serial",log,value)


#pipe 
log = "./gnuLog/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/GNU: Serial-time",log,value)

log = "./gnuLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/GNU: Serial-error",log,value)

log = "./gnuLog/stenosis.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example stenosis/GNU: Serial-time",log,value)


#rayleigh
log = "./gnuLog/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/GNU: Serial-time",log,value)

log = "./gnuLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/GNU: Serial-error",log,value)

log = "./gnuLog/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/GNU: Serial-time",log,value)

log = "./gnuLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/GNU: Serial-error",log,value)


#shear4 
log = "./gnuLog/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/GNU: Serial-time",log,value)

log = "./gnuLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/GNU: Serial-error",log,value)

log = "./gnuLog/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/GNU: Serial-time",log,value)

log = "./gnuLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/GNU: Serial-error",log,value)


#turbChannel 
log = "./gnuLog/turbChannel.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example turbChannel/GNU: Serial-time",log,value)

######################################################################
#---------------------INT----------------------------------------------
#---------------------Pn-Pn--------------------------------------------
#axi 
log = "./intLog/axi.log.1"
value = [['total solver time',0.01,2,2]]
Run("Example axi/INT: Serial-time",log,value)


#benard 
log = "./intLog/ray_9.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_9/INT: Serial-time",log,value)

log = "./intLog/ray_dd.log.1"
value = [['total solver time',0.01,24,2]]
Run("Example benard/ray_dd/INT: Serial-time",log,value)

log = "./intLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/INT: Serial-error",log,value)

log = "./intLog/ray_dn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_dn/INT: Serial-time",log,value)

log = "./intLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/INT: Serial-error",log,value)

log = "./intLog/ray_nn.log.1"
value = [['total solver time',0.01,30,2]]
Run("Example benard/ray_nn/INT: Serial-time",log,value)

log = "./intLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/INT: Serial-error",log,value)


#conj_ht 
log = "./intLog/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/INT: Serial-time",log,value)

log = "./intLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/INT: Serial-error",log,value)


#eddy 
log = "./intLog/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/INT: Serial-time",log,value)

log = "./intLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/INT: Serial-error",log,value)


#vortex
log = "./intLog/r1854a.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example vortex/INT: Serial-time",log,value)

log = "./intLog/vortex.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/INT: Serial-error",log,value)


#fs_2 
log = "./intLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/INT: Serial",log,value)

log = "./intLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/INT: Serial",log,value)

log = "./intLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/INT: Serial",log,value)


#fs_hydro 
log = "./intLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/INT: Serial",log,value)


#kovaszany 
log = "./intLog/kov.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example kov/INT: Serial-time",log,value)

log = "./intLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/INT: Serial-error",log,value)


#lowMach_test
log = "./intLog/lowMach_test.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example lowMach_test/INT: Serial-time",log,value)

log = "./intLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/INT: Serial-error",log,value)


#peris 
log = "./intLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/INT: Serial",log,value)


#pipe 
log = "./intLog/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/INT: Serial-time",log,value)

log = "./intLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/INT: Serial-error",log,value)

log = "./intLog/stenosis.log.1"
value = [['total solver time',0.01,60,2]]
Run("Example stenosis/INT: Serial-time",log,value)


#rayleigh 
log = "./intLog/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/INT: Serial-time",log,value)

log = "./intLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/INT: Serial-error",log,value)

log = "./intLog/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/INT: Serial-time",log,value)

log = "./intLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/INT: Serial-error",log,value)


#shear4 
log = "./intLog/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/INT: Serial-time",log,value)

log = "./intLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/INT: Serial-error",log,value)

log = "./intLog/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/INT: Serial-time",log,value)

log = "./intLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/INT: Serial-error",log,value)


#turbChannel
log = "./intLog/turbChannel.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example turbChannel/INT: Serial-time",log,value)

###############################################################################################
#---------------------MPI----------------------------------------------
#---------------------Pn-Pn-2------------------------------------------
print("\nBEGIN Pn-Pn-2 TESTING")  
#Test0001 
log = "./mpi2Log/test0001.log.1"
value = [['total solver time',0.01,166,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/MPI2: Serial",log,value)

log = "./mpi2Log/test0001.log.4"
value = [['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/MPI2: Parallel-error",log,value)


#axi 
log = "./mpi2Log/axi.log.1"
value = [['total solver time',0.01,4,2]]
Run("Example axi/MPI2: Serial-time",log,value)


#benard 
log = "./mpi2Log/ray_9.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example benard/ray_9/MPI2: Serial-time",log,value)

log = "./mpi2Log/ray_dd.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_dd/MPI2: Serial-time",log,value)

log = "./mpi2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/MPI2: Serial-error",log,value)

log = "./mpi2Log/ray_dn.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example benard/ray_dn/MPI2: Serial-time",log,value)

log = "./mpi2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/MPI2: Serial-error",log,value)

log = "./mpi2Log/ray_nn.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_nn/MPI2: Serial-time",log,value)

log = "./mpi2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/MPI2: Serial-error",log,value)


#conj_ht
log = "./mpi2Log/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/MPI2: Serial-time",log,value)

log = "./mpi2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI2: Serial-error",log,value)

log = "./mpi2Log/conj_ht.err.4"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI2: Parallel-error",log,value)


#eddy
log = "./mpi2Log/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/MPI2: Serial-time",log,value)

log = "./mpi2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/MPI2: Serial-error",log,value)

log = "./mpi2Log/eddy_uv.err.4"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/MPI2: Parallel-error",log,value)


#vortex 
log = "./mpi2Log/r1854a.log.1"
value = [['total solver time',0.01,50,2]]
Run("Example vortex/MPI2: Serial-time",log,value)

log = "./mpi2Log/vortex.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/MPI2: Serial-error",log,value)

log = "./mpi2Log/vortex.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/MPI2: Parallel-error",log,value)


#fs_2 
log = "./mpi2Log/st1.log.1"
value = [['total solver time',0.01,27.3,2]]
Run("Example st1/MPI2: Serial-time",log,value)

log = "./mpi2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/MPI2: Serial-error",log,value)

log = "./mpi2Log/st1.err.4"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/MPI2: Parallel-error",log,value)

log = "./mpi2Log/st2.log.1"
value = [['total solver time',0.01,23,2]]
Run("Example st2/MPI2: Serial-time",log,value)

log = "./mpi2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/MPI2: Serial-error",log,value)

log = "./mpi2Log/st2.err.4"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/MPI2: Parallel-error",log,value)

log = "./mpi2Log/std_wv.log.1"
value = [['total solver time',0.01,21,2]]
Run("Example std_wv/MPI2: Serial-time",log,value)

log = "./mpi2Log/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/MPI2: Serial-error",log,value)

log = "./mpi2Log/std_wv.err.4"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/MPI2: Parallel-error",log,value)


#fs_hydro 
log = "./mpi2Log/fs_hydro.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example fs_hydro/MPI2: Serial-time",log,value)

log = "./mpi2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/MPI2: Serial-error",log,value)

log = "./mpi2Log/fs_hydro.err.4"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/MPI2: Parallel-error",log,value)


#kovasznay
log = "./mpi2Log/kov.log.1"
value = [['total solver time',0.01,17,2]]
Run("Example kov/MPI2: Serial-time",log,value)

log = "./mpi2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/MPI2: Serial-error",log,value)

log = "./mpi2Log/kov.err.4"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/MPI2: Parallel-error",log,value)


#lowMach_test 
log = "./mpi2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/MPI2: Serial",log,value)

log = "./mpi2Log/lowMach_test.log.4"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/MPI2: Parallel",log,value)


#peris
log = "./mpi2Log/peris.log.1"
value = [['total solver time',0.01,13,2]]
Run("Example peris/MPI2: Serial-time",log,value)


#pipe 
log = "./mpi2Log/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/MPI2: Serial-time",log,value)

log = "./mpi2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/MPI2: Serial-error",log,value)

log = "./mpi2Log/helix.err.4"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/MPI2: Parallel-error",log,value)

log = "./mpi2Log/stenosis.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example stenosis/MPI2: Serial-time",log,value)


#rayleigh 
log = "./mpi2Log/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/MPI2: Serial-time",log,value)

log = "./mpi2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-05,3]]
Run("Example ray1/MPI2: Serial-error",log,value)

log = "./mpi2Log/ray1.err.4"
value = [['umax',3.897862E-03,1e-05,3]]
Run("Example ray1/MPI2: Parallel-error",log,value)

log = "./mpi2Log/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/MPI2: Serial-time",log,value)

log = "./mpi2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-05,3]]
Run("Example ray2/MPI2: Serial-error",log,value)

log = "./mpi2Log/ray2.err.4"
value = [['umax',6.091663E-03,1e-05,3]]
Run("Example ray2/MPI2: Parallel-error",log,value)


#shear4 
log = "./mpi2Log/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/MPI2: Serial-time",log,value)

log = "./mpi2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI2: Serial-error",log,value)

log = "./mpi2Log/shear4.err.4"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI2: Parallel-error",log,value)

log = "./mpi2Log/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/MPI2: Serial-time",log,value)

log = "./mpi2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/MPI2: Serial-error",log,value)

log = "./mpi2Log/thin.err.4"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/MPI2: Parallel-error",log,value)


#turbChannel 
log = "./mpi2Log/turbChannel.log.1"
value = [['total solver time',0.01,140,2]]
Run("Example turbChannel/MPI2: Serial-time",log,value)

######################################################################
#---------------------PGI----------------------------------------------
#---------------------Pn-Pn-2------------------------------------------
#axi
log = "./pgi2Log/axi.log.1"
value = [['total solver time',0.01,4,2]]
Run("Example axi/PGI2: Serial-time",log,value)


#benard 
log = "./pgi2Log/ray_9.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example benard/ray_9/PGI2: Serial-time",log,value)

log = "./pgi2Log/ray_dd.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_dd/PGI2: Serial-time",log,value)

log = "./pgi2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/PGI2: Serial-error",log,value)

log = "./pgi2Log/ray_dn.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example benard/ray_dn/PGI2: Serial-time",log,value)

log = "./pgi2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/PGI2: Serial-error",log,value)

log = "./pgi2Log/ray_nn.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_nn/PGI2: Serial-time",log,value)

log = "./pgi2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/PGI2: Serial-error",log,value)


#conj_ht 
log = "./pgi2Log/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/PGI2: Serial-time",log,value)

log = "./pgi2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/PGI2: Serial-error",log,value)


#eddy 
log = "./pgi2Log/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/PGI2: Serial-time",log,value)

log = "./pgi2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/PGI2: Serial-error",log,value)


#vortex
log = "./pgi2Log/r1854a.log.1"
value = [['total solver time',0.01,50,2]]
Run("Example vortex/PGI2: Serial-time",log,value)

log = "./pgi2Log/vortex.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/PGI2: Serial-error",log,value)


#fs_2 
log = "./pgi2Log/st1.log.1"
value = [['total solver time',0.01,18.3,2]]
Run("Example st1/PGI2: Serial-time",log,value)

log = "./pgi2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/PGI2: Serial-error",log,value)

log = "./pgi2Log/st2.log.1"
value = [['total solver time',0.01,23,2]]
Run("Example st2/PGI2: Serial-time",log,value)

log = "./pgi2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/PGI2: Serial-error",log,value)

log = "./pgi2Log/std_wv.log.1"
value = [['total solver time',0.01,21,2]]
Run("Example std_wv/PGI2: Serial-time",log,value)

log = "./pgi2Log/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/PGI2: Serial-error",log,value)


#fs_hydro 
log = "./pgi2Log/fs_hydro.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example fs_hydro/PGI2: Serial-time",log,value)

log = "./pgi2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/PGI2: Serial-error",log,value)


#kovasznay
log = "./pgi2Log/kov.log.1"
value = [['total solver time',0.01,17,2]]
Run("Example kov/PGI2: Serial-time",log,value)

log = "./pgi2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/PGI2: Serial-error",log,value)


#lowMach_test 
log = "./pgi2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/PGI2: Serial",log,value)


#peris 
log = "./pgi2Log/peris.log.1"
value = [['total solver time',0.01,13,2]]
Run("Example peris/PGI2: Serial-time",log,value)


#pipe
log = "./pgi2Log/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/PGI2: Serial-time",log,value)

log = "./pgi2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/PGI2: Serial-error",log,value)

log = "./pgi2Log/stenosis.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example stenosis/PGI2: Serial-time",log,value)


#rayleigh
log = "./pgi2Log/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/PGI2: Serial-time",log,value)

log = "./pgi2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/PGI2: Serial-error",log,value)

log = "./pgi2Log/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/PGI2: Serial-time",log,value)

log = "./pgi2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/PGI2: Serial-error",log,value)


#shear4 
log = "./pgi2Log/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/PGI2: Serial-time",log,value)

log = "./pgi2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/PGI2: Serial-error",log,value)

log = "./pgi2Log/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/PGI2: Serial-time",log,value)

log = "./pgi2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/PGI2: Serial-error",log,value)


#turbChannel 
log = "./pgi2Log/turbChannel.log.1"
value = [['total solver time',0.01,140,2]]
Run("Example turbChannel/PGI2: Serial-time",log,value)

######################################################################
#---------------------GNU----------------------------------------------
#---------------------Pn-Pn-2------------------------------------------
#axi 
log = "./gnu2Log/axi.log.1"
value = [['total solver time',0.01,9,2]]
Run("Example axi/GNU2: Serial-time",log,value)


#benard
log = "./gnu2Log/ray_9.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example benard/ray_9/GNU2: Serial-time",log,value)

log = "./gnu2Log/ray_dd.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_dd/GNU2: Serial-time",log,value)

log = "./gnu2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/GNU2: Serial-error",log,value)

log = "./gnu2Log/ray_dn.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example benard/ray_dn/GNU2: Serial-time",log,value)

log = "./gnu2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/GNU2: Serial-error",log,value)

log = "./gnu2Log/ray_nn.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_nn/GNU2: Serial-time",log,value)

log = "./gnu2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/GNU2: Serial-error",log,value)


#conj_ht 
log = "./gnu2Log/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/GNU2: Serial-time",log,value)

log = "./gnu2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/GNU2: Serial-error",log,value)


#eddy 
log = "./gnu2Log/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/GNU2: Serial-time",log,value)

log = "./gnu2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/GNU2: Serial-error",log,value)


#vortex
log = "./gnu2Log/r1854a.log.1"
value = [['total solver time',0.01,50,2]]
Run("Example vortex/GNU2: Serial-time",log,value)

log = "./gnu2Log/vortex.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/GNU2: Serial-error",log,value)


#fs_2 
log = "./gnu2Log/st1.log.1"
value = [['total solver time',0.01,18.3,2]]
Run("Example st1/GNU2: Serial-time",log,value)

log = "./gnu2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/GNU2: Serial-error",log,value)

log = "./gnu2Log/st2.log.1"
value = [['total solver time',0.01,23,2]]
Run("Example st2/GNU2: Serial-time",log,value)

log = "./gnu2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/GNU2: Serial-error",log,value)

log = "./gnu2Log/std_wv.log.1"
value = [['total solver time',0.01,21,2]]
Run("Example std_wv/GNU2: Serial-time",log,value)

log = "./gnu2Log/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/GNU2: Serial-error",log,value)


#fs_hydro
log = "./gnu2Log/fs_hydro.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example fs_hydro/GNU2: Serial-time",log,value)

log = "./gnu2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/GNU2: Serial-error",log,value)


#kovasznay
log = "./gnu2Log/kov.log.1"
value = [['total solver time',0.01,17,2]]
Run("Example kov/GNU2: Serial-time",log,value)

log = "./gnu2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/GNU2: Serial-error",log,value)


#lowMach_test 
log = "./gnu2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/GNU2: Serial",log,value)


#peris 
log = "./gnu2Log/peris.log.1"
value = [['total solver time',0.01,13,2]]
Run("Example peris/GNU2: Serial-time",log,value)


#pipe 
log = "./gnu2Log/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/GNU2: Serial-time",log,value)

log = "./gnu2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/GNU2: Serial-error",log,value)

log = "./gnu2Log/stenosis.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example stenosis/GNU2: Serial-time",log,value)


#rayleigh
log = "./gnu2Log/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/GNU2: Serial-time",log,value)

log = "./gnu2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/GNU2: Serial-error",log,value)

log = "./gnu2Log/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/GNU2: Serial-time",log,value)

log = "./gnu2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/GNU2: Serial-error",log,value)


#shear4 
log = "./gnu2Log/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/GNU2: Serial-time",log,value)

log = "./gnu2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/GNU2: Serial-error",log,value)

log = "./gnu2Log/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/GNU2: Serial-time",log,value)

log = "./gnu2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/GNU2: Serial-error",log,value)


#turbChannel 
log = "./gnu2Log/turbChannel.log.1"
value = [['total solver time',0.01,140,2]]
Run("Example turbChannel/GNU2: Serial-time",log,value)

######################################################################
#---------------------INT----------------------------------------------
#---------------------Pn-Pn-2------------------------------------------
#axi 
log = "./int2Log/axi.log.1"
value = [['total solver time',0.01,4,2]]
Run("Example axi/INT2: Serial-time",log,value)


#benard 
log = "./int2Log/ray_9.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example benard/ray_9/INT2: Serial-time",log,value)

log = "./int2Log/ray_dd.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_dd/INT2: Serial-time",log,value)

log = "./int2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/INT2: Serial-error",log,value)

log = "./int2Log/ray_dn.log.1"
value = [['total solver time',0.01,12,2]]
Run("Example benard/ray_dn/INT2: Serial-time",log,value)

log = "./int2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/INT2: Serial-error",log,value)

log = "./int2Log/ray_nn.log.1"
value = [['total solver time',0.01,20,2]]
Run("Example benard/ray_nn/INT2: Serial-time",log,value)

log = "./int2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/INT2: Serial-error",log,value)


#conj_ht 
log = "./int2Log/conj_ht.log.1"
value = [['total solver time',0.01,7,2]]
Run("Example conj_ht/INT2: Serial-time",log,value)

log = "./int2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/INT2: Serial-error",log,value)


#eddy 
log = "./int2Log/eddy_uv.log.1"
value = [['total solver time',0.01,80,2]]
Run("Example eddy/INT2: Serial-time",log,value)

log = "./int2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/INT2: Serial-error",log,value)


#vortex
log = "./int2Log/r1854a.log.1"
value = [['total solver time',0.01,50,2]]
Run("Example vortex/INT2: Serial-time",log,value)

log = "./int2Log/vortex.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/INT2: Serial-error",log,value)


#fs_2 
log = "./int2Log/st1.log.1"
value = [['total solver time',0.01,18.3,2]]
Run("Example st1/INT2: Serial-time",log,value)

log = "./int2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/INT2: Serial-error",log,value)

log = "./int2Log/st2.log.1"
value = [['total solver time',0.01,23,2]]
Run("Example st2/INT2: Serial-time",log,value)

log = "./int2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/INT2: Serial-error",log,value)

log = "./int2Log/std_wv.log.1"
value = [['total solver time',0.01,21,2]]
Run("Example std_wv/INT2: Serial-time",log,value)

log = "./int2Log/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/INT2: Serial-error",log,value)


#fs_hydro 
log = "./int2Log/fs_hydro.log.1"
value = [['total solver time',0.01,200,2]]
Run("Example fs_hydro/INT2: Serial-time",log,value)

log = "./int2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/INT2: Serial-error",log,value)


#kovasznay
log = "./int2Log/kov.log.1"
value = [['total solver time',0.01,17,2]]
Run("Example kov/INT2: Serial-time",log,value)

log = "./int2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/INT2: Serial-error",log,value)


#lowMach_test 
log = "./int2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/INT2: Serial",log,value)


#peris 
log = "./int2Log/peris.log.1"
value = [['total solver time',0.01,13,2]]
Run("Example peris/INT2: Serial-time",log,value)


#pipe 
log = "./int2Log/helix.log.1"
value = [['total solver time',0.01,22,2]]
Run("Example helix/INT2: Serial-time",log,value)

log = "./int2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/INT2: Serial-error",log,value)

log = "./int2Log/stenosis.log.1"
value = [['total solver time',0.01,40,2]]
Run("Example stenosis/INT2: Serial-time",log,value)


#rayleigh 
log = "./int2Log/ray1.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray1/INT2: Serial-time",log,value)

log = "./int2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/INT2: Serial-error",log,value)

log = "./int2Log/ray2.log.1"
value = [['total solver time',0.01,3,2]]
Run("Example ray2/INT2: Serial-time",log,value)

log = "./int2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/INT2: Serial-error",log,value)


#shear4 
log = "./int2Log/shear4.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thick/INT2: Serial-time",log,value)

log = "./int2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/INT2: Serial-error",log,value)

log = "./int2Log/thin.log.1"
value = [['total solver time',0.01,10,2]]
Run("Example shear4/thin/INT2: Serial-time",log,value)

log = "./int2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/INT2: Serial-error",log,value)


#turbChannel
log = "./int2Log/turbChannel.log.1"
value = [['total solver time',0.01,140,2]]
Run("Example turbChannel/INT2: Serial-time",log,value)

###############################################################################################
###############################################################################################
print("\n\nTest Summary :     %i/%i tests were successful"%(num_success,num_test))
print("End of top-down testing")  
