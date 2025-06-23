import streamlit as st

# -----------------------------
# Configuration de la page
# -----------------------------
st.set_page_config(
    page_title="Water Quality App",
    page_icon="💧",
    layout="centered",
)

# -----------------------------
# Initialisation de session_state
# -----------------------------
# On crée la clé "page" si elle n'existe pas encore,
# afin d'éviter l'erreur AttributeError et de garantir
# qu'une page par défaut est toujours définie.
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# -----------------------------
# Barre latérale de navigation
# -----------------------------
st.sidebar.title("Menu")

pages = [
    "Accueil",
    "Classification",
    "Prédiction",
    "Visualisation",
    "Export",
]

# Utilisation d'un radio‐button pour la navigation :
selected_page = st.sidebar.radio("Navigation", pages, index=pages.index(st.session_state.page))

# Mise à jour de la page courante dans session_state
st.session_state.page = selected_page

# -----------------------------
# Page : Accueil
# -----------------------------
if st.session_state.page == "Accueil":
    st.markdown(
        r"""
        <style>
            .accueil-container {
                text-align: center;
                padding: 3rem;
                background: linear-gradient(145deg, #e0f7fa, #ffffff);
                border-radius: 20px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
                margin-top: 2rem;
            }
            .accueil-title {
                font-size: 3em;
                font-weight: bold;
                color: #006699;
                margin-bottom: 0.5em;
            }
            .accueil-subtitle {
                font-size: 1.4em;
                color: #333;
                margin-bottom: 1.5em;
            }
            .accueil-description {
                font-size: 1.1em;
                color: #444;
                line-height: 1.7;
                max-width: 800px;
                margin: auto;
                text-align: left;
            }
            .accueil-footer {
                margin-top: 2.5rem;
                color: #666;
                font-style: italic;
                font-size: 0.95em;
            }
        </style>

        <div class="accueil-container">
            <h1 class="accueil-title">💧 Water Quality App</h1>
            <p class="accueil-subtitle">Plateforme intelligente pour l’analyse de la qualité de l’eau potable en Algérie</p>

            <div class="accueil-description">
                <p><b>🎓 Initiateurs :</b><br>
                👨‍🎓 <b>Yanis FETOUH</b> – Étudiant chercheur<br>
                👩‍🎓 <b>Louisa Lysa AYAD</b> – Étudiante chercheuse</p>

                <p><b>🧑‍🏫 Encadrement :</b><br>
                👩‍🏫 <b>BOUCHRAKI</b> – Promotrice<br>
                👨‍🏫 <b>[Nom du Co‑promoteur]</b> – Co‑promoteur</p>

                <p><b>🤝 En collaboration avec :</b><br>
                🔬 <b>Laboratoire de l’Algérienne des Eaux</b></p>

                <p><b>🏛️ Faculté de Technologie</b> – Département d’Hydraulique<br>
                <b>Université Abderrahmane Mira de Béjaïa</b></p>

                <p>Ce projet s’inscrit dans une dynamique de <b>recherche scientifique appliquée</b>,
                visant à contribuer à l’amélioration de la <b>santé publique</b> et de la <b>gestion des ressources en eau</b> en Algérie.</p>
            </div>

            <div class="accueil-footer">
                Version 1.0 – Propulsée par la science, l’innovation et la passion pour l’environnement 💙
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Page : Classification (placeholder)
# -----------------------------
elif st.session_state.page == "Classification":
    st.header("🧠 Classification")
    st.info("Fonctionnalité de classification à intégrer ici.")

# -----------------------------
# Page : Prédiction (placeholder)
# -----------------------------
elif st.session_state.page == "Prédiction":
    st.header("🔮 Prédiction")
    st.info("Fonctionnalité de prédiction à intégrer ici.")

# -----------------------------
# Page : Visualisation (placeholder)
# -----------------------------
elif st.session_state.page == "Visualisation":
    st.header("📊 Visualisation des données")
    st.info("Visualisations à ajouter ici.")

# -----------------------------
# Page : Export (placeholder)
# -----------------------------
elif st.session_state.page == "Export":
    st.header("📁 Export des résultats")
    st.info("Fonctions d'export Excel/PDF à implémenter.")

# -----------------------------
# Fin du fichier
# -----------------------------
