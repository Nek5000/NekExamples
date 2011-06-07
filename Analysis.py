#! /usr/bin/python
# Python module to run top-down tests for Nek

import sys
import os

###############################################################################
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
                       if (testvalue != 0.0) :                          #Checks that it is not 0.0(failure)
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
    
###############################################################################
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
###############################################################################
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

###############################################################################
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

###############################################################################
num_test = 0 
num_success = 0
print("Beginning of top-down testing\n\n")
print("    . : successful test, F : failed test\n\n")
###############################################################################
#---------------------Tools----------------------------------------------------
#---------------------Tests----------------------------------------------------
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
###############################################################################
#---------------------MPI------------------------------------------------------
#---------------------Pn-Pn----------------------------------------------------
print("\nTest0001")  
#MPI
log = "./mpiLog/test0001.log.1"
value = [['ANS1',5.742723E-07,1e-06,8], 
         ['gmres: ',32,3,6]]
Run("Test0001/MPI: Serial",log,value)

log = "./mpiLog/test0001.log.4"
value = [['ANS1',5.742723E-07,1e-06,8],
         ['gmres: ',32,3,6]]
Run("Test0001/MPI: Parallel-error",log,value)
#MPI2
log = "./mpi2Log/test0001.log.1"
value = [['ANS1',5.742723E-07,1e-06,8],
         ['gmres: ',12,3,6]]
Run("Test0001/MPI2: Serial",log,value)

log = "./mpi2Log/test0001.log.4"
value = [['ANS1',5.742723E-07,1e-06,8],
         ['gmres: ',12,3,6]]
Run("Test0001/MPI2: Parallel-error",log,value)

print("\n\naxi Example")  
#MPI
log = "./mpiLog/axi.log.1"
value = [['PRES: ',73,3,4]]
Run("Example axi/MPI: Serial-iter",log,value)

log = "./mpiLog/axi.log.4"
value = [['PRES: ',73,3,4]]
Run("Example axi/MPI: Parallel-iter",log,value)
#PGI
log = "./pgiLog/axi.log.1"
value = [['total solver time',0.1,2,2],
         ['PRES: ',73,3,4]]
Run("Example axi/PGI: Serial-time/iter",log,value)
#GNU
log = "./gnuLog/axi.log.1"
value = [['PRES: ',73,3,4]]
Run("Example axi/GNU: Serial-iter",log,value)
#INT
log = "./intLog/axi.log.1"
value = [['PRES: ',73,3,4]]
Run("Example axi/INT: Serial-iter",log,value)
#MPI2
log = "./mpi2Log/axi.log.1"
value = [['U-Press ',101,3,5]]
Run("Example axi/MPI2: Serial-iter",log,value)

log = "./mpi2Log/axi.log.4"
value = [['U-Press ',101,3,5]]
Run("Example axi/MPI2: Parallel-iter",log,value)
#PGI2
log = "./pgi2Log/axi.log.1"
value = [['total solver time',0.1,4,2],
         ['U-Press ',101,3,5]]
Run("Example axi/PGI2: Serial-iter",log,value)
#GNU2
log = "./gnu2Log/axi.log.1"
value = [['U-Press ',101,3,5]]
Run("Example axi/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/axi.log.1"
value = [['U-Press ',101,3,5]]
Run("Example axi/INT2: Serial-iter",log,value)



print("\n\nbenard-ray_9 Example")  
#MPI
log = "./mpiLog/ray_9.log.1"
value = [['gmres: ',20,3,6]]
Run("Example benard/ray_9/MPI: Serial-iter",log,value)
#PGI
log = "./pgiLog/ray_9.log.1"
value = [['total solver time',0.1,30,2],
         ['gmres: ',20,3,6]]
Run("Example benard/ray_9/PGI: Serial-iter",log,value)
#GNU
log = "./gnuLog/ray_9.log.1"
value = [['gmres: ',20,3,6]]
Run("Example benard/ray_9/GNU: Serial-iter",log,value)
#INT
log = "./intLog/ray_9.log.1"
value = [['gmres: ',20,3,6]]
Run("Example benard/ray_9/INT: Serial-iter",log,value)
#MPI2
log = "./mpi2Log/ray_9.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_9/MPI2: Serial-iter",log,value)
#PGI2
log = "./pgi2Log/ray_9.log.1"
value = [['total solver time',0.1,40,2],
         ['gmres: ',8,3,6]]
Run("Example benard/ray_9/PGI2: Serial-time/iter",log,value)
#GNU2
log = "./gnu2Log/ray_9.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_9/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/ray_9.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_9/INT2: Serial-iter",log,value)


print("\n\nbenard-ray_dd Example")  
#MPI
log = "./mpiLog/ray_dd.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dd/MPI: Serial-iter",log,value)

log = "./mpiLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/MPI: Serial-error",log,value)
#PGI
log = "./pgiLog/ray_dd.log.1"
value = [['total solver time',0.1,24,2],
         ['gmres: ',8,3,6]]
Run("Example benard/ray_dd/PGI: Serial-time/iter",log,value)

log = "./pgiLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/ray_dd.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dd/GNU: Serial-iter",log,value)

log = "./gnuLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/GNU: Serial-error",log,value)
#INT
log = "./intLog/ray_dd.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dd/INT: Serial-iter",log,value)

log = "./intLog/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/ray_dd.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dd/MPI2: Serial-iter",log,value)

log = "./mpi2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/MPI2: Serial-error",log,value)
#PGI2
log = "./pgi2Log/ray_dd.log.1"
value = [['total solver time',0.1,20,2],
         ['gmres: ',8,3,6]]
Run("Example benard/ray_dd/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/ray_dd.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dd/GNU2: Serial-iter",log,value)

log = "./gnu2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/ray_dd.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dd/INT2: Serial-iter",log,value)

log = "./int2Log/benard.err"
value = [['ray_dd.log.1',1707.760,1,7]]
Run("Example benard/ray_dd/INT2: Serial-error",log,value)


print("\n\nbenard-ray_dn Example")  
#MPI
log = "./mpiLog/ray_dn.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dn/MPI: Serial-iter",log,value)

log = "./mpiLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/MPI: Serial-error",log,value)
#PGI
log = "./pgiLog/ray_dn.log.1"
value = [['total solver time',0.1,30,2],
         ['gmres: ',8,3,6]]
Run("Example benard/ray_dn/PGI: Serial-time/iter",log,value)

log = "./pgiLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/ray_dn.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dn/GNU: Serial-iter",log,value)

log = "./gnuLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/GNU: Serial-error",log,value)
#INT
log = "./intLog/ray_dn.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dn/INT: Serial-iter",log,value)

log = "./intLog/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/ray_dn.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dn/MPI2: Serial-iter",log,value)

log = "./mpi2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/MPI2: Serial-error",log,value)
#PGI2
log = "./pgi2Log/ray_dn.log.1"
value = [['total solver time',0.1,12,2],
         ['gmres: ',8,3,6]]
Run("Example benard/ray_dn/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/ray_dn.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dn/GNU2: Serial-iter",log,value)

log = "./gnu2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/ray_dn.log.1"
value = [['gmres: ',8,3,6]]
Run("Example benard/ray_dn/INT2: Serial-iter",log,value)

log = "./int2Log/benard.err"
value = [['ray_dn.log.1',1100.650,1,7]]
Run("Example benard/ray_dn/INT2: Serial-error",log,value)


print("\n\nbenard-ray_nn Example")  
#MPI
log = "./mpiLog/ray_nn.log.1"
value = [['gmres: ',11,3,6]]
Run("Example benard/ray_nn/MPI: Serial-iter",log,value)

log = "./mpiLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/MPI: Serial-error",log,value)
#PGI
log = "./pgiLog/ray_nn.log.1"
value = [['total solver time',0.1,30,2],
         ['gmres: ',11,3,6]]
