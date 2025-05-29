import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches

# Set up the figure with subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Panel A: Refractive Index Field & Light Deflection
ax1 = fig.add_subplot(gs[0, 0])

# Create refractive index field (Gaussian distribution)
x = np.linspace(0, 10, 100)
y = np.linspace(0, 8, 80)
X, Y = np.meshgrid(x, y)

# Gaussian refractive index variation
x_center, y_center = 4, 4
sigma_x, sigma_y = 1.5, 1.0
n_base = 0.00033
n_variation = 0.00015
n_field = n_base + n_variation * np.exp(-((X - x_center)**2 / (2 * sigma_x**2) + 
                                          (Y - y_center)**2 / (2 * sigma_y**2)))

# Plot refractive index field
im1 = ax1.imshow(n_field, extent=[0, 10, 0, 8], origin='lower', 
                 cmap='hot', alpha=0.8, aspect='auto')

# Add light rays
ray_y_positions = np.linspace(1, 7, 5)
for i, y_pos in enumerate(ray_y_positions):
    if i == 2:  # Middle ray passes through disturbance
        # Deflected ray
        x_ray = np.linspace(0, 10, 100)
        deflection = 0.3 * np.exp(-((x_ray - x_center)**2 / (2 * sigma_x**2))) * \
                    np.exp(-((y_pos - y_center)**2 / (2 * sigma_y**2)))
        y_ray = y_pos + deflection
        ax1.plot(x_ray, y_ray, 'b-', linewidth=2, label='Deflected Ray' if i == 2 else '')
    else:
        # Straight rays
        ax1.axhline(y=y_pos, color='blue', linewidth=1.5, alpha=0.7)

# Add labels
ax1.text(0.5, 7.5, 'Incident\nParallel Rays', fontsize=10, ha='left')
ax1.text(8.5, 6.5, 'Deflected\nRays', fontsize=10, ha='center')

# Colorbar
cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8)
cbar1.set_label('Refractive Index', rotation=270, labelpad=15)

ax1.set_xlabel('x (mm)')
ax1.set_ylabel('y (mm)')
ax1.set_title('A) Refractive Index Field & Light Deflection', fontweight='bold')
ax1.grid(True, alpha=0.3)

# Panel B: Z-type Schlieren Configuration
ax2 = fig.add_subplot(gs[0, 1])

# Light source
ax2.plot(1, 3, 'yo', markersize=10, markeredgecolor='orange', markeredgewidth=2)
ax2.text(1, 2.5, 'Light\nSource', ha='center', fontsize=9)

# Parabolic mirror 1
mirror1_x = np.linspace(2, 2.5, 50)
mirror1_y = 2 + 2 * (mirror1_x - 2.25)**2 / 0.25**2
ax2.plot(mirror1_x, mirror1_y, 'k-', linewidth=3)

# Test section (dashed box)
test_box = Rectangle((4, 2), 2, 2, linewidth=2, edgecolor='blue', 
                    facecolor='lightblue', alpha=0.3, linestyle='--')
ax2.add_patch(test_box)
ax2.text(5, 1.5, 'Test Section', ha='center', fontsize=9)

# Parabolic mirror 2
mirror2_x = np.linspace(7.5, 8, 50)
mirror2_y = 4 - 2 * (mirror2_x - 7.75)**2 / 0.25**2
ax2.plot(mirror2_x, mirror2_y, 'k-', linewidth=3)
ax2.text(7.75, 2.5, 'Parabolic\nMirror 2', ha='center', fontsize=8)

# Knife edge
ax2.plot([9, 9], [2.8, 4.2], 'k-', linewidth=4)
ax2.text(9.2, 3.5, 'Knife\nEdge', ha='left', fontsize=9)

# Screen
ax2.plot([11, 11], [2, 4.5], 'gray', linewidth=6)
ax2.text(11, 1.5, 'Screen', ha='center', fontsize=9)

