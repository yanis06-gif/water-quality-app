import streamlit as st
st.write("PAGE ACTIVE :", st.session_state.page)

st.set_page_config(page_title="Test HTML", layout="centered")

st.markdown("""
    <style>
        .box {
            background: #e0f7fa;
            padding: 2rem;
            border-radius: 15px;
            font-family: Arial;
        }
    </style>

    <div class="box">
        <h2>💧 Water Quality App</h2>
        <p><b>🎓 Yanis FETOUH</b> – Étudiant chercheur</p>
        <p><b>👩‍🏫 BOUCHRAKI</b> – Promotrice</p>
    </div>
""", unsafe_allow_html=True)
