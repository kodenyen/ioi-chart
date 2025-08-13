import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import textwrap
import matplotlib.font_manager as fm

def create_gauge_chart(project_name, donated_amount, target_amount):
    # Set up figure with safe font fallbacks
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']  # Default serif that exists everywhere
    plt.rcParams['font.weight'] = 'bold'
    
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})

    # Calculate percentages
    actual_percentage = donated_amount / target_amount if target_amount > 0 else 0
    visual_percentage = min(actual_percentage, 1.0)

    # Draw gauge background (red arc)
    start_angle = 180
    end_angle = start_angle - 180
    theta = np.linspace(start_angle, end_angle, 100)
    ax.plot(np.cos(np.radians(theta)), np.sin(np.radians(theta)), color='red', lw=30)

    # Draw progress (green arc)
    progress_end_angle = start_angle - (visual_percentage * 180)
    theta_progress = np.linspace(start_angle, progress_end_angle, 100)
    ax.plot(np.cos(np.radians(theta_progress)), np.sin(np.radians(theta_progress)), color='green', lw=30)

    # Needle positioning
    if donated_amount == 0:
        needle_angle = start_angle + (0.03 * 180)
    else:
        if actual_percentage == 0.5:
            needle_angle = start_angle - 90
        else:
            needle_angle = progress_end_angle - 4.7

    # Draw needle
    needle_length = 0.92
    needle_width = 0.06
    needle_tip = (
        needle_length * np.cos(np.radians(needle_angle)),
        needle_length * np.sin(np.radians(needle_angle))
    )
    needle_base_left = (
        needle_width * np.cos(np.radians(needle_angle + 90)),
        needle_width * np.sin(np.radians(needle_angle + 90))
    )
    needle_base_right = (
        needle_width * np.cos(np.radians(needle_angle - 90)),
        needle_width * np.sin(np.radians(needle_angle - 90))
    )
    
    needle = plt.Polygon(
        [needle_tip, needle_base_left, needle_base_right],
        closed=True, color='black', zorder=3
    )
    ax.add_patch(needle)

    # Draw pivot
    pivot_circle = plt.Circle((0, 0), 0.06, color='black', zorder=5)
    ax.add_artist(pivot_circle)
    inner_circle = plt.Circle((0, 0), 0.03, color='white', zorder=6)
    ax.add_artist(inner_circle)

    # Draw needle base
    base_radius = 0.02
    base_angle = np.linspace(needle_angle - 90, needle_angle + 90, 100)
    base_x = base_radius * np.cos(np.radians(base_angle))
    base_y = base_radius * np.sin(np.radians(base_angle))
    ax.plot(base_x, base_y, color='black', lw=2, zorder=4)

    # Format amounts
    donated_amount_formatted = f"{donated_amount:,}"
    target_amount_formatted = f"{target_amount:,}"

    # Text labels
    ax.text(-1, -0.25, f'Donated: ${donated_amount_formatted}', 
            horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
    ax.text(1, -0.25, f'Target: ${target_amount_formatted}', 
            horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    progress_percentage = round(actual_percentage * 100)
    ax.text(0, -0.4, f'Progress: {progress_percentage}%', 
            horizontalalignment='center', fontsize=26, fontweight='bold', color='black')

    # Project title
    wrapped_project_name = textwrap.fill(project_name, width=20)
    plt.title(wrapped_project_name, fontsize=30, fontweight='bold', 
             pad=20, ha='center', va='center', multialignment='center')

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    return fig

def get_chart_image(fig):
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png", dpi=300, transparent=True)
    img_buffer.seek(0)
    return img_buffer

def main():
    st.set_page_config(layout="wide")  # Ensure proper page setup
    
    st.markdown("""
        <style>
            /* Use web-safe serif font */
            * {
                font-family: Georgia, serif !important;
            }
            
            /* Input styling */
            .stTextInput > div > input, .stNumberInput > div > input {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border: 2px solid #333333;
                background-color: #e6f7ff;
                color: #333333;
            }
            .stButton button {
                background-color: #00bfae;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
                margin-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Project Donation Tracker")

    with st.form("input_form"):
        project_name = st.text_input("Enter the project name:")
        donated_amount = st.number_input("Enter the donated amount:", min_value=0, step=1)
        target_amount = st.number_input("Enter the target amount:", min_value=1, step=1, value=100)
        
        if st.form_submit_button("Generate Chart"):
            if project_name:
                try:
                    fig = create_gauge_chart(project_name, donated_amount, target_amount)
                    st.pyplot(fig)
                    
                    img_buffer = get_chart_image(fig)
                    st.download_button(
                        label="Download Chart Image",
                        data=img_buffer,
                        file_name=f"{project_name}_progress_chart.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Error generating chart: {str(e)}")
            else:
                st.warning("Please enter a project name")

if __name__ == "__main__":
    main()
