#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IOI
#
# Created:     22/01/2025
# Copyright:   (c) IOI 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass
def create_gauge_chart(project_name, donated_amount, target_amount):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})  # Enlarged chart size

    # Calculate the actual percentage of the donated amount
    actual_percentage = donated_amount / target_amount  # Actual percentage based on donation
    visual_percentage = min(actual_percentage, 1.0)  # Clamp visual percentage to 100% for progress and needle

    # Draw the gauge background (red arc)
    start_angle = 180
    end_angle = start_angle - 180
    theta = np.linspace(start_angle, end_angle, 100)
    ax.plot(np.cos(np.radians(theta)), np.sin(np.radians(theta)), color='red', lw=30)

    # Draw the donation progress (green arc), stop at 100% visually
    progress_end_angle = start_angle - (visual_percentage * 180)  # Capped to 100% visually
    theta_progress = np.linspace(start_angle, progress_end_angle, 100)
    ax.plot(np.cos(np.radians(theta_progress)), np.sin(np.radians(theta_progress)), color='green', lw=30)

    # Move the needle 10% ahead of the green progress
    needle_angle = progress_end_angle - 4.3  # Adjust needle to be 18 degrees ahead

    # Reduce the length of the needle by scaling it (0.7 means 70% of the full length)
    needle_length = 0.91  # Scaling factor for needle length
    
    # Add a gradient effect to the needle (using a darker tone at the bottom for depth)
    ax.plot([0, needle_length * np.cos(np.radians(needle_angle))], 
            [0, needle_length * np.sin(np.radians(needle_angle))], 
            color='#00bfae', lw=6, solid_capstyle='round', zorder=3)  # Thick green needle with smooth edges

    # Draw the pivot (center circle) with more aesthetics (glow effect)
    pivot_circle = plt.Circle((0, 0), 0.05, color='black', zorder=5)
    ax.add_artist(pivot_circle)

    # Adjust text annotations to move them closer to the chart
    ax.text(-1, -0.15, f'Donated: ${donated_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
    ax.text(1, -0.15, f'Target: ${target_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Display actual donation percentage in the "Progress" label, rounded to a single digit (without decimals)
    progress_percentage = round(actual_percentage * 100)  # Round the progress percentage to the nearest integer
    ax.text(0, -0.25, f'Progress: {progress_percentage}%', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Add current amount donated as of current date, split the text to avoid crowding
    ax.text(0, -0.35, f'${donated_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Separate the labels to avoid crowding
    ax.text(0, -0.45, 'out of', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Increase space between "out of" and target amount
    ax.text(0, -0.55, f'${target_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Add project name as title (removed 'progress' from title)
    plt.title(f'{project_name}', fontsize=30, fontweight='bold', pad=20, ha='center')  # Title now just the project name

    # Set the aspect ratio and hide axes
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    return fig
