from numba import njit
import numpy as np
import params 

# Driving field parameters

w     = params.w*params.THz_conv                         # Driving pulse frequency
chirp = params.chirp*params.THz_conv                     # Pulse chirp frequency
alpha = params.alpha*params.fs_conv                      # Gaussian pulse width
phase = params.phase                              # Carrier-envelope phase

fitted_pulse    = params.fitted_pulse
tOpt, nOpt      = np.transpose(np.loadtxt("driving_field_parameters.txt") ) 
nOpt[2]         = params.nir_mu*params.fs_conv

#nOpt            = tOpt
#nOpt[4]         = 0
#nOpt[3]         *= 4

a   = nOpt[0]
b   = nOpt[1]
c   = nOpt[2]
d   = nOpt[3]
e   = nOpt[4]

nir_E0      = nOpt[0]
nir_sigma   = nOpt[1]
nir_mu      = nOpt[2]
nir_w       = nOpt[3]
nir_phi     = nOpt[4]

with_transient  = True

#if fitted_pulse:
#    parameters = nir.opt_pulses()
#
#    print("Amplitude (without unit) =", parameters[0] )
#    print("Broadening Gauss [fs]    =", parameters[1]/params.fs_conv  )
#    print("Time shift [fs]          =", parameters[2]/params.fs_conv  )
#    print("Frequency [THz]          =", parameters[3]/params.THz_conv )
#    print("Chirp [THz]              =", parameters[4]/params.THz_conv )
#    print("Phase                    =", parameters[5] )

@njit
def driving_field(Amplitude, t):
    '''
    Returns the instantaneous driving pulse field
    '''
    # Non-pulse
    # return E0*np.sin(2.0*np.pi*w*t)
    # Chirped Gaussian pulse
    if fitted_pulse:
        if with_transient:
            return transient(t, tOpt[0], tOpt[1], tOpt[2], tOpt[3], tOpt[4]) + nir(t, a, b, c, d, e)

        else:
            return nir.nir(t, a, b, c, d, e)

    else:
        return Amplitude*np.exp(-t**2.0/(2.0*alpha)**2)*np.sin(2.0*np.pi*w*t*(1 + chirp*t) + phase)


@njit
def transient(x, aT, sigmaT, muT, freqT, chirpT):
    return aT*np.exp(-((x-muT)/sigmaT)**2/2)*np.cos(2*np.pi*(1+chirpT*x)*freqT*x)

@njit
def nir(x, aN, sigmaN, muN, freqN, phiN):
    return aN*np.exp(-(x-muN)**2/sigmaN**2/2)*np.cos(2*np.pi*freqN*(x-muN)+phiN )