Run("Example benard/ray_nn/PGI: Serial-time/iter",log,value)

log = "./pgiLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/ray_nn.log.1"
value = [['gmres: ',11,3,6]]
Run("Example benard/ray_nn/GNU: Serial-iter",log,value)

log = "./gnuLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/GNU: Serial-error",log,value)
#INT
log = "./intLog/ray_nn.log.1"
value = [['gmres: ',11,3,6]]
Run("Example benard/ray_nn/INT: Serial-iter",log,value)

log = "./intLog/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/ray_nn.log.1"
value = [['gmres: ',11,3,6]]
Run("Example benard/ray_nn/MPI2: Serial-iter",log,value)

log = "./mpi2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/MPI2: Serial-error",log,value)
#PGI2
log = "./pgi2Log/ray_nn.log.1"
value = [['total solver time',0.1,20,2],
         ['gmres: ',11,3,6]]
Run("Example benard/ray_nn/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/ray_nn.log.1"
value = [['gmres: ',11,3,6]]
Run("Example benard/ray_nn/GNU2: Serial-iter",log,value)

log = "./gnu2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/ray_nn.log.1"
value = [['gmres: ',11,3,6]]
Run("Example benard/ray_nn/INT2: Serial-iter",log,value)

log = "./int2Log/benard.err"
value = [['ray_nn.log.1',657.511,.1,7]]
Run("Example benard/ray_nn/INT2: Serial-error",log,value)



print("\n\nconj_ht Example")  
#MPI
log = "./mpiLog/conj_ht.log.1"
value = [['gmres: ',43,3,6]]
Run("Example conj_ht/MPI: Serial-iter",log,value)

log = "./mpiLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI: Serial-error",log,value)

log = "./mpiLog/conj_ht.log.4"
value = [['gmres: ',43,3,6]]
Run("Example conj_ht/MPI: Parallel-iter",log,value)

log = "./mpiLog/conj_ht.err.4"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/conj_ht.log.1"
value = [['total solver time',0.1,7,2],
         ['gmres: ',43,3,6]]
Run("Example conj_ht/PGI: Serial-time/iter",log,value)

log = "./pgiLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/conj_ht.log.1"
value = [['gmres: ',43,3,6]]
Run("Example conj_ht/GNU: Serial-iter",log,value)

log = "./gnuLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/GNU: Serial-error",log,value)
#INT
log = "./intLog/conj_ht.log.1"
value = [['gmres: ',43,3,6]]
Run("Example conj_ht/INT: Serial-iter",log,value)

log = "./intLog/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/conj_ht.log.1"
value = [['gmres: ',23,3,6]]
Run("Example conj_ht/MPI2: Serial-iter",log,value)

log = "./mpi2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI2: Serial-error",log,value)

log = "./mpi2Log/conj_ht.log.4"
value = [['gmres: ',23,3,6]]
Run("Example conj_ht/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/conj_ht.err.4"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/conj_ht.log.1"
value = [['total solver time',0.1,7,2],
         ['gmres: ',23,3,6]]
Run("Example conj_ht/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/conj_ht.log.1"
value = [['gmres: ',23,3,6]]
Run("Example conj_ht/GNU2: Serial-iter",log,value)

log = "./gnu2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/conj_ht.log.1"
value = [['gmres: ',23,3,6]]
Run("Example conj_ht/INT2: Serial-iter",log,value)

log = "./int2Log/conj_ht.err.1"
value = [['tmax',1.31190E+01,1e-06,2]]
Run("Example conj_ht/INT2: Serial-error",log,value)



print("\n\ncone016 Example")  
#MPI
log = "./mpiLog/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/MPI: Serial-error",log,value)

log = "./mpiLog/cone016.err.4"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/cone016.log.1"
value = [['total solver time',0.1,7,2]]
Run("Example cone016/PGI: Serial-time",log,value)

log = "./pgiLog/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/GNU: Serial-error",log,value)
#INT
log = "./intLog/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/MPI2: Serial-error",log,value)

log = "./mpi2Log/cone016.err.4"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/cone016.log.1"
value = [['total solver time',0.1,14,2]]
Run("Example cone016/PGI2: Serial-time",log,value)

log = "./pgi2Log/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/cone016.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone016/INT2: Serial-error",log,value)



print("\n\ncone064 Example")  
#MPI
log = "./mpiLog/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/MPI: Serial-error",log,value)

log = "./mpiLog/cone064.err.4"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/cone064.log.1"
value = [['total solver time',0.1,7,2]]
Run("Example cone064/PGI: Serial-time",log,value)

log = "./pgiLog/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/GNU: Serial-error",log,value)
#INT
log = "./intLog/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/MPI2: Serial-error",log,value)

log = "./mpi2Log/cone064.err.4"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/cone064.log.1"
value = [['total solver time',0.1,7,2]]
Run("Example cone064/PGI2: Serial-time",log,value)

log = "./pgi2Log/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/cone064.err.1"
value = [['Tmax',6.4755E-01,1e-06,2]]
Run("Example cone064/INT2: Serial-error",log,value)



print("\n\ncone256 Example")  
#MPI
log = "./mpiLog/cone256.err.1"
value = [['Tmax',3.6963E-01,1e-06,2]]
Run("Example cone256/MPI: Serial-error",log,value)

log = "./mpiLog/cone256.err.4"
value = [['Tmax',3.6963E-01,1e-06,2]]
Run("Example cone256/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/cone256.log.1"
value = [['total solver time',0.1,9,2]]
Run("Example cone256/PGI: Serial-time",log,value)

log = "./pgiLog/cone256.err.1"
value = [['Tmax',3.6963E-01,1e-06,2]]
Run("Example cone256/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/cone256.err.1"
value = [['Tmax',3.6963E-01,1e-06,2]]
Run("Example cone256/GNU: Serial-error",log,value)
#INT
log = "./intLog/cone256.err.1"
value = [['Tmax',3.6963E-01,1e-06,2]]
Run("Example cone256/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/cone256.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone256/MPI2: Serial-error",log,value)

log = "./mpi2Log/cone256.err.4"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone256/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/cone256.log.1"
value = [['total solver time',0.1,14,2]]
Run("Example cone256/PGI2: Serial-time",log,value)

log = "./pgi2Log/cone256.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone256/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/cone256.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone256/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/cone256.err.1"
value = [['Tmax',5.7669E-01,1e-06,2]]
Run("Example cone256/INT2: Serial-error",log,value)

print("\n\neddy Example")  
#MPI
log = "./mpiLog/eddy_uv.log.1"
value = [['gmres: ',31,3,6]]
Run("Example eddy/MPI: Serial-iter",log,value)

log = "./mpiLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/MPI: Serial-error",log,value)

log = "./mpiLog/eddy_uv.log.4"
value = [['gmres: ',31,3,6]]
Run("Example eddy/MPI: Parallel-iter",log,value)

log = "./mpiLog/eddy_uv.err.4"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/eddy_uv.log.1"
value = [['total solver time',0.1,80,2],
         ['gmres: ',31,3,6]]
Run("Example eddy/PGI: Serial-time/iter",log,value)

log = "./pgiLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/eddy_uv.log.1"
value = [['gmres: ',31,3,6]]
Run("Example eddy/GNU: Serial-iter",log,value)

log = "./gnuLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/GNU: Serial-error",log,value)
#INT
log = "./intLog/eddy_uv.log.1"
value = [['gmres: ',31,3,6]]
Run("Example eddy/INT: Serial-iter",log,value)

log = "./intLog/eddy_uv.err.1"
value = [['X err',6.007702E-07,1e-06,6],['Y err',6.489061E-07,1e-06,6]]
Run("Example eddy/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/eddy_uv.log.1"
value = [['gmres: ',19,3,6]]
Run("Example eddy/MPI2: Serial-iter",log,value)

log = "./mpi2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/MPI2: Serial-error",log,value)

