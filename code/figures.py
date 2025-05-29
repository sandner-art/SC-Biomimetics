import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures
plt.style.use('default') # Using a default style that should be widely available
sns.set_palette("viridis") # A perceptually uniform colormap
plt.rcParams.update({
    'font.size': 10, # Adjusted for clarity in a multi-panel figure
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'lines.linewidth': 2,
    'axes.grid': True,
    'grid.alpha': 0.4,
    'patch.edgecolor': 'black', # Ensure patches have edges
    'figure.constrained_layout.use': True # Helps with layout
})

# Figure 5: Biomimetic Implementation Strategies and Evolution
def create_figure5():
    fig = plt.figure(figsize=(14, 8)) # Adjusted for better layout
    gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)

    # Panel A: Insect compound eye cross-section (Schematic)
    ax1 = fig.add_subplot(gs[0, 0])
    # Ommatidium body
    ax1.add_patch(patches.Rectangle((-0.25, -2), 0.5, 2, linewidth=1.5, edgecolor='black', facecolor='lightgrey'))
    # Cornea/Lens
    ax1.add_patch(patches.Ellipse((0, 0.1), 0.6, 0.4, edgecolor='black', facecolor='lightblue', alpha=0.7))
    ax1.text(0, 0.1, "Cornea", ha='center', va='center', fontsize=8)

    # Layered chitin
    for i in range(5):
        y_layer = -0.2 - i * 0.3
        ax1.axhline(y=y_layer, xmin=0.375, xmax=0.625, color='blue', linewidth=1.5, alpha=0.7)
    ax1.text(0.4, -1.0, "Layered\nChitin", ha='center', va='center', fontsize=8, color='blue')

    # Light rays (simplified bending)
    ax1.arrow(0, 0.4, 0, -0.5, head_width=0.05, head_length=0.1, fc='red', ec='red', alpha=0.6, length_includes_head=True)
    ax1.arrow(-0.1, 0.4, 0.05, -0.5, head_width=0.05, head_length=0.1, fc='red', ec='red', alpha=0.6, length_includes_head=True)
    ax1.arrow(0.1, 0.4, -0.05, -0.5, head_width=0.05, head_length=0.1, fc='red', ec='red', alpha=0.6, length_includes_head=True)
    ax1.text(0, 0.5, "Light", ha='center', va='top', fontsize=8, color='red')

    # Mechanoreceptors
    ax1.add_patch(patches.Rectangle((-0.2, -2.2), 0.4, 0.2, linewidth=1, edgecolor='green', facecolor='lightgreen', alpha=0.7))
    ax1.text(0, -2.1, 'Mechanoreceptors', ha='center', va='center', fontsize=8, color='darkgreen')

    ax1.set_xlim(-0.7, 0.7)
    ax1.set_ylim(-2.5, 0.7)
    ax1.set_title('A) Insect: Layered Ommatidium')
    ax1.set_xlabel('Schematic View')
    ax1.set_ylabel('')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.axis('equal') # Maintain aspect ratio

    # Panel B: Amphibian membrane structure (Schematic)
    ax2 = fig.add_subplot(gs[0, 1])
    # Nictitating membrane outline
    membrane_x = np.linspace(-1, 1, 100)
    membrane_top = 0.1 * np.sin(np.pi * membrane_x) + 0.2
    membrane_bottom = -0.1 * np.sin(np.pi * membrane_x) - 0.2
    ax2.plot(membrane_x, membrane_top, 'k-', linewidth=1.5)
    ax2.plot(membrane_x, membrane_bottom, 'k-', linewidth=1.5)
    ax2.fill_between(membrane_x, membrane_top, membrane_bottom, color='skyblue', alpha=0.4, label='Fluid Chamber')

    # Pressure sensors
    sensor_x = np.linspace(-0.7, 0.7, 5)
    ax2.scatter(sensor_x, np.full_like(sensor_x, -0.25), s=40, c='red', marker='s', label='Pressure Sensors', zorder=5)

    # Incident and bent light
    ax2.arrow(0, 0.6, 0, -0.3, head_width=0.05, head_length=0.1, fc='yellow', ec='black', linewidth=1, length_includes_head=True)
    ax2.arrow(0, 0.3, 0.15, -0.2, head_width=0.05, head_length=0.1, fc='orange', ec='black', linewidth=1, linestyle='--', label='Bent Light', length_includes_head=True)
    ax2.text(0, 0.7, "Incident Light", ha='center', va='bottom', fontsize=8)

    ax2.set_xlim(-1.2, 1.2)
    ax2.set_ylim(-0.7, 0.8)
    ax2.set_title('B) Amphibian: Fluid Chamber Membrane')
    ax2.set_xlabel('Schematic View')
    ax2.set_ylabel('')
    ax2.legend(fontsize=8, loc='lower center')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.axis('equal')

    # Panel C: Bird pecten structure (Schematic)
    ax3 = fig.add_subplot(gs[0, 2])
    # Pecten folds (simplified)
    num_folds = 4
    fold_base_y = -0.8
    for i in range(num_folds):
        x_start = -0.6 + i * (1.2 / num_folds) + 0.05
        x_end = -0.6 + (i + 1) * (1.2 / num_folds) - 0.05
        x_mid = (x_start + x_end) / 2
        ax3.add_patch(patches.Polygon([[x_start, fold_base_y], [x_mid, 0.4], [x_end, fold_base_y]],
                                     closed=True, edgecolor='black', facecolor='salmon', alpha=0.6))
        # Channels inside (simplified)
        for j in range(3):
            y_channel = fold_base_y + 0.3 + j*0.3
            if y_channel < 0.4 - (0.4-fold_base_y)*(abs(x_mid - x_mid)/( (x_end-x_start)/2 ) ): # crude check to keep inside
                 ax3.plot([x_mid-0.03, x_mid+0.03], [y_channel, y_channel], 'b--', linewidth=1, alpha=0.8)
        # Mechanoreceptors along channels
        ax3.scatter([x_mid]*2, [fold_base_y + 0.4, fold_base_y + 0.7], c='darkred', s=15, zorder=5, marker='o')

    ax3.text(0, 0.6, "Pecten Folds\n(Channels Inside)", ha='center', va='bottom', fontsize=8)
    ax3.text(0, -0.9, "Mechanoreceptors", ha='center', va='top', fontsize=8, color='darkred')

    ax3.set_xlim(-0.8, 0.8)
    ax3.set_ylim(-1.0, 0.8)
    ax3.set_title('C) Bird: Modified Pecten Oculi')
    ax3.set_xlabel('Schematic View')
    ax3.set_ylabel('')
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.axis('equal')

    # Panel D: Model Sensitivity to Gradient Magnitude
    ax4 = fig.add_subplot(gs[1, :2])
    gradient_magnitude = np.logspace(-3, 1, 100)  # Arbitrary units of density gradient strength

    # Sigmoidal response curves (Hill equation like)
    def model_response(x, k_half, n_hill):
        return (x**n_hill) / (k_half**n_hill + x**n_hill)

    # Hypothetical parameters for sensitivity curves
    # k_half: gradient strength for half-maximal response
    # n_hill: Hill coefficient (steepness)
    insect_sensitivity = model_response(gradient_magnitude, k_half=0.1, n_hill=1.5)
    amphibian_sensitivity = model_response(gradient_magnitude, k_half=0.03, n_hill=2.0) # More sensitive
    bird_sensitivity = model_response(gradient_magnitude, k_half=0.06, n_hill=1.8)    # Intermediate

    ax4.semilogx(gradient_magnitude, insect_sensitivity, label='Insect Model', linewidth=2.5)
    ax4.semilogx(gradient_magnitude, amphibian_sensitivity, label='Amphibian Model', linewidth=2.5)
    ax4.semilogx(gradient_magnitude, bird_sensitivity, label='Bird Model', linewidth=2.5)

    ax4.set_xlabel('Density Gradient Magnitude (Arbitrary Units)')
    ax4.set_ylabel('Normalized Sensory Response')
    ax4.set_title('D) Model Sensitivity to Gradient Magnitude')
    ax4.legend()
    ax4.set_ylim(0, 1.05)
    ax4.grid(True, which="both", ls="-", alpha=0.2)


    # Panel E: Plausibility of Evolutionary Stages
    ax5 = fig.add_subplot(gs[1, 2])
    stages = ['Basic\nMechanoreception', 'Fluid Structure\nSensitivity',
              'Optical Amplification\nMechanisms', 'Spatial\nResolution', 'Integrated Schlieren\nVision']
    # Hypothetical plausibility/novelty scores (lower is more plausible or less novel)
    # Inverted for bar chart: lower bar = earlier/easier stage
    novelty_complexity = np.array([0.1, 0.3, 0.4, 0.7, 0.9])

    colors = plt.cm.coolwarm_r(novelty_complexity / float(max(novelty_complexity))) # Reversed colormap

    bars = ax5.barh(stages, novelty_complexity, color=colors, edgecolor='black')

    # Add values on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax5.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                 f'{width:.2f}', ha='left', va='center', fontsize=8)

    ax5.set_xlabel('Evolutionary Novelty/Complexity (Arbitrary Scale)')
    ax5.set_ylabel('')
    ax5.set_title('E) Plausibility of Evolutionary Stages')
    ax5.set_xlim(0, 1.0)
    ax5.invert_yaxis() # To show 'Basic' at the top
    ax5.grid(True, axis='x', linestyle='--', alpha=0.3)


    fig.suptitle('Figure 5: Biomimetic Implementation Strategies and Evolution',
                 fontsize=14, fontweight='bold')
    # fig.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust layout to make space for suptitle
    return fig

if __name__ == '__main__':
    # To save the figure if running the script directly
    fig5 = create_figure5()
    plt.savefig("figure5_biomimetic_schlieren.png", dpi=300, bbox_inches='tight')
    plt.show()