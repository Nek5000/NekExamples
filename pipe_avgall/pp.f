c-----------------------------------------------------------------------
c
c     This usr file calculates the urms,vrms and wrms using the files
c     output by p1.usr.
c
c
c-----------------------------------------------------------------------
      subroutine uservp (ix,iy,iz,eg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
      integer e,f,eg

      udiff =0.
      utrans=0.
      return
      end
c-----------------------------------------------------------------------
      subroutine userf  (ix,iy,iz,eg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'

      integer e,f,eg
c     e = gllel(eg)


c     Note: this is an acceleration term, NOT a force!
c     Thus, ffx will subsequently be multiplied by rho(x,t).


      ffx = 0.0
      ffy = 0.0
      ffz = 0.0

      return
      end
c-----------------------------------------------------------------------
      subroutine userq  (ix,iy,iz,eg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'

      integer e,f,eg
      qvol   = 0.0

      return
      end
c-----------------------------------------------------------------------
      subroutine userchk
      include 'SIZE'
      include 'TOTAL'
      character*127 fname1,fname2

      fname1 = 'avg.list'
      fname2 = 'rms.list'
      nelxy = 224
      call getrms(fname1,fname2,nelxy)
      if (istep.eq.0) call exitt

      return
      end
c-----------------------------------------------------------------------
      subroutine getrms(fname1,fname2,nelxy)
      include 'SIZE'
      include 'TOTAL'
      real uk(lx1*ly1*lz1*lelt)
      real vk(lx1*ly1*lz1*lelt)
      real wk(lx1*ly1*lz1*lelt)
      real pk(lx1*ly1*lz1*lelt)
      integer gs_avg_hndl
      save    gs_avg_hndl
      data    gs_avg_hndl / 0 /
      integer lt,nelxy
      character*127 fname1,fname2

      lt = lx1*ly1*lz1*nelt
      ifld  = 1

ccc   avg all the avgp10.f0* files
      call auto_averager(fname1)

ccc   copy uk=vx**2, vk=vy**2, wk=vz**2
      call col3(uk,vx,vx,lt)
      call col3(vk,vy,vy,lt)
      call col3(wk,vz,vz,lt)

ccc   avg all the rmsp10.f0* files
      call auto_averager(fname2)

ccc   u'^2,v'^2,w'^2 = rms - avg**2
      call sub2(vx,uk,lt)
      call sub2(vy,vk,lt)
      call sub2(vz,wk,lt)

ccc   Average in the z direction
      call my_z_avg(uk,vx,gs_avg_hndl,nelxy,ifld)
      call my_z_avg(vk,vy,gs_avg_hndl,nelxy,ifld)
      call my_z_avg(wk,vz,gs_avg_hndl,nelxy,ifld)

ccc   TKE = 0.5*(u'^2+v'^2+w'^2)
      call add4(pk,uk,vk,wk,lt)
      call cmult(pk,0.5,lt)

ccc   output urms**2,vrms**2 and wrms**2 along with the TKE 
ccc   TKE is in pressure field
      call outpost(uk,vk,wk,pk,t,'   ')

      return
      end
c-----------------------------------------------------------------------
      subroutine userbc (ix,iy,iz,iside,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'

      ux=0.0
      uy=0.0
      uz=0.0
      temp=0.0



      return
      end
c-----------------------------------------------------------------------
      subroutine useric (ix,iy,iz,eg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
      integer e,eg
      common /mydomain/ zlength,radius

      xr = x/radius
      yr = y/radius
      rr = xr*xr + yr*yr
      if (rr.gt.0) rr=sqrt(rr)

      th = atan2(y,x)
      zo = 2*pi*z/zlength

      ux=0.0
      uy=0.0
      uz=6.*(1-rr**6)/5.

      temp=0

c     Assign a wiggly shear layer near the wall

      amp_z    = 0.35  ! Fraction of 2pi for z-based phase modification
      freq_z   = 4     ! Number of wiggles in axial- (z-) direction
      freq_t   = 9     ! Frequency of wiggles in azimuthal-direction

      amp_tht  = 5     ! Amplification factor for clipped sine function
      amp_clip = 0.2   ! Clipped amplitude

      blt      = 0.07  ! Fraction of boundary layer with momentum deficit

      phase_z = amp_z*(2*pi)*sin(freq_z*zo)

      arg_tht = freq_t*th + phase_z
      amp_sin = 5*sin(arg_tht)
      if (amp_sin.gt. amp_clip) amp_sin =  amp_clip
      if (amp_sin.lt.-amp_clip) amp_sin = -amp_clip

      if (rr.gt.(1-blt)) uz = uz + amp_sin

c     Quick P-independent randomizer

      big  = 1.e7*eg + 1.e6*ix + 1.e5*iy + 1.e4*iz
      rand = sin(big)
      uz   = uz + .01*rand
      ux   = ux + .05*rand*rand
      uy   = uy + .10*rand*rand*rand

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat
      include 'SIZE'
      include 'TOTAL'
      integer e,eg,f

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat2
      include 'SIZE'
      include 'TOTAL'
      common /mydomain/ zlength,radius

      integer e,f

      n = nx1*ny1*nz1*nelt

      call domain_size(xmin,xmax,ymin,ymax,zmin,zmax)
      zlength = zmax - zmin
      radius  = 0.5

      call fix_geom

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat3
      include 'SIZE'
      include 'TOTAL'
c
      return
      end
c-----------------------------------------------------------------------
      subroutine my_z_avg(ua,u,gs_avg_hndl,nelxy,ifld)
      include 'SIZE'
      include 'TOTAL'

      real u (lx1,ly1,lz1,lelt)
      real ua(lx1,ly1,lz1,lelt)

      integer gs_avg_hndl,e,ex,ey,ez,eg

      if (gs_avg_hndl.eq.0) then
          call set_gs_zavg_hndl(gs_avg_hndl,nelxy,ifld)
      endif

      nel = nelfld(ifld)
      n   = nx1*ny1*nz1*nel

      call copy(ua,bm1,n)              ! Set the averaging weights
      call fgslib_gs_op(gs_avg_hndl,ua,1,1,0) ! Sum weights over columns


      do i=1,n                          ! ua = (w_j*u_j)/( sum_i w_i)
         ua(i,1,1,1) = bm1(i,1,1,1)*u(i,1,1,1)/ua(i,1,1,1)
      enddo

      call fgslib_gs_op(gs_avg_hndl,ua,1,1,0) ! Sum weighted values


      return
      end
c-----------------------------------------------------------------------
      subroutine set_gs_zavg_hndl(gs_avg_hndl,nelxy,ifld)

c     Set the z-average handle

      include 'SIZE'
      include 'TOTAL'

      integer gs_avg_hndl,e,ex,ey,ez,eg

      common /nekmpi/ mid,mp,nekcomm,nekgroup,nekreal

      common /c_is1/ glo_num(lx1,ly1,lz1,lelv)
      integer*8 glo_num,ex_g


      nel = nelfld(ifld)
      do e=1,nel
         eg = lglel(e)
         call get_exyz(ex,ey,ez,eg,nelxy,1,1)

         ex_g = ex       ! Ensure int*8 promotion
         do k=1,nz1      ! Enumerate points in the x-y plane
            do j=1,ny1
            do i=1,nx1
               glo_num(i,j,k,e) = i+nx1*(j-1) + nx1*ny1*(ex_g-1)
            enddo
            enddo
         enddo

      enddo

      n = nel*nx1*ny1*nz1

      call fgslib_gs_setup(gs_avg_hndl,glo_num,n,nekcomm,mp)

      return
      end
c-----------------------------------------------------------------------

c automatically added by makenek
      subroutine usrsetvert(glo_num,nel,nx,ny,nz) ! to modify glo_num
      integer*8 glo_num(1)

      return
      end

c automatically added by makenek
      subroutine userqtl

      call userqtl_scig

      return
      end
