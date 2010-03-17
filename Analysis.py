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

#Test0001 serial
log = "./test0001/test0001.log.1"
value = [['total elapsed time',0,170,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001: Serial",log,value)

#Test0001 parallel
log = "./test0001/test0001.log.4"
value = [['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001: Parallel-error",log,value)



#Test0002 serial
log = "./test0002/test0002.log.1"
value = [['total elapsed time',0,930,2],['ANS1',2.6557E-06,1e-06,7]]
Run("Test0002: Serial",log,value)

#Test0002 parallel
log = "./test0002/test0002.log.4"
value = [['ANS1',2.6557E-06,1e-06,7]]
Run("Test0002: Parallel-error",log,value)



#Example Cases tested for time elapsed and error values
#axi
log = "../examples/axi/axi.log.1"
value = [['total elapsed time',0,6,2]]
Run("Example axi: Serial-time",log,value)



#eddy
log = "../examples/eddy/eddy_uv.log.1"
value = [['total elapsed time',0,108,2]]
Run("Example eddy: Serial-time",log,value)

log = "../examples/eddy/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy: Serial-error",log,value)

log = "../examples/eddy/eddy_uv.err.4"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy: Parallel-error",log,value)



#fs_2
log = "../examples/fs_2/st1.log.1"
value = [['total elapsed time',0,27.3,2]]
Run("Example st1: Serial-time",log,value)

log = "../examples/fs_2/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1: Serial-error",log,value)

log = "../examples/fs_2/st1.err.4"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1: Parallel-error",log,value)

log = "../examples/fs_2/st2.log.1"
value = [['total elapsed time',0,31.2,2]]
Run("Example st2: Serial-time",log,value)

log = "../examples/fs_2/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2: Serial-error",log,value)

log = "../examples/fs_2/st2.err.4"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2: Parallel-error",log,value)

log = "../examples/fs_2/std_wv.log.1"
value = [['total elapsed time',0,29,2]]
Run("Example std_wv: Serial-time",log,value)

log = "../examples/fs_2/std_wv.err.1"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv: Serial-error",log,value)

log = "../examples/fs_2/std_wv.err.4"
value = [['amp',9.011472E-01,1e-06,2]]
Run("Example std_wv: Parallel-error",log,value)



#fs_hydro
log = "../examples/fs_hydro/fs_hydro.log.1"
value = [['total elapsed time',0,52,2]]
Run("Example fs_hydro: Serial-time",log,value)

log = "../examples/fs_hydro/fs_hydro.err.1"
value = [['AMP',1.5581969E-03,1e-06,2]]
Run("Example fs_hydro: Serial-error",log,value)

log = "../examples/fs_hydro/fs_hydro.err.4"
value = [['AMP',3.1468195E-04,1e-06,2]]
Run("Example fs_hydro: Parallel-error",log,value)



#kovasznay
log = "../examples/kovasznay/kov.log.1"
value = [['total elapsed time',0,20,2]]
Run("Example kov: Serial-time",log,value)

log = "../examples/kovasznay/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov: Serial-error",log,value)

log = "../examples/kovasznay/kov.err.4"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov: Parallel-error",log,value)



#lowMach_test
log = "../examples/lowMach_test/lowMach_test.log.1"
value = [['total elapsed time',0,53.8,2]]
Run("Example lowMach_test: Serial-time",log,value)

log = "../examples/lowMach_test/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test: Serial-error",log,value)

log = "../examples/lowMach_test/lowMach_test.err.4"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test: Parallel-error",log,value)



#pipe
log = "../examples/pipe/helix.log.1"
value = [['total elapsed time',0,24.7,2]]
Run("Example helix: Serial-time",log,value)

log = "../examples/pipe/helix.err.1"
value = [['e2',1.9072258E+00,1e-05,2]]
Run("Example helix: Serial-error",log,value)

log = "../examples/pipe/helix.err.4"
value = [['e2',1.9080559E+00,1e-05,2]]
Run("Example helix: Parallel-error",log,value)

log = "../examples/pipe/stenosis.log.1"
value = [['total elapsed time',0,33.2,2]]
Run("Example stenosis: Serial-time",log,value)



#rayleigh 
log = "../examples/rayleigh/ray1.log.1"
value = [['total elapsed time',0,4,2]]
Run("Example ray1: Serial-time",log,value)

log = "../examples/rayleigh/ray1.err.1"
value = [['umax',3.798345E-03,1e-06,3]]
Run("Example ray1: Serial-error",log,value)

log = "../examples/rayleigh/ray1.err.4"
value = [['umax',3.413486E-03,1e-06,3]]
Run("Example ray1: Parallel-error",log,value)

log = "../examples/rayleigh/ray2.log.1"
value = [['total elapsed time',0,4,2]]
Run("Example ray2: Serial-time",log,value)

log = "../examples/rayleigh/ray2.err.1"
value = [['umax',3.239578E-03,1e-06,3]]
Run("Example ray2: Serial-error",log,value)

log = "../examples/rayleigh/ray2.err.4"
value = [['umax',2.958139E-03,1e-06,3]]
Run("Example ray2: Parallel-error",log,value)



#turbChannel
log = "../examples/turbChannel/turbChannel.log.1"
value = [['total elapsed time',0,156,2]]
Run("Example turbChannel: Serial-time",log,value)

###############################################################################################
    
print("\n\nTest Summary :     %i/%i tests were successful"%(num_success,num_test))
print("End of top-down testing")  
