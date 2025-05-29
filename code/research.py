import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Arrow
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines

# Set up the plotting style for professional scientific figures
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'DejaVu Sans',
    'axes.linewidth': 1.2,
    'lines.linewidth': 1.5,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def create_light_deflection_principle():
    """Create Figure 1: Fundamental Principle of Light Deflection"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Define y positions for the three scenarios
    y_positions = [6, 3.5, 1]
    scenarios = ['Uniform Medium (n₀)', 'Lower Density Region (n < n₀)', 'Higher Density Region (n > n₀)']
    
    for i, (y_pos, scenario) in enumerate(zip(y_positions, scenarios)):
        # Draw incident ray
        ax.arrow(1, y_pos, 3, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue', linewidth=2)
        ax.text(0.5, y_pos, 'Incident Ray', ha='right', va='center', fontsize=9, color='blue')
        
        # Draw medium region
        if i == 0:  # Uniform medium
            rect = patches.Rectangle((4, y_pos-0.3), 4, 0.6, linewidth=2, 
                                   edgecolor='black', facecolor='lightgray', alpha=0.3)
            ax.add_patch(rect)
            # Straight transmitted ray
            ax.arrow(8, y_pos, 3, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue', linewidth=2)
            ax.text(8.5, y_pos+0.3, 'Undeflected', ha='center', va='bottom', fontsize=9, color='blue')
            
        elif i == 1:  # Lower density (hot air plume)
            # Draw plume shape
            plume_x = np.array([4, 5, 6, 7, 8])
            plume_top = np.array([y_pos+0.5, y_pos+0.7, y_pos+0.8, y_pos+0.7, y_pos+0.5])
            plume_bottom = np.array([y_pos-0.2, y_pos-0.2, y_pos-0.2, y_pos-0.2, y_pos-0.2])
            
            ax.fill_between(plume_x, plume_bottom, plume_top, alpha=0.2, color='red', label='Hot air (n < n₀)')
            ax.plot(plume_x, plume_top, 'r--', linewidth=1.5)
            ax.plot(plume_x, plume_bottom, 'k-', linewidth=1)
            
            # Deflected ray (bent away from lower n)
            ax.arrow(8, y_pos, 2.5, 0.8, head_width=0.1, head_length=0.1, fc='blue', ec='blue', linewidth=2)
            ax.text(9, y_pos+0.6, 'Deflected\n(away from low n)', ha='center', va='center', fontsize=9, color='blue')
            
        else:  # Higher density region
            # Draw denser region
            rect = patches.Rectangle((4, y_pos-0.4), 4, 0.8, linewidth=2, 
                                   edgecolor='black', facecolor='lightblue', alpha=0.5)
            ax.add_patch(rect)
            ax.text(6, y_pos, 'n > n₀', ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Deflected ray (bent toward higher n)
            ax.arrow(8, y_pos, 2.5, -0.8, head_width=0.1, head_length=0.1, fc='blue', ec='blue', linewidth=2)
            ax.text(9, y_pos-0.6, 'Deflected\n(toward high n)', ha='center', va='center', fontsize=9, color='blue')
        
        # Add scenario label
        ax.text(0.2, y_pos, f'{i+1}.', fontsize=12, fontweight='bold', va='center')
        ax.text(12, y_pos, scenario, ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Add refractive index gradient explanation
    ax.text(6, 7.5, 'Light Deflection in Refractive Index Gradients', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(6, 0.2, 'Light rays bend toward regions of higher refractive index (∇n)', 
            ha='center', va='center', fontsize=11, style='italic')
    
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def create_classical_schlieren():
    """Create Figure 2: Classical (Toepler) Schlieren System"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Component positions
    source_x, source_y = 1, 4
    l1_x, l1_y = 3, 4
    test_x, test_y = 6, 4
    l2_x, l2_y = 9, 4
    knife_x, knife_y = 11, 4
    screen_x, screen_y = 13, 4
    
    # Draw components
    # Light source
    circle = Circle((source_x, source_y), 0.15, facecolor='yellow', edgecolor='orange', linewidth=2)
    ax.add_patch(circle)
    ax.text(source_x, source_y-0.5, 'Light Source\n(S)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Collimating lens L1
    lens1 = patches.Ellipse((l1_x, l1_y), 0.2, 1.5, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(lens1)
    ax.text(l1_x, l1_y-1, 'Collimating\nLens (L1)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Test section with flame
    flame_x = np.linspace(test_x-0.5, test_x+0.5, 20)
    flame_y = test_y + 0.3 * np.sin(10*flame_x) * np.exp(-(flame_x-test_x)**2/0.1)
    ax.fill_between(flame_x, test_y-0.3, flame_y, alpha=0.3, color='red')
    ax.plot(flame_x, flame_y, 'r-', linewidth=2)
    ax.text(test_x, test_y-1, 'Test Section\n(Schlieren Object)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Focusing lens L2
    lens2 = patches.Ellipse((l2_x, l2_y), 0.2, 1.5, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(lens2)
    ax.text(l2_x, l2_y-1, 'Focusing\nLens (L2)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Knife edge
    knife = patches.Rectangle((knife_x-0.05, knife_y-0.8), 0.1, 0.8, 
                             facecolor='black', edgecolor='black')
    ax.add_patch(knife)
    ax.text(knife_x, knife_y-1, 'Knife Edge\n(K)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Screen
    screen = patches.Rectangle((screen_x-0.1, screen_y-1), 0.2, 2, 
                              facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(screen)
    ax.text(screen_x, screen_y-1.3, 'Screen/Camera\n(I)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Draw light rays
    # Undeflected rays
    ax.plot([source_x+0.15, l1_x-0.1], [source_y, l1_y], 'b-', linewidth=1.5, alpha=0.7)
    ax.plot([l1_x+0.1, test_x-0.5], [l1_y, test_y], 'b-', linewidth=1.5, alpha=0.7)
    ax.plot([test_x+0.5, l2_x-0.1], [test_y, l2_y], 'b-', linewidth=1.5, alpha=0.7)
    ax.plot([l2_x+0.1, knife_x-0.05], [l2_y, knife_y], 'b-', linewidth=1.5, alpha=0.7)
    
    # Deflected rays
    ax.plot([test_x+0.5, l2_x-0.1], [test_y+0.2, l2_y+0.2], 'b-', linewidth=1.5, alpha=0.5)
    ax.plot([l2_x+0.1, screen_x-0.1], [l2_y+0.2, screen_y+0.5], 'b-', linewidth=1.5, alpha=0.5)
    ax.text(screen_x+0.3, screen_y+0.5, 'Brighter\nRegion', ha='left', va='center', fontsize=8, color='blue')
    
    ax.plot([test_x+0.5, l2_x-0.1], [test_y-0.2, l2_y-0.2], 'b-', linewidth=1.5, alpha=0.5)
    # This ray hits knife edge (blocked)
    ax.plot([l2_x+0.1, knife_x-0.05], [l2_y-0.2, knife_y-0.2], 'b--', linewidth=1.5, alpha=0.3)
    ax.text(knife_x+0.3, knife_y-0.5, 'Blocked\n(Darker Region)', ha='left', va='center', fontsize=8, color='red')
    
    # Add optical axis
    ax.plot([0.5, 13.5], [source_y, source_y], 'k--', linewidth=1, alpha=0.5)
    ax.text(7, 3.5, 'Optical Axis', ha='center', va='center', fontsize=9, style='italic')
    
    # Add title and annotations
    ax.text(7, 6, 'Classical (Toepler) Schlieren System', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    
    # Add sensitivity direction arrow
    ax.arrow(knife_x, knife_y+1.5, 0, -0.5, head_width=0.1, head_length=0.1, fc='red', ec='red')
    ax.text(knife_x, knife_y+1.8, 'Sensitivity\nDirection', ha='center', va='bottom', fontsize=8, color='red')
    
    ax.set_xlim(0, 14)
    ax.set_ylim(1, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def create_rainbow_schlieren():
    """Create Figure 3: Rainbow Schlieren System"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Component positions (similar to classical)
    source_x, source_y = 1, 4
    l1_x, l1_y = 3, 4
    test_x, test_y = 6, 4
    l2_x, l2_y = 9, 4
    filter_x, filter_y = 11, 4
    screen_x, screen_y = 13, 4
    
    # Draw components
    # White light source with slit
    rect_source = patches.Rectangle((source_x-0.1, source_y-0.3), 0.2, 0.6, 
                                   facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(rect_source)
    ax.text(source_x, source_y-0.7, 'White Light\nSource + Slit', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Collimating lens L1
    lens1 = patches.Ellipse((l1_x, l1_y), 0.2, 1.5, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(lens1)
    ax.text(l1_x, l1_y-1, 'Collimating\nLens (L1)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Test section with flame
    flame_x = np.linspace(test_x-0.5, test_x+0.5, 20)
    flame_y = test_y + 0.3 * np.sin(10*flame_x) * np.exp(-(flame_x-test_x)**2/0.1)
    ax.fill_between(flame_x, test_y-0.3, flame_y, alpha=0.3, color='red')
    ax.plot(flame_x, flame_y, 'r-', linewidth=2)
    ax.text(test_x, test_y-1, 'Test Section\n(Flow)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Focusing lens L2
    lens2 = patches.Ellipse((l2_x, l2_y), 0.2, 1.5, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(lens2)
    ax.text(l2_x, l2_y-1, 'Focusing\nLens (L2)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Color filter
    filter_height = 1.2
    colors = ['red', 'green', 'blue']
    filter_sections = 3
    section_height = filter_height / filter_sections
    
    for i, color in enumerate(colors):
        y_start = filter_y - filter_height/2 + i * section_height
        rect = patches.Rectangle((filter_x-0.05, y_start), 0.1, section_height, 
                               facecolor=color, edgecolor='black', alpha=0.7)
        ax.add_patch(rect)
    
    ax.text(filter_x, filter_y-1, 'Color Filter\n(R-G-B)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Screen
    screen = patches.Rectangle((screen_x-0.1, screen_y-1), 0.2, 2, 
                              facecolor='lightgray', edgecolor='black', linewidth=2)
    ax.add_patch(screen)
    ax.text(screen_x, screen_y-1.3, 'Screen/Camera\n(I)', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Draw light rays with colors
    # Undeflected ray (green)
    ax.plot([source_x+0.1, l1_x-0.1], [source_y, l1_y], 'gray', linewidth=1.5, alpha=0.7)
    ax.plot([l1_x+0.1, test_x-0.5], [l1_y, test_y], 'gray', linewidth=1.5, alpha=0.7)
    ax.plot([test_x+0.5, l2_x-0.1], [test_y, l2_y], 'gray', linewidth=1.5, alpha=0.7)
    ax.plot([l2_x+0.1, filter_x-0.05], [l2_y, filter_y], 'gray', linewidth=1.5, alpha=0.7)
    ax.plot([filter_x+0.05, screen_x-0.1], [filter_y, screen_y], 'green', linewidth=2)
    
    # Upward deflected ray (blue)
    ax.plot([test_x+0.5, l2_x-0.1], [test_y+0.2, l2_y+0.3], 'gray', linewidth=1.5, alpha=0.5)
    ax.plot([l2_x+0.1, filter_x-0.05], [l2_y+0.3, filter_y+0.4], 'gray', linewidth=1.5, alpha=0.5)
    ax.plot([filter_x+0.05, screen_x-0.1], [filter_y+0.4, screen_y+0.6], 'blue', linewidth=2)
    
    # Downward deflected ray (red)
    ax.plot([test_x+0.5, l2_x-0.1], [test_y-0.2, l2_y-0.3], 'gray', linewidth=1.5, alpha=0.5)
    ax.plot([l2_x+0.1, filter_x-0.05], [l2_y-0.3, filter_y-0.4], 'gray', linewidth=1.5, alpha=0.5)
    ax.plot([filter_x+0.05, screen_x-0.1], [filter_y-0.4, screen_y-0.6], 'red', linewidth=2)
    
    # Add color labels on screen
    ax.text(screen_x+0.3, screen_y+0.6, 'Blue\n(upward deflection)', ha='left', va='center', fontsize=8, color='blue')
    ax.text(screen_x+0.3, screen_y, 'Green\n(no deflection)', ha='left', va='center', fontsize=8, color='green')
    ax.text(screen_x+0.3, screen_y-0.6, 'Red\n(downward deflection)', ha='left', va='center', fontsize=8, color='red')
    
    # Add optical axis
    ax.plot([0.5, 13.5], [source_y, source_y], 'k--', linewidth=1, alpha=0.5)
    
    # Add title
    ax.text(7, 6, 'Rainbow Schlieren System', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    
    ax.set_xlim(0, 14)
    ax.set_ylim(1, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def create_bos_system():
    """Create Figure 4: Background Oriented Schlieren (BOS) System"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Component positions
    camera_x, camera_y = 2, 4
    test_x, test_y = 6, 4
    background_x, background_y = 10, 4
    
    # Draw camera
    camera_body = patches.Rectangle((camera_x-0.3, camera_y-0.2), 0.6, 0.4, 
                                   facecolor='black', edgecolor='black')
    ax.add_patch(camera_body)
    lens_circle = Circle((camera_x+0.4, camera_y), 0.15, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(lens_circle)
    ax.text(camera_x, camera_y-0.7, 'High-Resolution\nCamera', ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Draw test section with hot air plume
    flame_x = np.linspace(test_x-0.8, test_x+0.8, 30)
    flame_y = test_y + 0.5 * np.sin(8*flame_x) * np.exp(-2*(flame_x-test_x)**2/0.5)
    ax.fill_between(flame_x, test_y-0.3, flame_y, alpha=0.3, color='red')
    ax.plot(flame_x, flame_y, 'r-', linewidth=2)
    
    # Add some turbulent flow lines
    for i in range(5):
        y_offset = test_y + (i-2) * 0.1
        flow_x = np.linspace(test_x-0.5, test_x+0.5, 20)
        flow_y = y_offset + 0.05 * np.sin(15*flow_x + i) * np.exp(-(flow_x-test_x)**2/0.3)
        ax.plot(flow_x, flow_y, 'r-', alpha=0.3, linewidth=1)
    
    ax.text(test_x, test_y-1, 'Test Section\n(Flow with Density Gradients)', 
            ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Draw background pattern
    background = patches.Rectangle((background_x-0.1, background_y-1.5), 0.2, 3, 
                                  facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(background)
    
    # Add random dot pattern to background
    np.random.seed(42)  # For reproducible pattern
    n_dots = 50
    dot_x = np.random.uniform(background_x-0.08, background_x+0.08, n_dots)
    dot_y = np.random.uniform(background_y-1.4, background_y+1.4, n_dots)
    ax.scatter(dot_x, dot_y, c='black', s=3, alpha=0.8)
    
    ax.text(background_x, background_y-2, 'Background Pattern\n(Random Dots/Grid)', 
            ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Draw light rays showing deflection
    # Straight rays (no flow)
    for i in range(5):
        y_start = background_y + (i-2) * 0.4
        ax.plot([background_x-0.1, camera_x+0.4], [y_start, camera_y], 
                'gray', linewidth=1, alpha=0.3, linestyle='--')
    
    # Deflected rays (with flow)
    for i in range(5):
        y_start = background_y + (i-2) * 0.4
        # Add some deflection in the middle
        mid_x = (background_x + camera_x) / 2
        deflection = 0.1 * np.sin(i * np.pi / 2) if abs(i-2) <= 1 else 0
        
        ax.plot([background_x-0.1, mid_x], [y_start, camera_y + deflection], 
                'blue', linewidth=1.5, alpha=0.7)
        ax.plot([mid_x, camera_x+0.4], [camera_y + deflection, camera_y], 
                'blue', linewidth=1.5, alpha=0.7)
    
    # Add viewing direction arrow
    ax.arrow(camera_x+0.6, camera_y, 2, 0, head_width=0.1, head_length=0.1, 
             fc='green', ec='green', linewidth=2)
    ax.text(camera_x+1.5, camera_y+0.3, 'Viewing Direction', ha='center', va='bottom', 
            fontsize=9, color='green')
    
    # Add displacement vectors illustration
    ax.text(7, 5.5, 'Pattern Displacement Analysis', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='purple')
    
    # Show a few displacement vectors
    for i in range(3):
        x_pos = test_x + (i-1) * 0.3
        y_pos = test_y + 0.2
        dx = 0.1 * (i-1)
        dy = 0.05 * np.sin(i * np.pi)
        ax.arrow(x_pos, y_pos, dx, dy, head_width=0.05, head_length=0.03, 
                fc='purple', ec='purple', alpha=0.7)
    
    ax.text(test_x, test_y+0.8, 'Displacement\nVectors', ha='center', va='center', 
            fontsize=8, color='purple')
    
    # Add title
    ax.text(6, 6.5, 'Background Oriented Schlieren (BOS) System', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Add process flow
    process_text = [
        "1. Reference image (no flow)",
        "2. Test image (with flow)", 
        "3. Cross-correlation analysis",
        "4. Displacement field calculation",
        "5. Density gradient reconstruction"
    ]
    
    for i, text in enumerate(process_text):
        ax.text(1, 1.8 - i*0.3, text, ha='left', va='center', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.7))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def create_comparison_table():
    """Create Figure 5: Comparison Table of Schlieren Methods"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    
    # Data for comparison table
    methods = ['Classical (Toepler)', 'Rainbow Schlieren', 'Background Oriented (BOS)']
    features = [
        'Principle',
        'Cutoff Element', 
        'Optical Complexity',
        'Light Source',
        'Sensitivity',
        'Output',
        'Quantitative Analysis',
        'Alignment Difficulty',
        'Cost',
        'Best Applications'
    ]
    
    data = [
        ['Intensity modulation\nby knife-edge', 'Color modulation\nby multi-color filter', 'Background pattern\ndisplacement'],
        ['Knife-edge, slit,\nwire, graded filter', 'Color filter\n(strip or continuous)', 'No physical cutoff;\ncomputational analysis'],
        ['Two high-quality\nlenses/mirrors required', 'Two high-quality\nlenses/mirrors required', 'Simple: camera +\nbackground only'],
        ['Small, bright\n(point or slit)', 'White light,\noften slit source', 'Ambient or controlled\nillumination'],
        ['High; adjustable by\nknife-edge position', 'Moderate to High;\ndepends on filter', 'Moderate; depends on\npattern & algorithms'],
        ['Grayscale image\nshowing gradients', 'Color image; color\nindicates deflection', 'Displacement field,\nthen gradient field'],
        ['Primarily qualitative;\ncan be quantitative', 'Semi-quantitative\n(color ↔ deflection)', 'Highly quantitative\nwith proper processing'],
        ['Critical and\nchallenging', 'Critical and\nchallenging', 'Relatively easy\nalignment'],
        ['High due to\nquality optics', 'High due to\nquality optics', 'Lower optical cost,\nhigher computational'],
        ['Shock waves, ballistics,\nheat transfer, mixing', 'Similar to classical,\ngood for direction info', 'Large flows, aerodynamics,\nlimited optical access']
    ]
    
    # Create table
    n_methods = len(methods)
    n_features = len(features)
    
    # Set up grid
    cell_height = 0.8
    cell_width = 4.5
    
    # Draw table structure
    for i in range(n_features + 1):  # +1 for header
        y = (n_features - i) * cell_height
        ax.axhline(y=y, color='black', linewidth=1.5)
    
    for j in range(n_methods + 2):  # +2 for feature column and borders
        x = j * cell_width
        ax.axvline(x=x, color='black', linewidth=1.5)
    
    # Add headers
    ax.text(cell_width/2, (n_features + 0.5) * cell_height, 'Feature', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))
    
    colors = ['lightblue', 'lightgreen', 'lightyellow']
    for j, method in enumerate(methods):
        ax.text((j + 1.5) * cell_width, (n_features + 0.5) * cell_height, method, 
                ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[j]))
    
    # Add feature labels and data
    for i, feature in enumerate(features):
        y_pos = (n_features - i - 0.5) * cell_height
        
        # Feature label
        ax.text(cell_width/2, y_pos, feature, 
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Data for each method
        for j in range(n_methods):
            x_pos = (j + 1.5) * cell_width
            ax.text(x_pos, y_pos, data[i][j], 
                    ha='center', va='center', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=colors[j], alpha=0.3))
    
    ax.set_xlim(0, (n_methods + 1) * cell_width)
    ax.set_ylim(0, (n_features + 1) * cell_height)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add title
    ax.text((n_methods + 1) * cell_width / 2, (n_features + 1.3) * cell_height, 
            'Comparison of Schlieren Visualization Methods', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_all_figures():
    """Generate all Schlieren principle figures"""
    
    # Create all figures
    fig1 = create_light_deflection_principle()
    fig2 = create_classical_schlieren()
    fig3 = create_rainbow_schlieren()
    fig4 = create_bos_system()
    fig5 = create_comparison_table()
    
    # Save figures
    figures = [
        (fig1, 'schlieren_light_deflection_principle.png'),
        (fig2, 'classical_schlieren_system.png'),
        (fig3, 'rainbow_schlieren_system.png'),
        (fig4, 'bos_system.png'),
        (fig5, 'schlieren_methods_comparison.png')
    ]
    
    for fig, filename in figures:
        fig.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"Saved: {filename}")
    
    # Display all figures
    plt.show()
    
    return figures

# Additional utility function for creating a comprehensive summary figure
def create_schlieren_summary():
    """Create a comprehensive summary figure showing all principles"""
    fig = plt.figure(figsize=(20, 24))
    
    # Create subplots
    gs = fig.add_gridspec(4, 2, height_ratios=[1, 1, 1, 1.2], hspace=0.3, wspace=0.2)
    
    # Subplot 1: Light deflection principle
    ax1 = fig.add_subplot(gs[0, :])
    ax1.text(0.5, 0.9, 'A. Fundamental Principle: Light Deflection in Refractive Index Gradients', 
             transform=ax1.transAxes, ha='center', va='top', fontsize=14, fontweight='bold')
    
    # Simplified version of deflection principle
    scenarios = ['Uniform n₀', 'Hot air (n < n₀)', 'Dense region (n > n₀)']
    for i, scenario in enumerate(scenarios):
        y_base = 0.7 - i * 0.25
        x_start = 0.1
        
        # Incident ray
        ax1.arrow(x_start, y_base, 0.15, 0, transform=ax1.transAxes, 
                 head_width=0.01, head_length=0.01, fc='blue', ec='blue')
        ax1.text(x_start-0.02, y_base, scenario, transform=ax1.transAxes, 
                ha='right', va='center', fontsize=10)
        
        # Medium representation
        if i == 0:  # Uniform
            rect = patches.Rectangle((0.3, y_base-0.03), 0.2, 0.06, 
                                   transform=ax1.transAxes, facecolor='lightgray', alpha=0.5)
            ax1.add_patch(rect)
            # Straight ray
            ax1.arrow(0.5, y_base, 0.15, 0, transform=ax1.transAxes,
                     head_width=0.01, head_length=0.01, fc='blue', ec='blue')
        elif i == 1:  # Hot air
            # Curved region
            theta = np.linspace(0, np.pi, 20)
            x_curve = 0.4 + 0.1 * np.cos(theta)
            y_curve = y_base + 0.05 * np.sin(theta)
            ax1.fill_between(x_curve, y_base-0.02, y_curve, alpha=0.3, color='red')
            # Deflected upward
            ax1.arrow(0.5, y_base, 0.12, 0.05, transform=ax1.transAxes,
                     head_width=0.01, head_length=0.01, fc='blue', ec='blue')
        else:  # Dense
            rect = patches.Rectangle((0.3, y_base-0.04), 0.2, 0.08, 
                                   transform=ax1.transAxes, facecolor='lightblue', alpha=0.7)
            ax1.add_patch(rect)
            # Deflected downward
            ax1.arrow(0.5, y_base, 0.12, -0.05, transform=ax1.transAxes,
                     head_width=0.01, head_length=0.01, fc='blue', ec='blue')
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    
    # Subplot 2: Classical Schlieren
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.text(0.5, 0.95, 'B. Classical (Toepler) Schlieren', 
             transform=ax2.transAxes, ha='center', va='top', fontsize=12, fontweight='bold')
    
    # Simplified schematic
    components = ['S', 'L1', 'Test', 'L2', 'K', 'I']
    positions = np.linspace(0.1, 0.9, len(components))
    
    for i, (pos, comp) in enumerate(zip(positions, components)):
        if comp == 'K':  # Knife edge
            ax2.add_patch(patches.Rectangle((pos-0.01, 0.45), 0.02, 0.1, 
                                          transform=ax2.transAxes, facecolor='black'))
        elif comp in ['L1', 'L2']:  # Lenses
            ax2.add_patch(patches.Ellipse((pos, 0.5), 0.03, 0.2, 
                                        transform=ax2.transAxes, facecolor='lightblue'))
        elif comp == 'S':  # Source
            ax2.add_patch(Circle((pos, 0.5), 0.02, transform=ax2.transAxes, 
                               facecolor='yellow'))
        elif comp == 'Test':  # Test section
            # Flame shape
            flame_y = np.array([0.45, 0.6, 0.55, 0.45])
            flame_x = np.array([pos-0.02, pos, pos, pos+0.02])
            ax2.fill(flame_x, flame_y, transform=ax2.transAxes, color='red', alpha=0.3)
        else:  # Screen
            ax2.add_patch(patches.Rectangle((pos-0.01, 0.4), 0.02, 0.2, 
                                          transform=ax2.transAxes, facecolor='white', 
                                          edgecolor='black'))
        
        ax2.text(pos, 0.3, comp, transform=ax2.transAxes, ha='center', va='top', fontsize=10)
    
    # Light rays
    ax2.plot([0.1, 0.9], [0.5, 0.5], 'b-', transform=ax2.transAxes, alpha=0.7)
    ax2.plot([0.4, 0.9], [0.52, 0.6], 'b--', transform=ax2.transAxes, alpha=0.5)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    
    # Subplot 3: Rainbow Schlieren
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.text(0.5, 0.95, 'C. Rainbow Schlieren', 
             transform=ax3.transAxes, ha='center', va='top', fontsize=12, fontweight='bold')
    
    # Similar to classical but with color filter
    for i, (pos, comp) in enumerate(zip(positions, components)):
        if comp == 'K':  # Color filter instead of knife edge
            colors = ['red', 'green', 'blue']
            for j, color in enumerate(colors):
                ax3.add_patch(patches.Rectangle((pos-0.01, 0.45 + j*0.03), 0.02, 0.03, 
                                              transform=ax3.transAxes, facecolor=color, alpha=0.7))
            ax3.text(pos, 0.3, 'Filter', transform=ax3.transAxes, ha='center', va='top', fontsize=10)
        elif comp in ['L1', 'L2']:
            ax3.add_patch(patches.Ellipse((pos, 0.5), 0.03, 0.2, 
                                        transform=ax3.transAxes, facecolor='lightblue'))
            ax3.text(pos, 0.3, comp, transform=ax3.transAxes, ha='center', va='top', fontsize=10)
        elif comp == 'S':
            ax3.add_patch(patches.Rectangle((pos-0.015, 0.47), 0.03, 0.06, 
                                          transform=ax3.transAxes, facecolor='white', edgecolor='black'))
            ax3.text(pos, 0.3, 'White\nLight', transform=ax3.transAxes, ha='center', va='top', fontsize=8)
        elif comp == 'Test':
            flame_y = np.array([0.45, 0.6, 0.55, 0.45])
            flame_x = np.array([pos-0.02, pos, pos, pos+0.02])
            ax3.fill(flame_x, flame_y, transform=ax3.transAxes, color='red', alpha=0.3)
            ax3.text(pos, 0.3, comp, transform=ax3.transAxes, ha='center', va='top', fontsize=10)
        elif comp == 'I':
            ax3.add_patch(patches.Rectangle((pos-0.01, 0.4), 0.02, 0.2, 
                                          transform=ax3.transAxes, facecolor='white', edgecolor='black'))
            ax3.text(pos, 0.3, comp, transform=ax3.transAxes, ha='center', va='top', fontsize=10)
    
    # Colored light rays
    ax3.plot([0.4, 0.9], [0.5, 0.5], 'green', transform=ax3.transAxes, linewidth=2)
    ax3.plot([0.4, 0.9], [0.52, 0.58], 'blue', transform=ax3.transAxes, linewidth=2)
    ax3.plot([0.4, 0.9], [0.48, 0.42], 'red', transform=ax3.transAxes, linewidth=2)
    
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    
    # Subplot 4: BOS
    ax4 = fig.add_subplot(gs[2, :])
    ax4.text(0.5, 0.95, 'D. Background Oriented Schlieren (BOS)', 
             transform=ax4.transAxes, ha='center', va='top', fontsize=12, fontweight='bold')
    
    # Camera
    ax4.add_patch(patches.Rectangle((0.1, 0.45), 0.05, 0.1, 
                                  transform=ax4.transAxes, facecolor='black'))
    ax4.text(0.125, 0.3, 'Camera', transform=ax4.transAxes, ha='center', va='top', fontsize=10)
    
    # Test section
    flame_y = np.array([0.4, 0.7, 0.6, 0.4])
    flame_x = np.array([0.35, 0.5, 0.5, 0.65])
    ax4.fill(flame_x, flame_y, transform=ax4.transAxes, color='red', alpha=0.3)
    ax4.text(0.5, 0.3, 'Flow', transform=ax4.transAxes, ha='center', va='top', fontsize=10)
    
    # Background pattern
    ax4.add_patch(patches.Rectangle((0.85, 0.2), 0.05, 0.6, 
                                  transform=ax4.transAxes, facecolor='white', edgecolor='black'))
    # Add dots to background
    np.random.seed(42)
    dot_x = 0.875 + 0.02 * (np.random.random(20) - 0.5)
    dot_y = 0.5 + 0.25 * (np.random.random(20) - 0.5)
    ax4.scatter(dot_x, dot_y, transform=ax4.transAxes, c='black', s=2)
    ax4.text(0.875, 0.15, 'Background\nPattern', transform=ax4.transAxes, ha='center', va='top', fontsize=10)
    
    # Light rays (some deflected)
    for i in range(5):
        y_start = 0.3 + i * 0.1
        y_mid = y_start + 0.02 * np.sin(i * np.pi / 2) if i in [1, 2, 3] else y_start
        ax4.plot([0.85, 0.5], [y_start, y_mid], 'gray', transform=ax4.transAxes, alpha=0.5)
        ax4.plot([0.5, 0.15], [y_mid, 0.5], 'blue', transform=ax4.transAxes, alpha=0.7)
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    
    # Subplot 5: Applications summary
    ax5 = fig.add_subplot(gs[3, :])
    ax5.text(0.5, 0.95, 'E. Applications and Comparison', 
             transform=ax5.transAxes, ha='center', va='top', fontsize=12, fontweight='bold')
    
    # Create mini comparison
    methods = ['Classical\n(Toepler)', 'Rainbow\nSchlieren', 'BOS']
    features = ['High sensitivity', 'Color-coded direction', 'Quantitative analysis']
    applications = ['Shock waves\nBallistics', 'Flow direction\nvisualization', 'Large scale flows\nAerodynamics']
    
    for i, (method, feature, app) in enumerate(zip(methods, features, applications)):
        x_pos = 0.15 + i * 0.3
        
        # Method box
        ax5.add_patch(patches.FancyBboxPatch((x_pos-0.08, 0.7), 0.16, 0.15,
                                           transform=ax5.transAxes, 
                                           boxstyle="round,pad=0.02",
                                           facecolor=['lightblue', 'lightgreen', 'lightyellow'][i],
                                           edgecolor='black'))
        ax5.text(x_pos, 0.775, method, transform=ax5.transAxes, ha='center', va='center', 
                fontsize=10, fontweight='bold')
        
        # Feature
        ax5.text(x_pos, 0.6, feature, transform=ax5.transAxes, ha='center', va='center', 
                fontsize=9, style='italic')
        
        # Applications
        ax5.text(x_pos, 0.4, app, transform=ax5.transAxes, ha='center', va='center', 
                fontsize=9)
        
        # Arrow connecting
        ax5.arrow(x_pos, 0.65, 0, -0.15, transform=ax5.transAxes,
                 head_width=0.02, head_length=0.02, fc='gray', ec='gray', alpha=0.7)
    
    # Add key principle box
    ax5.add_patch(patches.FancyBboxPatch((0.1, 0.05), 0.8, 0.15,
                                       transform=ax5.transAxes, 
                                       boxstyle="round,pad=0.02",
                                       facecolor='lightcyan',
                                       edgecolor='navy', linewidth=2))
    ax5.text(0.5, 0.125, 'Key Principle: All Schlieren methods visualize refractive index gradients (∇n)\n' +
                         'caused by density, temperature, or pressure variations in transparent media',
             transform=ax5.transAxes, ha='center', va='center', 
             fontsize=11, fontweight='bold', color='navy')
    
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    
    plt.suptitle('Schlieren Visualization Principles: Complete Overview', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    return fig

# Main execution
if __name__ == "__main__":
    print("Generating professional Schlieren visualization figures...")
    
    # Create individual figures
    figures = create_all_figures()
    
    # Create comprehensive summary
    summary_fig = create_schlieren_summary()
    summary_fig.savefig('schlieren_complete_overview.png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    print("Saved: schlieren_complete_overview.png")
    
    print("\nAll figures generated successfully!")
    print("\nGenerated files:")
    print("1. schlieren_light_deflection_principle.png - Basic light bending principles")
    print("2. classical_schlieren_system.png - Traditional Toepler setup")  
    print("3. rainbow_schlieren_system.png - Color-coded visualization")
    print("4. bos_system.png - Background Oriented Schlieren")
    print("5. schlieren_methods_comparison.png - Detailed comparison table")
    print("6. schlieren_complete_overview.png - Comprehensive summary figure")
    
    plt.show()