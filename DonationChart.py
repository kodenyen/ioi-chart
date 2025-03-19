import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import textwrap  # Import textwrap for multiline text

# Function to create the gauge chart with a black triangular needle, curved base, and needle 10% ahead
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
    # If donated_amount is 0, reduce the needle angle by 18% to point to the very beginning
    if donated_amount == 0:
        needle_angle = start_angle + (0.02 * 180)  # Add 18% of 180 degrees to start_angle
    else:
        # Adjust needle angle to point exactly at the center when progress is 50%
        if actual_percentage == 0.5:
             progress_end_angle=progress_end_angle-90
    
            needle_angle = start_angle - 90  # Exactly at the center (vertical)
        
        
            
        else:
            needle_angle = progress_end_angle - 4.7  # Adjust needle to be 10% ahead

    # Define the triangular needle shape
    needle_length = 0.92  # Length of the needle
    needle_width = 0.06  # Width of the needle at its base

    # Coordinates for the triangular needle
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

    # Draw the triangular needle (black color)
    needle = plt.Polygon(
        [needle_tip, needle_base_left, needle_base_right],
        closed=True, color='black', zorder=3
    )
    ax.add_patch(needle)

    # Draw the pivot (center circle) with more aesthetics
    pivot_circle = plt.Circle((0, 0), 0.06, color='black', zorder=5)
    ax.add_artist(pivot_circle)

    # Add a smaller inner circle for a more defined pivot
    inner_circle = plt.Circle((0, 0), 0.03, color='white', zorder=6)
    ax.add_artist(inner_circle)

    # Add a curved base for the needle (semi-circle at the base)
    base_radius = 0.02  # Radius of the curved base
    base_angle = np.linspace(needle_angle - 90, needle_angle + 90, 100)  # 180-degree arc
    base_x = base_radius * np.cos(np.radians(base_angle))
    base_y = base_radius * np.sin(np.radians(base_angle))
    ax.plot(base_x, base_y, color='black', lw=2, zorder=4)

    # Format donated and target amounts with commas as thousand separators
    donated_amount_formatted = f"{donated_amount:,}"
    target_amount_formatted = f"{target_amount:,}"

    # Adjust text annotations to move them closer to the chart
    ax.text(-1, -0.15, f'Donated: ${donated_amount_formatted}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')
    ax.text(1, -0.15, f'Target: ${target_amount_formatted}', horizontalalignment='center', fontsize=14, fontweight='bold', color='black')

    # Display actual donation percentage in the "Progress" label, rounded to a single digit (without decimals)
    progress_percentage = round(actual_percentage * 100)  # Round the progress percentage to the nearest 1 decimal place
    ax.text(0, -0.35, f'Progress: {progress_percentage}%', horizontalalignment='center', fontsize=26, fontweight='bold', color='black')

    # Add project name as title with multiline support
    wrapped_project_name = textwrap.fill(project_name, width=20)  # Wrap text to 20 characters per line
    plt.title(wrapped_project_name, fontsize=30, fontweight='bold', pad=20, ha='center', va='center', multialignment='center')  # Centered multiline title

    # Set the aspect ratio and hide axes
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    return fig

# Function to save the chart as an image and prepare it for download
def get_chart_image(fig):
    # Save the figure to a BytesIO object with a transparent background
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png", dpi=300, transparent=True)  # transparent=True ensures a transparent background
    img_buffer.seek(0)
    return img_buffer

# Streamlit app interface
def main():
    # Inject custom CSS for borders, background, and input box colors
    st.markdown("""
        <style>
            /* Styling for the input fields */
            .stTextInput > div > input, .stNumberInput > div > input {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border: 2px solid #333333;  /* Darker border */
                background-color: #e6f7ff;  /* Light blue background */
                color: #333333;  /* Dark text */
            }
            .stTextInput label, .stNumberInput label {
                font-weight: bold;
                color: #333333;  /* Dark label text */
            }

            /* Styling for the container with light-dark background and thick green border */
            .input-container {
                border: 5px solid #006400;  /* Thick green border */
                padding: 20px;
                background-color: #d3d3d3;  /* Light dark background */
                border-radius: 10px;
            }

            /* Styling for the button */
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

            /* Styling the inputs inside the container */
            .stTextInput > div, .stNumberInput > div {
                margin-bottom: 20px;
            }

            /* Adding a subtle shadow effect to input boxes */
            .stTextInput > div, .stNumberInput > div {
                border: 2px solid #0099cc;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h2 style='text-align: center;'>Project Donation Tracker</h2>", unsafe_allow_html=True)

    # Input fields stacked vertically
    project_name = st.text_input("Enter the project name:")
    donated_amount = st.number_input("Enter the donated amount:", min_value=0, step=1)
    target_amount = st.number_input("Enter the target amount:", min_value=0, step=1)

    # Validation for target_amount
    if target_amount == 0:
        st.warning("Target amount cannot be zero!")

    # Generate chart button
    if st.button("Generate Chart"):
        if project_name and target_amount > 0:  # Allow donated_amount to be 0
            # Create the gauge chart
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
        else:
            st.warning("Please ensure that all fields are filled out correctly.")

if __name__ == "__main__":
    main()
