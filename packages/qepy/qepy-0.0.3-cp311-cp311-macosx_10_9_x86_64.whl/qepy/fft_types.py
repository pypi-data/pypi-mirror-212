"""
Module fft_types


Defined at fft_types.fpp lines 14-804

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy.fft_type_descriptor")
class fft_type_descriptor(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=fft_type_descriptor)
    
    
    Defined at fft_types.fpp lines 24-121
    
    """
    def __init__(self, at, bg, gcutm, comm, fft_fact=None, nyfft=None, handle=None):
        """
        self = Fft_Type_Descriptor(at, bg, gcutm, comm[, fft_fact, nyfft])
        
        
        Defined at fft_types.fpp lines 130-199
        
        Parameters
        ----------
        at : float array
        bg : float array
        gcutm : float
        comm : int
        fft_fact : int array
        nyfft : int
        
        Returns
        -------
        desc : Fft_Type_Descriptor
        
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_fft_type_allocate(at=at, bg=bg, gcutm=gcutm, comm=comm, \
            fft_fact=fft_fact, nyfft=nyfft)
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Fft_Type_Descriptor
        
        
        Defined at fft_types.fpp lines 201-245
        
        Parameters
        ----------
        desc : Fft_Type_Descriptor
        
        """
        if self._alloc:
            _qepy.f90wrap_fft_type_deallocate(desc=self._handle)
    
    @property
    def nr1(self):
        """
        Element nr1 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 28
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr1(self._handle)
    
    @nr1.setter
    def nr1(self, nr1):
        _qepy.f90wrap_fft_type_descriptor__set__nr1(self._handle, nr1)
    
    @property
    def nr2(self):
        """
        Element nr2 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 29
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr2(self._handle)
    
    @nr2.setter
    def nr2(self, nr2):
        _qepy.f90wrap_fft_type_descriptor__set__nr2(self._handle, nr2)
    
    @property
    def nr3(self):
        """
        Element nr3 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 30
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr3(self._handle)
    
    @nr3.setter
    def nr3(self, nr3):
        _qepy.f90wrap_fft_type_descriptor__set__nr3(self._handle, nr3)
    
    @property
    def nr1x(self):
        """
        Element nr1x ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 31
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr1x(self._handle)
    
    @nr1x.setter
    def nr1x(self, nr1x):
        _qepy.f90wrap_fft_type_descriptor__set__nr1x(self._handle, nr1x)
    
    @property
    def nr2x(self):
        """
        Element nr2x ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 32
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr2x(self._handle)
    
    @nr2x.setter
    def nr2x(self, nr2x):
        _qepy.f90wrap_fft_type_descriptor__set__nr2x(self._handle, nr2x)
    
    @property
    def nr3x(self):
        """
        Element nr3x ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 33
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr3x(self._handle)
    
    @nr3x.setter
    def nr3x(self, nr3x):
        _qepy.f90wrap_fft_type_descriptor__set__nr3x(self._handle, nr3x)
    
    @property
    def lpara(self):
        """
        Element lpara ftype=logical pytype=bool
        
        
        Defined at fft_types.fpp line 45
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__lpara(self._handle)
    
    @lpara.setter
    def lpara(self, lpara):
        _qepy.f90wrap_fft_type_descriptor__set__lpara(self._handle, lpara)
    
    @property
    def lgamma(self):
        """
        Element lgamma ftype=logical pytype=bool
        
        
        Defined at fft_types.fpp line 46
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__lgamma(self._handle)
    
    @lgamma.setter
    def lgamma(self, lgamma):
        _qepy.f90wrap_fft_type_descriptor__set__lgamma(self._handle, lgamma)
    
    @property
    def root(self):
        """
        Element root ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 47
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__root(self._handle)
    
    @root.setter
    def root(self, root):
        _qepy.f90wrap_fft_type_descriptor__set__root(self._handle, root)
    
    @property
    def comm(self):
        """
        Element comm ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 48
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__comm(self._handle)
    
    @comm.setter
    def comm(self, comm):
        _qepy.f90wrap_fft_type_descriptor__set__comm(self._handle, comm)
    
    @property
    def comm2(self):
        """
        Element comm2 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 49
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__comm2(self._handle)
    
    @comm2.setter
    def comm2(self, comm2):
        _qepy.f90wrap_fft_type_descriptor__set__comm2(self._handle, comm2)
    
    @property
    def comm3(self):
        """
        Element comm3 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 50
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__comm3(self._handle)
    
    @comm3.setter
    def comm3(self, comm3):
        _qepy.f90wrap_fft_type_descriptor__set__comm3(self._handle, comm3)
    
    @property
    def nproc(self):
        """
        Element nproc ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 51
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nproc(self._handle)
    
    @nproc.setter
    def nproc(self, nproc):
        _qepy.f90wrap_fft_type_descriptor__set__nproc(self._handle, nproc)
    
    @property
    def nproc2(self):
        """
        Element nproc2 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 52
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nproc2(self._handle)
    
    @nproc2.setter
    def nproc2(self, nproc2):
        _qepy.f90wrap_fft_type_descriptor__set__nproc2(self._handle, nproc2)
    
    @property
    def nproc3(self):
        """
        Element nproc3 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 53
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nproc3(self._handle)
    
    @nproc3.setter
    def nproc3(self, nproc3):
        _qepy.f90wrap_fft_type_descriptor__set__nproc3(self._handle, nproc3)
    
    @property
    def mype(self):
        """
        Element mype ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 54
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__mype(self._handle)
    
    @mype.setter
    def mype(self, mype):
        _qepy.f90wrap_fft_type_descriptor__set__mype(self._handle, mype)
    
    @property
    def mype2(self):
        """
        Element mype2 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 55
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__mype2(self._handle)
    
    @mype2.setter
    def mype2(self, mype2):
        _qepy.f90wrap_fft_type_descriptor__set__mype2(self._handle, mype2)
    
    @property
    def mype3(self):
        """
        Element mype3 ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 56
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__mype3(self._handle)
    
    @mype3.setter
    def mype3(self, mype3):
        _qepy.f90wrap_fft_type_descriptor__set__mype3(self._handle, mype3)
    
    @property
    def iproc(self):
        """
        Element iproc ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 57
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__iproc(self._handle)
        if array_handle in self._arrays:
            iproc = self._arrays[array_handle]
        else:
            iproc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__iproc)
            self._arrays[array_handle] = iproc
        return iproc
    
    @iproc.setter
    def iproc(self, iproc):
        self.iproc[...] = iproc
    
    @property
    def iproc2(self):
        """
        Element iproc2 ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 57
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__iproc2(self._handle)
        if array_handle in self._arrays:
            iproc2 = self._arrays[array_handle]
        else:
            iproc2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__iproc2)
            self._arrays[array_handle] = iproc2
        return iproc2
    
    @iproc2.setter
    def iproc2(self, iproc2):
        self.iproc2[...] = iproc2
    
    @property
    def iproc3(self):
        """
        Element iproc3 ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 57
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__iproc3(self._handle)
        if array_handle in self._arrays:
            iproc3 = self._arrays[array_handle]
        else:
            iproc3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__iproc3)
            self._arrays[array_handle] = iproc3
        return iproc3
    
    @iproc3.setter
    def iproc3(self, iproc3):
        self.iproc3[...] = iproc3
    
    @property
    def my_nr3p(self):
        """
        Element my_nr3p ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 61
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__my_nr3p(self._handle)
    
    @my_nr3p.setter
    def my_nr3p(self, my_nr3p):
        _qepy.f90wrap_fft_type_descriptor__set__my_nr3p(self._handle, my_nr3p)
    
    @property
    def my_nr2p(self):
        """
        Element my_nr2p ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 62
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__my_nr2p(self._handle)
    
    @my_nr2p.setter
    def my_nr2p(self, my_nr2p):
        _qepy.f90wrap_fft_type_descriptor__set__my_nr2p(self._handle, my_nr2p)
    
    @property
    def my_i0r3p(self):
        """
        Element my_i0r3p ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 63
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__my_i0r3p(self._handle)
    
    @my_i0r3p.setter
    def my_i0r3p(self, my_i0r3p):
        _qepy.f90wrap_fft_type_descriptor__set__my_i0r3p(self._handle, my_i0r3p)
    
    @property
    def my_i0r2p(self):
        """
        Element my_i0r2p ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 64
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__my_i0r2p(self._handle)
    
    @my_i0r2p.setter
    def my_i0r2p(self, my_i0r2p):
        _qepy.f90wrap_fft_type_descriptor__set__my_i0r2p(self._handle, my_i0r2p)
    
    @property
    def nr3p(self):
        """
        Element nr3p ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 65
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nr3p(self._handle)
        if array_handle in self._arrays:
            nr3p = self._arrays[array_handle]
        else:
            nr3p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nr3p)
            self._arrays[array_handle] = nr3p
        return nr3p
    
    @nr3p.setter
    def nr3p(self, nr3p):
        self.nr3p[...] = nr3p
    
    @property
    def nr3p_offset(self):
        """
        Element nr3p_offset ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 66
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nr3p_offset(self._handle)
        if array_handle in self._arrays:
            nr3p_offset = self._arrays[array_handle]
        else:
            nr3p_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nr3p_offset)
            self._arrays[array_handle] = nr3p_offset
        return nr3p_offset
    
    @nr3p_offset.setter
    def nr3p_offset(self, nr3p_offset):
        self.nr3p_offset[...] = nr3p_offset
    
    @property
    def nr2p(self):
        """
        Element nr2p ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 67
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nr2p(self._handle)
        if array_handle in self._arrays:
            nr2p = self._arrays[array_handle]
        else:
            nr2p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nr2p)
            self._arrays[array_handle] = nr2p
        return nr2p
    
    @nr2p.setter
    def nr2p(self, nr2p):
        self.nr2p[...] = nr2p
    
    @property
    def nr2p_offset(self):
        """
        Element nr2p_offset ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 68
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nr2p_offset(self._handle)
        if array_handle in self._arrays:
            nr2p_offset = self._arrays[array_handle]
        else:
            nr2p_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nr2p_offset)
            self._arrays[array_handle] = nr2p_offset
        return nr2p_offset
    
    @nr2p_offset.setter
    def nr2p_offset(self, nr2p_offset):
        self.nr2p_offset[...] = nr2p_offset
    
    @property
    def nr1p(self):
        """
        Element nr1p ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 69
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nr1p(self._handle)
        if array_handle in self._arrays:
            nr1p = self._arrays[array_handle]
        else:
            nr1p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nr1p)
            self._arrays[array_handle] = nr1p
        return nr1p
    
    @nr1p.setter
    def nr1p(self, nr1p):
        self.nr1p[...] = nr1p
    
    @property
    def nr1w(self):
        """
        Element nr1w ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 70
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nr1w(self._handle)
        if array_handle in self._arrays:
            nr1w = self._arrays[array_handle]
        else:
            nr1w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nr1w)
            self._arrays[array_handle] = nr1w
        return nr1w
    
    @nr1w.setter
    def nr1w(self, nr1w):
        self.nr1w[...] = nr1w
    
    @property
    def nr1w_tg(self):
        """
        Element nr1w_tg ftype=integer               pytype=int
        
        
        Defined at fft_types.fpp line 71
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nr1w_tg(self._handle)
    
    @nr1w_tg.setter
    def nr1w_tg(self, nr1w_tg):
        _qepy.f90wrap_fft_type_descriptor__set__nr1w_tg(self._handle, nr1w_tg)
    
    @property
    def i0r3p(self):
        """
        Element i0r3p ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 72
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__i0r3p(self._handle)
        if array_handle in self._arrays:
            i0r3p = self._arrays[array_handle]
        else:
            i0r3p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__i0r3p)
            self._arrays[array_handle] = i0r3p
        return i0r3p
    
    @i0r3p.setter
    def i0r3p(self, i0r3p):
        self.i0r3p[...] = i0r3p
    
    @property
    def i0r2p(self):
        """
        Element i0r2p ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 73
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__i0r2p(self._handle)
        if array_handle in self._arrays:
            i0r2p = self._arrays[array_handle]
        else:
            i0r2p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__i0r2p)
            self._arrays[array_handle] = i0r2p
        return i0r2p
    
    @i0r2p.setter
    def i0r2p(self, i0r2p):
        self.i0r2p[...] = i0r2p
    
    @property
    def ir1p(self):
        """
        Element ir1p ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 74
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__ir1p(self._handle)
        if array_handle in self._arrays:
            ir1p = self._arrays[array_handle]
        else:
            ir1p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__ir1p)
            self._arrays[array_handle] = ir1p
        return ir1p
    
    @ir1p.setter
    def ir1p(self, ir1p):
        self.ir1p[...] = ir1p
    
    @property
    def indp(self):
        """
        Element indp ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 75
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__indp(self._handle)
        if array_handle in self._arrays:
            indp = self._arrays[array_handle]
        else:
            indp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__indp)
            self._arrays[array_handle] = indp
        return indp
    
    @indp.setter
    def indp(self, indp):
        self.indp[...] = indp
    
    @property
    def ir1w(self):
        """
        Element ir1w ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 76
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__ir1w(self._handle)
        if array_handle in self._arrays:
            ir1w = self._arrays[array_handle]
        else:
            ir1w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__ir1w)
            self._arrays[array_handle] = ir1w
        return ir1w
    
    @ir1w.setter
    def ir1w(self, ir1w):
        self.ir1w[...] = ir1w
    
    @property
    def indw(self):
        """
        Element indw ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 77
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__indw(self._handle)
        if array_handle in self._arrays:
            indw = self._arrays[array_handle]
        else:
            indw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__indw)
            self._arrays[array_handle] = indw
        return indw
    
    @indw.setter
    def indw(self, indw):
        self.indw[...] = indw
    
    @property
    def ir1w_tg(self):
        """
        Element ir1w_tg ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 78
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__ir1w_tg(self._handle)
        if array_handle in self._arrays:
            ir1w_tg = self._arrays[array_handle]
        else:
            ir1w_tg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__ir1w_tg)
            self._arrays[array_handle] = ir1w_tg
        return ir1w_tg
    
    @ir1w_tg.setter
    def ir1w_tg(self, ir1w_tg):
        self.ir1w_tg[...] = ir1w_tg
    
    @property
    def indw_tg(self):
        """
        Element indw_tg ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 79
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__indw_tg(self._handle)
        if array_handle in self._arrays:
            indw_tg = self._arrays[array_handle]
        else:
            indw_tg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__indw_tg)
            self._arrays[array_handle] = indw_tg
        return indw_tg
    
    @indw_tg.setter
    def indw_tg(self, indw_tg):
        self.indw_tg[...] = indw_tg
    
    @property
    def nst(self):
        """
        Element nst ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 80
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nst(self._handle)
    
    @nst.setter
    def nst(self, nst):
        _qepy.f90wrap_fft_type_descriptor__set__nst(self._handle, nst)
    
    @property
    def nsp(self):
        """
        Element nsp ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 81
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nsp(self._handle)
        if array_handle in self._arrays:
            nsp = self._arrays[array_handle]
        else:
            nsp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nsp)
            self._arrays[array_handle] = nsp
        return nsp
    
    @nsp.setter
    def nsp(self, nsp):
        self.nsp[...] = nsp
    
    @property
    def nsp_offset(self):
        """
        Element nsp_offset ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 83
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nsp_offset(self._handle)
        if array_handle in self._arrays:
            nsp_offset = self._arrays[array_handle]
        else:
            nsp_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nsp_offset)
            self._arrays[array_handle] = nsp_offset
        return nsp_offset
    
    @nsp_offset.setter
    def nsp_offset(self, nsp_offset):
        self.nsp_offset[...] = nsp_offset
    
    @property
    def nsw(self):
        """
        Element nsw ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 84
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nsw(self._handle)
        if array_handle in self._arrays:
            nsw = self._arrays[array_handle]
        else:
            nsw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nsw)
            self._arrays[array_handle] = nsw
        return nsw
    
    @nsw.setter
    def nsw(self, nsw):
        self.nsw[...] = nsw
    
    @property
    def nsw_offset(self):
        """
        Element nsw_offset ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 85
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nsw_offset(self._handle)
        if array_handle in self._arrays:
            nsw_offset = self._arrays[array_handle]
        else:
            nsw_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nsw_offset)
            self._arrays[array_handle] = nsw_offset
        return nsw_offset
    
    @nsw_offset.setter
    def nsw_offset(self, nsw_offset):
        self.nsw_offset[...] = nsw_offset
    
    @property
    def nsw_tg(self):
        """
        Element nsw_tg ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 86
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nsw_tg(self._handle)
        if array_handle in self._arrays:
            nsw_tg = self._arrays[array_handle]
        else:
            nsw_tg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nsw_tg)
            self._arrays[array_handle] = nsw_tg
        return nsw_tg
    
    @nsw_tg.setter
    def nsw_tg(self, nsw_tg):
        self.nsw_tg[...] = nsw_tg
    
    @property
    def ngl(self):
        """
        Element ngl ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 87
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__ngl(self._handle)
        if array_handle in self._arrays:
            ngl = self._arrays[array_handle]
        else:
            ngl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__ngl)
            self._arrays[array_handle] = ngl
        return ngl
    
    @ngl.setter
    def ngl(self, ngl):
        self.ngl[...] = ngl
    
    @property
    def nwl(self):
        """
        Element nwl ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 88
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nwl(self._handle)
        if array_handle in self._arrays:
            nwl = self._arrays[array_handle]
        else:
            nwl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nwl)
            self._arrays[array_handle] = nwl
        return nwl
    
    @nwl.setter
    def nwl(self, nwl):
        self.nwl[...] = nwl
    
    @property
    def ngm(self):
        """
        Element ngm ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 89
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__ngm(self._handle)
    
    @ngm.setter
    def ngm(self, ngm):
        _qepy.f90wrap_fft_type_descriptor__set__ngm(self._handle, ngm)
    
    @property
    def ngw(self):
        """
        Element ngw ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 93
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__ngw(self._handle)
    
    @ngw.setter
    def ngw(self, ngw):
        _qepy.f90wrap_fft_type_descriptor__set__ngw(self._handle, ngw)
    
    @property
    def iplp(self):
        """
        Element iplp ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 97
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__iplp(self._handle)
        if array_handle in self._arrays:
            iplp = self._arrays[array_handle]
        else:
            iplp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__iplp)
            self._arrays[array_handle] = iplp
        return iplp
    
    @iplp.setter
    def iplp(self, iplp):
        self.iplp[...] = iplp
    
    @property
    def iplw(self):
        """
        Element iplw ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 98
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__iplw(self._handle)
        if array_handle in self._arrays:
            iplw = self._arrays[array_handle]
        else:
            iplw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__iplw)
            self._arrays[array_handle] = iplw
        return iplw
    
    @iplw.setter
    def iplw(self, iplw):
        self.iplw[...] = iplw
    
    @property
    def nnp(self):
        """
        Element nnp ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 99
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nnp(self._handle)
    
    @nnp.setter
    def nnp(self, nnp):
        _qepy.f90wrap_fft_type_descriptor__set__nnp(self._handle, nnp)
    
    @property
    def nnr(self):
        """
        Element nnr ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 100
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nnr(self._handle)
    
    @nnr.setter
    def nnr(self, nnr):
        _qepy.f90wrap_fft_type_descriptor__set__nnr(self._handle, nnr)
    
    @property
    def nnr_tg(self):
        """
        Element nnr_tg ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 104
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__nnr_tg(self._handle)
    
    @nnr_tg.setter
    def nnr_tg(self, nnr_tg):
        _qepy.f90wrap_fft_type_descriptor__set__nnr_tg(self._handle, nnr_tg)
    
    @property
    def iss(self):
        """
        Element iss ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 105
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__iss(self._handle)
        if array_handle in self._arrays:
            iss = self._arrays[array_handle]
        else:
            iss = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__iss)
            self._arrays[array_handle] = iss
        return iss
    
    @iss.setter
    def iss(self, iss):
        self.iss[...] = iss
    
    @property
    def isind(self):
        """
        Element isind ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 106
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__isind(self._handle)
        if array_handle in self._arrays:
            isind = self._arrays[array_handle]
        else:
            isind = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__isind)
            self._arrays[array_handle] = isind
        return isind
    
    @isind.setter
    def isind(self, isind):
        self.isind[...] = isind
    
    @property
    def ismap(self):
        """
        Element ismap ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 107
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__ismap(self._handle)
        if array_handle in self._arrays:
            ismap = self._arrays[array_handle]
        else:
            ismap = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__ismap)
            self._arrays[array_handle] = ismap
        return ismap
    
    @ismap.setter
    def ismap(self, ismap):
        self.ismap[...] = ismap
    
    @property
    def nl(self):
        """
        Element nl ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 108
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nl(self._handle)
        if array_handle in self._arrays:
            nl = self._arrays[array_handle]
        else:
            nl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nl)
            self._arrays[array_handle] = nl
        return nl
    
    @nl.setter
    def nl(self, nl):
        self.nl[...] = nl
    
    @property
    def nlm(self):
        """
        Element nlm ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 109
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__nlm(self._handle)
        if array_handle in self._arrays:
            nlm = self._arrays[array_handle]
        else:
            nlm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__nlm)
            self._arrays[array_handle] = nlm
        return nlm
    
    @nlm.setter
    def nlm(self, nlm):
        self.nlm[...] = nlm
    
    @property
    def tg_snd(self):
        """
        Element tg_snd ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 112
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__tg_snd(self._handle)
        if array_handle in self._arrays:
            tg_snd = self._arrays[array_handle]
        else:
            tg_snd = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__tg_snd)
            self._arrays[array_handle] = tg_snd
        return tg_snd
    
    @tg_snd.setter
    def tg_snd(self, tg_snd):
        self.tg_snd[...] = tg_snd
    
    @property
    def tg_rcv(self):
        """
        Element tg_rcv ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 113
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__tg_rcv(self._handle)
        if array_handle in self._arrays:
            tg_rcv = self._arrays[array_handle]
        else:
            tg_rcv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__tg_rcv)
            self._arrays[array_handle] = tg_rcv
        return tg_rcv
    
    @tg_rcv.setter
    def tg_rcv(self, tg_rcv):
        self.tg_rcv[...] = tg_rcv
    
    @property
    def tg_sdsp(self):
        """
        Element tg_sdsp ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 114
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__tg_sdsp(self._handle)
        if array_handle in self._arrays:
            tg_sdsp = self._arrays[array_handle]
        else:
            tg_sdsp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__tg_sdsp)
            self._arrays[array_handle] = tg_sdsp
        return tg_sdsp
    
    @tg_sdsp.setter
    def tg_sdsp(self, tg_sdsp):
        self.tg_sdsp[...] = tg_sdsp
    
    @property
    def tg_rdsp(self):
        """
        Element tg_rdsp ftype=integer pytype=int
        
        
        Defined at fft_types.fpp line 115
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_fft_type_descriptor__array__tg_rdsp(self._handle)
        if array_handle in self._arrays:
            tg_rdsp = self._arrays[array_handle]
        else:
            tg_rdsp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_fft_type_descriptor__array__tg_rdsp)
            self._arrays[array_handle] = tg_rdsp
        return tg_rdsp
    
    @tg_rdsp.setter
    def tg_rdsp(self, tg_rdsp):
        self.tg_rdsp[...] = tg_rdsp
    
    @property
    def has_task_groups(self):
        """
        Element has_task_groups ftype=logical pytype=bool
        
        
        Defined at fft_types.fpp line 117
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__has_task_groups(self._handle)
    
    @has_task_groups.setter
    def has_task_groups(self, has_task_groups):
        _qepy.f90wrap_fft_type_descriptor__set__has_task_groups(self._handle, \
            has_task_groups)
    
    @property
    def rho_clock_label(self):
        """
        Element rho_clock_label ftype=character(len=12) pytype=str
        
        
        Defined at fft_types.fpp line 119
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__rho_clock_label(self._handle)
    
    @rho_clock_label.setter
    def rho_clock_label(self, rho_clock_label):
        _qepy.f90wrap_fft_type_descriptor__set__rho_clock_label(self._handle, \
            rho_clock_label)
    
    @property
    def wave_clock_label(self):
        """
        Element wave_clock_label ftype=character(len=12) pytype=str
        
        
        Defined at fft_types.fpp line 120
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__wave_clock_label(self._handle)
    
    @wave_clock_label.setter
    def wave_clock_label(self, wave_clock_label):
        _qepy.f90wrap_fft_type_descriptor__set__wave_clock_label(self._handle, \
            wave_clock_label)
    
    @property
    def grid_id(self):
        """
        Element grid_id ftype=integer  pytype=int
        
        
        Defined at fft_types.fpp line 121
        
        """
        return _qepy.f90wrap_fft_type_descriptor__get__grid_id(self._handle)
    
    @grid_id.setter
    def grid_id(self, grid_id):
        _qepy.f90wrap_fft_type_descriptor__set__grid_id(self._handle, grid_id)
    
    def __str__(self):
        ret = ['<fft_type_descriptor>{\n']
        ret.append('    nr1 : ')
        ret.append(repr(self.nr1))
        ret.append(',\n    nr2 : ')
        ret.append(repr(self.nr2))
        ret.append(',\n    nr3 : ')
        ret.append(repr(self.nr3))
        ret.append(',\n    nr1x : ')
        ret.append(repr(self.nr1x))
        ret.append(',\n    nr2x : ')
        ret.append(repr(self.nr2x))
        ret.append(',\n    nr3x : ')
        ret.append(repr(self.nr3x))
        ret.append(',\n    lpara : ')
        ret.append(repr(self.lpara))
        ret.append(',\n    lgamma : ')
        ret.append(repr(self.lgamma))
        ret.append(',\n    root : ')
        ret.append(repr(self.root))
        ret.append(',\n    comm : ')
        ret.append(repr(self.comm))
        ret.append(',\n    comm2 : ')
        ret.append(repr(self.comm2))
        ret.append(',\n    comm3 : ')
        ret.append(repr(self.comm3))
        ret.append(',\n    nproc : ')
        ret.append(repr(self.nproc))
        ret.append(',\n    nproc2 : ')
        ret.append(repr(self.nproc2))
        ret.append(',\n    nproc3 : ')
        ret.append(repr(self.nproc3))
        ret.append(',\n    mype : ')
        ret.append(repr(self.mype))
        ret.append(',\n    mype2 : ')
        ret.append(repr(self.mype2))
        ret.append(',\n    mype3 : ')
        ret.append(repr(self.mype3))
        ret.append(',\n    iproc : ')
        ret.append(repr(self.iproc))
        ret.append(',\n    iproc2 : ')
        ret.append(repr(self.iproc2))
        ret.append(',\n    iproc3 : ')
        ret.append(repr(self.iproc3))
        ret.append(',\n    my_nr3p : ')
        ret.append(repr(self.my_nr3p))
        ret.append(',\n    my_nr2p : ')
        ret.append(repr(self.my_nr2p))
        ret.append(',\n    my_i0r3p : ')
        ret.append(repr(self.my_i0r3p))
        ret.append(',\n    my_i0r2p : ')
        ret.append(repr(self.my_i0r2p))
        ret.append(',\n    nr3p : ')
        ret.append(repr(self.nr3p))
        ret.append(',\n    nr3p_offset : ')
        ret.append(repr(self.nr3p_offset))
        ret.append(',\n    nr2p : ')
        ret.append(repr(self.nr2p))
        ret.append(',\n    nr2p_offset : ')
        ret.append(repr(self.nr2p_offset))
        ret.append(',\n    nr1p : ')
        ret.append(repr(self.nr1p))
        ret.append(',\n    nr1w : ')
        ret.append(repr(self.nr1w))
        ret.append(',\n    nr1w_tg : ')
        ret.append(repr(self.nr1w_tg))
        ret.append(',\n    i0r3p : ')
        ret.append(repr(self.i0r3p))
        ret.append(',\n    i0r2p : ')
        ret.append(repr(self.i0r2p))
        ret.append(',\n    ir1p : ')
        ret.append(repr(self.ir1p))
        ret.append(',\n    indp : ')
        ret.append(repr(self.indp))
        ret.append(',\n    ir1w : ')
        ret.append(repr(self.ir1w))
        ret.append(',\n    indw : ')
        ret.append(repr(self.indw))
        ret.append(',\n    ir1w_tg : ')
        ret.append(repr(self.ir1w_tg))
        ret.append(',\n    indw_tg : ')
        ret.append(repr(self.indw_tg))
        ret.append(',\n    nst : ')
        ret.append(repr(self.nst))
        ret.append(',\n    nsp : ')
        ret.append(repr(self.nsp))
        ret.append(',\n    nsp_offset : ')
        ret.append(repr(self.nsp_offset))
        ret.append(',\n    nsw : ')
        ret.append(repr(self.nsw))
        ret.append(',\n    nsw_offset : ')
        ret.append(repr(self.nsw_offset))
        ret.append(',\n    nsw_tg : ')
        ret.append(repr(self.nsw_tg))
        ret.append(',\n    ngl : ')
        ret.append(repr(self.ngl))
        ret.append(',\n    nwl : ')
        ret.append(repr(self.nwl))
        ret.append(',\n    ngm : ')
        ret.append(repr(self.ngm))
        ret.append(',\n    ngw : ')
        ret.append(repr(self.ngw))
        ret.append(',\n    iplp : ')
        ret.append(repr(self.iplp))
        ret.append(',\n    iplw : ')
        ret.append(repr(self.iplw))
        ret.append(',\n    nnp : ')
        ret.append(repr(self.nnp))
        ret.append(',\n    nnr : ')
        ret.append(repr(self.nnr))
        ret.append(',\n    nnr_tg : ')
        ret.append(repr(self.nnr_tg))
        ret.append(',\n    iss : ')
        ret.append(repr(self.iss))
        ret.append(',\n    isind : ')
        ret.append(repr(self.isind))
        ret.append(',\n    ismap : ')
        ret.append(repr(self.ismap))
        ret.append(',\n    nl : ')
        ret.append(repr(self.nl))
        ret.append(',\n    nlm : ')
        ret.append(repr(self.nlm))
        ret.append(',\n    tg_snd : ')
        ret.append(repr(self.tg_snd))
        ret.append(',\n    tg_rcv : ')
        ret.append(repr(self.tg_rcv))
        ret.append(',\n    tg_sdsp : ')
        ret.append(repr(self.tg_sdsp))
        ret.append(',\n    tg_rdsp : ')
        ret.append(repr(self.tg_rdsp))
        ret.append(',\n    has_task_groups : ')
        ret.append(repr(self.has_task_groups))
        ret.append(',\n    rho_clock_label : ')
        ret.append(repr(self.rho_clock_label))
        ret.append(',\n    wave_clock_label : ')
        ret.append(repr(self.wave_clock_label))
        ret.append(',\n    grid_id : ')
        ret.append(repr(self.grid_id))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def fft_stick_index(self, i, j):
    """
    fft_stick_index = fft_stick_index(self, i, j)
    
    
    Defined at fft_types.fpp lines 791-802
    
    Parameters
    ----------
    desc : Fft_Type_Descriptor
    i : int
    j : int
    
    Returns
    -------
    fft_stick_index : int
    
    """
    fft_stick_index = _qepy.f90wrap_fft_stick_index(desc=self._handle, i=i, j=j)
    return fft_stick_index


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "fft_types".')

for func in _dt_array_initialisers:
    func()
