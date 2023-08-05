 module neighbor_list

  ! use helpers
  
  implicit none

contains

  pure subroutine pbc(r,box,hbox)
    double precision, intent(inout) :: r(:)
    double precision, intent(in)    :: box(:), hbox(:)
    where (abs(r) > hbox)
       r = r - sign(box,r)
    end where
  end subroutine pbc

  pure subroutine distance(i,j,pos,rij)
    integer, intent(in) :: i, j
    double precision, intent(in)    :: pos(:,:)
    double precision, intent(inout) :: rij(:)
    rij = pos(:,i) - pos(:,j)
  end subroutine distance

  pure subroutine dot(r1,r2,out)
    double precision, intent(in)  :: r1(:), r2(:)
    double precision, intent(out) :: out
    out = dot_product(r1,r2)
  end subroutine dot

  subroutine zero(x)
    double precision, intent(inout)  :: x(:,:)
    !$omp parallel workshare
    x = 0.d0
    !$omp end parallel workshare
  end subroutine zero

  subroutine compute(box,pos,ids,rcut,neighbors,number_neighbors,error)
    !! Compute neighbor lists using III Newton law
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:), rcut(:,:)
    integer,          intent(in)    :: ids(:)
    integer,          intent(inout) :: neighbors(:,:), number_neighbors(size(pos,2))
    logical,          intent(out)   :: error
    double precision                :: rij(size(pos,1)), rijsq, hbox(size(pos,1))
    integer                         :: i, j, isp, jsp
    error = .false.
    hbox = box / 2
    !$omp parallel default(private) firstprivate(rcut) shared(pos,ids,box,hbox,neighbors,number_neighbors,error)
    !$omp do schedule(runtime)
    do i = 1,size(pos,2)
       number_neighbors(i) = 0
       isp = ids(i)
       do j = i+1,size(pos,2)
          jsp = ids(j)
          call distance(i,j,pos,rij)
          call pbc(rij,box,hbox)
          call dot(rij,rij,rijsq)
          if (rijsq <= rcut(isp,jsp)**2) then
             number_neighbors(i) = number_neighbors(i) + 1
             if (number_neighbors(i) <= size(neighbors,1)) then
                neighbors(number_neighbors(i),i) = j
             else
                error = .true.
             end if
          end if
       end do
    end do
    !$omp end parallel
  end subroutine compute

  logical function need_update_largest(displacement, skin)
    !! Update is needed if the largest displacement exceeds 1/2
    !! of the Verlet skin (from Allen & Tildesley)
    real(8), intent(in) :: displacement(:,:), skin
    real(8) :: dr(size(displacement,2)), dr_max, dr_tmp
    integer ::i
    dr_max = 0.d0
    !$omp parallel do private(dr_tmp) schedule(static) reduction(max:dr_max)
    do i = 1,size(displacement,2)
       dr_tmp = dot_product(displacement(:,i),displacement(:,i))
       if (dr_tmp > dr_max) dr_max = dr_tmp
    end do
    need_update_largest = dr_max > (skin / 2)**2
  end function need_update_largest

  subroutine add_displacement(pos,pos_old,box,displacement)
    !! Add displacements of particles for a subset of particles specified by index.
    !! Assume that PBC has been applied, hence we need to refold them.
    real(8), intent(in)    :: pos(:,:)
    real(8), intent(inout) :: pos_old(:,:), displacement(:,:)
    real(8), intent(in)    :: box(:)
    real(8) :: hbox(size(box))
    integer :: i
    hbox = box / 2
    !$omp parallel do schedule(static)
    do i = 1,size(pos,2)
       displacement(:,i) = displacement(:,i) + pos(:,i) - pos_old(:,i)
       call pbc(displacement(:,i),box,hbox)
       pos_old(:,i) = pos(:,i)
    end do
  end subroutine add_displacement
  
end module neighbor_list

