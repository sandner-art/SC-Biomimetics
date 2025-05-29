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
    'lines.linewidth': 1.5,
    'axes.grid': False,
    'figure.constrained_layout.use': True
})

def create_figure_1_schlieren_principle():
    """Figure 1: Physical principles of schlieren imaging"""
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Panel A: Refractive index field and light deflection
    axA = fig.add_subplot(gs[0, 0])
    axA.set_title('A) Refractive Index Field & Light Deflection')
    
    # Create refractive index field (Gaussian profile)
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 8, 80)
    X, Y = np.meshgrid(x, y)
    
    # Gaussian refractive index field (heated region)
    n_field = 1.0003 + 0.0002 * np.exp(-((X-5)**2 + (Y-4)**2) / 2)
    
    # Plot refractive index field
    im = axA.contourf(X, Y, n_field, levels=20, cmap='YlOrRd', alpha=0.7)
    cbar = plt.colorbar(im, ax=axA, shrink=0.8)
    cbar.set_label('Refractive Index', fontsize=9)
    
    # Add light rays with proper deflection
    y_rays = [2, 3, 4, 5, 6]
    for i, y_start in enumerate(y_rays):
        # Calculate ray path through gradient field
        x_ray = np.linspace(0, 10, 50)
        y_ray = np.full_like(x_ray, y_start)
        
        # Apply deflection based on gradient (simplified)
        for j in range(1, len(x_ray)):
            if 3 < x_ray[j] < 7:  # In gradient region
                gradient_y = -(Y[int(y_ray[j-1]*10), int(x_ray[j]*10)] - 4) * 0.1
                y_ray[j] = y_ray[j-1] + gradient_y * 0.1
        
        axA.plot(x_ray, y_ray, 'b-', linewidth=2, alpha=0.8)
        axA.arrow(x_ray[-2], y_ray[-2], x_ray[-1]-x_ray[-2], y_ray[-1]-y_ray[-2], 
                 head_width=0.1, head_length=0.2, fc='blue', ec='blue')
    
    axA.text(0.5, 7, 'Incident\nParallel Rays', fontsize=9, ha='center')
    axA.text(8.5, 6.5, 'Deflected\nRays', fontsize=9, ha='center')
    axA.set_xlim(0, 10)
    axA.set_ylim(0, 8)
    axA.set_xlabel('x (mm)')
    axA.set_ylabel('y (mm)')

    # Panel B: Z-type Schlieren Setup (Accurate)
    axB = fig.add_subplot(gs[0, 1])
    axB.set_title('B) Z-type Schlieren Configuration')
    
    # Light source
    axB.add_patch(patches.Circle((0.5, 4), 0.2, color='yellow', ec='black'))
    axB.text(0.5, 3.5, 'Light\nSource', ha='center', fontsize=8)
    
    # Concave mirror 1 (parabolic)
    mirror1_x = np.linspace(1.8, 2.2, 20)
    mirror1_y = 6 - 2*(mirror1_x - 2)**2  # Parabolic shape
    axB.plot(mirror1_x, mirror1_y, 'k-', linewidth=4)
    axB.text(2, 7, 'Parabolic\nMirror 1', ha='center', fontsize=8)
    
    # Test section
    test_section = patches.Rectangle((4, 3), 2, 2, linewidth=2, 
                                   linestyle='--', edgecolor='blue', facecolor='none')
    axB.add_patch(test_section)
    axB.text(5, 2.5, 'Test Section', ha='center', fontsize=8)
    
    # Heat source in test section
    flame_x = [4.8, 5, 5.2, 5]
    flame_y = [3.2, 4.5, 3.2, 3.2]
    axB.fill(flame_x, flame_y, color='orangered', alpha=0.7)
    
    # Concave mirror 2
    mirror2_x = np.linspace(7.8, 8.2, 20)
    mirror2_y = 2 + 2*(mirror2_x - 8)**2
    axB.plot(mirror2_x, mirror2_y, 'k-', linewidth=4)
    axB.text(8, 1, 'Parabolic\nMirror 2', ha='center', fontsize=8)
    
    # Knife edge at focal point
    axB.plot([9, 9], [3.8, 4.2], 'k-', linewidth=6)
    axB.text(9, 3.5, 'Knife\nEdge', ha='center', fontsize=8)
    
    # Screen
    axB.plot([10, 10], [1, 7], 'gray', linewidth=8)
    axB.text(10, 0.5, 'Screen', ha='center', fontsize=8)
    
    # Light paths (simplified representation)
    # Undeflected ray
    axB.plot([0.7, 1.9, 4, 6, 8.1, 9, 10], [4, 5.8, 4, 4, 2.2, 4, 4], 
             'g-', linewidth=2, alpha=0.7, label='Undeflected')
    # Deflected ray
    axB.plot([0.7, 1.9, 4, 5, 6, 8.1, 9], [4, 5.8, 4, 4.3, 3.7, 2.2, 3.9], 
             'r--', linewidth=2, alpha=0.7, label='Deflected')
    
    axB.set_xlim(0, 11)
    axB.set_ylim(0, 8)
    axB.legend(loc='upper right', fontsize=8)
    axB.axis('off')

    # Panel C: Knife Edge Effect
    axC = fig.add_subplot(gs[1, 0])
    axC.set_title('C) Knife Edge Cutoff Mechanism')
    
    # Focal point representation
    axC.axhline(y=0, color='k', linewidth=1, alpha=0.5)
    
    # Undeflected rays converging to focus
    angles = np.linspace(-0.3, 0.3, 7)
    for angle in angles:
        x_ray = np.linspace(-2, 2, 100)
        y_ray = angle * x_ray
        # Rays converge at x=0
        mask = x_ray <= 0
        axC.plot(x_ray[mask], y_ray[mask], 'g-', alpha=0.6, linewidth=1)
        # Diverging rays after focus
        mask = x_ray > 0
        axC.plot(x_ray[mask], y_ray[mask], 'g-', alpha=0.6, linewidth=1)
    
    # Deflected rays (shifted focus)
    for angle in angles:
        x_ray = np.linspace(-2, 2, 100)
        y_ray = angle * x_ray + 0.2  # Shifted up
        mask = x_ray <= 0
        axC.plot(x_ray[mask], y_ray[mask], 'r--', alpha=0.6, linewidth=1)
        mask = x_ray > 0
        axC.plot(x_ray[mask], y_ray[mask], 'r--', alpha=0.6, linewidth=1)
    
    # Knife edge
    axC.fill_between([0.5, 2], [-2, -2], [0.1, 0.1], color='black', alpha=0.8)
    axC.text(1.2, -0.3, 'Knife Edge', fontsize=9)
    
    axC.set_xlim(-2, 2)
    axC.set_ylim(-0.8, 0.8)
    axC.set_xlabel('Distance from focus (mm)')
    axC.set_ylabel('Ray height (mm)')
    axC.grid(True, alpha=0.3)

    # Panel D: Resulting Image Contrast
    axD = fig.add_subplot(gs[1, 1])
    axD.set_title('D) Schlieren Image Formation')
    
    # Simulate schlieren image
    x_img = np.linspace(-5, 5, 100)
    y_img = np.linspace(-5, 5, 100)
    X_img, Y_img = np.meshgrid(x_img, y_img)
    
    # Create a thermal plume-like density field
    density_gradient = np.exp(-((X_img)**2 + (Y_img+2)**2) / 4) - \
                      np.exp(-((X_img)**2 + (Y_img-2)**2) / 4)
    
    # Convert to grayscale intensity (knife edge effect)
    intensity = 0.5 + 0.3 * np.tanh(2 * density_gradient)
    
    im_schlieren = axD.imshow(intensity, extent=[-5, 5, -5, 5], 
                             cmap='gray', origin='lower')
    axD.set_xlabel('x (mm)')
    axD.set_ylabel('y (mm)')
    
    # Add colorbar
    cbar = plt.colorbar(im_schlieren, ax=axD, shrink=0.8)
    cbar.set_label('Image Intensity', fontsize=9)

    fig.suptitle('Figure 1: Physical Principles of Schlieren Imaging', 
                fontsize=14, fontweight='bold', y=0.95)
    return fig

