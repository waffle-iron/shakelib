#!/usr/bin/env python

import numpy as np
import pytest

import os.path
import sys

homedir = os.path.dirname(os.path.abspath(__file__))  # where is this script?
shakedir = os.path.abspath(os.path.join(homedir, '..', '..', '..'))
sys.path.insert(0, shakedir)

import shakelib.grind.correlation.boore_2003 as b03


def test_boore2003():
    cormod = b03.Boore2003()
    d = np.linspace(0, 10, 101)
    cor = cormod.getSpatialCorrelation(d)
    cor_target = np.array(
        [1.,  0.78274448,  0.70722235,  0.65425109,  0.61268892,
         0.57826528,  0.54881164,  0.52305217,  0.50016346,  0.47957887,
         0.46088963,  0.44378998,  0.42804449,  0.41346762,  0.39991025,
         0.38725058,  0.37538771,  0.36423701,  0.35372678,  0.34379565,
         0.33439073,  0.32546602,  0.31698129,  0.30890113,  0.30119421,
         0.29383266,  0.28679156,  0.28004858,  0.27358357,  0.26737835,
         0.26141639,  0.25568267,  0.25016348,  0.24484627,  0.23971952,
         0.23477265,  0.22999589,  0.22538022,  0.22091729,  0.21659937,
         0.21241926,  0.20837025,  0.20444612,  0.20064104,  0.19694955,
         0.19336655,  0.18988726,  0.18650718,  0.18322209,  0.18002801,
         0.17692121,  0.17389814,  0.17095547,  0.16809005,  0.16529889,
         0.16257917,  0.15992821,  0.15734346,  0.15482253,  0.1523631,
         0.14996301,  0.14762018,  0.14533263,  0.14309848,  0.14091593,
         0.13878327,  0.13669886,  0.13466114,  0.1326686,  0.13071982,
         0.12881344,  0.12694812,  0.12512263,  0.12333575,  0.12158633,
         0.11987325,  0.11819545,  0.11655191,  0.11494164,  0.11336369,
         0.11181716,  0.11030117,  0.10881487,  0.10735745,  0.10592813,
         0.10452615,  0.10315079,  0.10180135,  0.10047714,  0.09917751,
         0.09790183,  0.0966495,  0.09541991,  0.0942125,  0.09302673,
         0.09186205,  0.09071795,  0.08959394,  0.08848952,  0.08740424,
         0.08633763]
    )
    np.testing.assert_allclose(cor, cor_target)

    with pytest.raises(Exception) as a:
        cormod.getSpatialCorrelation(d, imt="PGV")


if __name__ == '__main__':
    test_boore2003()