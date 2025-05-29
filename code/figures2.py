import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures
plt.style.use('default')
sns.set_palette("viridis") # Using a consistent, perceptually uniform colormap
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 13, # Slightly larger title
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 16, # Main figure title
    'lines.linewidth': 2,
    'axes.grid': True,
    'grid.linestyle': ':',
    'grid.alpha': 0.7,
    'figure.constrained_layout.use': True # Helps with layout
})

# --- Constants for Seawater Properties ---
# For density calculation (IES 80, simplified for ρ(S,T,0))
# Coefficients for ρ_w (pure water density) as a function of T (degC)
# (Polynomial fit to standard data, for illustrative purposes)
RHO_COEFFS = [9.9983952e+02, 6.793952e-02, -9.095290e-03, 1.001685e-04, -1.120083e-06, 6.536332e-09]
# Coefficients for effect of Salinity (S) on density
# (Simplified from IES 80 structure for illustration)
A_COEFFS = [8.24493e-1, -4.0899e-3, 7.6438e-5, -8.2467e-7, 5.3875e-9]
B_COEFFS = [-5.72466e-3, 1.0227e-4, -1.6546e-6]
C_COEFF = 4.8314e-4

def calculate_seawater_density_ies80_simplified(S, T):
    """
    Simplified calculation of seawater density at atmospheric pressure based on IES 80.
    S in PSU, T in degC. Returns density in kg/m^3.
    This is an illustrative simplification. For precise oceanographic work, use full IES 80.
    """
    T_poly = np.polyval(RHO_COEFFS[::-1], T) # Pure water density component
    A_S = (A_COEFFS[0] + (A_COEFFS[1] + (A_COEFFS[2] + (A_COEFFS[3] + A_COEFFS[4]*T)*T)*T)*T)
    B_S_sqrt = (B_COEFFS[0] + (B_COEFFS[1] + B_COEFFS[2]*T)*T)
    density = T_poly + A_S*S + B_S_sqrt*(S**1.5) + C_COEFF*(S**2)
    return density

def calculate_refractive_index_seawater(S, T, wavelength_nm=532):
    """
    Calculates refractive index of seawater.
    S in PSU, T in degC. Wavelength in nm.
    Using formula structure from Quan and Fry (1995) or similar simplified forms.
    For this example, using coefficients from Shang et al. (2015) for λ=532nm as mentioned in prompt.
    n(S,T) = n0 + nS*S + nT*T + nST*S*T + nT2*T^2 + nS2*S^2
    Coefficients for λ = 532 nm from Shang et al. (2015) are approximately:
    n = 1.33374 + 1.831e-4 * S - 2.105e-6 * T - 3.89e-8 * T^2
    (Note: Original paper might have more terms or slightly different coefficients. This is for illustration.)
    """
    n0 = 1.33374
    nS_coeff = 1.831e-4
    nT_coeff = -2.105e-6
    nT2_coeff = -3.89e-8
    # nST and nS2 terms are small for typical ranges or zero in some simplifications for specific wavelengths.
    # Using the simplified form from the prompt:
    n = n0 + nS_coeff * S + nT_coeff * T + nT2_coeff * (T**2)
    return n

