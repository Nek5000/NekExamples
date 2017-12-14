# Implementations of turbulent inflow in nek5000

Som Dutta, Ketan Mittal and Paul Fischer
December 2017

In many cases, one requires the flow coming into the domain to be fully
turbulent. In general there are two ways to address the situation: 

Illustration:

	 ______________________ 
	 |                         | 
	 |    ---------------------|-----------------------------
	 |                         |
	 in ===>                   |                            out
	                           |
	      ---------------------|-----------------------------  
	               cross-section from which
	               flow is recycled

1. First by recycling the flow from a part of the domain, which is done by 
   mapping the flow from a cross-section to the inflow. This to an extent is
   simialar to having a periodic boundary condition 

   For implementing the recycling boundary condition, we can adopt two
   methodologies. 

   * The traditional method, which is turned on in the turbInflow.usr
     using the call to 

     set_inflow(nslab) 
     
     where nslab = number of "slabs" between the inflow and the
     cross-section from which the flow is recycled. 
     An important thing to remember about using this method is that
     the channel that is used for recycling has to be made using 
     genbox, and also the numbering of the elements of the channel
     has to start from the inflow.

     Example:
     In the current case the channel has 10 elements
     along the x-axis (see box file used to create the channel). 
     Thus, in order to map the velocity from the cross-section 
     at x=5, we have to use nslab = 5.

     Instead of 10 elements between x=0 to x=10, if there were
     100 equally placed elements. We would have to use 
     nslab = 50

   *  A recent implementation of the recycling boundary has been done
      using the fast interpolaotion routines  "fgslib_findpts_*", 
      and called using 

      set_inflow_fpt(dx,dy,dz,ubar)

      where dx,dy,dz is the vector between he inflow 
      cross-section and the section from which the velocity 
      is being mapped, and ubar is the mean inflow velocity.
      
      Example: 
      In this case, dx=5, dy=0 and dz=0

   The major advantage of the new implementaiton is that it does not require the
   use of genbox to create the mesh, which opens up the possibility of using 
   the recycling inflow for complex geometries. 

   There is no difference in accuracy between the two methods, though the
   traditional method might be slightly faster for larger problems.  

     
2. The second way to have a turbulent inflow is to use synthetic turblence.                           
   An implementation of synthetic turbulence is currently under construciton, 
   and will be added to the updates of this example in the near future. 