def create_figure_2_sensitivity_analysis():
    """Figure 2: Sensitivity and optical setup variations"""
    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Panel A: Sensitivity vs. Focal Length
    axA = fig.add_subplot(gs[0, 0])
    focal_lengths = np.linspace(100, 1000, 50)  # mm
    sensitivity = 1 / focal_lengths  # Inverse relationship
    axA.plot(focal_lengths, sensitivity * 1000, 'b-', linewidth=2)
    axA.set_xlabel('Focal Length (mm)')
    axA.set_ylabel('Sensitivity (×10⁻³ rad⁻¹)')
    axA.set_title('A) Sensitivity vs. Focal Length')
    axA.grid(True, alpha=0.3)

    # Panel B: Knife Edge Orientations
    axB = fig.add_subplot(gs[0, 1])
    axB.set_title('B) Knife Edge Orientations')
    
    # Horizontal knife edge
    axB.fill_between([-1, 1], [0, 0], [1, 1], color='black', alpha=0.8)
    axB.text(0, 0.5, 'Horizontal\n(Vertical gradients)', ha='center', fontsize=9)
    axB.arrow(-0.5, -0.5, 0, 0.3, head_width=0.1, head_length=0.1, 
              fc='red', ec='red')
    axB.text(-0.5, -0.7, '∂n/∂y', ha='center', fontsize=9, color='red')
    
    # Vertical knife edge (in different subplot region)
    axB.fill_between([0, 1], [-1, -1], [1, 1], color='black', alpha=0.8)
    axB.text(0.5, 0, 'Vertical\n(Horizontal gradients)', ha='center', fontsize=9)
    axB.arrow(-0.8, 0, 0.3, 0, head_width=0.1, head_length=0.1, 
              fc='blue', ec='blue')
    axB.text(-0.8, -0.2, '∂n/∂x', ha='center', fontsize=9, color='blue')
    
    axB.set_xlim(-1, 1)
    axB.set_ylim(-1, 1)
    axB.axis('off')

    # Panel C: Color Schlieren Setup
    axC = fig.add_subplot(gs[1, 0])
    axC.set_title('C) Color Schlieren Configuration')
    
    # Similar to B but with colored elements
    # Rainbow filter instead of knife edge
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    for i, color in enumerate(colors):
        axC.add_patch(patches.Rectangle((8 + i*0.1, 3), 0.1, 2, 
                                       facecolor=color, alpha=0.8))
    
    axC.text(8.3, 2.5, 'Color Filter', ha='center', fontsize=9)
    
    # Other components (simplified)
    axC.add_patch(patches.Circle((1, 4), 0.2, color='yellow', ec='black'))
    axC.plot([2, 2.4], [5.5, 4], 'k-', linewidth=4)  # Mirror 1
    axC.add_patch(patches.Rectangle((4, 3), 2, 2, linewidth=2, 
                                   linestyle='--', edgecolor='blue', facecolor='none'))
    axC.plot([7.6, 8], [2.5, 4], 'k-', linewidth=4)  # Mirror 2
    axC.plot([9.5, 9.5], [1, 7], 'gray', linewidth=8)  # Screen
    
    axC.set_xlim(0, 10)
    axC.set_ylim(0, 8)
    axC.axis('off')

    # Panel D: Image Processing and Analysis
    axD = fig.add_subplot(gs[1, 1])
    axD.set_title('D) Quantitative Analysis')
    
    # Simulate a line profile through schlieren image
    x_profile = np.linspace(-5, 5, 100)
    intensity_profile = 0.5 + 0.3 * np.exp(-(x_profile)**2) * np.sin(2*x_profile)
    
    axD.plot(x_profile, intensity_profile, 'k-', linewidth=2, label='Intensity')
    
    # Derivative (proportional to density gradient)
    gradient_profile = np.gradient(intensity_profile, x_profile)
    axD.plot(x_profile, gradient_profile, 'r--', linewidth=2, label='∇I ∝ ∇ρ')
    
    axD.set_xlabel('Position (mm)')
    axD.set_ylabel('Normalized Value')
    axD.legend()
    axD.grid(True, alpha=0.3)

    fig.suptitle('Figure 2: Schlieren System Configuration and Analysis', 
                fontsize=14, fontweight='bold', y=0.95)
    return fig

