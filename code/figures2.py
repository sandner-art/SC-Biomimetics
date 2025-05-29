import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures
plt.style.use('default')
sns.set_palette("viridis")
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 8, # Adjusted for potentially more items in Panel D legend
    'figure.titlesize': 16,
    'lines.linewidth': 2,
    'axes.grid': True,
    'grid.linestyle': ':',
    'grid.alpha': 0.7,
    'figure.constrained_layout.use': True
})

# --- Constants for Seawater Properties (using the same simplified functions) ---
RHO_COEFFS = [9.9983952e+02, 6.793952e-02, -9.095290e-03, 1.001685e-04, -1.120083e-06, 6.536332e-09]
A_COEFFS = [8.24493e-1, -4.0899e-3, 7.6438e-5, -8.2467e-7, 5.3875e-9]
B_COEFFS = [-5.72466e-3, 1.0227e-4, -1.6546e-6]
C_COEFF = 4.8314e-4

def calculate_seawater_density_ies80_simplified(S, T):
    T_poly = np.polyval(RHO_COEFFS[::-1], T)
    A_S = (A_COEFFS[0] + (A_COEFFS[1] + (A_COEFFS[2] + (A_COEFFS[3] + A_COEFFS[4]*T)*T)*T)*T)
    B_S_sqrt = (B_COEFFS[0] + (B_COEFFS[1] + B_COEFFS[2]*T)*T)
    density = T_poly + A_S*S + B_S_sqrt*(S**1.5) + C_COEFF*(S**2)
    return density

def calculate_refractive_index_seawater(S, T, wavelength_nm=532):
    n0 = 1.33374
    nS_coeff = 1.831e-4
    nT_coeff = -2.105e-6
    nT2_coeff = -3.89e-8
    n = n0 + nS_coeff * S + nT_coeff * T + nT2_coeff * (T**2)
    return n

