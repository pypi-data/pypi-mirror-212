"""
Module command_line_options


Defined at command_line_options.fpp lines 13-242

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging

_arrays = {}
_objs = {}

def get_command_line(input_command_line_=None):
    """
    get_command_line([input_command_line_])
    
    
    Defined at command_line_options.fpp lines 55-186
    
    Parameters
    ----------
    input_command_line_ : str
    
    """
    _qepy.f90wrap_get_command_line(input_command_line_=input_command_line_)

def my_iargc(input_command_line):
    """
    my_iargc = my_iargc(input_command_line)
    
    
    Defined at command_line_options.fpp lines 189-200
    
    Parameters
    ----------
    input_command_line : str
    
    Returns
    -------
    my_iargc : int
    
    """
    my_iargc = _qepy.f90wrap_my_iargc(input_command_line=input_command_line)
    return my_iargc

def my_getarg(input_command_line, narg):
    """
    arg = my_getarg(input_command_line, narg)
    
    
    Defined at command_line_options.fpp lines 203-225
    
    Parameters
    ----------
    input_command_line : str
    narg : int
    
    Returns
    -------
    arg : str
    
    """
    arg = _qepy.f90wrap_my_getarg(input_command_line=input_command_line, narg=narg)
    return arg

def set_command_line(nimage=None, npool=None, ntg=None, nyfft=None, nband=None, \
    ndiag=None):
    """
    set_command_line([nimage, npool, ntg, nyfft, nband, ndiag])
    
    
    Defined at command_line_options.fpp lines 227-240
    
    Parameters
    ----------
    nimage : int
    npool : int
    ntg : int
    nyfft : int
    nband : int
    ndiag : int
    
    """
    _qepy.f90wrap_set_command_line(nimage=nimage, npool=npool, ntg=ntg, nyfft=nyfft, \
        nband=nband, ndiag=ndiag)

def get_nargs():
    """
    Element nargs ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 42
    
    """
    return _qepy.f90wrap_command_line_options__get__nargs()

def set_nargs(nargs):
    _qepy.f90wrap_command_line_options__set__nargs(nargs)

def get_nimage_():
    """
    Element nimage_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 44
    
    """
    return _qepy.f90wrap_command_line_options__get__nimage_()

def set_nimage_(nimage_):
    _qepy.f90wrap_command_line_options__set__nimage_(nimage_)

def get_npool_():
    """
    Element npool_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 44
    
    """
    return _qepy.f90wrap_command_line_options__get__npool_()

def set_npool_(npool_):
    _qepy.f90wrap_command_line_options__set__npool_(npool_)

def get_ndiag_():
    """
    Element ndiag_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 44
    
    """
    return _qepy.f90wrap_command_line_options__get__ndiag_()

def set_ndiag_(ndiag_):
    _qepy.f90wrap_command_line_options__set__ndiag_(ndiag_)

def get_nband_():
    """
    Element nband_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 44
    
    """
    return _qepy.f90wrap_command_line_options__get__nband_()

def set_nband_(nband_):
    _qepy.f90wrap_command_line_options__set__nband_(nband_)

def get_ntg_():
    """
    Element ntg_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 44
    
    """
    return _qepy.f90wrap_command_line_options__get__ntg_()

def set_ntg_(ntg_):
    _qepy.f90wrap_command_line_options__set__ntg_(ntg_)

def get_nyfft_():
    """
    Element nyfft_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 44
    
    """
    return _qepy.f90wrap_command_line_options__get__nyfft_()

def set_nyfft_(nyfft_):
    _qepy.f90wrap_command_line_options__set__nyfft_(nyfft_)

def get_library_init():
    """
    Element library_init ftype=logical pytype=bool
    
    
    Defined at command_line_options.fpp line 46
    
    """
    return _qepy.f90wrap_command_line_options__get__library_init()

def set_library_init(library_init):
    _qepy.f90wrap_command_line_options__set__library_init(library_init)

def get_input_file_():
    """
    Element input_file_ ftype=character(len=256) pytype=str
    
    
    Defined at command_line_options.fpp line 48
    
    """
    return _qepy.f90wrap_command_line_options__get__input_file_()

def set_input_file_(input_file_):
    _qepy.f90wrap_command_line_options__set__input_file_(input_file_)

def get_command_line_():
    """
    Element command_line ftype=character(len=512) pytype=str
    
    
    Defined at command_line_options.fpp line 50
    
    """
    return _qepy.f90wrap_command_line_options__get__command_line()

def set_command_line_(command_line):
    _qepy.f90wrap_command_line_options__set__command_line(command_line)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "command_line_options".')

for func in _dt_array_initialisers:
    func()
