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

# Function to create the gauge chart with enhanced aesthetic needle
def create_gauge_chart(project_name, donated_amount, target_amount):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})  # Enlarged chart size

    actual_percentage = donated_amount / target_amount  # Calculate donation progress
    visual_percentage = min(actual_percentage, 1.0)  # Cap the visual percentage to 100%

    # Draw the gauge background (red arc)
    start_angle = 180
    end_angle = start_angle - 180
    theta = np.linspace(start_angle, end_angle, 100)
    ax.plot(np.cos(np.radians(theta)), np.sin(np.radians(theta)), color='red', lw=30)

    # Draw the donation progress (green arc)
    progress_end_angle = start_angle - (visual_percentage * 180)
    theta_progress = np.linspace(start_angle, progress_end_angle, 100)
    ax.plot(np.cos(np.radians(theta_progress)), np.sin(np.radians(theta_progress)), color='green', lw=30)

    # Enhanced Needle Styling
    needle_angle = progress_end_angle - 3  # Adjust needle position
    needle_length = 0.9  # Scaling factor for needle length

    # Create a gradient-like needle effect
    ax.plot([0, needle_length * np.cos(np.radians(needle_angle))], 
            [0, needle_length * np.sin(np.radians(needle_angle))], 
            color='#00bfae', lw=10, solid_capstyle='round', zorder=3, alpha=0.8)  # Thicker with transparency

    ax.plot([0, (needle_length - 0.05) * np.cos(np.radians(needle_angle))], 
            [0, (needle_length - 0.05) * np.sin(np.radians(needle_angle))], 
            color='black', lw=5, solid_capstyle='round', zorder=4)  # Inner black core for contrast

    # Enhanced Pivot Circle (Metallic look with shadow effect)
    pivot_circle_outer = plt.Circle((0, 0), 0.06, color='gray', zorder=5)
    pivot_circle_inner = plt.Circle((0, 0), 0.03, color='black', zorder=6)
    ax.add_artist(pivot_circle_outer)
    ax.add_artist(pivot_circle_inner)

    # Text Display
    progress_percentage = round(actual_percentage * 100)  # Convert progress to percentage
    ax.text(0, -0.35, f'Progress: {progress_percentage}%', horizontalalignment='center', fontsize=26, fontweight='bold', color='black')
    plt.title(f'{project_name}', fontsize=30, fontweight='bold', pad=20, ha='center')

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    return fig

# Streamlit App
def main():
    st.markdown("""
        <style>
            .stTextInput > div > input, .stNumberInput > div > input {
                width: 100%;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #333;
                background-color: #e6f7ff;
                color: #333;
            }
            .stButton button {
                background-color: #00bfae;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
            }
            .stButton button:hover {
                background-color: #009b83;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center;'>Project Donation Tracker</h2>", unsafe_allow_html=True)
    project_name = st.text_input("Enter the project name:")
    donated_amount = st.number_input("Enter the donated amount:", min_value=0, step=1)
    target_amount = st.number_input("Enter the target amount:", min_value=0, step=1)

    if target_amount == 0:
        st.warning("Target amount cannot be zero!")
    
    if st.button("Generate Chart"):
        if project_name and donated_amount > 0 and target_amount > 0:
            fig = create_gauge_chart(project_name, donated_amount, target_amount)
            st.pyplot(fig)
        else:
            st.warning("Please ensure all fields are filled correctly.")

if __name__ == "__main__":
    main()