# Figure 7: Detectability of Oceanic Pycnoclines by Biomimetic Schlieren Vision
def create_figure7_revised_for_detects():
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3) # Adjusted spacing

    # --- Simulation Parameters (More Aggressive Gradients) ---
    depth = np.linspace(0, 350, 350) # Depth in meters
    
    T_surface = 28.0  # Increased surface temperature
    T_deep = 4.0      # Decreased deep water temperature
    thermocline_center = 60 # Slightly shallower
    thermocline_thickness = 10 # Made MUCH sharper (was 30, then 15)
    temperature = T_deep + (T_surface - T_deep) / (1 + np.exp((depth - thermocline_center) / (thermocline_thickness / 4)))

    S_surface = 34.0  # Slightly lower surface salinity for bigger difference
    S_deep = 35.5     # Increased deep water salinity (was 35.0, then 35.2)
    halocline_center = 80 # Slightly shallower
    halocline_thickness = 15 # Made MUCH sharper (was 40, then 20)
    # Ensure salinity increases with depth using a positive sign in exp for this formulation
    salinity = S_surface + (S_deep - S_surface) / (1 + np.exp(-(depth - halocline_center) / (halocline_thickness / 4)))


    # --- Panel A: Simulated Oceanic Profiles ---
    axA = fig.add_subplot(gs[0, 0])
    color_temp = 'crimson'
    axA.plot(temperature, -depth, color=color_temp, label='Temperature (°C)')
    axA.set_xlabel('Temperature (°C)', color=color_temp)
    axA.tick_params(axis='x', labelcolor=color_temp)
    axA.set_ylabel('Depth (m)')

    axA_twin = axA.twiny()
    color_sal = 'steelblue'
    axA_twin.plot(salinity, -depth, color=color_sal, linestyle='--', label='Salinity (PSU)')
    axA_twin.set_xlabel('Salinity (PSU)', color=color_sal)
    axA_twin.tick_params(axis='x', labelcolor=color_sal)

    axA.set_ylim(-200, 0)
    axA.set_title('A) Simulated Oceanic Profiles')
    lines, labels = axA.get_legend_handles_labels()
    lines2, labels2 = axA_twin.get_legend_handles_labels()
    axA_twin.legend(lines + lines2, labels + labels2, loc='center right', fontsize=8) # Adjusted legend
    axA.grid(True, linestyle=':', alpha=0.7)
    axA_twin.grid(False)
    source_text_A = "Profiles simulated to generate strong pycnoclines\n(Illustrative, not from specific Argo float)."
    axA.text(0.02, 0.02, source_text_A, transform=axA.transAxes, fontsize=7,
             ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.6))

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
    axB_twin.plot(refractive_index_profile, -depth, color=color_n, linestyle='--', label='Refractive Index')
    axB_twin.set_xlabel('Refractive Index (n)', color=color_n)
    axB_twin.tick_params(axis='x', labelcolor=color_n, rotation=30)
    axB_twin.xaxis.set_major_formatter(plt.FormatStrFormatter('%.6f'))

    axB.set_ylim(-200, 0)
    axB.set_title('B) Calculated Density & Refractive Index')
    lines, labels = axB.get_legend_handles_labels()
    lines2, labels2 = axB_twin.get_legend_handles_labels()
    axB_twin.legend(lines + lines2, labels + labels2, loc='center right', fontsize=8) # Adjusted legend
    axB.grid(True, linestyle=':', alpha=0.7)
    axB_twin.grid(False)
    source_text_B = "Density: Simplified IES 80. Refractive Index: Simplified from Shang et al. (2015) for λ=532nm."
    axB.text(0.02, 0.02, source_text_B, transform=axB.transAxes, fontsize=7,
             ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.6))

    # --- Panel C: Calculated Vertical Gradients (Pycnoclines) ---
    axC = fig.add_subplot(gs[1, 0])
    dz = np.abs(depth[1] - depth[0])
    d_rho_dz = np.abs(np.gradient(density_profile, dz))
    d_n_dz = np.abs(np.gradient(refractive_index_profile, dz))
    
    # Diagnostic print
    print(f"[Revised Plot] Max |∂n/∂z|: {np.max(d_n_dz):.3e} m^-1")


    color_d_rho = 'darkorange'
    axC.plot(d_rho_dz, -depth, color=color_d_rho, label=r'$|\partial\rho/\partial z|$ (kg/m$^4$)')
    axC.set_xlabel(r'$|\partial\rho/\partial z|$ (kg/m$^4$)', color=color_d_rho)
    axC.tick_params(axis='x', labelcolor=color_d_rho)
    axC.set_ylabel('Depth (m)')

    axC_twin = axC.twiny()
    color_d_n = 'deepskyblue'
    axC_twin.plot(d_n_dz, -depth, color=color_d_n, linestyle='--', label=r'$|\partial n/\partial z|$ (m$^{-1}$)')
    axC_twin.set_xlabel(r'$|\partial n/\partial z|$ (m$^{-1}$)', color=color_d_n)
    axC_twin.tick_params(axis='x', labelcolor=color_d_n, rotation=30)
    axC_twin.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1e'))

    axC.set_ylim(-200, 0)
    axC.set_title('C) Vertical Gradients (Pycnoclines)')
    lines, labels = axC.get_legend_handles_labels()
    lines2, labels2 = axC_twin.get_legend_handles_labels()
    axC_twin.legend(lines + lines2, labels + labels2, loc='upper right', fontsize=8)
    axC.grid(True, linestyle=':', alpha=0.7)
    axC_twin.grid(False)

    # --- Panel D: Detectability by Schlieren Models ---
    axD = fig.add_subplot(gs[1, 1])
    threshold_amphibian = 1.0e-5
    threshold_bird = 3.0e-5
    threshold_insect = 8.0e-5
    
    # Diagnostic prints for thresholds
    print(f"Amphibian Threshold: {threshold_amphibian:.1e} m^-1, Bird: {threshold_bird:.1e} m^-1, Insect: {threshold_insect:.1e} m^-1")
    print(f"Points where d_n_dz >= amphibian_thresh: {np.sum(d_n_dz >= threshold_amphibian)}")
    print(f"Points where d_n_dz >= bird_thresh: {np.sum(d_n_dz >= threshold_bird)}")
    print(f"Points where d_n_dz >= insect_thresh: {np.sum(d_n_dz >= threshold_insect)}")


    axD.semilogx(d_n_dz, -depth, color='black', linewidth=1.5, label=r'Actual $|\partial n/\partial z|$')
    axD.axvline(threshold_amphibian, color='blue', linestyle=':', linewidth=1.5, label=f'Amphibian Thresh. ({threshold_amphibian:.1e})')
    axD.axvline(threshold_bird, color='green', linestyle=':', linewidth=1.5, label=f'Bird Thresh. ({threshold_bird:.1e})')
    axD.axvline(threshold_insect, color='red', linestyle=':', linewidth=1.5, label=f'Insect Thresh. ({threshold_insect:.1e})')

    axD.fill_betweenx(-depth, threshold_amphibian, d_n_dz, where=(d_n_dz >= threshold_amphibian),
                      color='blue', alpha=0.25, interpolate=True, label='Amphibian Detects')
    axD.fill_betweenx(-depth, threshold_bird, d_n_dz, where=(d_n_dz >= threshold_bird),
                      color='green', alpha=0.25, interpolate=True, label='Bird Detects')
    axD.fill_betweenx(-depth, threshold_insect, d_n_dz, where=(d_n_dz >= threshold_insect),
                      color='red', alpha=0.25, interpolate=True, label='Insect Detects')

    axD.set_xlabel(r'$|\partial n/\partial z|$ (m$^{-1}$)')
    axD.set_ylabel('Depth (m)')
    axD.set_ylim(-200, 0)
    # Ensure xlim_left is positive and smaller than min(d_n_dz) or min_threshold
    min_relevant_x = min(np.min(d_n_dz[d_n_dz > 0]) if np.any(d_n_dz > 0) else 1e-7, threshold_amphibian/10)
    axD.set_xlim(left=max(1e-6, min_relevant_x) , right=max(np.max(d_n_dz)*2, threshold_insect*5)) # Adjusted xlim
    axD.set_title('D) Detectability by Schlieren Models')
    
    handles, labels = axD.get_legend_handles_labels()
    try: # Reordering legend can fail if some labels are missing (e.g. no fill)
        order = [labels.index(r'Actual $|\partial n/\partial z|$'),
                 labels.index(f'Amphibian Thresh. ({threshold_amphibian:.1e})'), labels.index('Amphibian Detects'),
                 labels.index(f'Bird Thresh. ({threshold_bird:.1e})'), labels.index('Bird Detects'),
                 labels.index(f'Insect Thresh. ({threshold_insect:.1e})'), labels.index('Insect Detects')]
        axD.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='bottom right', fontsize=7) # Smaller legend font
    except ValueError: # If a label isn't found (e.g., a 'Detects' region is empty)
        axD.legend(loc='best', fontsize=7)

#    note_text_D = "Thresholds hypothetical (units: m⁻¹)"
#    axD.text(0.5, -0.15, note_text_D, transform=axD.transAxes, fontsize=7,
#             ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.6))

    fig.suptitle('Figure 7: Detectability of Oceanic Pycnoclines by Biomimetic Schlieren Vision', fontsize=16, fontweight='bold')
    return fig

if __name__ == '__main__':
    fig7_final = create_figure7_revised_for_detects()
    plt.savefig("figure7_detectability_pycnoclines_final.png", dpi=300, bbox_inches='tight')
    plt.show()