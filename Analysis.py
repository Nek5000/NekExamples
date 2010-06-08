#! /usr/bin/python
# Python module to run top-down tests for Nek

import sys
import os

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
        print("%s : F"%name)



###############################################################################################
num_test = 0 
num_success = 0
print("Beginning of top-down testing\n\n")
print("    . : successful test, F : failed test\n\n")
###############################################################################################

#Test0001 - MPI 
log = "./mpiLog/test0001.log.1"
value = [['total solver time',0,166,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/MPI: Serial",log,value)

log = "./mpiLog/test0001.log.4"
value = [['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/MPI: Parallel-error",log,value)

#Test0001 - PGI
log = "./pgiLog/test0001.log.1"
value = [['total solver time',0,166,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/PGI: Serial",log,value)

#Test0001 - GNU
log = "./gnuLog/test0001.log.1"
value = [['total solver time',0,166,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/GNU: Serial",log,value)

#Test0001 - INT
log = "./intLog/test0001.log.1"
value = [['total solver time',0,166,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001/INT: Serial",log,value)



#Example Cases tested for time elapsed and error values
#axi - MPI
log = "./mpiLog/axi.log.1"
value = [['total solver time',0,4,2]]
Run("Example axi/MPI: Serial-time",log,value)

#axi - PGI
log = "./pgiLog/axi.log.1"
value = [['total solver time',0,4,2]]
Run("Example axi/PGI: Serial-time",log,value)

#axi - GNU
log = "./gnuLog/axi.log.1"
value = [['total solver time',0,9,2]]
Run("Example axi/GNU: Serial-time",log,value)

#axi - INT
log = "./intLog/axi.log.1"
value = [['total solver time',0,4,2]]
Run("Example axi/INT: Serial-time",log,value)



#benard - MPI
log = "./mpiLog/ray_9.log.1"
value = [['total solver time',0,11,2]]
Run("Example benard/ray_9/MPI: Serial-time",log,value)

log = "./mpiLog/ray_dd.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dd/MPI: Serial-time",log,value)

log = "./mpiLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/MPI: Serial-error",log,value)

log = "./mpiLog/ray_dn.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dn/MPI: Serial-time",log,value)

log = "./mpiLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/MPI: Serial-error",log,value)

log = "./mpiLog/ray_nn.log.1"
value = [['total solver time',0,13,2]]
Run("Example benard/ray_nn/MPI: Serial-time",log,value)

log = "./mpiLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/MPI: Serial-error",log,value)

#benard - PGI
log = "./pgiLog/ray_9.log.1"
value = [['total solver time',0,11,2]]
Run("Example benard/ray_9/PGI: Serial-time",log,value)

log = "./pgiLog/ray_dd.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dd/PGI: Serial-time",log,value)

log = "./pgiLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/PGI: Serial-error",log,value)

log = "./pgiLog/ray_dn.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dn/PGI: Serial-time",log,value)

log = "./pgiLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/PGI: Serial-error",log,value)

log = "./pgiLog/ray_nn.log.1"
value = [['total solver time',0,13,2]]
Run("Example benard/ray_nn/PGI: Serial-time",log,value)

log = "./pgiLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/PGI: Serial-error",log,value)

#benard - GNU
log = "./gnuLog/ray_9.log.1"
value = [['total solver time',0,11,2]]
Run("Example benard/ray_9/GNU: Serial-time",log,value)

log = "./gnuLog/ray_dd.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dd/GNU: Serial-time",log,value)

log = "./gnuLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/GNU: Serial-error",log,value)

log = "./gnuLog/ray_dn.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dn/GNU: Serial-time",log,value)

log = "./gnuLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/GNU: Serial-error",log,value)

log = "./gnuLog/ray_nn.log.1"
value = [['total solver time',0,13,2]]
Run("Example benard/ray_nn/GNU: Serial-time",log,value)

log = "./gnuLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/GNU: Serial-error",log,value)

#benard - INT
log = "./intLog/ray_9.log.1"
value = [['total solver time',0,11,2]]
Run("Example benard/ray_9/INT: Serial-time",log,value)

log = "./intLog/ray_dd.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dd/INT: Serial-time",log,value)

