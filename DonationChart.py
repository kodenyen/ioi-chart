import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import textwrap
import matplotlib.font_manager as fm
from matplotlib import rcParams

def create_gauge_chart(project_name, donated_amount, target_amount):
    # Load Garamond font explicitly
    try:
        # Try to find Garamond in system fonts
        garamond_path = fm.findfont('Garamond')
        fm.fontManager.addfont(garamond_path)
        rcParams['font.family'] = 'serif'
        rcParams['font.serif'] = ['Garamond']
    except:
        # Fallback to Times New Roman if Garamond not found
        rcParams['font.family'] = 'serif'
        rcParams['font.serif'] = ['Times New Roman']
    
    rcParams['font.weight'] = 'bold'
    
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'aspect': 'equal'})

    # [Rest of your existing gauge chart code...]
    # Make sure all text elements include fontproperties
    ax.text(-1, -0.25, f'Donated: ${donated_amount:,}', 
            horizontalalignment='center', fontsize=14, 
            fontweight='bold', color='black',
            fontproperties=fm.FontProperties(family='serif', style='normal', weight='bold'))
    
    # [Include the same fontproperties in all other text elements]

def main():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;700&display=swap');
            
            /* Apply Garamond to all elements */
            * {
                font-family: 'EB Garamond', serif !important;
            }
            
            /* Your existing CSS... */
        </style>
    """, unsafe_allow_html=True)
    
    # [Rest of your existing code...]

if __name__ == "__main__":
    main()