log = "./mpi2Log/eddy_uv.log.4"
value = [['gmres: ',19,3,6]]
Run("Example eddy/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/eddy_uv.err.4"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/eddy_uv.log.1"
value = [['total solver time',0.1,80,2],
         ['gmres: ',19,3,6]]
Run("Example eddy/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/eddy_uv.log.1"
value = [['gmres: ',19,3,6]]
Run("Example eddy/GNU2: Serial-iter",log,value)

log = "./gnu2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/eddy_uv.log.1"
value = [['gmres: ',19,3,6]]
Run("Example eddy/INT2: Serial-iter",log,value)

log = "./int2Log/eddy_uv.err.1"
value = [['X err',6.759103E-05,1e-06,6],['Y err',7.842019E-05,1e-06,6]]
Run("Example eddy/INT2: Serial-error",log,value)


 
print("\n\neddy_neknek Example")  
#MPI
log = "./mpiLog/eddy_neknek.err.2"
value = [['X err  inside' ,4.550086E-04,1e-06,7],
         ['Y err  inside' ,6.630053E-04,1e-06,7],
         ['X err  outside',4.595605E-04,1e-06,7],
         ['Y err  outside',6.887475E-04,1e-06,7]]
Run("Example eddy_neknek/MPI: 2--error",log,value)

log = "./mpiLog/eddy_neknek.err.4"
value = [['X err  inside' ,4.550086E-04,1e-06,7],
         ['Y err  inside' ,6.630053E-04,1e-06,7],
         ['X err  outside',4.595605E-04,1e-06,7],
         ['Y err  outside',6.887475E-04,1e-06,7]]
Run("Example eddy_neknek/MPI: 4--error",log,value)
#MPI2
log = "./mpi2Log/eddy_neknek.err.2"
value = [['X err  inside' ,3.925388E-03,1e-06,7],
         ['Y err  inside' ,6.299443E-03,1e-06,7],
         ['X err  outside',6.604101E-04,1e-06,7],
         ['Y err  outside',7.844337E-04,1e-06,7]]
Run("Example eddy_neknek/MPI2: 2--error",log,value)

log = "./mpi2Log/eddy_neknek.err.4"
value = [['X err  inside' ,3.925388E-03,1e-06,7],
         ['Y err  inside' ,6.299443E-03,1e-06,7],
         ['X err  outside',6.604101E-04,1e-06,7],
         ['Y err  outside',7.844337E-04,1e-06,7]]
Run("Example eddy_neknek/MPI2: 4--error",log,value)



print("\n\next_cyl Example")  
#MPI 
log = "./mpiLog/ext_cyl.log.1"
value = [['gmres: ',82,3,6]]
Run("Example ext_cyl/MPI: Serial-iter",log,value)

log = "./mpiLog/ext_cyl.err.1"
value = [['dragx',1.2138790E+00,1e-06,4],['dragy',1.3040301E-07,1e-06,4]]
Run("Example ext_cyl/MPI: Serial-error",log,value)

log = "./mpiLog/ext_cyl.log.4"
value = [['gmres: ',82,3,6]]
Run("Example ext_cyl/MPI: Parallel-iter",log,value)

log = "./mpiLog/ext_cyl.err.4"
value = [['dragx',1.2138790E+00,1e-06,4],['dragy',1.3040301E-07,1e-06,4]]
Run("Example ext_cyl/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/ext_cyl.log.1"
value = [['total solver time',0.1,400,2],
         ['gmres: ',82,3,6]]
Run("Example ext_cyl/PGI: Serial-time/iter",log,value)

log = "./pgiLog/ext_cyl.err.1"
value = [['dragx',1.2138790E+00,1e-06,4],['dragy',1.3040301E-07,1e-06,4]]
Run("Example ext_cyl/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/ext_cyl.log.1"
value = [['gmres: ',82,3,6]]
Run("Example ext_cyl/GNU: Serial-iter",log,value)

log = "./gnuLog/ext_cyl.err.1"
value = [['dragx',1.2138790E+00,1e-06,4],['dragy',1.3040301E-07,1e-06,4]]
Run("Example ext_cyl/GNU: Serial-error",log,value)
#INT
log = "./intLog/ext_cyl.log.1"
value = [['gmres: ',82,3,6]]
Run("Example ext_cyl/INT: Serial-iter",log,value)

log = "./intLog/ext_cyl.err.1"
value = [['dragx',1.2138790E+00,1e-06,4],['dragy',1.3040301E-07,1e-06,4]]
Run("Example ext_cyl/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/ext_cyl.log.1"
value = [['gmres: ',23,3,6]]
Run("Example ext_cyl/MPI2: Serial-iter",log,value)

log = "./mpi2Log/ext_cyl.err.1"
value = [['dragx',1.2138878E+00,1e-05,4],['dragy',3.2334222E-07,1e-06,4]]
Run("Example ext_cyl/MPI2: Serial-error",log,value)

log = "./mpi2Log/ext_cyl.log.4"
value = [['gmres: ',23,3,6]]
Run("Example ext_cyl/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/ext_cyl.err.4"
value = [['dragx',1.2138878E+00,1e-05,4],['dragy',3.2334222E-07,1e-06,4]]
Run("Example ext_cyl/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/ext_cyl.log.1"
value = [['total solver time',0.1,380,2],
         ['gmres: ',23,3,6]]
Run("Example ext_cyl/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/ext_cyl.err.1"
value = [['dragx',1.2138878E+00,1e-05,4],['dragy',3.2334222E-07,1e-06,4]]
Run("Example ext_cyl/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/ext_cyl.log.1"
value = [['gmres: ',23,3,6]]
Run("Example ext_cyl/GNU2: Serial-iter",log,value)

log = "./gnu2Log/ext_cyl.err.1"
value = [['dragx',1.2138878E+00,1e-05,4],['dragy',3.2334222E-07,1e-06,4]]
Run("Example ext_cyl/GNU2: Serial-error",log,value)
#INT
log = "./int2Log/ext_cyl.log.1"
value = [['gmres: ',23,3,6]]
Run("Example ext_cyl/INT2: Serial-iter",log,value)

log = "./int2Log/ext_cyl.err.1"
value = [['dragx',1.2138878E+00,1e-05,4],['dragy',3.2334222E-07,1e-06,4]]
Run("Example ext_cyl/INT2: Serial-error",log,value)



print("\n\nfs_2-st1 Example")  
#MPI 
log = "./mpiLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/MPI: Serial",log,value)

log = "./mpiLog/st1.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/PGI: Serial",log,value)
#GNU
log = "./gnuLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/GNU: Serial",log,value)
#INT
log = "./intLog/st1.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st1/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/st1.log.1"
value = [['gmres: ',35,3,6]]
Run("Example st1/MPI2: Serial-iter",log,value)

log = "./mpi2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/MPI2: Serial-error",log,value)

log = "./mpi2Log/st1.log.4"
value = [['gmres: ',35,3,6]]
Run("Example st1/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/st1.err.4"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/st1.log.1"
value = [['total solver time',0.1,18.3,2],
         ['gmres: ',35,3,6]]
Run("Example st1/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/st1.log.1"
value = [['gmres: ',35,3,6]]
Run("Example st1/GNU2: Serial-iter",log,value)

log = "./gnu2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/st1.log.1"
value = [['gmres: ',35,3,6]]
Run("Example st1/INT2: Serial-iter",log,value)

log = "./int2Log/st1.err.1"
value = [['amp',6.382536E-01,1e-06,2]]
Run("Example st1/INT2: Serial-error",log,value)


print("\n\nfs_2-st2 Example")  
#MPI 
log = "./mpiLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/MPI: Serial",log,value)

log = "./mpiLog/st2.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/PGI: Serial",log,value)
#GNU
log = "./gnuLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/GNU: Serial",log,value)
#INT
log = "./intLog/st2.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example st2/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/st2.log.1"
value = [['gmres: ',35,3,6]]
Run("Example st2/MPI2: Serial-iter",log,value)

log = "./mpi2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/MPI2: Serial-error",log,value)

log = "./mpi2Log/st2.log.4"
value = [['gmres: ',35,3,6]]
Run("Example st2/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/st2.err.4"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/st2.log.1"
value = [['total solver time',0.1,23,2],
         ['gmres: ',35,3,6]]
Run("Example st2/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/st2.log.1"
value = [['gmres: ',35,3,6]]
Run("Example st2/GNU2: Serial-iter",log,value)

log = "./gnu2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/st2.log.1"
value = [['gmres: ',35,3,6]]
Run("Example st2/INT2: Serial-iter",log,value)

log = "./int2Log/st2.err.1"
value = [['amp',6.376303E-01,1e-06,2]]
Run("Example st2/INT2: Serial-error",log,value)


print("\n\nfs_2-std_wv Example")  
#MPI 
log = "./mpiLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/MPI: Serial",log,value)

log = "./mpiLog/std_wv.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/PGI: Serial",log,value)
#GNU
log = "./gnuLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/GNU: Serial",log,value)
#INT
log = "./intLog/std_wv.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example std_wv/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/std_wv.log.1"
value = [['gmres: ',17,3,6]]
Run("Example std_wv/MPI2: Serial-iter",log,value)

log = "./mpi2Log/std_wv.err.1"
value = [['amp',1.403051E-01,1e-06,2]]
Run("Example std_wv/MPI2: Serial-error",log,value)

log = "./mpi2Log/std_wv.log.4"
value = [['gmres: ',17,3,6]]
Run("Example std_wv/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/std_wv.err.4"
value = [['amp',1.403051E-01,1e-06,2]]
Run("Example std_wv/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/std_wv.log.1"
value = [['total solver time',0.1,21,2],
         ['gmres: ',17,3,6]]
Run("Example std_wv/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/std_wv.err.1"
value = [['amp',1.403051E-01,1e-06,2]]
Run("Example std_wv/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/std_wv.log.1"
value = [['gmres: ',17,3,6]]
Run("Example std_wv/GNU2: Serial-iter",log,value)

log = "./gnu2Log/std_wv.err.1"
value = [['amp',1.403051E-01,1e-06,2]]
Run("Example std_wv/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/std_wv.log.1"
value = [['gmres: ',17,3,6]]
Run("Example std_wv/INT2: Serial-iter",log,value)

log = "./int2Log/std_wv.err.1"
value = [['amp',1.403051E-01,1e-06,2]]
Run("Example std_wv/INT2: Serial-error",log,value)



print("\n\nfs_hydro Example")  
#MPI
log = "./mpiLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/MPI: Serial",log,value)

log = "./mpiLog/fs_hydro.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/PGI: Serial",log,value)
#GNU
log = "./gnuLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/GNU: Serial",log,value)
#INT
log = "./intLog/fs_hydro.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example fs_hydro/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/fs_hydro.log.1"
value = [['gmres: ',105,3,6]]
Run("Example fs_hydro/MPI2: Serial-iter",log,value)

log = "./mpi2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/MPI2: Serial-error",log,value)

log = "./mpi2Log/fs_hydro.log.4"
value = [['gmres: ',105,3,6]]
Run("Example fs_hydro/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/fs_hydro.err.4"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/fs_hydro.log.1"
value = [['total solver time',0.1,200,2],
         ['gmres: ',105,3,6]]
Run("Example fs_hydro/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/fs_hydro.log.1"
value = [['gmres: ',105,3,6]]
Run("Example fs_hydro/GNU2: Serial-iter",log,value)

log = "./gnu2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/fs_hydro.log.1"
value = [['gmres: ',105,3,6]]
Run("Example fs_hydro/INT2: Serial-iter",log,value)

log = "./int2Log/fs_hydro.err.1"
value = [['AMP',-6.4616452E-05,2e-03,2]]
Run("Example fs_hydro/INT2: Serial-error",log,value)



print("\n\nkovasznay Example")  
#MPI
log = "./mpiLog/kov.log.1"
value = [['gmres: ',31,3,6]]
Run("Example kov/MPI: Serial-iter",log,value)

log = "./mpiLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/MPI: Serial-error",log,value)

log = "./mpiLog/kov.log.4"
value = [['gmres: ',31,3,6]]
Run("Example kov/MPI: Parallel-iter",log,value)

log = "./mpiLog/kov.err.4"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/kov.log.1"
value = [['total solver time',0.1,12,2],
         ['gmres: ',31,3,6]]
Run("Example kov/PGI: Serial-time/iter",log,value)

log = "./pgiLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/kov.log.1"
value = [['gmres: ',31,3,6]]
Run("Example kov/GNU: Serial-iter",log,value)

log = "./gnuLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/GNU: Serial-error",log,value)
#INT
log = "./intLog/kov.log.1"
value = [['gmres: ',31,3,6]]
Run("Example kov/INT: Serial-iter",log,value)

log = "./intLog/kov.err.1"
value = [['err',5.14316E-13,1e-06,3]]
Run("Example kov/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/kov.log.1"
value = [['gmres: ',11,3,6]]
Run("Example kov/MPI2: Serial-iter",log,value)

log = "./mpi2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/MPI2: Serial-error",log,value)

log = "./mpi2Log/kov.log.4"
value = [['gmres: ',11,3,6]]
Run("Example kov/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/kov.err.4"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/kov.log.1"
value = [['total solver time',0.1,17,2],
         ['gmres: ',11,3,6]]
Run("Example kov/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/kov.log.1"
value = [['gmres: ',11,3,6]]
Run("Example kov/GNU2: Serial-iter",log,value)

log = "./gnu2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/kov.log.1"
value = [['gmres: ',11,3,6]]
Run("Example kov/INT2: Serial-iter",log,value)

log = "./int2Log/kov.err.1"
value = [['err',5.90551E-13,1e-06,3]]
Run("Example kov/INT2: Serial-error",log,value)



print("\n\nlowMach_test Example")  
#MPI
log = "./mpiLog/lowMach_test.log.1"
value = [['gmres: ',97,3,6]]
Run("Example lowMach_test/MPI: Serial-iter",log,value)

log = "./mpiLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/MPI: Serial-error",log,value)

log = "./mpiLog/lowMach_test.log.4"
value = [['gmres: ',97,3,6]]
Run("Example lowMach_test/MPI: Parallel-iter",log,value)

log = "./mpiLog/lowMach_test.err.4"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/lowMach_test.log.1"
value = [['total solver time',0.1,40,2],
         ['gmres: ',97,3,6]]
Run("Example lowMach_test/PGI: Serial-time/iter",log,value)

log = "./pgiLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/lowMach_test.log.1"
value = [['gmres: ',97,3,6]]
Run("Example lowMach_test/GNU: Serial-iter",log,value)

log = "./gnuLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/GNU: Serial-error",log,value)
#INT
log = "./intLog/lowMach_test.log.1"
value = [['gmres: ',97,3,6]]
Run("Example lowMach_test/INT: Serial-iter",log,value)

log = "./intLog/lowMach_test.err.1"
value = [['VX',2.4635E-09,1e-06,5],['T',4.5408E-12,1e-06,5],['QTL',2.6557E-06,1e-06,5]]
Run("Example lowMach_test/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/MPI2: Serial",log,value)

log = "./mpi2Log/lowMach_test.log.4"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/MPI2: Parallel",log,value)
#PGI2
log = "./pgi2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/PGI2: Serial",log,value)
#GNU2
log = "./gnu2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/GNU2: Serial",log,value)
#INT2
log = "./int2Log/lowMach_test.log.1"
value = "ABORT: For lowMach,"
FindPhrase("Example lowMach_test/INT2: Serial",log,value)



print("\n\nmhd-gpf Example")  
#MPI
log = "./mpiLog/gpf.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf/MPI: Serial",log,value)

