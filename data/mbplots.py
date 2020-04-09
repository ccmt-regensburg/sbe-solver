import matplotlib.pyplot as plt
import numpy as np
from plot_utilities import read_data, logplot_fourier

fs_conv = 41.34137335                  # (1fs    = 41.341473335 a.u.)
E_conv = 0.0001944690381               # (1MV/cm = 1.944690381*10^-4 a.u.)
THz_conv = 0.000024188843266           # (1THz   = 2.4188843266*10^-5 a.u.)
amp_conv = 150.97488474                # (1A     = 150.97488474)
eV_conv = 0.03674932176                # (1eV    = 0.036749322176 a.u.)


plt.rcParams['text.usetex'] = True
plt.rcParams['figure.figsize'] = (20, 10)
plt.rcParams['font.size'] = 20


orderpath = './data-sbe/resummed_hamiltonian/Msweep_E2.5MV_dt0.01_Nk1-800_Nk2-80_T1on/'
parampaths = ['mb_{:.0f}meV/'.format(m) for m in np.arange(0, 15, 10)]
paramlegend = [m.strip('/').replace('_', '=') for m in parampaths]
dirpath = 'K_dir/'
dirname = dirpath.strip('/').replace('_', '-').replace('/', '-')

Idata, Iexactdata, Jdata, Pdata = read_data(orderpath, dirpath, parampaths)
freqw = Idata[:, 3]
Int_E_dir = Idata[:, 6]
Int_ortho = Idata[:, 7]
ylabel = r'$[I](\omega)$ intensity in a.u.'
logplot_fourier(freqw, Int_E_dir, Int_ortho, ylabel=ylabel,
                paramlegend=paramlegend, dirname=dirname,
                savename='Int-' + dirname)

freqw = Iexactdata[:, 3]
Int_exact_E_dir = Iexactdata[:, 6]
Int_exact_ortho = Iexactdata[:, 7]
ylabel = r'$[I_\mathrm{exact}](\omega)$ intensity in a.u.'
logplot_fourier(freqw, Int_exact_E_dir, Int_exact_ortho, ylabel=ylabel,
                paramlegend=paramlegend, dirname=dirname,
                savename='Int-exact-' + dirname)


# Iw_E_dir = Idata[:, 4]
# Iw_ortho = Idata[:, 5]
# ylabel = r'$[\dot P](\omega)$ (total = emitted E-field) in a.u.'
# logplot_fourier(freqw, np.abs(Iw_E_dir), np.abs(Iw_ortho), ylabel=ylabel,
#                 savename='Iw-' + dirname)

# Jw_E_dir = Jdata[:, 4]
# Jw_ortho = Jdata[:, 5]
# ylabel = r'$[\dot P](\omega)$ (intraband) in a.u. $\parallel \mathbf{E}_{in}$ (blue), $\bot \mathbf{E}_{in}$ (orange)'
# logplot_fourier(freqw, np.abs(Jw_E_dir), np.abs(Jw_ortho), ylabel=ylabel,
#                 savename='Jw-' + dirname)

# Pw_E_dir = Pdata[:, 4]
# Pw_ortho = Pdata[:, 5]
# ylabel = r'$[\dot P](\omega)$ (interband) in a.u. $\parallel \mathbf{E}_{in}$ (blue), $\bot \mathbf{E}_{in}$ (orange)'
# logplot_fourier(freqw, np.abs(Pw_E_dir), np.abs(Pw_ortho), ylabel=ylabel,
#                 savename='Pw-' + dirname)
