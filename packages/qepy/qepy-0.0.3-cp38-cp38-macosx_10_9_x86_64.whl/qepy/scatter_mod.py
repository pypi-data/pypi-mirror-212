"""
Module scatter_mod


Defined at scatter_mod.fpp lines 20-363

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging

_arrays = {}
_objs = {}

def fft_scatter_xy(self, f_in, f_aux, nxx_, isgn):
    """
    fft_scatter_xy(self, f_in, f_aux, nxx_, isgn)
    
    
    Defined at scatter_mod.fpp lines 46-86
    
    Parameters
    ----------
    desc : Fft_Type_Descriptor
    f_in : complex array
    f_aux : complex array
    nxx_ : int
    isgn : int
    
    -----------------------------------------------------------------------
     transpose of the fft xy planes across the desc%comm2 communicator
     a) From Y-oriented columns to X-oriented partial slices(isgn > 0)
        Active columns along the Y direction corresponding to a subset of the
        active X values and a range of Z values(in this order) are stored
        consecutively for each processor and are such that the subgroup owns
        all data for a range of Z values.
        The Y pencil -> X-oriented partial slices transposition is performed
        in the subgroup of processors(desc%comm2) owning this range of Z values.
        The transpose takes place in two steps:
        1) on each processor the columns are sliced into sections along Y
           that are stored one after the other. On each processor, slices for
           processor "iproc2" are desc%nr2p(iproc2)*desc%nr1p(me2)*desc%my_nr3p big.
        2) all processors communicate to exchange slices(all sectin of columns with
           Y in the slice belonging to "me" must be received, all the others
           must be sent to "iproc2")
        Finally one gets the "partial slice" representation: each processor has
        all the X values of desc%my_nr2p Y and desc%my_nr3p Z values.
        Data are organized with the X index running fastest, then Y, then Z.
        f_in  contains the input Y columns, is destroyed on output
        f_aux contains the output X-oriented partial slices.
      b) From planes to columns(isgn < 0)
        Quite the same in the opposite direction
        f_aux contains the input X-oriented partial slices, is destroyed on output
        f_in  contains the output Y columns.
    """
    _qepy.f90wrap_fft_scatter_xy(desc=self._handle, f_in=f_in, f_aux=f_aux, \
        nxx_=nxx_, isgn=isgn)

def fft_scatter_yz(self, f_in, f_aux, nxx_, isgn):
    """
    fft_scatter_yz(self, f_in, f_aux, nxx_, isgn)
    
    
    Defined at scatter_mod.fpp lines 90-129
    
    Parameters
    ----------
    desc : Fft_Type_Descriptor
    f_in : complex array
    f_aux : complex array
    nxx_ : int
    isgn : int
    
    -----------------------------------------------------------------------
     transpose of the fft yz planes across the desc%comm3 communicator
     a) From Z-oriented columns to Y-oriented colums(isgn > 0)
        Active columns(or sticks or pencils) along the Z direction for each
        processor are stored consecutively and are such that they correspond
        to a subset of the active X values.
        The pencil -> slices transposition is performed in the subgroup
        of processors(desc%comm3) owning these X values.
        The transpose takes place in two steps:
        1) on each processor the columns are sliced into sections along Z
           that are stored one after the other. On each processor, slices for
           processor "iproc3" are desc%nr3p(iproc3)*desc%nsw/nsp(me) big.
        2) all processors communicate to exchange slices(all columns with
           Z in the slice belonging to "me" must be received, all the others
           must be sent to "iproc3")
        Finally one gets the "slice" representation: each processor has
        desc%nr3p(mype3) Z values of all the active pencils along Y for the
        X values of the current group. Data are organized with the Y index
        running fastest, then the reordered X values, then Z.
        f_in  contains the input Z columns, is destroyed on output
        f_aux contains the output Y colums.
      b) From planes to columns(isgn < 0)
        Quite the same in the opposite direction
        f_aux contains the input Y columns, is destroyed on output
        f_in  contains the output Z columns.
    """
    _qepy.f90wrap_fft_scatter_yz(desc=self._handle, f_in=f_in, f_aux=f_aux, \
        nxx_=nxx_, isgn=isgn)

def fft_scatter_tg(self, f_in, f_aux, nxx_, isgn):
    """
    fft_scatter_tg(self, f_in, f_aux, nxx_, isgn)
    
    
    Defined at scatter_mod.fpp lines 133-155
    
    Parameters
    ----------
    desc : Fft_Type_Descriptor
    f_in : complex array
    f_aux : complex array
    nxx_ : int
    isgn : int
    
    -----------------------------------------------------------------------
     task group wavefunction redistribution
     a) (isgn >0 ) From many-wfc partial-plane arrangement to single-wfc whole-plane \
         one
     b) (isgn <0 ) From single-wfc whole-plane arrangement to many-wfc partial-plane \
         one
     in both cases:
        f_in  contains the input data, is overwritten with the desired output
        f_aux is used as working array, may contain garbage in output
    """
    _qepy.f90wrap_fft_scatter_tg(desc=self._handle, f_in=f_in, f_aux=f_aux, \
        nxx_=nxx_, isgn=isgn)

def fft_scatter_tg_opt(self, f_in, f_out, nxx_, isgn):
    """
    fft_scatter_tg_opt(self, f_in, f_out, nxx_, isgn)
    
    
    Defined at scatter_mod.fpp lines 159-181
    
    Parameters
    ----------
    desc : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    nxx_ : int
    isgn : int
    
    -----------------------------------------------------------------------
     task group wavefunction redistribution
     a) (isgn >0 ) From many-wfc partial-plane arrangement to single-wfc whole-plane \
         one
     b) (isgn <0 ) From single-wfc whole-plane arrangement to many-wfc partial-plane \
         one
     in both cases:
        f_in  contains the input data
        f_out contains the output data
    """
    _qepy.f90wrap_fft_scatter_tg_opt(desc=self._handle, f_in=f_in, f_out=f_out, \
        nxx_=nxx_, isgn=isgn)

def cgather_sym(self, f_in, f_out):
    """
    cgather_sym(self, f_in, f_out)
    
    
    Defined at scatter_mod.fpp lines 279-298
    
    Parameters
    ----------
    dfftp : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    
    -----------------------------------------------------------------------
     ... gather complex data for symmetrization(used in phonon code)
     ... Differs from gather_grid because mpi_allgatherv is used instead
     ... of mpi_gatherv - all data is gathered on ALL processors
     ... COMPLEX*16  f_in  = distributed variable(nrxx)
     ... COMPLEX*16  f_out = gathered variable(nr1x*nr2x*nr3x)
    """
    _qepy.f90wrap_cgather_sym(dfftp=self._handle, f_in=f_in, f_out=f_out)

def cgather_sym_many(self, f_in, f_out, nbnd, nbnd_proc, start_nbnd_proc):
    """
    cgather_sym_many(self, f_in, f_out, nbnd, nbnd_proc, start_nbnd_proc)
    
    
    Defined at scatter_mod.fpp lines 303-328
    
    Parameters
    ----------
    dfftp : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    nbnd : int
    nbnd_proc : int array
    start_nbnd_proc : int array
    
    -----------------------------------------------------------------------
     ... Written by A. Dal Corso
     ... This routine generalizes cgather_sym, receiveng nbnd complex
     ... distributed functions and collecting nbnd_proc(dfftp%mype+1)
     ... functions in each processor.
     ... start_nbnd_proc(dfftp%mype+1), says where the data for each processor
     ... start in the distributed variable
     ... COMPLEX*16  f_in  = distributed variable(nrxx,nbnd)
     ... COMPLEX*16 f_out = gathered variable(nr1x*nr2x*nr3x,nbnd_proc(dfftp%mype+1))
    """
    _qepy.f90wrap_cgather_sym_many(dfftp=self._handle, f_in=f_in, f_out=f_out, \
        nbnd=nbnd, nbnd_proc=nbnd_proc, start_nbnd_proc=start_nbnd_proc)

def cscatter_sym_many(self, f_in, f_out, target_ibnd, nbnd, nbnd_proc, \
    start_nbnd_proc):
    """
    cscatter_sym_many(self, f_in, f_out, target_ibnd, nbnd, nbnd_proc, \
        start_nbnd_proc)
    
    
    Defined at scatter_mod.fpp lines 333-361
    
    Parameters
    ----------
    dfftp : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    target_ibnd : int
    nbnd : int
    nbnd_proc : int array
    start_nbnd_proc : int array
    
    ----------------------------------------------------------------------------
     ... Written by A. Dal Corso
     ... generalizes cscatter_sym. It assumes that each processor has
     ... a certain number of bands(nbnd_proc(dfftp%mype+1)). The processor
     ... that has target_ibnd scatters it to all the other processors
     ... that receive a distributed part of the target function.
     ... start_nbnd_proc(dfftp%mype+1) is used to identify the processor
     ... that has the required band
     ... COMPLEX*16 f_in = gathered variable(nr1x*nr2x*nr3x, nbnd_proc(dfftp%mype+1) \
         )
     ... COMPLEX*16  f_out = distributed variable(nrxx)
    """
    _qepy.f90wrap_cscatter_sym_many(dfftp=self._handle, f_in=f_in, f_out=f_out, \
        target_ibnd=target_ibnd, nbnd=nbnd, nbnd_proc=nbnd_proc, \
        start_nbnd_proc=start_nbnd_proc)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "scatter_mod".')

for func in _dt_array_initialisers:
    func()