log = "./mpiLog/gpf.log.4"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/gpf.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf/PGI: Serial",log,value)
#GNU
log = "./gnuLog/gpf.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf/GNU: Serial",log,value)
#INT
log = "./intLog/gpf.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/gpf.log.1"
value = [['gmres: ',12,3,6]]
Run("Example MHD-gpf/MPI2: Serial-iter",log,value)

log = "./mpi2Log/gpf.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf/MPI2: Serial-error",log,value)

log = "./mpi2Log/gpf.log.4"
value = [['gmres: ',12,3,6]]
Run("Example MHD-gpf/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/gpf.err.4"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/gpf.log.1"
value = [['total solver time',0.1,130,2],
         ['gmres: ',12,3,6]]
Run("Example MHD-gpf/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/gpf.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/gpf.log.1"
value = [['gmres: ',12,3,6]]
Run("Example MHD-gpf/GNU2: Serial-iter",log,value)

log = "./gnu2Log/gpf.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/gpf.log.1"
value = [['gmres: ',12,3,6]]
Run("Example MHD-gpf/INT2: Serial-iter",log,value)

log = "./int2Log/gpf.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf/INT2: Serial-error",log,value)


print("\n\nmhd-gpf_m Example")  
#MPI
log = "./mpiLog/gpf_m.log.1"
value = "ERROR: FDM"
FindPhrase("Example MHD-gpf_m/MPI: Serial",log,value)

log = "./mpiLog/gpf_m.log.4"
value = "ERROR: FDM"
FindPhrase("Example MHD-gpf_m/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/gpf_m.log.1"
value = "ERROR: FDM"
FindPhrase("Example MHD-gpf_m/PGI: Serial",log,value)
#GNU
log = "./gnuLog/gpf_m.log.1"
value = "ERROR: FDM"
FindPhrase("Example MHD-gpf_m/GNU: Serial",log,value)
#INT
log = "./intLog/gpf_m.log.1"
value = "ERROR: FDM"
FindPhrase("Example MHD-gpf_m/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/gpf_m.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_m/MPI2: Serial-error",log,value)

log = "./mpi2Log/gpf_m.err.4"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_m/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/gpf_m.log.1"
value = [['total solver time',0.1,130,2]]
Run("Example MHD-gpf_m/PGI2: Serial-time",log,value)

log = "./pgi2Log/gpf_m.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_m/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/gpf_m.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_m/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/gpf_m.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_m/INT2: Serial-error",log,value)


print("\n\nmhd-gpf_b Example")  
#MPI
log = "./mpiLog/gpf_b.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf_b/MPI: Serial",log,value)

