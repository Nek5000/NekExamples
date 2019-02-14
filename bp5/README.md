# BP5
This CEED benchmark solves a standard Poisson equation.
For more informations, see here: https://ceed.exascaleproject.org/bps

## How to run this example

### Step 1 - Generate mesh
* edit genbox.in and change number of elements in x,y,z 
* run genbox and rename box.re2 into bp5.re2 
* run genmap

### Step 2 - Build
* edit bp5.par and adjust parameters polynomialOder and/or minNumProcesses 
* run mkSIZE
* run makenek (make sure to compile with vector instructions like AVX)  

### Step 3 - Run
```
nekbmpi bp5 32
```