log = "./intLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/INT: Serial-error",log,value)

log = "./intLog/ray_dn.log.1"
value = [['total solver time',0,8,2]]
Run("Example benard/ray_dn/INT: Serial-time",log,value)

log = "./intLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/INT: Serial-error",log,value)

log = "./intLog/ray_nn.log.1"
value = [['total solver time',0,13,2]]
Run("Example benard/ray_nn/INT: Serial-time",log,value)

log = "./intLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/INT: Serial-error",log,value)



#conj_ht - MPI
log = "./mpiLog/conj_ht.log.1"
value = [['total solver time',0,7,2]]
Run("Example conj_ht/MPI: Serial-time",log,value)

log = "./mpiLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI: Serial-error",log,value)

log = "./mpiLog/conj_ht.err.4"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI: Parallel-error",log,value)

#conj_ht - PGI
log = "./pgiLog/conj_ht.log.1"
value = [['total solver time',0,7,2]]
Run("Example conj_ht/PGI: Serial-time",log,value)

log = "./pgiLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/PGI: Serial-error",log,value)

#conj_ht - GNU
log = "./gnuLog/conj_ht.log.1"
value = [['total solver time',0,7,2]]
Run("Example conj_ht/GNU: Serial-time",log,value)

log = "./gnuLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/GNU: Serial-error",log,value)

#conj_ht - INT
log = "./intLog/conj_ht.log.1"
value = [['total solver time',0,7,2]]
Run("Example conj_ht/INT: Serial-time",log,value)

log = "./intLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/INT: Serial-error",log,value)



#eddy - MPI
log = "./mpiLog/eddy_uv.log.1"
value = [['total solver time',0,80,2]]
Run("Example eddy/MPI: Serial-time",log,value)

log = "./mpiLog/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/MPI: Serial-error",log,value)

log = "./mpiLog/eddy_uv.err.4"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/MPI: Parallel-error",log,value)

#eddy - PGI
log = "./pgiLog/eddy_uv.log.1"
value = [['total solver time',0,80,2]]
Run("Example eddy/PGI: Serial-time",log,value)

log = "./pgiLog/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/PGI: Serial-error",log,value)

#eddy - GNU
log = "./gnuLog/eddy_uv.log.1"
value = [['total solver time',0,80,2]]
Run("Example eddy/GNU: Serial-time",log,value)

log = "./gnuLog/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/GNU: Serial-error",log,value)

#eddy - INT
log = "./intLog/eddy_uv.log.1"
value = [['total solver time',0,80,2]]
Run("Example eddy/INT: Serial-time",log,value)

log = "./intLog/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/INT: Serial-error",log,value)



#escudier -MPI
log = "./mpiLog/r1854a.log.1"
value = [['total solver time',0,50,2]]
Run("Example escudier/MPI: Serial-time",log,value)

log = "./mpiLog/escudier.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example escudier/MPI: Serial-error",log,value)

log = "./mpiLog/escudier.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example escudier/MPI: Parallel-error",log,value)

#escudier -PGI
log = "./pgiLog/r1854a.log.1"
value = [['total solver time',0,50,2]]
Run("Example escudier/PGI: Serial-time",log,value)

log = "./pgiLog/escudier.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example escudier/PGI: Serial-error",log,value)

#escudier -GNU
log = "./gnuLog/r1854a.log.1"
value = [['total solver time',0,50,2]]
Run("Example escudier/GNU: Serial-time",log,value)

log = "./gnuLog/escudier.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example escudier/GNU: Serial-error",log,value)

#escudier -INT
log = "./intLog/r1854a.log.1"
value = [['total solver time',0,50,2]]
Run("Example escudier/INT: Serial-time",log,value)

log = "./intLog/escudier.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example escudier/INT: Serial-error",log,value)



#fs_2 - MPI
log = "./mpiLog/st1.log.1"
value = [['total solver time',0,27.3,2]]
Run("Example st1/MPI: Serial-time",log,value)

log = "./mpiLog/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/MPI: Serial-error",log,value)

log = "./mpiLog/st1.err.4"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/MPI: Parallel-error",log,value)

