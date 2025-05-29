import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures
plt.style.use('default')
sns.set_palette("muted") # A slightly desaturated palette
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
    'grid.linestyle': ':', # Dotted grid lines
    'grid.alpha': 0.6,
    'figure.constrained_layout.use': True # Helps with layout
})

# Figure 4: Environmental Applications and Selective Advantages
def create_figure4():
    fig = plt.figure(figsize=(14, 10)) # Adjusted for better layout
    gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

    # --- Panel A: Aquatic density gradients ---
    axA = fig.add_subplot(gs[0, 0])
    depth_ocean = np.linspace(0, 1000, 200)  # meters

    # Simulated ocean temperature profile (e.g., similar to NOAA data patterns)
    T_surface_ocean = 25  # °C
    T_deep_ocean = 4    # °C
    thermocline_depth_start = 50
    thermocline_depth_end = 250
    temp_ocean = np.piecewise(depth_ocean,
        [depth_ocean < thermocline_depth_start,
         (depth_ocean >= thermocline_depth_start) & (depth_ocean <= thermocline_depth_end),
         depth_ocean > thermocline_depth_end],
        [lambda d: T_surface_ocean,
         lambda d: T_surface_ocean - (T_surface_ocean - T_deep_ocean) * \
                   ((d - thermocline_depth_start) / (thermocline_depth_end - thermocline_depth_start))**0.8, # Smoother transition
         lambda d: T_deep_ocean]
    )

    # Simplified water density calculation (density increases as temp decreases)
    # rho = rho_ref + alpha * (T_ref - T)
    rho_ref_water = 1020 # kg/m^3
    alpha_thermal_expansion = 0.2 # kg/m^3/°C (illustrative)
    density_ocean = rho_ref_water + alpha_thermal_expansion * (T_surface_ocean - temp_ocean)

    # Plot density profile
    axA.plot(density_ocean, -depth_ocean, 'b-', linewidth=2.5, label='Water Density (kg/m³)')
    axA.set_xlabel('Density (kg/m³)')
    axA.set_ylabel('Depth (m)')
    axA.set_ylim(-1000, 0)

    # Highlight thermocline region (where density changes most rapidly)
    axA.axhspan(-thermocline_depth_end, -thermocline_depth_start, alpha=0.2, color='yellow',
                label='Thermocline Zone')

    # Add temperature profile on a twin axis
    axA_twin = axA.twiny()
    axA_twin.plot(temp_ocean, -depth_ocean, 'r:', linewidth=2, label='Temperature (°C)')
    axA_twin.set_xlabel('Temperature (°C)', color='red')
    axA_twin.tick_params(axis='x', labelcolor='red')
    axA_twin.set_xlim(0, 30) # Reasonable temperature range

    axA.set_title('A) Aquatic Density & Temp. Gradients')
    # Combine legends
    lines, labels = axA.get_legend_handles_labels()
    lines2, labels2 = axA_twin.get_legend_handles_labels()
    axA.legend(lines + lines2, labels + labels2, loc='lower right')
    axA.grid(True, linestyle=':', alpha=0.7)
    axA_twin.grid(False)

    caption_A = "Source: Profiles simulated based on typical oceanic data (e.g., NOAA thermocline patterns)."
    axA.text(0.01, -0.25, caption_A, transform=axA.transAxes, fontsize=7, ha='left', va='top')


    # --- Panel B: Aerial density variations ---
    axB = fig.add_subplot(gs[0, 1])
    height_air = np.linspace(0, 2000, 200)  # meters

    # Simulated atmospheric temperature profile (e.g., ISA principles, boundary layer effects)
    T_surface_air = 20  # °C (ground level)
    lapse_rate_std = 6.5 / 1000  # °C/m (standard lapse rate in troposphere)
    mixing_layer_height = 1000 # meters
    temp_air_profile = np.zeros_like(height_air)
    # Simplified boundary layer: constant lapse rate up to mixing height, then stable
    for i, h_val in enumerate(height_air):
        if h_val <= mixing_layer_height:
            temp_air_profile[i] = T_surface_air - lapse_rate_std * h_val
        else: # Simplified inversion or stable layer above mixing height
            temp_air_profile[i] = T_surface_air - lapse_rate_std * mixing_layer_height - 0.002 * (h_val - mixing_layer_height)


    # Air density (simplified ideal gas law: rho ~ P / T; P decreases with height)
    # For illustration, focus on temperature effect primarily at lower altitudes
    # rho = rho0 * (T0 / T)
    rho0_air = 1.225 # kg/m^3 at sea level, 15°C
    T0_kelvin = 273.15 + 15
    density_air = rho0_air * (T0_kelvin / (temp_air_profile + 273.15))
    # Add a slight decrease with height to simulate pressure effect
    density_air *= np.exp(-height_air / 8000) # Scale height ~8km

    axB.plot(density_air, height_air, 'g-', linewidth=2.5, label='Air Density (kg/m³)')
    axB.set_xlabel('Air Density (kg/m³)')
    axB.set_ylabel('Height (m)')
    axB.set_ylim(0, 2000)

    # Highlight atmospheric boundary layer
    axB.axhspan(0, mixing_layer_height, alpha=0.2, color='lightblue', label='Mixing Layer')

    # Add temperature profile on a twin axis
    axB_twin = axB.twiny()
    axB_twin.plot(temp_air_profile, height_air, 'm:', linewidth=2, label='Temperature (°C)')
    axB_twin.set_xlabel('Temperature (°C)', color='magenta')
    axB_twin.tick_params(axis='x', labelcolor='magenta')

    axB.set_title('B) Aerial Density & Temp. Variations')
    lines, labels = axB.get_legend_handles_labels()
    lines2, labels2 = axB_twin.get_legend_handles_labels()
    axB.legend(lines + lines2, labels + labels2, loc='upper right')
    axB.grid(True, linestyle=':', alpha=0.7)
    axB_twin.grid(False)

    caption_B = "Source: Profiles simulated based on typical atmospheric conditions (e.g., ISA, boundary layers)."
    axB.text(0.01, -0.25, caption_B, transform=axB.transAxes, fontsize=7, ha='left', va='top')

    # --- Panel C: Predator-prey scenarios ---
    axC = fig.add_subplot(gs[1, 0])
    scenarios = ['Camouflaged\nPrey (Water)', 'Turbulent\nWater Flow', 'Thermal\nPlumes (Air)',
                 'Boundary\nLayers (Air)', 'Subtle Prey\nMoment (Water)']
    # Hypothetical detection success rates (%)
    traditional_vision_success = [20, 15, 10, 25, 10]
    schlieren_vision_success = [85, 75, 90, 80, 88]

    x_scenarios = np.arange(len(scenarios))
    bar_width = 0.35

    bars1 = axC.bar(x_scenarios - bar_width/2, traditional_vision_success, bar_width,
                    label='Traditional Vision', color='lightcoral', alpha=0.85)
    bars2 = axC.bar(x_scenarios + bar_width/2, schlieren_vision_success, bar_width,
                    label='Schlieren Vision', color='skyblue', alpha=0.85)

    # Add value labels on bars
    def add_bar_labels(bars):
        for bar in bars:
            height = bar.get_height()
            axC.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                     f'{height}%', ha='center', va='bottom', fontsize=8)
    add_bar_labels(bars1)
    add_bar_labels(bars2)

    axC.set_xlabel('Scenario')
    axC.set_ylabel('Detection Success Rate (%)')
    axC.set_title('C) Predator-Prey Advantage (Illustrative)')
    axC.set_xticks(x_scenarios)
    axC.set_xticklabels(scenarios, rotation=15, ha='right')
    axC.legend(loc='upper left')
    axC.set_ylim(0, 105)


    # --- Panel D: Navigation and migration applications ---
    axD = fig.add_subplot(gs[1, 1])
    # Conceptual map with density features (e.g., currents, thermals)
    x_nav = np.linspace(0, 10, 50)
    y_nav = np.linspace(0, 10, 50)
    X_nav, Y_nav = np.meshgrid(x_nav, y_nav)

    # Simulate density features (e.g., a meandering current or thermal street)
    density_features = np.sin(X_nav * 0.8) * np.cos(Y_nav * 0.5) + \
                       0.3 * np.sin(Y_nav * 1.5) * np.cos(X_nav * 0.3)
    contour = axD.contourf(X_nav, Y_nav, density_features, levels=15, cmap='coolwarm', alpha=0.7)

    # Illustrative navigation paths
    # Schlieren-guided path (exploiting density features)
    optimal_x = [1, 2.5, 4.5, 6, 7.5, 9]
    optimal_y = [1, 2,   1.5, 3, 5.5, 8] # Path that might follow a feature
    axD.plot(optimal_x, optimal_y, 'g-', linewidth=3, marker='o', markersize=5, label='Schlieren-guided Path')

    # Traditional path (more direct, less informed by subtle density cues)
    traditional_x = [1, 3, 5, 7, 9]
    traditional_y = [1, 2.5, 4, 5.5, 7]
    axD.plot(traditional_x, traditional_y, 'k--', linewidth=2.5, label='Traditional Path')

    # Start and End points
    axD.scatter([1, 9], [1, max(optimal_y[-1], traditional_y[-1])], s=100, c=['limegreen', 'red'],
                marker='*', zorder=5, edgecolors='black', linewidth=1)
    axD.text(1, 0.5, 'Start', ha='center', va='top', fontweight='bold')
    axD.text(9, max(optimal_y[-1], traditional_y[-1]) + 0.5, 'Target', ha='center', va='bottom', fontweight='bold')

    axD.set_xlabel('X Coordinate (Arbitrary Units)')
    axD.set_ylabel('Y Coordinate (Arbitrary Units)')
    axD.set_title('D) Navigation with Density Cues (Illustrative)')
    axD.legend(loc='upper left')
    axD.set_aspect('equal', adjustable='box') # Make it look more like a map

    cbar = plt.colorbar(contour, ax=axD, shrink=0.8, aspect=10)
    cbar.set_label('Relative Density Feature Strength')


    fig.suptitle('Figure 4: Environmental Applications and Selective Advantages',
                 fontsize=14, fontweight='bold')
    # fig.tight_layout(rect=[0, 0.03, 1, 0.96]) # Adjust for suptitle and captions
    return fig


if __name__ == '__main__':
    # To save the figure if running the script directly
    fig4 = create_figure4()
    plt.savefig("figure4_environmental_applications.png", dpi=300, bbox_inches='tight')
    plt.show()