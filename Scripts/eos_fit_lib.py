#!/usr/bin/env python3
import numpy as np
from scipy.optimize import leastsq

np.random.seed(seed=42)


def equation_of_state(psibarpsi, beta, am, A, betac, p, B, delta):
    """Powerlaw equation of state - lhs"""
    return np.array(
        A * (beta - betac) * psibarpsi**p + B * psibarpsi**delta - am,
        dtype=np.float64)


def error_on_equation_of_state_bootstrap(psibarpsi, psibarpsiErr, beta, am, A,
                                         betac, p, B, delta):
    """Error on Powerlaw equation of state - lhs"""
    eqerrors = []
    nbootstrap = 500
    bootstrap_values = np.random.normal(size=nbootstrap)
    for i in range(nbootstrap):  # bootstrap with 10 samples
        pbp = psibarpsi + psibarpsiErr * bootstrap_values[i]
        eqerrors.append(
            equation_of_state(pbp, beta, am, A, betac, p, B, delta))

    return np.vstack(eqerrors).std(axis=0)


def error_on_equation_of_state_derivs(psibarpsi, psibarpsiErr, beta, am, A,
                                      betac, p, B, delta):
    """Error on Powerlaw equation of state - lhs"""
    return np.array(
        (A * (beta - betac) * p * psibarpsi**(p - 1) + B * delta * psibarpsi**
         (delta - 1) - am) * psibarpsiErr,
        dtype=np.float64)


def residuals(params,
              beta,
              psibarpsi,
              psibarpsiErr,
              am,
              error_on_equation_of_state_f=error_on_equation_of_state_derivs):
    A, betac, p, B, delta = params
    num = equation_of_state(psibarpsi, beta, am, A, betac, p, B, delta)
    den = error_on_equation_of_state_f(psibarpsi, psibarpsiErr, beta, am, A,
                                       betac, p, B, delta)
    return num / den

initial_guesses = {
    12: {  # L
        8:  # Ls
        np.array([1.61942364, 0.04759547, 1.00925691, 1.76346148, 3.07111699]),
        16:  # Ls
        np.array([ 2.19456444,  0.16955859,  1.0226929,  78.99706323,  5.11663105]),
        24:  # Ls
        np.array([2.39404955, 0.2123614,  1.01420946, 2.99930075, 3.25397893]),
        32:  # Ls
        np.array([2.90937512, 0.24170218, 1.0349304, 9.66141308, 3.85308926]),
        40:  # Ls
        np.array([3.30445818, 0.25055222, 1.06456595, 32.295855, 4.64339238]),
        48:  # Ls
        np.array([3.11646997, 0.25647005, 1.0538188, 11.59937539, 3.94485828])
    },
    16: {  # L
        8:  # Ls
        np.array([1.61942364, 0.04759547, 1.00925691, 1.76346148, 3.07111699]),
        16:  # Ls
        np.array([ 2.19456444,  0.16955859,  1.0226929,  78.99706323,  5.11663105]),
        24:  # Ls
        np.array([2.39404955, 0.2123614,  1.01420946, 2.99930075, 3.25397893]),
        32:  # Ls
        np.array([2.90937512, 0.24170218, 1.0349304, 9.66141308, 3.85308926]),
        40:  # Ls
        np.array([3.30445818, 0.25055222, 1.06456595, 32.295855, 4.64339238]),
        48:  # Ls
        np.array([3.11646997, 0.25647005, 1.0538188, 11.59937539, 3.94485828])
    }
}

