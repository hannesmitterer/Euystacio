# Transmission Equation of Resonance - User Guide

## Overview

The Transmission Equation of Resonance module implements the mathematical framework for enhanced communication stability and jitter elimination under the Lex Amoris Framework.

## Mathematical Formula

The resonance equation governing packet transmission:

```
Φ_res = lim_{j→0} ∫[t₀ to t∞] [Lex Amoris(t) / (S-ROI · e^{iωt})] dt
```

Where:
- **j → 0**: Eliminates control-induced jitter
- **ω = 0.432 Hz**: Synchronization frequency for the Lex Amoris Framework
- **S-ROI = 1.450**: Resonance-yield scaling factor

## Quick Start

### Basic Usage

```python
from resonance_transmission import calculate_resonance, analyze_resonance_packet

# Calculate resonance for time interval [0, 10] seconds
phi_res = calculate_resonance(t0=0.0, t_infinity=10.0)
print(f"Resonance result: {phi_res}")

# Perform comprehensive analysis
analysis = analyze_resonance_packet(t0=0.0, t_infinity=10.0)
print(f"Magnitude: {analysis['magnitude']:.4f}")
print(f"Phase: {analysis['phase_degrees']:.2f}°")
print(f"Jitter elimination: {analysis['jitter_elimination']:.4f}")
```

### Custom Parameters

```python
# Use custom S-ROI and omega values
phi_res = calculate_resonance(
    t0=0.0,
    t_infinity=20.0,
    s_roi=2.0,      # Custom resonance-yield factor
    omega=0.5       # Custom frequency in Hz
)
```

### Custom Lex Amoris Function

```python
import numpy as np

# Define a custom Lex Amoris function
def my_lex_amoris(t):
    return np.cos(0.5 * t) + 0.5 * np.sin(0.3 * t)

# Use it in calculations
phi_res = calculate_resonance(
    t0=0.0,
    t_infinity=15.0,
    lex_amoris_func=my_lex_amoris
)
```

## API Reference

### Functions

#### `calculate_resonance(t0, t_infinity, s_roi=1.450, omega=0.432, lex_amoris_func=None, num_points=1000)`

Calculate the resonance integral Φ_res.

**Parameters:**
- `t0` (float): Initial time point
- `t_infinity` (float): Final time point
- `s_roi` (float, optional): Resonance-yield scaling factor (default: 1.450)
- `omega` (float, optional): Synchronization frequency in Hz (default: 0.432)
- `lex_amoris_func` (callable, optional): Custom Lex Amoris function
- `num_points` (int, optional): Number of integration points (default: 1000)

**Returns:**
- `complex`: The resonance integral result

#### `analyze_resonance_packet(t0, t_infinity, s_roi=1.450, omega=0.432)`

Perform comprehensive resonance analysis.

**Returns:** Dictionary containing:
- `phi_res`: Complex resonance result
- `magnitude`: Magnitude of resonance
- `phase`: Phase angle in radians
- `phase_degrees`: Phase angle in degrees
- `jitter_elimination`: Jitter elimination factor
- `parameters`: Input parameters used

#### `get_resonance_magnitude(phi_res)`

Extract the magnitude from a resonance result.

#### `get_resonance_phase(phi_res)`

Extract the phase angle (in radians) from a resonance result.

#### `calculate_jitter_elimination_factor(phi_res, baseline_jitter=1.0)`

Calculate the jitter elimination factor. Lower values indicate better jitter elimination.

## Examples

### Example 1: Basic Calculation

```python
from resonance_transmission import calculate_resonance, get_resonance_magnitude

phi_res = calculate_resonance(0.0, 10.0)
magnitude = get_resonance_magnitude(phi_res)
print(f"Resonance magnitude: {magnitude:.4f}")
```

### Example 2: Parameter Sensitivity Analysis

```python
from resonance_transmission import calculate_resonance, get_resonance_magnitude

# Test different S-ROI values
for s_roi in [1.0, 1.450, 2.0, 2.5]:
    phi = calculate_resonance(0, 10, s_roi=s_roi)
    mag = get_resonance_magnitude(phi)
    print(f"S-ROI={s_roi:.3f}: Magnitude={mag:.4f}")
```

### Example 3: Jitter Analysis

```python
from resonance_transmission import (
    calculate_resonance,
    calculate_jitter_elimination_factor
)

phi_res = calculate_resonance(0.0, 20.0)
jitter_factor = calculate_jitter_elimination_factor(phi_res)
jitter_reduction_percent = (1 - jitter_factor) * 100

print(f"Jitter reduction: {jitter_reduction_percent:.1f}%")
```

## Running Tests

To verify the installation and run the test suite:

```bash
python3 test_resonance_transmission.py
```

Expected output: All 26 tests should pass.

## Technical Notes

- The implementation uses numerical integration via scipy's `trapezoid` method
- Complex number arithmetic is used throughout for phase-sensitive calculations
- Higher `num_points` values provide more accurate integration at the cost of computation time
- The default parameters (ω=0.432 Hz, S-ROI=1.450) are specified by the Lex Amoris Framework

## Integration with Euystacio

This module complements the existing Eternal Resonance Protocol (ERP) which operates at 0.043 Hz. While the ERP provides global synchronization, the Transmission Equation of Resonance (0.432 Hz) focuses on packet-level communication stability.

## Dependencies

- `numpy`: Numerical operations and array handling
- `scipy`: Numerical integration

Install with:
```bash
pip install numpy scipy
```

## License

See [SACRED_COMMONS_LICENSE.md](./SACRED_COMMONS_LICENSE.md) for license information.