log = "./mpiLog/st2.log.1"
value = [['total solver time',0,23,2]]
Run("Example st2/MPI: Serial-time",log,value)

log = "./mpiLog/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/MPI: Serial-error",log,value)

log = "./mpiLog/st2.err.4"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/MPI: Parallel-error",log,value)

log = "./mpiLog/std_wv.log.1"
value = [['total solver time',0,21,2]]
Run("Example std_wv/MPI: Serial-time",log,value)

log = "./mpiLog/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/MPI: Serial-error",log,value)

log = "./mpiLog/std_wv.err.4"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/MPI: Parallel-error",log,value)

#fs_2 - PGI
log = "./pgiLog/st1.log.1"
value = [['total solver time',0,18.3,2]]
Run("Example st1/PGI: Serial-time",log,value)

log = "./pgiLog/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/PGI: Serial-error",log,value)

log = "./pgiLog/st2.log.1"
value = [['total solver time',0,23,2]]
Run("Example st2/PGI: Serial-time",log,value)

log = "./pgiLog/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/PGI: Serial-error",log,value)

log = "./pgiLog/std_wv.log.1"
value = [['total solver time',0,21,2]]
Run("Example std_wv/PGI: Serial-time",log,value)

log = "./pgiLog/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/PGI: Serial-error",log,value)

#fs_2 - GNU
log = "./gnuLog/st1.log.1"
value = [['total solver time',0,18.3,2]]
Run("Example st1/GNU: Serial-time",log,value)

log = "./gnuLog/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/GNU: Serial-error",log,value)

log = "./gnuLog/st2.log.1"
value = [['total solver time',0,23,2]]
Run("Example st2/GNU: Serial-time",log,value)

log = "./gnuLog/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/GNU: Serial-error",log,value)

log = "./gnuLog/std_wv.log.1"
value = [['total solver time',0,21,2]]
Run("Example std_wv/GNU: Serial-time",log,value)

log = "./gnuLog/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/GNU: Serial-error",log,value)

#fs_2 - INT
log = "./intLog/st1.log.1"
value = [['total solver time',0,18.3,2]]
Run("Example st1/INT: Serial-time",log,value)

log = "./intLog/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/INT: Serial-error",log,value)

log = "./intLog/st2.log.1"
value = [['total solver time',0,23,2]]
Run("Example st2/INT: Serial-time",log,value)

log = "./intLog/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/INT: Serial-error",log,value)

log = "./intLog/std_wv.log.1"
value = [['total solver time',0,21,2]]
Run("Example std_wv/INT: Serial-time",log,value)

log = "./intLog/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv/INT: Serial-error",log,value)



#fs_hydro - MPI
log = "./mpiLog/fs_hydro.log.1"
value = [['total solver time',0,200,2]]
Run("Example fs_hydro/MPI: Serial-time",log,value)

log = "./mpiLog/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/MPI: Serial-error",log,value)

log = "./mpiLog/fs_hydro.err.4"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/MPI: Parallel-error",log,value)

#fs_hydro - PGI
log = "./pgiLog/fs_hydro.log.1"
value = [['total solver time',0,200,2]]
Run("Example fs_hydro/PGI: Serial-time",log,value)

log = "./pgiLog/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/PGI: Serial-error",log,value)

#fs_hydro - GNU
log = "./gnuLog/fs_hydro.log.1"
value = [['total solver time',0,200,2]]
Run("Example fs_hydro/GNU: Serial-time",log,value)

log = "./gnuLog/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/GNU: Serial-error",log,value)

#fs_hydro - INT
log = "./intLog/fs_hydro.log.1"
value = [['total solver time',0,200,2]]
Run("Example fs_hydro/INT: Serial-time",log,value)

log = "./intLog/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/INT: Serial-error",log,value)



#kovasznay - MPI
log = "./mpiLog/kov.log.1"
value = [['total solver time',0,12,2]]
Run("Example kov/MPI: Serial-time",log,value)

log = "./mpiLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/MPI: Serial-error",log,value)

log = "./mpiLog/kov.err.4"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/MPI: Parallel-error",log,value)

#kovaszany - PGI
log = "./pgiLog/kov.log.1"
value = [['total solver time',0,12,2]]
Run("Example kov/PGI: Serial-time",log,value)

