import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures (can reuse from SP1 or define again)
plt.style.use('default')
sns.set_palette("pastel") # Using a softer palette for "natural" scenes
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'lines.linewidth': 1.5,
    'axes.grid': False,
    'figure.constrained_layout.use': True
})

def create_figure_sp2_natural_schlieren_effects():
    fig = plt.figure(figsize=(10, 6)) # Adjusted for 2 panels
    gs = GridSpec(1, 2, figure=fig, wspace=0.25)

    # --- Panel A: Thermal Plumes in Air ---
    axA = fig.add_subplot(gs[0, 0])
    axA.set_title('A) Thermal Plumes in Air')
    axA.set_facecolor('azure') # Light blue background for "sky"

    # Ground
    ground = patches.Rectangle((-0.1, -0.1), 1.2, 0.3, color='lightgreen', ec='darkgreen')
    axA.add_patch(ground)

    # Animal outline (simplified mammal - e.g., rabbit or deer silhouette)
    # Body
    animal_body = patches.Ellipse((0.5, 0.35), 0.3, 0.18, color='sienna', alpha=0.8)
    axA.add_patch(animal_body)
    # Head
    animal_head = patches.Ellipse((0.32, 0.42), 0.12, 0.1, angle=30, color='sienna', alpha=0.8)
    axA.add_patch(animal_head)
    # Ears
    ear1 = patches.Ellipse((0.28, 0.52), 0.04, 0.1, angle=50, color='sienna', alpha=0.8)
    ear2 = patches.Ellipse((0.33, 0.53), 0.04, 0.1, angle=70, color='sienna', alpha=0.8)
    axA.add_patch(ear1)
    axA.add_patch(ear2)
    axA.text(0.5, 0.2, "Warm Animal", ha='center', va='top', fontsize=9)


    # Thermal plumes (wavy lines - density gradients)
    num_plumes = 7
    for i in range(num_plumes):
        start_x = 0.35 + (i * 0.3 / num_plumes) + np.random.uniform(-0.02, 0.02)
        start_y = 0.45 # Starting from top of animal's back
        plume_height = 0.4 + np.random.uniform(-0.05, 0.05)
        y_coords = np.linspace(start_y, start_y + plume_height, 30)
        # Make plumes wider and more diffuse as they rise
        x_amplitude = 0.02 + (y_coords - start_y) * 0.15
        x_coords = start_x + x_amplitude * np.sin(y_coords * 15 / plume_height * np.pi + np.random.rand()*np.pi)
        axA.plot(x_coords, y_coords, color='salmon', linestyle='-', linewidth=1, alpha=0.5)

    axA.text(0.5, 0.9, "Thermal Plumes\n(Refractive Index Gradients)", ha='center', va='center', fontsize=8, color='firebrick')

    # Conceptual observer's line of sight (light rays being subtly bent)
    # Ray passing above plume
    axA.plot([0.05, 0.95], [0.8, 0.8], 'y--', alpha=0.6, label='Undisturbed Light Path')
    # Ray passing through plume (slightly distorted)
    y_distorted_start = 0.65
    x_distorted = np.linspace(0.05, 0.95, 50)
    y_distorted = y_distorted_start + 0.015 * np.sin(x_distorted * 10 * np.pi) * np.exp(-(x_distorted-0.5)**2 / 0.1) # Distortion localized
    axA.plot(x_distorted, y_distorted, 'y-', alpha=0.8, label='Light Path through Plume')

    axA.legend(loc='lower left', fontsize=7)
    axA.set_xlim(0, 1)
    axA.set_ylim(0.1, 1) # Focus above ground
    axA.set_xticks([])
    axA.set_yticks([])


    # --- Panel B: Disturbances in Water ---
    axB = fig.add_subplot(gs[0, 1])
    axB.set_title('B) Disturbances in Water')
    axB.set_facecolor('paleturquoise') # Light blue-green for water

    # Fish silhouette
    fish_body = patches.Ellipse((0.3, 0.5), 0.3, 0.12, color='royalblue', alpha=0.9)
    axB.add_patch(fish_body)
    fish_tail_poly = patches.Polygon([[0.15, 0.5], [0.0, 0.55], [0.0, 0.45]], closed=True, color='royalblue', alpha=0.9)
    axB.add_patch(fish_tail_poly)
    fish_eye = patches.Circle((0.42, 0.51), 0.01, color='white')
    axB.add_patch(fish_eye)
    axB.text(0.3, 0.6, "Moving Fish", ha='center', va='bottom', fontsize=9)


    # Wake / Disturbance (Schlieren patterns - refractive index variations)
    # Conceptual swirling patterns behind the fish
    num_swirls = 5
    for i in range(num_swirls):
        center_x = 0.1 - i*0.05 + np.random.uniform(-0.05, 0.05) # Trail behind tail
        center_y = 0.5 + np.random.uniform(-0.1, 0.1)
        radius = 0.05 + np.random.rand() * 0.08
        swirl = patches.Circle((center_x, center_y), radius, facecolor='none',
                               edgecolor='lightcyan', linestyle='--', linewidth=1.0 + np.random.rand()*0.5, alpha=0.6 + np.random.rand()*0.3)
        axB.add_patch(swirl)
        # Add some smaller "eddies"
        if i < 3:
            axB.add_patch(patches.Circle((center_x + np.random.uniform(-0.02,0.02), center_y + np.random.uniform(-0.02,0.02)),
                                         radius*0.4, facecolor='none', edgecolor='lightcyan', linestyle=':', alpha=0.5))


    axB.text(0.6, 0.2, "Wake / Mixing\n(Refractive Index Gradients)", ha='center', va='center', fontsize=8, color='navy')

    # Light rays passing through water (one distorted by wake)
    # Sunlight from above (conceptual)
    for x_sunray in [0.2, 0.5, 0.8]:
        if x_sunray < 0.3: # Ray interacting with wake
            y_sun_distorted = np.linspace(0.95, 0.05, 50)
            x_sun_distorted = x_sunray + 0.03 * np.sin(y_sun_distorted * 8 * np.pi + 0.5) * np.exp(-(y_sun_distorted-0.4)**2 / 0.1) # Distortion in wake area
            axB.plot(x_sun_distorted, y_sun_distorted, 'lemonchiffon', linestyle='-', linewidth=1.5, alpha=0.7)
        else: # Relatively undisturbed rays
            axB.plot([x_sunray, x_sunray - 0.05], [0.95, 0.05], 'lemonchiffon', linestyle='-', linewidth=1.5, alpha=0.7)

    axB.text(0.8, 0.9, "Sunlight", ha='center', va='bottom', fontsize=8, color='darkgoldenrod')


    axB.set_xlim(-0.1, 1.1)
    axB.set_ylim(0, 1)
    axB.set_xticks([])
    axB.set_yticks([])

    fig.suptitle('Figure SP2: Conceptual Schlieren Effects in Nature', fontsize=14, fontweight='bold')
    return fig

if __name__ == '__main__':
    fig_sp2 = create_figure_sp2_natural_schlieren_effects()
    plt.savefig("figure_sp2_natural_schlieren_effects.png", dpi=300, bbox_inches='tight')
    plt.show()