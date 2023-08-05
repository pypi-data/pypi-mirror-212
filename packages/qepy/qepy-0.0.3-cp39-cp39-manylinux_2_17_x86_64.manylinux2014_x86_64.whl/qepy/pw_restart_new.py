"""
Module pw_restart_new


Defined at pw_restart_new.fpp lines 13-1255

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging

_arrays = {}
_objs = {}

def pw_write_schema(only_init, wf_collect):
    """
    pw_write_schema(only_init, wf_collect)
    
    
    Defined at pw_restart_new.fpp lines 60-675
    
    Parameters
    ----------
    only_init : bool
    wf_collect : bool
    
    ------------------------------------------------------------------------
     only_init  = T  write only variables that are known after the
                     initial steps of initialization(e.g. structure)
                = F  write the complete xml file
     wf_collect = T  if final wavefunctions in portable format are written,
                  F  if wavefunctions are either not written or are written
                     in binary non-portable form(for checkpointing)
                     NB: wavefunctions are not written here in any case
    """
    _qepy.f90wrap_pw_write_schema(only_init=only_init, wf_collect=wf_collect)

def pw_write_binaries():
    """
    pw_write_binaries()
    
    
    Defined at pw_restart_new.fpp lines 679-803
    
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_pw_write_binaries()

def read_xml_file():
    """
    wfc_is_collected = read_xml_file()
    
    
    Defined at pw_restart_new.fpp lines 891-1136
    
    
    Returns
    -------
    wfc_is_collected : bool
    
    ------------------------------------------------------------------------
     ... This routine allocates space for all quantities already computed
     ... in the pwscf program and reads them from the data file.
     ... All quantities that are initialized in subroutine "setup" when
     ... starting from scratch should be initialized here when restarting
    """
    wfc_is_collected = _qepy.f90wrap_read_xml_file()
    return wfc_is_collected

def read_collected_wfc(dirname, ik, evc):
    """
    read_collected_wfc(dirname, ik, evc)
    
    
    Defined at pw_restart_new.fpp lines 1140-1253
    
    Parameters
    ----------
    dirname : str
    ik : int
    evc : complex array
    
    ------------------------------------------------------------------------
     ... reads from directory "dirname" (new file format) for k-point "ik"
     ... wavefunctions from collected format into distributed array "evc"
    """
    _qepy.f90wrap_read_collected_wfc(dirname=dirname, ik=ik, evc=evc)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "pw_restart_new".')

for func in _dt_array_initialisers:
    func()