log = "./pgiLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/PGI: Serial-error",log,value)

#kovaszany - GNU
log = "./gnuLog/kov.log.1"
value = [['total solver time',0,12,2]]
Run("Example kov/GNU: Serial-time",log,value)

log = "./gnuLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/GNU: Serial-error",log,value)

#kovaszany - INT
log = "./intLog/kov.log.1"
value = [['total solver time',0,12,2]]
Run("Example kov/INT: Serial-time",log,value)

log = "./intLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/INT: Serial-error",log,value)



#lowMach_test - MPI
log = "./mpiLog/lowMach_test.log.1"
value = [['total solver time',0,40,2]]
Run("Example lowMach_test/MPI: Serial-time",log,value)

log = "./mpiLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/MPI: Serial-error",log,value)

log = "./mpiLog/lowMach_test.err.4"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/MPI: Parallel-error",log,value)

#lowMach_test - PGI
log = "./pgiLog/lowMach_test.log.1"
value = [['total solver time',0,40,2]]
Run("Example lowMach_test/PGI: Serial-time",log,value)

log = "./pgiLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/PGI: Serial-error",log,value)

#lowMach_test - GNU
log = "./gnuLog/lowMach_test.log.1"
value = [['total solver time',0,40,2]]
Run("Example lowMach_test/GNU: Serial-time",log,value)

log = "./gnuLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/GNU: Serial-error",log,value)

#lowMach_test - INT
log = "./intLog/lowMach_test.log.1"
value = [['total solver time',0,40,2]]
Run("Example lowMach_test/INT: Serial-time",log,value)

log = "./intLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/INT: Serial-error",log,value)



#peris - MPI
log = "./mpiLog/peris.log.1"
value = [['total solver time',0,13,2]]
Run("Example peris/MPI: Serial-time",log,value)

#peris - PGI
log = "./pgiLog/peris.log.1"
value = [['total solver time',0,13,2]]
Run("Example peris/PGI: Serial-time",log,value)

#peris - GNU
log = "./gnuLog/peris.log.1"
value = [['total solver time',0,13,2]]
Run("Example peris/GNU: Serial-time",log,value)

#peris - INT
log = "./intLog/peris.log.1"
value = [['total solver time',0,13,2]]
Run("Example peris/INT: Serial-time",log,value)



#pipe - MPI
log = "./mpiLog/helix.log.1"
value = [['total solver time',0,22,2]]
Run("Example helix/MPI: Serial-time",log,value)

log = "./mpiLog/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/MPI: Serial-error",log,value)

log = "./mpiLog/helix.err.4"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/MPI: Parallel-error",log,value)

log = "./mpiLog/stenosis.log.1"
value = [['total solver time',0,28,2]]
Run("Example stenosis/MPI: Serial-time",log,value)

#pipe - PGI
log = "./pgiLog/helix.log.1"
value = [['total solver time',0,22,2]]
Run("Example helix/PGI: Serial-time",log,value)

log = "./pgiLog/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/PGI: Serial-error",log,value)

log = "./pgiLog/stenosis.log.1"
value = [['total solver time',0,28,2]]
Run("Example stenosis/PGI: Serial-time",log,value)

#pipe - GNU
log = "./gnuLog/helix.log.1"
value = [['total solver time',0,22,2]]
Run("Example helix/GNU: Serial-time",log,value)

log = "./gnuLog/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/GNU: Serial-error",log,value)

log = "./gnuLog/stenosis.log.1"
value = [['total solver time',0,28,2]]
Run("Example stenosis/GNU: Serial-time",log,value)

#pipe - INT
log = "./intLog/helix.log.1"
value = [['total solver time',0,22,2]]
Run("Example helix/INT: Serial-time",log,value)

log = "./intLog/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/INT: Serial-error",log,value)

log = "./intLog/stenosis.log.1"
value = [['total solver time',0,28,2]]
Run("Example stenosis/INT: Serial-time",log,value)



#rayleigh - MPI 
log = "./mpiLog/ray1.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray1/MPI: Serial-time",log,value)