log = "./mpiLog/gpf_b.log.4"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf_b/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/gpf_b.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf_b/PGI: Serial",log,value)
#GNU
log = "./gnuLog/gpf_b.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf_b/GNU: Serial",log,value)
#INT
log = "./intLog/gpf_b.log.1"
value = "ABORT: MHD"
FindPhrase("Example MHD-gpf_b/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/gpf_b.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_b/MPI2: Serial-error",log,value)

log = "./mpi2Log/gpf_b.err.4"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_b/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/gpf_b.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_b/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/gpf_b.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_b/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/gpf_b.log.1"
value = [['total solver time',0.1,130,2]]
Run("Example MHD-gpf_b/INT2: Serial-time",log,value)

log = "./int2Log/gpf_b.err.1"
value = [['rtavg_gr_Em', 2.56712250E-01,.02,4]]
Run("Example MHD-gpf_b/INT2: Serial-error",log,value)



print("\n\nmoab Example")  
#MPI
log = "./mpiLog/pipe.log.1"
value = [['gmres: ',35,3,6]]
Run("Example moab/MPI: Serial-iter",log,value)

log = "./mpiLog/pipe.log.4"
value = [['gmres: ',35,3,6]]
Run("Example moab/MPI: Parallel-iter",log,value)
#PGI
log = "./pgiLog/pipe.log.1"
value = [['total solver time',0.1,180,2],
         ['gmres: ',35,3,6]]
Run("Example moab/PGI: Serial-time/iter",log,value)
#GNU
log = "./gnuLog/pipe.log.1"
value = [['gmres: ',35,3,6]]
Run("Example moab/GNU: Serial-iter",log,value)
#INT
log = "./intLog/pipe.log.1"
value = [['gmres: ',35,3,6]]
Run("Example moab/INT: Serial-iter",log,value)
#MPI2
log = "./mpi2Log/pipe.log.1"
value = [['gmres: ',19,3,6]]
Run("Example moab/MPI2: Serial-iter",log,value)

log = "./mpi2Log/pipe.log.4"
value = [['gmres: ',19,3,6]]
Run("Example moab/MPI2: Parallel-iter",log,value)
#PGI2
log = "./pgi2Log/pipe.log.1"
value = [['total solver time',0.1,180,2],
         ['gmres: ',19,3,6]]