def create_figure_3_applications():
    """Figure 3: Schlieren imaging applications"""
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)

    # Panel A: Combustion
    axA = fig.add_subplot(gs[0, 0])
    axA.set_title('A) Combustion')
    
    # Simulate flame schlieren image
    x = np.linspace(-3, 3, 60)
    y = np.linspace(0, 8, 80)
    X, Y = np.meshgrid(x, y)
    
    # Flame-like structure
    flame_intensity = np.exp(-X**2/2) * np.exp(-(Y-4)**2/8) * (1 + 0.3*np.sin(5*Y))
    flame_intensity += np.random.normal(0, 0.05, flame_intensity.shape)  # Noise
    
    im = axA.imshow(flame_intensity, extent=[-3, 3, 0, 8], cmap='hot', origin='lower')
    axA.set_xlabel('x (mm)')
    axA.set_ylabel('y (mm)')

    # Panel B: Supersonic Flow
    axB = fig.add_subplot(gs[0, 1])
    axB.set_title('B) Supersonic Flow')
    
    # Simulate shock wave pattern
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    
    # Oblique shock pattern
    shock_pattern = np.zeros_like(X)
    shock_pattern[np.abs(Y - 0.5*X) < 0.2] = 1
    shock_pattern[np.abs(Y + 0.5*X) < 0.2] = -1
    
    im = axB.imshow(shock_pattern, extent=[-5, 5, -3, 3], cmap='RdBu', origin='lower')
    axB.set_xlabel('x (mm)')
    axB.set_ylabel('y (mm)')

    # Panel C: Heat Transfer
    axC = fig.add_subplot(gs[0, 2])
    axC.set_title('C) Heat Transfer')
    
    # Thermal boundary layer
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # Boundary layer profile
    boundary_layer = np.exp(-Y/2) * (1 - np.exp(-X/5))
    
    im = axC.imshow(boundary_layer, extent=[0, 10, 0, 5], cmap='YlOrRd', origin='lower')
    axC.set_xlabel('x (mm)')
    axC.set_ylabel('y (mm)')

    # Panel D: Mixing and Turbulence
    axD = fig.add_subplot(gs[1, 0])
    axD.set_title('D) Mixing & Turbulence')
    
    # Turbulent mixing layer
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    
    # Create turbulent-like structures
    turbulence = np.sin(2*X + 0.5*Y) * np.cos(X - 0.3*Y) + \
                0.5*np.sin(4*X + Y) * np.cos(2*X - Y)
    
    im = axD.imshow(turbulence, extent=[-5, 5, -5, 5], cmap='seismic', origin='lower')
    axD.set_xlabel('x (mm)')
    axD.set_ylabel('y (mm)')

    # Panel E: Quantitative Measurements
    axE = fig.add_subplot(gs[1, 1:])
    axE.set_title('E) Quantitative Data Extraction')
    
    # Example: velocity profile from PIV-like analysis
    y_positions = np.linspace(0, 10, 20)
    velocity = 5 * (1 - np.exp(-y_positions/2)) + np.random.normal(0, 0.2, len(y_positions))
    
    axE.errorbar(velocity, y_positions, xerr=0.2, fmt='bo-', capsize=3, 
                label='Experimental Data')
    
    # Theoretical curve
    y_theory = np.linspace(0, 10, 100)
    v_theory = 5 * (1 - np.exp(-y_theory/2))
    axE.plot(v_theory, y_theory, 'r-', linewidth=2, label='Theoretical Profile')
    
    axE.set_xlabel('Velocity (m/s)')
    axE.set_ylabel('Height (mm)')
    axE.legend()
    axE.grid(True, alpha=0.3)

    fig.suptitle('Figure 3: Applications of Schlieren Imaging', 
                fontsize=14, fontweight='bold', y=0.95)
    return fig

if __name__ == '__main__':
    # Create all figures
    fig1 = create_figure_1_schlieren_principle()
    fig2 = create_figure_2_sensitivity_analysis()
    fig3 = create_figure_3_applications()
    
    # Save figures
    fig1.savefig("figure_1_schlieren_principles.png", dpi=300, bbox_inches='tight')
    fig2.savefig("figure_2_schlieren_analysis.png", dpi=300, bbox_inches='tight')
    fig3.savefig("figure_3_schlieren_applications.png", dpi=300, bbox_inches='tight')
    
    plt.show()