# Figure 7: Detectability of Oceanic Pycnoclines by Biomimetic Schlieren Vision
def create_figure7_improved():
    fig = plt.figure(figsize=(14, 10)) # Adjusted for better layout
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25) # Increased hspace

    # --- Simulation Parameters ---
    depth = np.linspace(0, 350, 350) # Depth in meters
    
    # Temperature profile (stronger thermocline)
    T_surface = 25.0  # Surface temperature (°C)
    T_deep = 5.0      # Deep water temperature (°C)
    thermocline_center = 70
    thermocline_thickness = 30 # Made sharper
    temperature = T_deep + (T_surface - T_deep) / (1 + np.exp((depth - thermocline_center) / (thermocline_thickness / 4)))

    # Salinity profile (halocline slightly more pronounced)
    S_surface = 34.5  # Surface salinity (PSU)
    S_deep = 35.0     # Deep water salinity (PSU)
    halocline_center = 100
    halocline_thickness = 40 # Made sharper
    salinity = S_surface + (S_deep - S_surface) / (1 + np.exp(-(depth - halocline_center) / (halocline_thickness / 4)))
    salinity[depth < 20] = S_surface # Ensure surface layer is well mixed salinity

    # --- Panel A: Simulated Oceanic Profiles ---
    axA = fig.add_subplot(gs[0, 0])
    color_temp = 'crimson'
    axA.plot(temperature, -depth, color=color_temp, label='Temperature (°C)')
    axA.set_xlabel('Temperature (°C)', color=color_temp)
    axA.tick_params(axis='x', labelcolor=color_temp)
    axA.set_ylabel('Depth (m)')

    axA_twin = axA.twiny() # Share y-axis
    color_sal = 'steelblue'
    axA_twin.plot(salinity, -depth, color=color_sal, linestyle='--', label='Salinity (PSU)')
    axA_twin.set_xlabel('Salinity (PSU)', color=color_sal)
    axA_twin.tick_params(axis='x', labelcolor=color_sal)

    axA.set_ylim(-250, 0)
    axA.set_title('A) Simulated Oceanic Profiles')
    lines, labels = axA.get_legend_handles_labels()
    lines2, labels2 = axA_twin.get_legend_handles_labels()
    axA_twin.legend(lines + lines2, labels + labels2, loc='lower right', fontsize=8)
    axA.grid(True, linestyle=':', alpha=0.7)
    axA_twin.grid(False) # Avoid double grid

    # Source text for Panel A
    source_text_A = "Profiles simulated based on typical subtropical ocean patterns\n(e.g., Argo Program data with sharpened gradients for illustration)."
    axA.text(0.02, 0.02, source_text_A, transform=axA.transAxes, fontsize=7,
             ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))


    # --- Panel B: Calculated Seawater Density & Refractive Index ---
    axB = fig.add_subplot(gs[0, 1])
    density_profile = calculate_seawater_density_ies80_simplified(salinity, temperature)
    refractive_index_profile = calculate_refractive_index_seawater(salinity, temperature)

    color_dens = 'forestgreen'
    axB.plot(density_profile, -depth, color=color_dens, label='Density (kg/m³)')
    axB.set_xlabel('Density (kg/m³)', color=color_dens)
    axB.tick_params(axis='x', labelcolor=color_dens)
    axB.set_ylabel('Depth (m)')

    axB_twin = axB.twiny()
    color_n = 'darkviolet'
    # Formatting refractive index to show small changes
    n_mean = np.mean(refractive_index_profile)
    axB_twin.plot(refractive_index_profile, -depth, color=color_n, linestyle='--', label='Refractive Index')
    axB_twin.set_xlabel('Refractive Index (n)', color=color_n)
    axB_twin.tick_params(axis='x', labelcolor=color_n, rotation=30)
    axB_twin.xaxis.set_major_formatter(plt.FormatStrFormatter('%.6f'))


    axB.set_ylim(-250, 0)
    axB.set_title('B) Calculated Density & Refractive Index')
    lines, labels = axB.get_legend_handles_labels()
    lines2, labels2 = axB_twin.get_legend_handles_labels()
    axB_twin.legend(lines + lines2, labels + labels2, loc='lower right', fontsize=8)
    axB.grid(True, linestyle=':', alpha=0.7)
    axB_twin.grid(False)

    # Source text for Panel B
    source_text_B = "Density: Simplified IES 80. Refractive Index: Shang et al. (2015) for λ=532nm.\n(Calculations are illustrative)."
    axB.text(0.02, 0.02, source_text_B, transform=axB.transAxes, fontsize=7,
             ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))

    # --- Panel C: Calculated Vertical Gradients (Pycnoclines) ---
    axC = fig.add_subplot(gs[1, 0])
    dz = np.abs(depth[1] - depth[0]) # Depth step

    d_rho_dz = np.abs(np.gradient(density_profile, dz))
    d_n_dz = np.abs(np.gradient(refractive_index_profile, dz))

    color_d_rho = 'darkorange'
    axC.plot(d_rho_dz, -depth, color=color_d_rho, label=r'$|\partial\rho/\partial z|$ (kg/m$^4$)')
    axC.set_xlabel(r'$|\partial\rho/\partial z|$ (kg/m$^4$)', color=color_d_rho)
    axC.tick_params(axis='x', labelcolor=color_d_rho)
    axC.set_ylabel('Depth (m)')

    axC_twin = axC.twiny()
    color_d_n = 'deepskyblue'
    axC_twin.plot(d_n_dz, -depth, color=color_d_n, linestyle='--', label=r'$|\partial n/\partial z|$ (m$^{-1}$)')
    axC_twin.set_xlabel(r'$|\partial n/\partial z|$ (m$^{-1}$)', color=color_d_n)
    axC_twin.tick_params(axis='x', labelcolor=color_d_n)
    axC_twin.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1e')) # Scientific notation

    axC.set_ylim(-250, 0)
    axC.set_title('C) Vertical Gradients (Pycnoclines)')
    lines, labels = axC.get_legend_handles_labels()
    lines2, labels2 = axC_twin.get_legend_handles_labels()
    axC_twin.legend(lines + lines2, labels + labels2, loc='upper right', fontsize=8)
    axC.grid(True, linestyle=':', alpha=0.7)
    axC_twin.grid(False)

    # --- Panel D: Detectability by Schlieren Models ---
    axD = fig.add_subplot(gs[1, 1])

    # Hypothetical Minimum Detectable Refractive Index Gradients ( (∂n/∂z)_min )
    # These are parameters of the *models*, not derived from the oceanic data itself
    threshold_amphibian = 1.0e-5  # m^-1 (Most sensitive)
    threshold_bird = 3.0e-5       # m^-1 (Intermediate)
    threshold_insect = 8.0e-5     # m^-1 (Least sensitive for this fine gradient)

    axD.semilogx(d_n_dz, -depth, color='black', linewidth=1.5, label=r'Actual $|\partial n/\partial z|$')

    # Plot thresholds as vertical lines
    axD.axvline(threshold_amphibian, color='blue', linestyle=':', linewidth=1.5, label=f'Amphibian Threshold ({threshold_amphibian:.1e})')
    axD.axvline(threshold_bird, color='green', linestyle=':', linewidth=1.5, label=f'Bird Threshold ({threshold_bird:.1e})')
    axD.axvline(threshold_insect, color='red', linestyle=':', linewidth=1.5, label=f'Insect Threshold ({threshold_insect:.1e})')

    # Shaded regions where actual gradient exceeds threshold
    axD.fill_betweenx(-depth, threshold_amphibian, d_n_dz, where=(d_n_dz >= threshold_amphibian),
                      color='blue', alpha=0.2, interpolate=True, label='Amphibian Detects')
    axD.fill_betweenx(-depth, threshold_bird, d_n_dz, where=(d_n_dz >= threshold_bird),
                      color='green', alpha=0.2, interpolate=True, label='Bird Detects')
    axD.fill_betweenx(-depth, threshold_insect, d_n_dz, where=(d_n_dz >= threshold_insect),
                      color='red', alpha=0.2, interpolate=True, label='Insect Detects')

    axD.set_xlabel(r'$|\partial n/\partial z|$ (m$^{-1}$)')
    axD.set_ylabel('Depth (m)')
    axD.set_ylim(-250, 0)
    axD.set_xlim(left=1e-6, right=max(np.max(d_n_dz)*1.5, threshold_insect*2)) # Adjust xlim for log
    axD.set_title('D) Detectability by Schlieren Models')

    # Sort legend items for Panel D
    handles, labels = axD.get_legend_handles_labels()
    # Define a preferred order or sort by threshold if needed
    order = [labels.index(r'Actual $|\partial n/\partial z|$'),
             labels.index(f'Amphibian Threshold ({threshold_amphibian:.1e})'),
             labels.index('Amphibian Detects'),
             labels.index(f'Bird Threshold ({threshold_bird:.1e})'),
             labels.index('Bird Detects'),
             labels.index(f'Insect Threshold ({threshold_insect:.1e})'),
             labels.index('Insect Detects')
            ]
    axD.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='best', fontsize=8)
    axD.grid(True, which="both", ls=":", alpha=0.7) # Grid for semilog

    # Explanatory note for Panel D
    note_text_D = "Note: Minimum detectable gradients for models are hypothetical, based on assumed sensitivities\nand amplification factors from the paper's framework. Thresholds are m⁻¹."
    axD.text(0.02, 0.02, note_text_D, transform=axD.transAxes, fontsize=7,
             ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))


    fig.suptitle('Figure 7: Detectability of Oceanic Pycnoclines by Biomimetic Schlieren Vision', fontsize=16, fontweight='bold')
    # fig.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ensure suptitle and bottom notes fit
    return fig

if __name__ == '__main__':
    fig7_improved = create_figure7_improved()
    plt.savefig("figure7_detectability_pycnoclines_improved.png", dpi=300, bbox_inches='tight')
    plt.show()