Run("Example moab/PGI2: Serial-time/iter",log,value)
#GNU2
log = "./gnu2Log/pipe.log.1"
value = [['gmres: ',19,3,6]]
Run("Example moab/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/pipe.log.1"
value = [['gmres: ',19,3,6]]
Run("Example moab/INT2: Serial-iter",log,value)



print("\n\nos7000 Example")  
#MPI
log = "./mpiLog/u3_t020_n13.log.1"
value = [['gmres: ',206,3,6]]
Run("Example os7000/MPI: Serial-iter",log,value)

log = "./mpiLog/u3_t020_n13.err.1"
value = [['egn',4.74797903E-05,1e-06,2]]
Run("Example os7000/MPI: Serial-error",log,value)

log = "./mpiLog/u3_t020_n13.log.4"
value = [['gmres: ',206,3,6]]
Run("Example os7000/MPI: Parallel-iter",log,value)

log = "./mpiLog/u3_t020_n13.err.4"
value = [['egn',4.74797903E-05,1e-06,2]]
Run("Example os7000/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/u3_t020_n13.log.1"
value = [['total solver time',0.1,40,2],
         ['gmres: ',206,3,6]]
Run("Example os7000/PGI: Serial-time/iter",log,value)

log = "./mpiLog/u3_t020_n13.err.1"
value = [['egn',4.74797903E-05,1e-06,2]]
Run("Example os7000/MPI: Serial-error",log,value)
#GNU
log = "./gnuLog/u3_t020_n13.log.1"
value = [['gmres: ',206,3,6]]
Run("Example os7000/GNU: Serial-iter",log,value)

log = "./gnuLog/u3_t020_n13.err.1"
value = [['egn',4.74797903E-05,1e-06,2]]
Run("Example os7000/GNU: Serial-error",log,value)
#INT
log = "./intLog/u3_t020_n13.log.1"
value = [['gmres: ',206,3,6]]
Run("Example os7000/INT: Serial-iter",log,value)

log = "./intLog/u3_t020_n13.err.1"
value = [['egn',4.74797903E-05,1e-06,2]]
Run("Example os7000/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/u3_t020_n13.log.1"
value = [['gmres: ',28,3,6]]
Run("Example os7000/MPI2: Serial-iter",log,value)

log = "./mpi2Log/u3_t020_n13.err.1"
value = [['egn',5.93471252E-05,1e-06,2]]
Run("Example os7000/MPI2: Serial-error",log,value)
    
log = "./mpi2Log/u3_t020_n13.log.4"
value = [['gmres: ',28,3,6]]
Run("Example os7000/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/u3_t020_n13.err.4"
value = [['egn',5.93471252E-05,1e-06,2]]
Run("Example os7000/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/u3_t020_n13.log.1"
value = [['total solver time',0.1,40,2],
         ['gmres: ',28,3,6]]
Run("Example os7000/PGI2: Serial-iter",log,value)

log = "./pgi2Log/u3_t020_n13.err.1"
value = [['egn',5.93471252E-05,1e-06,2]]
Run("Example os7000/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/u3_t020_n13.log.1"
value = [['gmres: ',28,3,6]]
Run("Example os7000/GNU2: Serial-iter",log,value)

log = "./gnu2Log/u3_t020_n13.err.1"
value = [['egn',5.93471252E-05,1e-06,2]]
Run("Example os7000/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/u3_t020_n13.log.1"
value = [['gmres: ',28,3,6]]
Run("Example os7000/int2: Serial-iter",log,value)

log = "./int2Log/u3_t020_n13.err.1"
value = [['egn',5.93471252E-05,1e-06,2]]
Run("Example os7000/int2: Serial-error",log,value)



print("\n\nperis Example")  
#MPI
log = "./mpiLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/MPI: Serial",log,value)

log = "./mpiLog/peris.log.4"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/PGI: Serial",log,value)
#GNU
log = "./gnuLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/GNU: Serial",log,value)
#INT
log = "./intLog/peris.log.1"
value = "ABORT: Moving boundary"
FindPhrase("Example peris/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/peris.log.1"
value = [['gmres: ',11,3,6]]
Run("Example peris/MPI2: Serial-iter",log,value)

log = "./mpi2Log/peris.log.4"
value = [['gmres: ',11,3,6]]
Run("Example peris/MPI2: Parallel-iter",log,value)
#PGI2
log = "./pgi2Log/peris.log.1"
value = [['total solver time',0.1,13,2],
         ['gmres: ',11,3,6]]
Run("Example peris/PGI2: Serial-time/iter",log,value)
#GNU2
log = "./gnu2Log/peris.log.1"
value = [['gmres: ',11,3,6]]
Run("Example peris/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/peris.log.1"
value = [['gmres: ',11,3,6]]
Run("Example peris/INT2: Serial-iter",log,value)



print("\n\npipe-helix Example")  
#MPI 
log = "./mpiLog/helix.log.1"
value = [['gmres: ',58,3,6]]
Run("Example helix/MPI: Serial-iter",log,value)

log = "./mpiLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/MPI: Serial-error",log,value)

log = "./mpiLog/helix.log.4"
value = [['gmres: ',58,3,6]]
Run("Example helix/MPI: Parallel-iter",log,value)

log = "./mpiLog/helix.err.4"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/MPI: Serial-error",log,value)
#PGI
log = "./pgiLog/helix.log.1"
value = [['total solver time',0.1,22,2],
         ['gmres: ',58,3,6]]
Run("Example helix/PGI: Serial-time/iter",log,value)

log = "./pgiLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/helix.log.1"
value = [['gmres: ',58,3,6]]
Run("Example helix/GNU: Serial-iter",log,value)

log = "./gnuLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/GNU: Serial-error",log,value)
#INT
log = "./intLog/helix.log.1"
value = [['gmres: ',58,3,6]]
Run("Example helix/INT: Serial-iter",log,value)

log = "./intLog/helix.err.1"
value = [['err2',1.9077617E+00,1e-06,2]]
Run("Example helix/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/helix.log.1"
value = [['gmres: ',120,3,6]]
Run("Example helix/MPI2: Serial-iter",log,value)

log = "./mpi2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/MPI2: Serial-error",log,value)

log = "./mpi2Log/helix.log.4"
value = [['gmres: ',120,3,6]]
Run("Example helix/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/helix.err.4"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/helix.log.1"
value = [['total solver time',0.1,22,2],
         ['gmres: ',120,3,6]]
Run("Example helix/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/helix.log.1"
value = [['gmres: ',120,3,6]]
Run("Example helix/GNU2: Serial-iter",log,value)

log = "./gnu2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/helix.log.1"
value = [['gmres: ',120,3,6]]
Run("Example helix/INT2: Serial-iter",log,value)

log = "./int2Log/helix.err.1"
value = [['err2',1.9072258E+00,1e-06,2]]
Run("Example helix/INT2: Serial-error",log,value)


print("\n\npipe-stenosis Example")  
#MPI 
log = "./mpiLog/stenosis.log.1"
value = [['gmres: ',193,3,6]]
Run("Example stenosis/MPI: Serial-iter",log,value)

log = "./mpiLog/stenosis.log.4"
value = [['gmres: ',193,3,6]]
Run("Example stenosis/MPI: Parallel-iter",log,value)
#PGI
log = "./pgiLog/stenosis.log.1"
value = [['total solver time',0.1,80,2],
         ['gmres: ',193,3,6]]
Run("Example stenosis/PGI: Serial-time/iter",log,value)
#GNU
log = "./gnuLog/stenosis.log.1"
value = [['gmres: ',193,3,6]]
Run("Example stenosis/GNU: Serial-iter",log,value)
#INT
log = "./intLog/stenosis.log.1"
value = [['gmres: ',193,3,6]]
Run("Example stenosis/INT: Serial-iter",log,value)
#MPI2
log = "./mpi2Log/stenosis.log.1"
value = [['gmres: ',48,3,6]]
Run("Example stenosis/MPI2: Serial-iter",log,value)

log = "./mpi2Log/stenosis.log.4"
value = [['gmres: ',48,3,6]]
Run("Example stenosis/MPI2: Parallel-iter",log,value)
#PGI2
log = "./pgi2Log/stenosis.log.1"
value = [['total solver time',0.1,40,2],
         ['gmres: ',48,3,6]]
Run("Example stenosis/PGI2: Serial-time/iter",log,value)
#GNU2
log = "./gnu2Log/stenosis.log.1"
value = [['gmres: ',48,3,6]]
Run("Example stenosis/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/stenosis.log.1"
value = [['gmres: ',48,3,6]]
Run("Example stenosis/INT2: Serial-iter",log,value)



print("\n\nrayleigh-ray1 Example")  
#MPI
log = "./mpiLog/ray1.log.1"
value = [['gmres: ',29,3,6]]
Run("Example ray1/MPI: Serial-iter",log,value)

log = "./mpiLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/MPI: Serial-error",log,value)

log = "./mpiLog/ray1.log.4"
value = [['gmres: ',29,3,6]]
Run("Example ray1/MPI: Parallel-iter",log,value)

log = "./mpiLog/ray1.err.4"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/ray1.log.1"
value = [['total solver time',0.1,3,2],
         ['gmres: ',29,3,6]]
Run("Example ray1/PGI: Serial-time/iter",log,value)

log = "./pgiLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/ray1.log.1"
value = [['gmres: ',29,3,6]]
Run("Example ray1/GNU: Serial-iter",log,value)

log = "./gnuLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/GNU: Serial-error",log,value)
#INT
log = "./intLog/ray1.log.1"
value = [['gmres: ',29,3,6]]
Run("Example ray1/INT: Serial-iter",log,value)

log = "./intLog/ray1.err.1"
value = [['umax',2.792052E-03,1e-05,3]]
Run("Example ray1/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/ray1.log.1"
value = [['gmres: ',8,3,6]]
Run("Example ray1/MPI2: Serial-iter",log,value)

log = "./mpi2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-05,3]]
Run("Example ray1/MPI2: Serial-error",log,value)

log = "./mpi2Log/ray1.log.4"
value = [['gmres: ',8,3,6]]
Run("Example ray1/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/ray1.err.4"
value = [['umax',3.897862E-03,1e-05,3]]
Run("Example ray1/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/ray1.log.1"
value = [['total solver time',0.1,3,2],
         ['gmres: ',8,3,6]]
Run("Example ray1/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/ray1.log.1"
value = [['gmres: ',8,3,6]]
Run("Example ray1/GNU2: Serial-iter",log,value)

log = "./gnu2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/ray1.log.1"
value = [['gmres: ',8,3,6]]
Run("Example ray1/INT2: Serial-iter",log,value)

log = "./int2Log/ray1.err.1"
value = [['umax',3.897862E-03,1e-06,3]]
Run("Example ray1/INT2: Serial-error",log,value)


print("\n\nrayleigh-ray2 Example")  
#MPI
log = "./mpiLog/ray2.log.1"
value = [['gmres: ',28,3,6]]
Run("Example ray2/MPI: Serial-iter",log,value)

log = "./mpiLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/MPI: Serial-error",log,value)

log = "./mpiLog/ray2.log.4"
value = [['gmres: ',28,3,6]]
Run("Example ray2/MPI: Parallel-iter",log,value)

log = "./mpiLog/ray2.err.4"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/ray2.log.1"
value = [['total solver time',0.1,3,2],
         ['gmres: ',28,3,6]]
Run("Example ray2/PGI: Serial-time/iter",log,value)

log = "./pgiLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/ray2.log.1"
value = [['gmres: ',28,3,6]]
Run("Example ray2/GNU: Serial-iter",log,value)

log = "./gnuLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/GNU: Serial-error",log,value)
#INT
log = "./intLog/ray2.log.1"
value = [['gmres: ',28,3,6]]
Run("Example ray2/INT: Serial-iter",log,value)

log = "./intLog/ray2.err.1"
value = [['umax',4.833071E-03,1e-05,3]]
Run("Example ray2/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/ray2.log.1"
value = [['gmres: ',8,3,6]]
Run("Example ray2/MPI2: Serial-iter",log,value)

log = "./mpi2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-05,3]]
Run("Example ray2/MPI2: Serial-error",log,value)

log = "./mpi2Log/ray2.log.4"
value = [['gmres: ',8,3,6]]
Run("Example ray2/MPI2: Parellel-iter",log,value)

log = "./mpi2Log/ray2.err.4"
value = [['umax',6.091663E-03,1e-05,3]]
Run("Example ray2/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/ray2.log.1"
value = [['total solver time',0.1,3,2],
         ['gmres: ',8,3,6]]
Run("Example ray2/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/ray2.log.1"
value = [['gmres: ',8,3,6]]
Run("Example ray2/GNU2: Serial-iter",log,value)

log = "./gnu2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/ray2.log.1"
value = [['gmres: ',8,3,6]]
Run("Example ray2/INT2: Serial-iter",log,value)

log = "./int2Log/ray2.err.1"
value = [['umax',6.091663E-03,1e-06,3]]
Run("Example ray2/INT2: Serial-error",log,value)



print("\n\nshear4-shear4 Example")  
#MPI 
log = "./mpiLog/shear4.log.1"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thick/MPI: Serial-iter",log,value)

log = "./mpiLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI: Serial-error",log,value)

log = "./mpiLog/shear4.log.4"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thick/MPI: Parallel-iter",log,value)

log = "./mpiLog/shear4.err.4"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/shear4.log.1"
value = [['total solver time',0.1,10,2],
         ['gmres: ',23,3,6]]
Run("Example shear4/thick/PGI: Serial-time/iter",log,value)

log = "./pgiLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/shear4.log.1"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thick/GNU: Serial-iter",log,value)

log = "./gnuLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/GNU: Serial-error",log,value)
#INT
log = "./intLog/shear4.log.1"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thick/INT: Serial-iter",log,value)

log = "./intLog/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/shear4.log.1"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thick/MPI2: Serial-iter",log,value)

log = "./mpi2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI2: Serial-error",log,value)

log = "./mpi2Log/shear4.log.4"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thick/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/shear4.err.4"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/shear4.log.1"
value = [['total solver time',0.1,10,2],
         ['gmres: ',14,3,6]]
Run("Example shear4/thick/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/shear4.log.1"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thick/GNU2: Serial-iter",log,value)

log = "./gnu2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/shear4.log.1"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thick/INT2: Serial-iter",log,value)

log = "./int2Log/shear4.err.1"
value = [['peak vorticity',3.031328E+01,1e-06,3]]
Run("Example shear4/thick/INT2: Serial-error",log,value)


print("\n\nshear4-thin Example")  
#MPI
log = "./mpiLog/thin.log.1"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thin/MPI: Serial-iter",log,value)

log = "./mpiLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/MPI: Serial-error",log,value)

log = "./mpiLog/thin.log.4"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thin/MPI: Parallel-iter",log,value)

log = "./mpiLog/thin.err.4"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/thin.log.1"
value = [['total solver time',0.1,10,2],
         ['gmres: ',23,3,6]]
Run("Example shear4/thin/PGI: Serial-time/iter",log,value)

log = "./pgiLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/thin.log.1"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thin/GNU: Serial-iter",log,value)

log = "./gnuLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/GNU: Serial-error",log,value)
#INT
log = "./intLog/thin.log.1"
value = [['gmres: ',23,3,6]]
Run("Example shear4/thin/INT: Serial-iter",log,value)

log = "./intLog/thin.err.1"
value = [['peak vorticity',9.991753E+01,1e-06,3]]
Run("Example shear4/thin/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/thin.log.1"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thin/MPI2: Serial-iter",log,value)

log = "./mpi2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/MPI2: Serial-error",log,value)

log = "./mpi2Log/thin.log.4"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thin/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/thin.err.4"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/thin.log.1"
value = [['total solver time',0.1,10,2],
         ['gmres: ',14,3,6]]
Run("Example shear4/thin/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/thin.log.1"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thin/GNU2: Serial-iter",log,value)

log = "./gnu2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/thin.log.1"
value = [['gmres: ',14,3,6]]
Run("Example shear4/thin/INT2: Serial-iter",log,value)

log = "./int2Log/thin.err.1"
value = [['peak vorticity',9.991556E+01,1e-06,3]]
Run("Example shear4/thin/INT2: Serial-error",log,value)



print("\n\nturbChannel Example")  
#MPI
log = "./mpiLog/turbChannel.log.1"
value = [['gmres: ',92,3,6]]
Run("Example turbChannel/MPI: Serial-iter",log,value)

log = "./mpiLog/turbChannel.log.4"
value = [['gmres: ',92,3,6]]
Run("Example turbChannel/MPI: Parallel-iter",log,value)
#PGI
log = "./pgiLog/turbChannel.log.1"
value = [['total solver time',0.1,200,2],
         ['gmres: ',92,3,6]]
Run("Example turbChannel/PGI: Serial-time/iter",log,value)
#GNU
log = "./gnuLog/turbChannel.log.1"
value = [['gmres: ',92,3,6]]
Run("Example turbChannel/GNU: Serial-iter",log,value)
#INT
log = "./intLog/turbChannel.log.1"
value = [['gmres: ',92,3,6]]
Run("Example turbChannel/INT: Serial-iter",log,value)
#MPI2
log = "./mpi2Log/turbChannel.log.1"
value = [['gmres: ',23,3,6]]
Run("Example turbChannel/MPI2: Serial-iter",log,value)

log = "./mpi2Log/turbChannel.log.4"
value = [['gmres: ',23,3,6]]
Run("Example turbChannel/MPI2: Parallel-iter",log,value)
#PGI2
log = "./pgi2Log/turbChannel.log.1"
value = [['total solver time',0.1,140,2],
         ['gmres: ',23,3,6]]
Run("Example turbChannel/PGI2: Serial-time/iter",log,value)
#GNU2
log = "./gnu2Log/turbChannel.log.1"
value = [['gmres: ',23,3,6]]
Run("Example turbChannel/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/turbChannel.log.1"
value = [['gmres: ',23,3,6]]
Run("Example turbChannel/INT2: Serial-iter",log,value)



print("\n\nvar_vis Example")  
#MPI 
log = "./mpiLog/var_vis.log.1"
value = "ABORT: Stress"
FindPhrase("Example var_vis/MPI: Serial",log,value)

log = "./mpiLog/var_vis.log.4"
value = "ABORT: Stress"
FindPhrase("Example var_vis/MPI: Parallel",log,value)
#PGI
log = "./pgiLog/var_vis.log.1"
value = "ABORT: Stress"
FindPhrase("Example var_vis/PGI: Serial",log,value)
#GNU
log = "./gnuLog/var_vis.log.1"
value = "ABORT: Stress"
FindPhrase("Example var_vis/GNU: Serial",log,value)
#INT
log = "./intLog/var_vis.log.1"
value = "ABORT: Stress"
FindPhrase("Example var_vis/INT: Serial",log,value)
#MPI2
log = "./mpi2Log/var_vis.log.1"
value = [['gmres: ',16,3,6]]
Run("Example var_vis/MPI2: Serial-iter",log,value)

log = "./mpi2Log/var_vis.log.4"
value = [['gmres: ',16,3,6]]
Run("Example var_vis/MPI2: Parallel-iter",log,value)
#PGI2
log = "./pgi2Log/var_vis.log.1"
value = [['total solver time',0.1,30,2],
         ['gmres: ',16,3,6]]
Run("Example var_vis/PGI2: Serial-time/iter",log,value)
#GNU2
log = "./gnu2Log/var_vis.log.1"
value = [['gmres: ',16,3,6]]
Run("Example var_vis/GNU2: Serial-iter",log,value)
#INT2
log = "./int2Log/var_vis.log.1"
value = [['gmres: ',16,3,6]]
Run("Example var_vis/INT2: Serial-iter",log,value)



print("\n\nvortex Example")  
#MPI
log = "./mpiLog/r1854a.log.1"
value = [['gmres: ',62,3,6]]
Run("Example vortex/MPI: Serial-int",log,value)

log = "./mpiLog/r1854a.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/MPI: Serial-error",log,value)

log = "./mpiLog/r1854a.log.4"
value = [['gmres: ',62,3,6]]
Run("Example vortex/MPI: Parallel-int",log,value)

log = "./mpiLog/r1854a.err.4"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/r1854a.log.1"
value = [['total solver time',0.1,60,2],
         ['gmres: ',62,3,6]]
Run("Example vortex/PGI: Serial-time/iter",log,value)

log = "./pgiLog/r1854a.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/r1854a.log.1"
value = [['gmres: ',62,3,6]]
Run("Example vortex/GNU: Serial-iter",log,value)

log = "./gnuLog/r1854a.err.1"
value = [['VMIN',-1.910312E-03,1e-06,2]]
Run("Example vortex/GNU: Serial-error",log,value)
#INT
log = "./intLog/r1854a.log.1"
value = [['gmres: ',58,3,6]]
Run("Example vortex/INT: Serial-iter",log,value)

log = "./intLog/r1854a.err.1"
value = [['VMIN',-1.910312E-03,1e-05,2]]
Run("Example vortex/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/r1854a.log.1"
value = [['gmres: ',14,3,6]]
Run("Example vortex/MPI2: Serial-iter",log,value)

log = "./mpi2Log/r1854a.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/MPI2: Serial-error",log,value)

log = "./mpi2Log/r1854a.log.4"
value = [['gmres: ',14,3,6]]
Run("Example vortex/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/r1854a.err.4"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/r1854a.log.1"
value = [['total solver time',0.1,50,2],
         ['gmres: ',14,3,6]]
Run("Example vortex/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/r1854a.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/r1854a.log.1"
value = [['gmres: ',14,3,6]]
Run("Example vortex/GNU2: Serial-iter",log,value)

log = "./gnu2Log/r1854a.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/r1854a.log.1"
value = [['gmres: ',14,3,6]]
Run("Example vortex/INT2: Serial-iter",log,value)

log = "./int2Log/r1854a.err.1"
value = [['VMIN',-1.839120E-03,1e-06,2]]
Run("Example vortex/INT2: Serial-error",log,value)



print("\n\nvortex2 Example")  
#MPI
#first nine time steps fail in pressure
log = "./mpiLog/v2d.log.1"
value = [['PRES:  ',97,3,4]]
Run("Example vortex2/MPI: Serial-iter",log,value)

log = "./mpiLog/v2d.err.1"
value = [['umin',-1.453402E-03,1e-06,2]]
Run("Example vortex2/MPI: Serial-error",log,value)

log = "./mpiLog/v2d.log.4"
value = [['PRES:  ',97,3,4]]
Run("Example vortex2/MPI: Parallel-iter",log,value)

log = "./mpiLog/v2d.err.4"
value = [['umin',-1.453402E-03,1e-06,2]]
Run("Example vortex2/MPI: Parallel-error",log,value)
#PGI
log = "./pgiLog/v2d.log.1"
value = [['total solver time',0.1,80,2],
         ['PRES: ',97,3,4]]
Run("Example vortex2/PGI: Serial-time/iter",log,value)

log = "./pgiLog/v2d.err.1"
value = [['umin',-1.453402E-03,1e-06,2]]
Run("Example vortex2/PGI: Serial-error",log,value)
#GNU
log = "./gnuLog/v2d.log.1"
value = [['PRES: ',97,3,4]]
Run("Example vortex2/GNU: Serial-iter",log,value)

log = "./gnuLog/v2d.err.1"
value = [['umin',-1.453402E-03,1e-06,2]]
Run("Example vortex2/GNU: Serial-error",log,value)
#INT
log = "./intLog/v2d.log.1"
value = [['PRES: ',97,3,4]]
Run("Example vortex2/INT: Serial-iter",log,value)

log = "./intLog/v2d.err.1"
value = [['umin',-1.453402E-03,1e-06,2]]
Run("Example vortex2/INT: Serial-error",log,value)
#MPI2
log = "./mpi2Log/v2d.log.1"
value = [['U-Press ',1,3,5]]
Run("Example vortex2/MPI2: Serial-iter",log,value)

log = "./mpi2Log/v2d.err.1"
value = [['umin',-2.448980E-03,1e-06,2]]
Run("Example vortex2/MPI2: Serial-error",log,value)

log = "./mpi2Log/v2d.log.4"
value = [['U-Press ',1,3,5]]
Run("Example vortex2/MPI2: Parallel-iter",log,value)

log = "./mpi2Log/v2d.err.4"
value = [['umin',-2.448980E-03,1e-06,2]]
Run("Example vortex2/MPI2: Parallel-error",log,value)
#PGI2
log = "./pgi2Log/v2d.log.1"
value = [['total solver time',0.1,80,2],
         ['U-Press ',1,3,5]]
Run("Example vortex2/PGI2: Serial-time/iter",log,value)

log = "./pgi2Log/v2d.err.1"
value = [['umin',-2.448980E-03,1e-06,2]]
Run("Example vortex2/PGI2: Serial-error",log,value)
#GNU2
log = "./gnu2Log/v2d.log.1"
value = [['U-Press ',1,3,5]]
Run("Example vortex2/GNU2: Serial-iter",log,value)

log = "./gnu2Log/v2d.err.1"
value = [['umin',-2.448980E-03,1e-06,2]]
Run("Example vortex2/GNU2: Serial-error",log,value)
#INT2
log = "./int2Log/v2d.log.1"
value = [['U-Press ',1,3,5]]
Run("Example vortex2/INT2: Serial-iter",log,value)

log = "./int2Log/v2d.err.1"
value = [['umin',-2.448980E-03,1e-06,2]]
Run("Example vortex2/INT2: Serial-error",log,value)
###############################################################################
###############################################################################
print("\n\nTest Summary :     %i/%i tests were successful"%(num_success,num_test))
print("End of top-down testing")
######################################################################
