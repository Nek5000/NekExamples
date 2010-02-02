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
Run("Test0001 Serial",log,value)
   
#Test0001 parallel
log = "./test0001/test0001.log.4"
value = [['total elapsed time',0,50,2],['ANS1',5.742723E-07,1e-06,8]]
Run("Test0001 Parallel",log,value)



#Test0002 serial
log = "./test0002/test0002.log.1"
value = [['total elapsed time',0,930,2],['FINAL',2.6557E-06,1e-06,7]]
Run("Test0002 Serial",log,value)
   
#Test0002 parallel
log = "./test0002/test0002.log.4"
value = [['total elapsed time',0,400,2],['FINAL',2.6557E-06,1e-06,7]]
Run("Test0002 Parallel",log,value)



#Example Cases tested for time elapsed
#Example turbJet is too big(?) and doesn't work at all
#2D/EDDY serial
log = "../examples/2D/EDDY/eddy_uv.log.1"
value = [['total elapsed time',0,108,2]]
Run("Example 2D/EDDY- Serial",log,value)
   
#2D/EDDY parallel
log = "../examples/2D/EDDY/eddy_uv.log.4"
value = [['total elapsed time',0,37.3,2]]
Run("Example 2D/EDDY- Parallel",log,value)


#axi
log = "../examples/axi/axi.log.1"
value = [['total elapsed time',0,6,2]]
Run("Example axi- Serial",log,value)

log = "../examples/axi/axi.log.4"
value = [['total elapsed time',0,16.6,2]]
Run("Example axi- Parallel",log,value)



#free_surf
log = "../examples/free_surf/fs_growth.log.1"
value = [['total elapsed time',0,53.3,2]]
Run("Example fs_growth- Serial",log,value)

log = "../examples/free_surf/fs_growth.log.4"
value = [['total elapsed time',0,21,2]]
Run("Example fs_growth- Parallel",log,value)



#fs_2
log = "../examples/fs_2/st1.log.1"
value = [['total elapsed time',0,27.3,2]]
Run("Example st1- Serial",log,value)

log = "../examples/fs_2/st1.log.4"
value = [['total elapsed time',0,21.3,2]]
Run("Example st1- Parallel",log,value)

log = "../examples/fs_2/st2.log.1"
value = [['total elapsed time',0,31.2,2]]
Run("Example st2- Serial",log,value)

log = "../examples/fs_2/st2.log.4"
value = [['total elapsed time',0,26.1,2]]
Run("Example st2- Parallel",log,value)

log = "../examples/fs_2/std_wv.log.1"
value = [['total elapsed time',0,29,2]]
Run("Example std_wv- Serial",log,value)

log = "../examples/fs_2/std_wv.log.4"
value = [['total elapsed time',0,23.8,2]]
Run("Example std_wv- Parallel",log,value)



#kovasznay
log = "../examples/kovasznay/kov.log.1"
value = [['total elapsed time',0,20,2]]
Run("Example kov- Serial",log,value)

log = "../examples/kovasznay/kov.log.4"
value = [['total elapsed time',0,16,2]]
Run("Example kov- Parallel",log,value)



#lowMach_test
log = "../examples/lowMach_test/lowMach_test.log.1"
value = [['total elapsed time',0,53.8,2]]
Run("Example lowMach_test- Serial",log,value)

log = "../examples/lowMach_test/lowMach_test.log.4"
value = [['total elapsed time',0,19,2]]
Run("Example lowMach_test- Parallel",log,value)



#pipe
log = "../examples/pipe/helix.log.1"
value = [['total elapsed time',0,24.7,2]]
Run("Example helix- Serial",log,value)

log = "../examples/pipe/helix.log.4"
value = [['total elapsed time',0,40,2]]
Run("Example helix- Parallel",log,value)

log = "../examples/pipe/stenosis.log.1"
value = [['total elapsed time',0,33.2,2]]
Run("Example stenosis- Serial",log,value)

log = "../examples/pipe/stenosis.log.4"
value = [['total elapsed time',0,10.2,2]]
Run("Example stenosis- Parallel",log,value)



#turbChannel
log = "../examples/turbChannel/turbChannel.log.1"
value = [['total elapsed time',0,156,2]]
Run("Example turbChannel- Serial",log,value)

log = "../examples/turbChannel/turbChannel.log.4"
value = [['total elapsed time',0,50,2]]
Run("Example turbChannel- Parallel",log,value)


###############################################################################################
    
print("\n\nTest Summary :     %i/%i tests were successful"%(num_success,num_test))
print("End of top-down testing")  
