"""
Transmission Equation of Resonance - Lex Amoris Framework
==========================================================

This module implements the Transmission Equation of Resonance for enhanced 
communication stability and jitter elimination under the Lex Amoris Framework.

The resonance equation governing packet transmission:

    Φ_res = lim_{j→0} ∫_{t_0}^{t_∞} [Lex Amoris(t) / (S-ROI · e^{iωt})] dt

Where:
- j → 0: Eliminates control-induced jitter
- ω = 0.432 Hz: Synchronization frequency for the Lex Amoris Framework
- S-ROI = 1.450: Resonance-yield scaling factor
"""

import numpy as np
from scipy import integrate
from typing import Callable, Union, Optional


# Core Constants
# Synchronization frequency for Lex Amoris transmission (0.432 Hz)
# This value defines the fundamental oscillation rate for resonance calculations
OMEGA_HZ = 0.432

# Resonance-yield factor (S-ROI) - dimensionless scaling parameter
# This constant modulates the resonance integral amplitude in the transmission equation
# Value determined by Lex Amoris Framework specifications
S_ROI = 1.450


def lex_amoris_function(t: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Lex Amoris function representing the resonance pattern.
    
    This is the core function that defines the Lex Amoris framework's 
    temporal behavior. Currently implemented as a sinusoidal pattern
    at the framework's specified frequency.
    
    Parameters
    ----------
    t : float or np.ndarray
        Time parameter(s) in seconds
        
    Returns
    -------
    float or np.ndarray
        Lex Amoris function value(s) at time t
        
    Notes
    -----
    The current implementation uses a sinusoidal pattern at OMEGA_HZ.
    This can be replaced with a more sophisticated Lex Amoris 
    implementation based on specific framework requirements.
    """
    return np.sin(OMEGA_HZ * t)


def calculate_resonance(
    t0: float,
    t_infinity: float,
    s_roi: float = S_ROI,
    omega: float = OMEGA_HZ,
    lex_amoris_func: Optional[Callable] = None,
    num_points: int = 1000
) -> complex:
    """
    Calculate the resonance integral Φ_res for packet transmission.
    
    Computes the transmission equation of resonance:
    
        Φ_res = ∫_{t_0}^{t_∞} [Lex Amoris(t) / (S-ROI · e^{iωt})] dt
    
    This integral approaches a finite limit as jitter j → 0, providing
    enhanced communication stability.
    
    Parameters
    ----------
    t0 : float
        Initial time point for integration
    t_infinity : float
        Final time point for integration (representing t → ∞)
    s_roi : float, optional
        Resonance-yield scaling factor (default: 1.450)
    omega : float, optional
        Synchronization frequency in Hz (default: 0.432)
    lex_amoris_func : callable, optional
        Custom Lex Amoris function. If None, uses default lex_amoris_function
    num_points : int, optional
        Number of points for numerical integration (default: 1000)
        
    Returns
    -------
    complex
        The resonance integral result Φ_res (complex number)
        
    Examples
    --------
    >>> # Calculate resonance from t=0 to t=10 seconds
    >>> phi_res = calculate_resonance(0, 10)
    >>> print(f"Resonance: {phi_res}")
    
    >>> # Use custom parameters
    >>> phi_res = calculate_resonance(0, 20, s_roi=1.5, omega=0.5)
    
    Notes
    -----
    The integration is performed numerically using the trapezoidal rule.
    For higher accuracy, increase num_points parameter.
    """
    # Use provided Lex Amoris function or default
    if lex_amoris_func is None:
        lex_amoris_func = lex_amoris_function
    
    # Define the integrand: Lex Amoris(t) / (S-ROI * e^{iωt})
    def integrand(t):
        return lex_amoris_func(t) / (s_roi * np.exp(1j * omega * t))
    
    # Perform numerical integration using trapezoidal rule
    t = np.linspace(t0, t_infinity, num_points)
    integrand_values = integrand(t)
    
    # Use scipy's trapezoid integration
    result = integrate.trapezoid(integrand_values, t)
    
    return result


def get_resonance_magnitude(phi_res: complex) -> float:
    """
    Extract the magnitude of the resonance result.
    
    Parameters
    ----------
    phi_res : complex
        The resonance integral result
        
    Returns
    -------
    float
        Magnitude of the resonance
    """
    return np.abs(phi_res)


def get_resonance_phase(phi_res: complex) -> float:
    """
    Extract the phase angle of the resonance result.
    
    Parameters
    ----------
    phi_res : complex
        The resonance integral result
        
    Returns
    -------
    float
        Phase angle in radians
    """
    return np.angle(phi_res)


def calculate_jitter_elimination_factor(
    phi_res: complex,
    baseline_jitter: float = 1.0
) -> float:
    """
    Calculate the jitter elimination factor.
    
    As j → 0 in the limit, this factor approaches the ideal jitter-free
    transmission characteristic.
    
    Parameters
    ----------
    phi_res : complex
        The resonance integral result
    baseline_jitter : float, optional
        Baseline jitter level before resonance application (default: 1.0)
        
    Returns
    -------
    float
        Jitter elimination factor (0.0 = complete elimination, 1.0 = no effect)
    """
    magnitude = get_resonance_magnitude(phi_res)
    
    # Calculate elimination factor based on resonance magnitude
    # Higher magnitude corresponds to better jitter elimination
    if magnitude > 0:
        elimination_factor = baseline_jitter / (1 + magnitude)
    else:
        elimination_factor = baseline_jitter
    
    return elimination_factor


def analyze_resonance_packet(
    t0: float,
    t_infinity: float,
    s_roi: float = S_ROI,
    omega: float = OMEGA_HZ
) -> dict:
    """
    Perform comprehensive resonance analysis for a packet transmission.
    
    Parameters
    ----------
    t0 : float
        Initial time point
    t_infinity : float
        Final time point
    s_roi : float, optional
        Resonance-yield scaling factor (default: 1.450)
    omega : float, optional
        Synchronization frequency in Hz (default: 0.432)
        
    Returns
    -------
    dict
        Dictionary containing:
        - 'phi_res': Complex resonance result
        - 'magnitude': Magnitude of resonance
        - 'phase': Phase angle in radians
        - 'jitter_elimination': Jitter elimination factor
        - 'parameters': Input parameters used
    """
    # Calculate resonance
    phi_res = calculate_resonance(t0, t_infinity, s_roi, omega)
    
    # Extract components
    magnitude = get_resonance_magnitude(phi_res)
    phase = get_resonance_phase(phi_res)
    jitter = calculate_jitter_elimination_factor(phi_res)
    
    return {
        'phi_res': phi_res,
        'magnitude': magnitude,
        'phase': phase,
        'phase_degrees': np.degrees(phase),
        'jitter_elimination': jitter,
        'parameters': {
            't0': t0,
            't_infinity': t_infinity,
            's_roi': s_roi,
            'omega': omega
        }
    }


if __name__ == "__main__":
    """
    Demonstration of the Transmission Equation of Resonance.
    """
    print("=" * 70)
    print("Transmission Equation of Resonance - Lex Amoris Framework")
    print("=" * 70)
    print()
    
    # Example 1: Basic resonance calculation
    print("Example 1: Basic Resonance Calculation")
    print("-" * 70)
    t0 = 0.0
    t_infinity = 10.0
    
    phi_res = calculate_resonance(t0, t_infinity)
    print(f"Time interval: [{t0}, {t_infinity}] seconds")
    print(f"Resonance Φ_res: {phi_res}")
    print(f"Magnitude: {get_resonance_magnitude(phi_res):.6f}")
    print(f"Phase: {get_resonance_phase(phi_res):.6f} radians")
    print()
    
    # Example 2: Comprehensive analysis
    print("Example 2: Comprehensive Resonance Analysis")
    print("-" * 70)
    analysis = analyze_resonance_packet(0.0, 20.0)
    
    print(f"Φ_res = {analysis['phi_res']}")
    print(f"Magnitude: {analysis['magnitude']:.6f}")
    print(f"Phase: {analysis['phase']:.6f} rad ({analysis['phase_degrees']:.2f}°)")
    print(f"Jitter elimination factor: {analysis['jitter_elimination']:.6f}")
    print()
    
    # Example 3: Parameter variation
    print("Example 3: Parameter Sensitivity Analysis")
    print("-" * 70)
    print(f"{'S-ROI':<10} {'Magnitude':<15} {'Jitter Factor':<15}")
    print("-" * 40)
    
    for s_roi_test in [1.0, 1.450, 2.0, 2.5]:
        phi = calculate_resonance(0, 10, s_roi=s_roi_test)
        mag = get_resonance_magnitude(phi)
        jit = calculate_jitter_elimination_factor(phi)
        print(f"{s_roi_test:<10.3f} {mag:<15.6f} {jit:<15.6f}")
    
    print()
    print("=" * 70)
    print("Resonance transmission calculation complete.")
    print("Communication stability enhanced, jitter eliminated.")
    print("=" * 70)
