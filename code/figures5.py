import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set style for scientific figures
plt.style.use('default')
sns.set_palette("muted")
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'lines.linewidth': 1.5, # Slightly thinner lines for schematics
    'axes.grid': False, # Usually no grid for these types of schematics
    'figure.constrained_layout.use': True
})

def create_figure_sp1_schlieren_fundamentals():
    fig = plt.figure(figsize=(12, 5)) # Adjusted for 3 panels horizontally
    gs = GridSpec(1, 3, figure=fig, wspace=0.3)

    # --- Panel A: Light in Homogeneous Medium ---
    axA = fig.add_subplot(gs[0, 0])
    axA.set_title('A) Homogeneous Medium')

    # Medium box
    medium_A = patches.Rectangle((0.1, 0.2), 0.8, 0.6, linewidth=1, edgecolor='gray', facecolor='aliceblue', alpha=0.7)
    axA.add_patch(medium_A)
    axA.text(0.5, 0.5, "Homogeneous\nMedium", ha='center', va='center', fontsize=9, color='darkslategray')

    # Light rays (straight)
    for y_ray in [0.35, 0.5, 0.65]:
        axA.arrow(-0.1, y_ray, 1.2, 0, head_width=0.02, head_length=0.03, fc='gold', ec='orange', length_includes_head=True)
    axA.text(-0.15, 0.75, "Incident Light", ha='left', va='center', fontsize=9)

    axA.set_xlim(-0.2, 1.2)
    axA.set_ylim(0, 1)
    axA.axis('off') # Turn off axis lines and ticks

    # --- Panel B: Light in Density Gradient ---
    axB = fig.add_subplot(gs[0, 1])
    axB.set_title('B) Density Gradient Effect')

    # Medium box
    medium_B = patches.Rectangle((0.1, 0.2), 0.8, 0.6, linewidth=1, edgecolor='gray', facecolor='lightyellow', alpha=0.5)
    axB.add_patch(medium_B)

    # Candle flame (simplified) - source of gradient
    flame_body = patches.Ellipse((0.5, 0.35), 0.1, 0.25, color='orangered', alpha=0.8)
    flame_tip = patches.Ellipse((0.5, 0.55), 0.06, 0.15, color='yellow', alpha=0.9)
    wick = patches.Rectangle((0.49, 0.2), 0.02, 0.1, color='black')
    axB.add_patch(wick)
    axB.add_patch(flame_body)
    axB.add_patch(flame_tip)
    axB.text(0.5, 0.1, "Heat Source\n(Density Gradient)", ha='center', va='top', fontsize=8)

    # Wavy lines indicating thermal plume / gradient
    for i in range(4):
        plume_x = 0.5 + np.random.uniform(-0.05, 0.05)
        plume_y = np.linspace(0.55, 0.8 + np.random.uniform(-0.05, 0.05), 20)
        plume_x_coords = plume_x + 0.03 * np.sin(plume_y * 20 + np.random.rand()*np.pi)
        axB.plot(plume_x_coords, plume_y, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)


    # Light rays (bending)
    # Ray 1 (above flame - slight upward bend)
    axB.plot([-0.1, 0.45, 0.55, 1.1], [0.7, 0.7, 0.72, 0.75], color='gold', linewidth=1.5)
    axB.arrow(1.1, 0.75, 0.001, 0, head_width=0.02, head_length=0.03, fc='gold', ec='orange', length_includes_head=True, shape='full')
    # Ray 2 (through edge of flame - stronger bend)
    axB.plot([-0.1, 0.4, 0.6, 1.1], [0.5, 0.5, 0.42, 0.38], color='gold', linewidth=1.5)
    axB.arrow(1.1, 0.38, 0.001, 0, head_width=0.02, head_length=0.03, fc='gold', ec='orange', length_includes_head=True, shape='full')
    # Ray 3 (below flame - less affected or slight downward if gradient extends)
    axB.plot([-0.1, 0.45, 0.55, 1.1], [0.3, 0.3, 0.29, 0.28], color='gold', linewidth=1.5)
    axB.arrow(1.1, 0.28, 0.001, 0, head_width=0.02, head_length=0.03, fc='gold', ec='orange', length_includes_head=True, shape='full')

    axB.text(-0.15, 0.85, "Incident Light", ha='left', va='center', fontsize=9)
    axB.text(1.15, 0.8, "Deflected\nLight", ha='left', va='center', fontsize=9)


    axB.set_xlim(-0.2, 1.2)
    axB.set_ylim(0, 1)
    axB.axis('off')

    # --- Panel C: Simplified Z-type Schlieren Setup ---
    axC = fig.add_subplot(gs[0, 2])
    axC.set_title('C) Simplified Schlieren Setup (Z-type)')

    # Components
    axC.text(0.05, 0.85, "Light\nSource", ha='center', va='center', fontsize=8)
    axC.add_patch(patches.Circle((0.05, 0.8), 0.03, color='yellow', ec='black'))

    # Mirror 1 (Collimating)
    m1 = patches.Rectangle((0.18, 0.7), 0.04, 0.2, angle=-45, color='silver', ec='black')
    axC.add_patch(m1)
    axC.text(0.2, 0.6, "Mirror 1\n(Collimating)", ha='center', va='top', fontsize=8)

    # Test Section
    test_section = patches.Rectangle((0.35, 0.45), 0.3, 0.1, linewidth=1, linestyle='--', edgecolor='blue', facecolor='none')
    axC.add_patch(test_section)
    axC.text(0.5, 0.4, "Test Section\n(Density Gradient)", ha='center', va='top', fontsize=8)
    # Flame in test section
    flame_C_body = patches.Ellipse((0.5, 0.5), 0.03, 0.07, color='orangered', alpha=0.6)
    axC.add_patch(flame_C_body)


    # Mirror 2 (Focusing)
    m2 = patches.Rectangle((0.78, 0.1), 0.04, 0.2, angle=45, color='silver', ec='black')
    axC.add_patch(m2)
    axC.text(0.8, 0.4, "Mirror 2\n(Focusing)", ha='center', va='top', fontsize=8)


    # Knife Edge
    knife_edge = patches.Rectangle((0.88, 0.48), 0.02, 0.15, color='dimgray', ec='black') # y slightly offset for deflected ray
    axC.add_patch(knife_edge)
    axC.text(0.9, 0.38, "Knife\nEdge", ha='center', va='top', fontsize=8)

    # Screen
    screen = patches.Rectangle((0.95, 0.05), 0.02, 0.9, color='lightgray', ec='black')
    axC.add_patch(screen)
    axC.text(0.96, -0.02, "Screen", ha='center', va='top', fontsize=8)
    # Schlieren image on screen (conceptual)
    axC.add_patch(patches.Ellipse((0.96, 0.7), 0.008, 0.05, color='black', alpha=0.6)) # Dark region for deflected
    axC.add_patch(patches.Ellipse((0.96, 0.3), 0.008, 0.07, color='white', ec='darkgray', alpha=0.8)) # Bright region

    # Light path (simplified)
    # Source to M1
    axC.plot([0.08, 0.19], [0.8, 0.8], 'y-', alpha=0.7)
    # M1 to Test Section (collimated - represented by two rays)
    axC.plot([0.25, 0.35], [0.75, 0.52], 'y-', alpha=0.7) # Upper ray
    axC.plot([0.25, 0.35], [0.70, 0.47], 'y-', alpha=0.7) # Lower ray
    # Through Test Section (one ray deflected)
    axC.plot([0.35, 0.65], [0.52, 0.52], 'y-', alpha=0.7) # Undeflected upper
    axC.plot([0.35, 0.5, 0.65], [0.47, 0.48, 0.46], 'y-', alpha=0.7) # Deflected lower (bends down slightly more)
    # From Test Section to M2
    axC.plot([0.65, 0.79], [0.52, 0.25], 'y-', alpha=0.7) # Undeflected
    axC.plot([0.65, 0.79], [0.46, 0.18], 'y-', alpha=0.7) # Deflected (focuses lower)
    # From M2 to Knife-Edge/Screen
    axC.plot([0.82, 0.95], [0.24, 0.7], 'y-', alpha=0.7) # Undeflected, mostly passes over knife, hits screen high
    axC.plot([0.82, 0.885], [0.19, 0.48], 'y-', alpha=0.7) # Deflected, hits knife edge
    axC.plot([0.82, 0.95], [0.19, 0.3], 'y--', alpha=0.5) # Deflected, what might pass if knife is adjusted or misses slightly


    axC.set_xlim(0, 1)
    axC.set_ylim(0, 1)
    axC.axis('off')

    fig.suptitle('Figure SP1: Fundamentals of Schlieren Imaging', fontsize=14, fontweight='bold')
    return fig

if __name__ == '__main__':
    fig_sp1 = create_figure_sp1_schlieren_fundamentals()
    plt.savefig("figure_sp1_schlieren_fundamentals.png", dpi=300, bbox_inches='tight')
    plt.show()