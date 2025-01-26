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

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from io import BytesIO

# Function to create the gauge chart
def create_gauge_chart(project_name, donated_amount, target_amount):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})  # Enlarged chart size

    # Validate that the target amount is greater than 0
    if target_amount <= 0:
        st.error("Target amount must be greater than 0.")
        return None

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
    ax.plot([0, np.cos(np.radians(needle_angle))], [0, np.sin(np.radians(needle_angle))], color='black', lw=2)

    # Draw the pivot
    pivot_circle = plt.Circle((0, 0), 0.05, color='black', zorder=5)
    ax.add_artist(pivot_circle)

    # Adjust text annotations to move them closer to the chart
    ax.text(-1, -0.15, f'Donated: ${donated_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
    ax.text(1, -0.15, f'Target: ${target_amount:,.2f}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Display actual donation percentage in the "Progress" label, even if it exceeds 100%
    ax.text(0, -0.25, f'Progress: {actual_percentage * 100:.2f}%', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

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

# Function to save the chart as an image and prepare it for download
def get_chart_image(fig):
    # Save the figure to a BytesIO object
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png", dpi=300, transparent=True)
    img_buffer.seek(0)
    return img_buffer

# Streamlit app interface
def main():
    st.title("Donation Progress Chart")

    # Input fields for project name, donated amount, and target amount (set to empty by default)
    project_name = st.text_input("Enter the project name:")
    donated_amount = st.number_input("Enter the donated amount:", min_value=0.0, step=0.01)  # Empty by default
    target_amount = st.number_input("Enter the target amount:", min_value=0.0, step=0.01)  # Empty by default

    # Validate that the user has input values
    if project_name == "":
        st.error("Please enter the project name.")
    elif donated_amount < 0:
        st.error("Please enter a valid donated amount greater than or equal to 0.")
    elif target_amount <= 0:
        st.error("Please enter a valid target amount greater than 0.")
    else:
        # Create the gauge chart
        fig = create_gauge_chart(project_name, donated_amount, target_amount)

        if fig is not None:
            # Display the chart in the Streamlit app
            st.pyplot(fig)

            # Generate the image for download
            img_buffer = get_chart_image(fig)

            # Provide a download button for the image
            st.download_button(
                label="Download Chart Image",
                data=img_buffer,
                file_name=f"{project_name}_progress_chart.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()

