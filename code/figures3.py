import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures
# plt.style.use('seaborn-v0_8-whitegrid') # A good seaborn style
plt.style.use('default') # Using a default style that should be widely available
sns.set_palette("husl") # A colorblind-friendly palette
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'lines.linewidth': 2,
    'axes.grid': True,
    'grid.alpha': 0.5, # Make grid lines slightly more prominent
    'figure.constrained_layout.use': True # Helps with layout
})

# Figure 3: Mathematical Model Validation and Sensitivity Analysis
def create_figure3():
    fig = plt.figure(figsize=(15, 11)) # Adjusted figure size
    gs = GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.3) # Adjusted grid: 3 rows, 2 cols

    # --- Panel A: Amplification factor vs. structural parameters ---
    ax1 = fig.add_subplot(gs[0, 0])
    L_values = np.linspace(0.1, 5.0, 50)  # Path length in mm (L from paper)
    n_layers_options = np.array([5, 10, 20, 50])  # Number of layers (conceptual)
    delta_n_per_layer_eff = 0.0005  # Effective refractive index change *per layer* contributing to bending

    # A = N_layers * delta_n_eff * L (Conceptual amplification factor related to cumulative bending)
    # This is a simplified model for A based on the idea that more layers and longer path length increase effect.
    # The actual formula for 'A' would be specific to the optical physics of the layered structure.
    # For illustration, let A ~ N_layers * L * (effective_gradient_per_layer_unit_length)
    # Or simply, A increases with N and L.
    # Let's use the paper's formula style: A represents the ratio of final to initial angular deflection.
    # Assuming the paper's A is more abstract, we can plot a relationship where A grows with parameters.
    # Let's define A = (Path Length * Number of Layers * Layer_Factor) / Reference_Deflection
    # Or for the graph, A = L_values * n_layers * constant_factor.
    # A = (K * L * N_layers * delta_n_per_layer) / delta_theta_min_ref , or just plot a representation
    # From paper draft: A is a general amplification factor. The plot should show A increasing with L and number of layers.
    # The previous A = n * delta_n * L_values * 1000 was an interpretation.
    # Let's plot a plausible relationship where A grows, e.g., A = c1 * L + c2 * N_layers
    # Or more likely A proportional to L * N_layers * (some optical efficiency)
    
    amplification_base = 0.5 # Base amplification per mm per layer (arbitrary unit for illustration)
    
    colors_A = sns.color_palette("viridis", n_colors=len(n_layers_options))

    for i, n_layers in enumerate(n_layers_options):
        # Simplified A = L_values (mm) * n_layers * amplification_base_factor
        A = L_values * n_layers * amplification_base
        ax1.plot(L_values, A, color=colors_A[i], label=f'{n_layers} layers', linewidth=2)

    ax1.set_xlabel('Path Length (L, mm)')
    ax1.set_ylabel('Amplification Factor (A)')
    ax1.set_title('A) Amplification vs. Path Length & Layers')
    ax1.legend(title="# Layers")
    ax1.set_xlim(0, 5)
    ax1.set_ylim(bottom=0) # Ensure A starts from 0 or slightly above if baseline exists

    # --- Panel B: Detection threshold vs. mechanoreceptor sensitivity ---
    # Formula from paper: Δρ_min ≈ (Δθ_min) / (K * A * L)
    ax2 = fig.add_subplot(gs[0, 1])
    delta_theta_min_values = np.logspace(-7, -4, 50)  # Min. detectable angular deflection in radians (sensitive range)
    K_gladstone_dale = 2.3e-4  # Gladstone-Dale constant for air (m^3/kg)
    A_fixed = 50          # Fixed general amplification factor (from Panel A range)
    L_fixed_m = 2.0 / 1000 # Fixed path length in meters (e.g., 2mm)

    # Δρ_min in kg/m³
    delta_rho_min_values = (delta_theta_min_values) / (K_gladstone_dale * A_fixed * L_fixed_m)

    ax2.loglog(delta_theta_min_values * 1e6, delta_rho_min_values * 1000, 'b-', linewidth=2) # Δθ in μrad, Δρ in g/m³
    ax2.set_xlabel('Min. Detectable Angle (Δθ$_{min}$, μrad)')
    ax2.set_ylabel('Min. Detectable Density Change (Δρ$_{min}$, g/m³)')
    ax2.set_title('B) Detection Threshold vs. Sensor Sensitivity')
    ax2.grid(True, which="both", ls=":", alpha=0.7) # Grid for log-log

    # --- Panel C: Spatial resolution vs. sensing unit density ---
    ax3 = fig.add_subplot(gs[1, 0])
    unit_densities_per_mm2 = np.linspace(10, 1000, 100)  # units per mm²

    # Angular resolution (θ_res) inversely related to sqrt(density) for array sensors.
    # θ_res ≈ 1 / (d * sqrt(density_angular)), where d is unit spacing.
    # For simpler illustration: Resolution improves with density.
    # Let's assume higher density allows resolving smaller angles.
    # For compound eyes, interommatidial angle Δφ ≈ D_lens / R_eye.
    # If unit density implies smaller units or denser packing on a given area:
    # Higher unit density -> smaller effective pixel size -> better angular resolution.
    # Angular resolution in degrees = constant / sqrt(unit_density_per_solid_angle)
    # Let's relate unit_densities_per_mm2 to angular resolution.
    # Assume a fixed field of view mapped to this area.
    # For illustration, let's use a relationship where resolution improves (angle gets smaller).
    
    # Example: Angular Resolution (degrees) = C / sqrt(unit_densities_per_mm2)
    # C needs to be chosen to give a reasonable range.
    # From paper's previous code:
    # insect_resolution = 180 / (np.pi * np.sqrt(unit_densities))
    # This implies unit_densities is units per steradian or similar.
    # Let's adapt this for units/mm^2 and an assumed mapping to angular space.
    
    # Assume resolution angle is inversely proportional to linear density of units
    # Higher density (units/mm^2) means more units in a line (sqrt(density))
    # This is illustrative. Realistic models are more complex.
    constant_factor_res = 20 # To get degrees in a reasonable range

    insect_resolution = constant_factor_res / np.sqrt(unit_densities_per_mm2)
    # Amphibian and Bird models might have different efficiency in converting unit density to angular resolution
    amphibian_resolution = constant_factor_res * 1.5 / np.sqrt(unit_densities_per_mm2) # Less efficient packing for resolution
    bird_resolution = constant_factor_res * 1.2 / np.sqrt(unit_densities_per_mm2)    # Intermediate

    ax3.plot(unit_densities_per_mm2, insect_resolution, label='Insect (High Efficiency)', linewidth=2)
    ax3.plot(unit_densities_per_mm2, bird_resolution, label='Bird (Intermediate)', linewidth=2)
    ax3.plot(unit_densities_per_mm2, amphibian_resolution, label='Amphibian (Lower Efficiency)', linewidth=2)

    ax3.set_xlabel('Sensing Unit Density (units/mm²)')
    ax3.set_ylabel('Angular Resolution (degrees)') # Smaller is better
    ax3.set_title('C) Spatial Resolution vs. Unit Density')
    ax3.legend()
    ax3.set_xlim(10, 1000)
    ax3.set_ylim(bottom=0, top=max(amphibian_resolution)*1.1) # Ensure y-axis starts at 0

    # --- Panel D: Trade-off curves (Sensitivity vs. Resolution) ---
    ax4 = fig.add_subplot(gs[1, 1])
    # Illustrative trade-off: higher sensitivity often means compromises in resolution.
    # Example: larger sensors for sensitivity might be less dense for resolution.
    # Let relative_sensitivity be on x-axis.
    relative_sensitivity_pts = np.linspace(1, 10, 100) # Arbitrary units
    # Assume angular_resolution = Base_Res + (Max_Impact / relative_sensitivity_pts)
    # Or a curve like Res = k / Sensitivity^alpha
    base_resolution = 0.5 # degrees (best possible)
    trade_off_factor = 10
    angular_resolution_tradeoff = base_resolution + trade_off_factor / relative_sensitivity_pts

    ax4.plot(relative_sensitivity_pts, angular_resolution_tradeoff, 'r-', linewidth=2.5, label='Sensitivity-Resolution Frontier')

    # Hypothetical positions of the models on this trade-off curve
    model_names = ['Insect', 'Amphibian', 'Bird']
    # Relative sensitivity (arbitrary units, consistent with x-axis)
    model_sensitivity_tradeoff = {'Insect': 4, 'Amphibian': 8, 'Bird': 6}
    # Corresponding resolution from the trade-off curve
    model_resolution_tradeoff = {
        name: base_resolution + trade_off_factor / sens
        for name, sens in model_sensitivity_tradeoff.items()
    }
    
    colors_D = sns.color_palette("Set2", n_colors=len(model_names))

    for i, name in enumerate(model_names):
        ax4.scatter(model_sensitivity_tradeoff[name], model_resolution_tradeoff[name],
                    s=150, color=colors_D[i], label=name, zorder=5, edgecolors='k')
        ax4.text(model_sensitivity_tradeoff[name], model_resolution_tradeoff[name] + 0.2, name,
                 ha='center', va='bottom', fontsize=9)


    ax4.set_xlabel('Relative Sensitivity (Arbitrary Units)')
    ax4.set_ylabel('Angular Resolution (degrees)') # Smaller is better
    ax4.set_title('D) Sensitivity-Resolution Trade-off')
    ax4.legend()
    ax4.set_ylim(0, max(angular_resolution_tradeoff) * 1.1)
    ax4.set_xlim(0, 11)


    # --- Panel E: Cost vs Performance (Energy Cost vs. Overall System Performance) ---
    ax5 = fig.add_subplot(gs[2, :]) # Spanning both columns in the last row
    performance_metric = np.linspace(0, 100, 100) # Overall system performance (%)

    # Hypothetical energy cost functions (e.g., cost ~ performance^exponent)
    # Exponents > 1 indicate increasing marginal cost
    cost_insect = 0.1 * performance_metric**1.5  # Complex structure, higher cost scaling
    cost_amphibian = 0.05 * performance_metric**1.2 # Potentially simpler, lower cost scaling
    cost_bird = 0.08 * performance_metric**1.3   # Intermediate complexity

    ax5.plot(performance_metric, cost_insect, label='Insect Model', linewidth=2, color=colors_D[0])
    ax5.plot(performance_metric, cost_amphibian, label='Amphibian Model', linewidth=2, color=colors_D[1])
    ax5.plot(performance_metric, cost_bird, label='Bird Model', linewidth=2, color=colors_D[2])

    # Illustrative optimal operating points (where benefits justify costs for each model type)
    optimal_perf_insect = 60
    optimal_perf_amphibian = 80
    optimal_perf_bird = 70

    ax5.scatter(optimal_perf_insect, 0.1 * optimal_perf_insect**1.5,
                s=100, marker='*', color=colors_D[0], label='Optimal Insect', zorder=5, edgecolors='k')
    ax5.scatter(optimal_perf_amphibian, 0.05 * optimal_perf_amphibian**1.2,
                s=100, marker='*', color=colors_D[1], label='Optimal Amphibian', zorder=5, edgecolors='k')
    ax5.scatter(optimal_perf_bird, 0.08 * optimal_perf_bird**1.3,
                s=100, marker='*', color=colors_D[2], label='Optimal Bird', zorder=5, edgecolors='k')

    ax5.set_xlabel('System Performance (Arbitrary Units %)')
    ax5.set_ylabel('Relative Energy Cost (Arbitrary Units)')
    ax5.set_title('E) Cost vs. Performance Analysis')
    ax5.legend(ncol=2) # Arrange legend in two columns if many items
    ax5.set_xlim(0, 100)
    ax5.set_ylim(bottom=0)

    fig.suptitle('Figure 3: Mathematical Model Validation and Sensitivity Analysis',
                 fontsize=14, fontweight='bold')
    # fig.tight_layout(rect=[0, 0, 1, 0.96]) # Make space for suptitle
    return fig


if __name__ == '__main__':
    # To save the figure if running the script directly
    fig3 = create_figure3()
    plt.savefig("figure3_model_validation.png", dpi=300, bbox_inches='tight')
    plt.show()