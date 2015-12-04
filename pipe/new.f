c-----------------------------------------------------------------------
c
c     12/2/2015 Haomin Yuan
c
c     This is a test case for foamToNek mesh convertor. 
c     foamToNek converts mesh from OpenFOAM to Nek5000.
c
c     This is the .usr file for a 3D pipe, assuming
c     a unit-diameter pipe (in the y-z plane) with flow in the x direction.
c
c     diameter is 1.0, and length is 5.0. 
c
c     Periodic boundary conditions in x are assumed.
c
c     A parabolic profile velocity is specified as U = 0.25-r^2. (R=0.5)
c
c     The required forcing function, dp/dx, is given by:
c
c     A*dx*dp/dx = 2piR*dx*mu*(dU/dr|r=R)
c	  where A is pipe area, R is radius.
c
c          dp
c     ==>  -- = - 4 mu
c          dx
c
c-----------------------------------------------------------------------
      subroutine uservp (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
C
      udiff =0.
      utrans=0.
      return
      end
c-----------------------------------------------------------------------
      subroutine userf  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
c
      ffx = 0.0
      ffy = 0.0
      ffz = 0.0
      return
      end
c-----------------------------------------------------------------------
      subroutine userq  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
C
      qvol   = 0.0
      source = 0.0
      return
      end
c-----------------------------------------------------------------------
      subroutine userchk    ! called once per step
      include 'SIZE'
      include 'TOTAL'

      return
      end
c-----------------------------------------------------------------------
      subroutine userbc (i,j,k,eg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
      common /ogeom/ ox(lx1,ly1,lz1,lelv)
     $             , oy(lx1,ly1,lz1,lelv)
     $             , oz(lx1,ly1,lz1,lelv)
      integer e,eg
c
      e = gllel(eg)

      xo = ox(i,j,k,e)
      yo = oy(i,j,k,e)
      zo = oz(i,j,k,e)

      uy = 0.0
      uz = 0.0

      r2 = yo*yo + zo*zo
      ux = 0.25 - r2

      temp=0.0

      return
      end
c-----------------------------------------------------------------------
      subroutine useric (i,j,k,eg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
      common /ogeom/ ox(lx1,ly1,lz1,lelv)
     $             , oy(lx1,ly1,lz1,lelv)
     $             , oz(lx1,ly1,lz1,lelv)
      integer e,eg
c
      e = gllel(eg)

      xo = ox(i,j,k,e)
      yo = oy(i,j,k,e)
      zo = oz(i,j,k,e)

      uy = 0.0
      uz = 0.0

      r2 = yo*yo + zo*zo
      ux = 0.25 - r2

      temp=0.0

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat3
      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat
      include 'SIZE'
      include 'TOTAL'

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat2
      include 'SIZE'
      include 'TOTAL'

      return
      end
c-----------------------------------------------------------------------
c
c automatically added by makenek
      subroutine usrsetvert(glo_num,nel,nx,ny,nz) ! to modify glo_num
      integer*8 glo_num(1)
      return
      end