log = "./mpiLog/ray1.err.1"
value = [['umax',3.897862E-03,1e-05,3]]
Run("Example ray1/MPI: Serial-error",log,value)

log = "./mpiLog/ray1.err.4"
value = [['umax',3.897862E-03,1e-05,3]]
Run("Example ray1/MPI: Parallel-error",log,value)

log = "./mpiLog/ray2.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray2/MPI: Serial-time",log,value)

log = "./mpiLog/ray2.err.1"
value = [['umax',6.091663E-03,1e-05,3]]
Run("Example ray2/MPI: Serial-error",log,value)

log = "./mpiLog/ray2.err.4"
value = [['umax',6.091663E-03,1e-05,3]]
Run("Example ray2/MPI: Parallel-error",log,value)

#rayleigh - PGI
log = "./pgiLog/ray1.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray1/PGI: Serial-time",log,value)

log = "./pgiLog/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/PGI: Serial-error",log,value)

log = "./pgiLog/ray2.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray2/PGI: Serial-time",log,value)

log = "./pgiLog/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/PGI: Serial-error",log,value)

#rayleigh - GNU
log = "./gnuLog/ray1.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray1/GNU: Serial-time",log,value)

log = "./gnuLog/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/GNU: Serial-error",log,value)

log = "./gnuLog/ray2.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray2/GNU: Serial-time",log,value)

log = "./gnuLog/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/GNU: Serial-error",log,value)

#rayleigh - INT
log = "./intLog/ray1.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray1/INT: Serial-time",log,value)

log = "./intLog/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/INT: Serial-error",log,value)

log = "./intLog/ray2.log.1"
value = [['total solver time',0,3,2]]
Run("Example ray2/INT: Serial-time",log,value)

log = "./intLog/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/INT: Serial-error",log,value)



#shear4 - MPI
log = "./mpiLog/shear4.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thick/MPI: Serial-time",log,value)

log = "./mpiLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI: Serial-error",log,value)

log = "./mpiLog/shear4.err.4"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI: Parallel-error",log,value)

log = "./mpiLog/thin.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thin/MPI: Serial-time",log,value)

log = "./mpiLog/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/MPI: Serial-error",log,value)

log = "./mpiLog/thin.err.4"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/MPI: Parallel-error",log,value)

#shear4 - PGI
log = "./pgiLog/shear4.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thick/PGI: Serial-time",log,value)

log = "./pgiLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/PGI: Serial-error",log,value)

log = "./pgiLog/thin.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thin/PGI: Serial-time",log,value)

log = "./pgiLog/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/PGI: Serial-error",log,value)

#shear4 - GNU
log = "./gnuLog/shear4.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thick/GNU: Serial-time",log,value)

log = "./gnuLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/GNU: Serial-error",log,value)

log = "./gnuLog/thin.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thin/GNU: Serial-time",log,value)

log = "./gnuLog/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/GNU: Serial-error",log,value)

#shear4 - INT
log = "./intLog/shear4.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thick/INT: Serial-time",log,value)

log = "./intLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/INT: Serial-error",log,value)

log = "./intLog/thin.log.1"
value = [['total solver time',0,10,2]]
Run("Example shear4/thin/INT: Serial-time",log,value)

log = "./intLog/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/INT: Serial-error",log,value)



#turbChannel - MPI
log = "./mpiLog/turbChannel.log.1"
value = [['total solver time',0,140,2]]
Run("Example turbChannel/MPI: Serial-time",log,value)

#turbChannel - PGI
log = "./pgiLog/turbChannel.log.1"
value = [['total solver time',0,140,2]]
Run("Example turbChannel/PGI: Serial-time",log,value)

#turbChannel - GNU
log = "./gnuLog/turbChannel.log.1"
value = [['total solver time',0,140,2]]
Run("Example turbChannel/GNU: Serial-time",log,value)

#turbChannel - INT
log = "./intLog/turbChannel.log.1"
value = [['total solver time',0,140,2]]
Run("Example turbChannel/INT: Serial-time",log,value)
###############################################################################################
    
print("\n\nTest Summary :     %i/%i tests were successful"%(num_success,num_test))
print("End of top-down testing")  
