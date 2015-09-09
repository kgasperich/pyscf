#!/usr/bin/env python
# -*- coding: utf-8
# Author: Qiming Sun <osirpt.sun@gmail.com>

import os
import imp
from pyscf.gto.basis import parse_nwchem

def parse(string):
    '''Parse the basis text which is in NWChem format, return an internal
    basis format which can be assigned to :attr:`Mole.basis`

    Args:
        string : Blank linke and the lines of "BASIS SET" and "END" will be ignored

    Examples:

    >>> mol = gto.Mole()
    >>> mol.basis = {'O': gto.basis.parse("""
    ... #BASIS SET: (6s,3p) -> [2s,1p]
    ... C    S
    ...      71.6168370              0.15432897
    ...      13.0450960              0.53532814
    ...       3.5305122              0.44463454
    ... C    SP
    ...       2.9412494             -0.09996723             0.15591627
    ...       0.6834831              0.39951283             0.60768372
    ...       0.2222899              0.70011547             0.39195739
    ... """)}
    '''
    return parse_nwchem.parse_str(string)

def load(basis_name, symb):
    '''Convert the basis of the given symbol to internal format

    Args:
        basis_name : str
            Case insensitive basis set name. Special characters will be removed.
        symb : str
            Atomic symbol, Special characters will be removed.

    Examples:
        Load STO 3G basis of carbon to oxygen atom

    >>> mol = gto.Mole()
    >>> mol.basis = {'O': load('sto-3g', 'C')}
    '''
    alias = {
        'ano'        : 'ano.dat'        ,
        'anoroosdz'  : 'roos-dz.dat'    ,
        'anoroostz'  : 'roos-tz.dat'    ,
        'roosdz'     : 'roos-dz.dat'    ,
        'roostz'     : 'roos-tz.dat'    ,
        'ccpvdz'     : 'cc-pvdz.dat'    ,
        'ccpvtz'     : 'cc-pvtz.dat'    ,
        'ccpvqz'     : 'cc-pvqz.dat'    ,
        'ccpv5z'     : 'cc-pv5z.dat'    ,
        'augccpvdz'  : 'aug-cc-pvdz.dat',
        'augccpvtz'  : 'aug-cc-pvtz.dat',
        'augccpvqz'  : 'aug-cc-pvqz.dat',
        'ccpvdzdk'   : 'cc-pvdz-dk.dat' ,
        'ccpvtzdk'   : 'cc-pvtz-dk.dat' ,
        'ccpvqzdk'   : 'cc-pvqz-dk.dat' ,
        'ccpv5zdk'   : 'cc-pv5z-dk.dat' ,
        'augccpvdzdk': 'aug-cc-pvdz-dk.dat',
        'augccpvtzdk': 'aug-cc-pvtz-dk.dat',
        'augccpvqzdk': 'aug-cc-pvqz-dk.dat',
        'ccpvdzdkh'   : 'cc-pvdz-dk.dat' ,
        'ccpvtzdkh'   : 'cc-pvtz-dk.dat' ,
        'ccpvqzdkh'   : 'cc-pvqz-dk.dat' ,
        'ccpv5zdkh'   : 'cc-pv5z-dk.dat' ,
        'augccpvdzdkh': 'aug-cc-pvdz-dk.dat',
        'augccpvtzdkh': 'aug-cc-pvtz-dk.dat',
        'augccpvqzdkh': 'aug-cc-pvqz-dk.dat',
        'dyalldz'    : 'dyall_dz'       ,
        'dyallqz'    : 'dyall_qz'       ,
        'dyalltz'    : 'dyall_tz'       ,
        'faegredz'   : 'faegre_dz'      ,
        'iglo'       : 'iglo3'          ,
        'iglo3'      : 'iglo3'          ,
        '321g'       : '3-21g.dat'      ,
        '431g'       : '4-31g.dat'      ,
        '631g'       : '6-31g.dat'      ,
        '631gs'      : '6-31gs.dat'     ,
        '6311g'      : '6-311g.dat'     ,
        '6311gs'     : '6-311gs.dat'    ,
        '6311gsp'    : '6-311gsp.dat'   ,
        '6311gps'    : '6-311gsp.dat'   ,
        '631g*'      : '6-31gs.dat'     ,
        '6311g*'     : '6-311gs.dat'    ,
        '6311g*+'    : '6-311gsp.dat'   ,
        '6311g+*'    : '6-311gsp.dat'   ,
        'sto3g'      : 'sto-3g.dat'     ,
        'sto6g'      : 'sto-6g.dat'     ,
        'minao'      : 'minao'          ,
        'dz'         : 'dz.dat'         ,
        'dzpdunning' : 'dzp_dunning'    ,
        'dzp'        : 'dzp.dat'        ,
        'tzp'        : 'tzp.dat'        ,
        'qzp'        : 'qzp.dat'        ,
        'dzpdk'      : 'dzp-dkh.dat'    ,
        'tzpdk'      : 'tzp-dkh.dat'    ,
        'qzpdk'      : 'qzp-dkh.dat'    ,
        'dzpdkh'     : 'dzp-dkh.dat'    ,
        'tzpdkh'     : 'tzp-dkh.dat'    ,
        'qzpdkh'     : 'qzp-dkh.dat'    ,
        'def2svp'    : 'def2-svp.dat'   ,
        'def2svpd'   : 'def2-svpd.dat'  ,
        'def2qzvpd'  : 'def2-qzvpd.dat' ,
        'def2qzvppd' : 'def2-qzvppd.dat',
        'def2qzvpp'  : 'def2-qzvpp.dat' ,
        'def2qzvp'   : 'def2-qzvp.dat'  ,
        'def2tzvpd'  : 'def2-tzvpd.dat' ,
        'def2tzvppd' : 'def2-tzvppd.dat',
        'def2tzvpp'  : 'def2-tzvpp.dat' ,
        'def2tzvp'   : 'def2-tzvp.dat'  ,
        'tzv'        : 'tzv.dat'        ,
        'weigend'    : 'weigend_cfit.dat',
        'demon'      : 'demon_cfit.dat' ,
        'ahlrichs'   : 'ahlrichs_cfit.dat',
        'ccpvtzfit'  : 'cc-pvtz_fit.dat',
        'ccpvdzfit'  : 'cc-pvdz_fit.dat',
        'dgaussa1cfit': 'DgaussA1_dft_cfit.dat',
        'dgaussa1xfit': 'DgaussA1_dft_xfit.dat',
        'dgaussa2cfit': 'DgaussA2_dft_cfit.dat',
        'dgaussa2xfit': 'DgaussA2_dft_xfit.dat',
    }
    name = basis_name.lower().replace(' ', '').replace('-', '').replace('_', '')
    basmod = alias[name]
    symb = ''.join(i for i in symb if i.isalpha())
    if 'dat' in basmod:
        b = parse_nwchem.parse(os.path.join(os.path.dirname(__file__), basmod), symb)
    else:
        fp, pathname, description = imp.find_module(basmod, __path__)
        mod = imp.load_module(name, fp, pathname, description)
        #mod = __import__(basmod, globals={'__path__': __path__, '__name__': __name__})
        b = mod.__getattribute__(symb)
        fp.close()
    return b

