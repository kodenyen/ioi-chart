import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import textwrap

def create_gauge_chart(project_name, donated_amount, target_amount):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})
    
    # Set Garamond font for matplotlib
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Garamond']
    
    actual_percentage = donated_amount / target_amount
    visual_percentage = min(actual_percentage, 1.0)

    # Rest of your existing gauge chart code...
    # [All the existing gauge chart implementation remains the same]
    
    return fig

def get_chart_image(fig):
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png", dpi=300, transparent=True)
    img_buffer.seek(0)
    return img_buffer

def main():
    st.markdown("""
        <style>
            /* Garamond font for all elements */
            body, .stTextInput > div > input, .stNumberInput > div > input,
            .stTextInput label, .stNumberInput label, h2, .stButton button {
                font-family: "Garamond", serif !important;
            }
            
            /* Your existing CSS remains the same */
            .stTextInput > div > input, .stNumberInput > div > input {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border: 2px solid #333333;
                background-color: #e6f7ff;
                color: #333333;
            }
            /* ... rest of your existing CSS ... */
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center;'>Project Donation Tracker</h2>", unsafe_allow_html=True)
    
    # Rest of your existing Streamlit implementation...
    # [All the existing Streamlit code remains the same]

if __name__ == "__main__":
    main()
