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
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from io import BytesIO
from matplotlib.animation import FuncAnimation

# Function to create the gauge chart (static frame)
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

    # Draw the needle, synced with the actual donation percentage
    needle_angle = start_angle - (min(actual_percentage, 1.0) * 180)  # Capped at 100% visually

    # Reduce the length of the needle by scaling it (0.7 means 70% of the full length)
    needle_length = 0.91  # Scaling factor for needle length
    
    # Add a gradient effect to the needle (using a darker tone at the bottom for depth)
    ax.plot([0, needle_length * np.cos(np.radians(needle_angle))], 
            [0, needle_length * np.sin(np.radians(needle_angle))], 
            color='#00bfae', lw=6, solid_capstyle='round', zorder=3)  # Thick green needle with smooth edges

    # Add shadow for the needle to give it a 3D effect
    ax.plot([0, needle_length * np.cos(np.radians(needle_angle + 2))], 
            [0, needle_length * np.sin(np.radians(needle_angle + 2))], 
            color='gray', lw=6, alpha=0.3, solid_capstyle='round', zorder=2)  # Subtle shadow to make it look 3D

    # Draw the pivot (center circle) with more aesthetics (glow effect)
    pivot_circle = plt.Circle((0, 0), 0.05, color='black', zorder=5)
    ax.add_artist(pivot_circle)

    # Adjust text annotations to move them closer to the chart
    ax.text(-1, -0.15, f'Donated: ${donated_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
    ax.text(1, -0.15, f'Target: ${target_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Display actual donation percentage in the "Progress" label, even if it exceeds 100%
    ax.text(0, -0.25, f'Progress: {round(actual_percentage * 100, 1)}%', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Add current amount donated as of current date, split the text to avoid crowding
    current_date = datetime.now().strftime("%b, %Y")

    # Separate the labels to avoid crowding
    ax.text(0, -0.35, f'${donated_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Add some space between the "out of" label and the amounts
    ax.text(0, -0.45, 'out of', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Increase space between "out of" and target amount
    ax.text(0, -0.55, f'${target_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Add the date on the next line to prevent overlap
    ax.text(0, -0.65, f'Donated as of {current_date}', horizontalalignment='center', fontsize=12, fontweight='bold', color='black')

    # Add project name as title (removed 'progress' from title)
    plt.title(f'{project_name}', fontsize=16, fontweight='bold', pad=20, ha='center')  # Title now just the project name

    # Set the aspect ratio and hide axes
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    return fig

# Function to create animation (save as gif or video)
def create_animation(project_name, donated_amount, target_amount):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})  # Enlarged chart size

    # Calculate the actual percentage of the donated amount
    actual_percentage = donated_amount / target_amount  # Actual percentage based on donation

    # Draw the gauge background (red arc)
    start_angle = 180
    end_angle = start_angle - 180
    theta = np.linspace(start_angle, end_angle, 100)
    ax.plot(np.cos(np.radians(theta)), np.sin(np.radians(theta)), color='red', lw=30)

    # Draw the needle, synced with the actual donation percentage
    needle_length = 0.91  # Scaling factor for needle length
    
    # Animation update function
    def update(frame):
        ax.clear()
        # Redraw the background
        ax.plot(np.cos(np.radians(theta)), np.sin(np.radians(theta)), color='red', lw=30)
        # Update the needle position
        needle_angle = start_angle - (min(frame / 100.0, 1.0) * 180)
        ax.plot([0, needle_length * np.cos(np.radians(needle_angle))], 
                [0, needle_length * np.sin(np.radians(needle_angle))], 
                color='#00bfae', lw=6, solid_capstyle='round', zorder=3)

        # Add text and labels (same as in the static chart)
        ax.text(-1, -0.15, f'Donated: ${donated_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
        ax.text(1, -0.15, f'Target: ${target_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
        ax.text(0, -0.25, f'Progress: {round(frame, 1)}%', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

        # More text and labels...
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
    
    ani = FuncAnimation(fig, update, frames=np.linspace(0, actual_percentage * 100, 100), interval=50)
    
    # Save the animation as gif or video (optional)
    ani.save(f'{project_name}_donation_progress.gif', writer='imagemagick', fps=30)
    
    return ani

# Streamlit app interface
def main():
    st.markdown("<h2 style='text-align: center;'>Project Donation Tracker</h2>", unsafe_allow_html=True)

    # Input fields stacked vertically
    project_name = st.text_input("Enter the project name:")
    donated_amount = st.number_input("Enter the donated amount:", min_value=0.0, step=0.01)
    target_amount = st.number_input("Enter the target amount:", min_value=0.0, step=0.01)

    # Validation for target_amount
    if target_amount == 0.0:
        st.warning("Target amount cannot be zero!")

    # Generate chart button
    if st.button("Generate Chart"):
        if project_name and donated_amount > 0.0 and target_amount > 0.0:
            # Generate the static final frame
            fig = create_gauge_chart(project_name, donated_amount, target_amount)

            # Display the chart in the Streamlit app
            st.pyplot(fig)

            # Generate the image for download
            img_buffer = get_chart_image(fig)

            # Remove the "Donated as of" text and directly place the download button below the chart
            st.download_button(
                label="Download Chart Image",
                data=img_buffer,
                file_name=f"{project_name}_progress_chart.png",
                mime="image/png"
            )

            # Optionally, generate and save animation (this will generate a gif)
            create_animation(project_name, donated_amount, target_amount)
            st.success("Animation generated! Check the output folder for the gif.")
        else:
            st.warning("Please ensure that all fields are filled out correctly.")

if __name__ == "__main__":
    main()