# Light rays
# Undeflected ray
ax2.plot([1.2, 2.2], [3.1, 3.1], 'g-', linewidth=2)
ax2.plot([2.5, 4], [3.1, 3.1], 'g-', linewidth=2)
ax2.plot([6, 7.5], [3.1, 3.1], 'g-', linewidth=2)
ax2.plot([8, 9], [3.1, 3.1], 'g-', linewidth=2, label='Undeflected')

# Deflected ray
ax2.plot([1.2, 2.2], [2.9, 3.3], 'r--', linewidth=2)
ax2.plot([2.5, 4], [3.3, 3.5], 'r--', linewidth=2)
ax2.plot([6, 7.5], [3.5, 3.3], 'r--', linewidth=2)
ax2.plot([8, 9], [3.3, 3.8], 'r--', linewidth=2, label='Deflected')

ax2.set_xlim(0, 12)
ax2.set_ylim(1, 5)
ax2.set_title('B) Z-type Schlieren Configuration', fontweight='bold')
ax2.legend(loc='upper right')
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

# Panel C: Knife Edge Cutoff Mechanism
ax3 = fig.add_subplot(gs[1, 0])

# Create ray diagram
distances = np.linspace(-2, 2, 100)
ray_heights = np.linspace(-0.8, 0.8, 17)

# Plot rays
for i, height in enumerate(ray_heights):
    if height > 0.15:  # Rays above knife edge (blocked)
        ax3.plot(distances, [height] * len(distances), 'r--', alpha=0.6, linewidth=1)
    else:  # Rays below knife edge (pass through)
        ax3.plot(distances, [height] * len(distances), 'g-', alpha=0.8, linewidth=1)

# Knife edge
knife_x = np.linspace(0.8, 2, 50)
knife_y = np.linspace(0.15, 0.15, 50)
ax3.fill_between([0.8, 2], [0.15, 0.15], [0.8, 0.8], color='black', alpha=0.8)
ax3.text(1.4, 0.5, 'Knife Edge', ha='center', fontsize=10, color='white', fontweight='bold')

# Focus point
ax3.plot(0, 0, 'ko', markersize=8)
ax3.plot(0, 0.2, 'ro', markersize=6)  # Deflected focus

# Grid and labels
ax3.grid(True, alpha=0.3)
ax3.set_xlabel('Distance from focus (mm)')
ax3.set_ylabel('Ray Height (mm)')
ax3.set_title('C) Knife Edge Cutoff Mechanism', fontweight='bold')
ax3.set_xlim(-2, 2)
ax3.set_ylim(-0.8, 0.8)

# Panel D: Schlieren Image Formation
ax4 = fig.add_subplot(gs[1, 1])

# Create synthetic Schlieren image
x_img = np.linspace(-5, 5, 100)
y_img = np.linspace(-5, 5, 100)
X_img, Y_img = np.meshgrid(x_img, y_img)

# Create a circular disturbance pattern
r = np.sqrt(X_img**2 + Y_img**2)
intensity = 0.5 + 0.3 * np.exp(-r**2 / 4) * np.cos(2 * np.pi * r / 3)

# Add some noise for realism
intensity += 0.05 * np.random.randn(*intensity.shape)
intensity = np.clip(intensity, 0, 1)

im4 = ax4.imshow(intensity, extent=[-5, 5, -5, 5], cmap='gray', origin='lower')
ax4.set_xlabel('x (mm)')
ax4.set_ylabel('y (mm)')
ax4.set_title('D) Schlieren Image Formation', fontweight='bold')

# Add colorbar
cbar4 = plt.colorbar(im4, ax=ax4, shrink=0.8)
cbar4.set_label('Image Intensity', rotation=270, labelpad=15)

# Main title
fig.suptitle('Figure 1: Physical Principles of Schlieren Imaging', 
             fontsize=16, fontweight='bold', y=0.95)

plt.tight_layout()
plt.show()