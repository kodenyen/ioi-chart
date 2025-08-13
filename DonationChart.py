import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import textwrap
from matplotlib import font_manager

def create_gauge_chart(project_name, donated_amount, target_amount):
    # Set up figure with proper dimensions
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100, subplot_kw={'aspect': 'equal'})
    
    # Try to load Garamond font
    try:
        # Attempt to find and load Garamond
        font_path = font_manager.findfont('Garamond')
        garamond = font_manager.FontProperties(fname=font_path)
        title_font = {'fontproperties': garamond, 'fontsize': 24, 'fontweight': 'bold'}
        label_font = {'fontproperties': garamond, 'fontsize': 14, 'fontweight': 'bold'}
        progress_font = {'fontproperties': garamond, 'fontsize': 20, 'fontweight': 'bold'}
    except:
        # Fallback to Times New Roman if Garamond not available
        title_font = {'fontfamily': 'serif', 'fontsize': 24, 'fontweight': 'bold'}
        label_font = {'fontfamily': 'serif', 'fontsize': 14, 'fontweight': 'bold'}
        progress_font = {'fontfamily': 'serif', 'fontsize': 20, 'fontweight': 'bold'}

    # Calculate percentages
    actual_percentage = donated_amount / target_amount if target_amount > 0 else 0
    visual_percentage = min(actual_percentage, 1.0)

    # Draw gauge arcs (same as before)
    start_angle = 180
    end_angle = 0
    theta = np.linspace(start_angle, end_angle, 100)
    r = 1.0
    
    # Background arc (red)
    ax.plot(r * np.cos(np.radians(theta)), 
            r * np.sin(np.radians(theta)), 
            color='red', lw=25, solid_capstyle='round')
    
    # Progress arc (green)
    progress_end = start_angle - (visual_percentage * 180)
    theta_progress = np.linspace(start_angle, progress_end, 100)
    ax.plot(r * np.cos(np.radians(theta_progress)), 
            r * np.sin(np.radians(theta_progress)), 
            color='green', lw=25, solid_capstyle='round')

    # Needle (same as before)
    needle_length = 0.9
    needle_width = 0.05
    if donated_amount == 0:
        needle_angle = start_angle + 5
    else:
        needle_angle = progress_end - 5 if actual_percentage != 0.5 else 90
    
    needle_tip = (needle_length * np.cos(np.radians(needle_angle)),
                 needle_length * np.sin(np.radians(needle_angle)))
    needle_base_left = (needle_width * np.cos(np.radians(needle_angle + 90)),
                       needle_width * np.sin(np.radians(needle_angle + 90)))
    needle_base_right = (needle_width * np.cos(np.radians(needle_angle - 90)),
                        needle_width * np.sin(np.radians(needle_angle - 90)))
    
    ax.add_patch(plt.Polygon([needle_tip, needle_base_left, needle_base_right],
                           closed=True, color='black', zorder=3))

    # Center circle
    ax.add_patch(plt.Circle((0, 0), 0.05, color='black', zorder=5))
    ax.add_patch(plt.Circle((0, 0), 0.025, color='white', zorder=6))

    # Add text labels with Garamond font
    ax.text(0, -1.3, f'Progress: {round(actual_percentage * 100)}%',
           ha='center', va='center', color='black', **progress_font)
    
    ax.text(-0.5, -1.1, f'Donated: ${donated_amount:,}',
           ha='center', va='center', color='black', **label_font)
    
    ax.text(0.5, -1.1, f'Target: ${target_amount:,}',
           ha='center', va='center', color='black', **label_font)

    # Add title with Garamond
    wrapped_title = '\n'.join(textwrap.wrap(project_name, width=20))
    ax.set_title(wrapped_title, pad=20, **title_font)

    # Set axis limits and turn off axes
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.axis('off')

    return fig

def main():
    st.set_page_config(layout="centered")
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;700&display=swap');
            
            /* Apply to Streamlit components */
            .stTextInput input, .stNumberInput input, 
            .stButton button, .stTitle, .stMarkdown {
                font-family: 'EB Garamond', serif !important;
            }
            
            .stApp {
                max-width: 900px;
                padding: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Donation Progress Tracker")
    
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", "Community Garden")
    with col2:
        target_amount = st.number_input("Target Amount ($)", min_value=100, value=10000)
    
    donated_amount = st.number_input("Donated Amount ($)", min_value=0, value=3500)
    
    if st.button("Generate Gauge Chart"):
        try:
            fig = create_gauge_chart(project_name, donated_amount, target_amount)
            st.pyplot(fig)
            
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=120)
            st.download_button(
                "Download Chart",
                buf.getvalue(),
                file_name="donation_progress.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"Error generating chart: {str(e)}")

if __name__ == "__main__":
    main()
