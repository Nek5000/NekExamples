# Natural convection between the two concentric cylinders

This case demonstrates the application of Nek5000 to simulation of natural
convection between the two concentric cylinders as considered by:
* Grigull \& Hauf, _Proc. of the 3rd Int. Heat Transfer Conf. 2_, p. 182--195 (1966)
* M. Van Dyke _An Album of Fluid Motion_, Parabolic Press, Stanford, CA, 1982.

The inner cylinder (diameter _D/3_) is slightly heated with with 
respect to the outer one (diameter _D_). The Boussinesq approximation is used
to formulate the equations of motion, valid in situations where density
differences are small enough to be neglected everywhere except in the
gravitational forcing.  

Normalizing the Navier-Stokes and energy equations with 
* _D_ for the length scale 
* _D/U_ for the time scale (_U_ is the characteristic velocity in the given problem)
* _(T-T\_0)/(T_1-T\_0)_ nondimensional temperature, where T_0 and T_1 are the
respective temperatures of the outer and inner cylinders, the governing
nondimensional equations are
\begin{eqnarray}
\pp{\bu}{t} + \bu \cdot\nabla \bu &=&-\nabla p + \frac{1}{\sqrt{Gr}} \nabla^{2} \bu 
+ \theta,
\qquad
\nabla \bu=0  \\ \nonumber
\pp{\theta}{t} + \bu\cdot\nabla \theta&=&\frac{1}{\sqrt{Gr}\,Pr} 
\nabla^2 \theta \nonumber.
\end{eqnarray}
where two nondimensional parameters were introduced
\begin{equation}
Gr=\frac{\beta\,g\,(T_{1}-T_{0})\,D^{3}}{\nu^{2}},\hspace{.3in} 
Pr=\frac{\alpha}{\nu},
\end{equation}
denoting Grashof number and Prandtl number, respectively.
Here, $\bu$ is the velocity vector, $p$ is the pressure divided by density,
$\nu$ is the kinematic viscosity, $\alpha$ is the thermal diffusivity,
$\beta$ is the volumetric thermal expansion
coefficient, and $g$ is the acceleration due to gravity.  

The computational mesh for a steady-state result at $Gr$=$120,000$ and
$Pr=0.8$ is shown in Fig.~\ref{fig:2d_convection} (left). 
The simulations are run until the computational time $t\,D/U\sim1000$, by which
time a steady-state solution is obtained, indicated by the change in velocity
magnitude $\sim10^{-7}$ between successive time steps. The steady-state
streamlines and isotherms are visualized in Fig.~\ref{fig:2d_convection} 
center and right panels.  The results are in excellent agreement with the
results of Grigull \& Hauf that were published by Van Dyke.

\begin{figure}[b]
\centering

{\setlength{\unitlength}{1.0in}
   \begin{picture}(5.800,2.000)(0,0)
      \put(0.00,0.00){\begin{picture}(0,0)
        \put(0.00,0.00){\psfig{figure=2D_ANNULUS/grid.eps,angle=-90,width=1.8in}}
        \put(2.00,0.00){\psfig{figure=2D_ANNULUS/stream.eps,angle=-90,width=1.8in}}
        \put(4.00,0.00){\psfig{figure=2D_ANNULUS/temp.eps,angle=-90,width=1.8in}}
       \end{picture}}
   \end{picture}}
\caption{
2D natural convection:
(left) mesh with $E$=32 spectral elements;
(center) streamlines for $Gr$=120,000;
and
(right) isothermal lines.
}
\label{fig:2d_convection}
\end{figure}

