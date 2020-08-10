import numpy as np
import os
from params import params

import hfsbe.dipole
import hfsbe.example
import hfsbe.utility
# Set BZ type independent parameters
# Hamiltonian parameters
from SBE import main as solver


def run():

    C2                  = 5.39018     # k^2 coefficient
    A                   = 0.19732     # Fermi velocity
    R                   = 5.52658     # k^3 coefficient
    mb                  = 0.000373195 # Splitting of cones.(10 meV)
    k_cut               = 0.05        # Model hamiltonian cutoff
    order               = 4           # hz order in periodic hamiltonian
     
    # Initialize sympy bandstructure, energies/derivatives, dipoles
    # ## Bismuth Teluride calls
    # system = hfsbe.example.BiTe(C0=C0, C2=C2, A=A, R=R, kcut=k_cut)
    # Sweep Wilson mass
    for E in np.arange(2.00, 4.10, 0.50):
        mw = 0
        print("Current C2: ", C2)
        print("Current mass: ", mw)
        params.E0 = E
        print("Current E-field: ", params.E0)
        dirname = 'E_{:1.2f}'.format(params.E0)
        if (not os.path.exists(dirname)):
            os.mkdir(dirname)
        os.chdir(dirname)
        # system = hfsbe.example.BiTe(C0=0, C2=C2, A=A, R=R, mb=mb, kcut=k_cut)
        system = hfsbe.example.BiTePeriodic(C2=C2, A=A, R=R, a=params.a,
                                            mw=mw, mb=mb, order=order)
        h_sym, ef_sym, wf_sym, ediff_sym = system.eigensystem(gidx=1)
        dipole = hfsbe.dipole.SymbolicDipole(h_sym, ef_sym, wf_sym)
        solver(system, dipole, params)
        os.chdir('..')


if __name__ == "__main__":
    run()