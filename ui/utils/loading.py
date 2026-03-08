import streamlit as st
import time

def render_loading_screen():
    """
    Renders a professional, premium splash screen for SiGURU.
    """
    if 'loading_finished' not in st.session_state:
        st.session_state['loading_finished'] = False

    if not st.session_state['loading_finished']:
        # Custom CSS for the splash screen
        st.markdown("""
        <style>
            .splash-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background-color: #0e1117;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 999999;
                transition: opacity 0.8s ease-out;
            }
            
            .logo-animation {
                font-size: 5rem;
                margin-bottom: 2rem;
                animation: pulse 2s infinite ease-in-out;
            }
            
            .app-name {
                color: #4A90E2;
                font-size: 3rem;
                font-weight: 800;
                letter-spacing: 0.2rem;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, #4A90E2, #357ABD);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .app-tagline {
                color: #888;
                font-size: 1.1rem;
                margin-bottom: 3rem;
            }
            
            .loader-bar {
                width: 300px;
                height: 4px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 2px;
                position: relative;
                overflow: hidden;
            }
            
            .loader-progress {
                position: absolute;
                top: 0;
                left: 0;
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #4A90E2, #357ABD);
                animation: load 2.5s cubic-bezier(0.1, 0, 0.2, 1) forwards;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(74, 144, 226, 0)); }
                50% { transform: scale(1.05); filter: drop-shadow(0 0 20px rgba(74, 144, 226, 0.4)); }
                100% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(74, 144, 226, 0)); }
            }
            
            @keyframes load {
                0% { width: 0%; }
                20% { width: 15%; }
                50% { width: 65%; }
                80% { width: 90%; }
                100% { width: 100%; }
            }
            
            @keyframes fadeOut {
                to { opacity: 0; visibility: hidden; }
            }
            
            .fade-out {
                animation: fadeOut 0.8s forwards;
            }
        </style>
        
        <div id="splash" class="splash-container">
            <div class="logo-animation">🎓</div>
            <div class="app-name">SiGURU AI</div>
            <div class="app-tagline">Smart Assistant for Better Education</div>
            <div class="loader-bar">
                <div class="loader-progress"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Artificial delay to show the nice animation
        time.sleep(2.8)
        st.session_state['loading_finished'] = True
        st.rerun()

def show_nav_loader():
    """Shows a thin loading bar at the top during internal navigation."""
    st.markdown("""
    <div id="nav-loading-bar" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #4A90E2, #357ABD, #4A90E2);
        background-size: 200% 100%;
        animation: navLoading 2s infinite linear;
        z-index: 10000;
    "></div>
    <style>
        @keyframes navLoading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    """, unsafe_allow_html=True)

def hide_default_loaders():
    """Hides Streamlit's default 'Running...' widget and page dimming."""
    st.markdown("""
        <style>
            /* Hide the running widget in the top right */
            [data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
            /* Prevent the screen from dimming/blurring during a rerun */
            .stApp {
                transition: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
