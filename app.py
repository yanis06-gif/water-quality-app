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
    st.markdown("## 💧 Water Quality App")
    st.markdown("### Plateforme intelligente pour l’analyse de la qualité de l’eau potable en Algérie")

    st.info("""
    **🎓 Initiateurs :**  
   👨‍🎓 Yanis FETOUH – Étudiant chercheur  
   👩‍🎓 Louisa Lysa AYAD – Étudiante chercheuse  

    **🧑‍🏫 Encadrement :**  
    👩‍🏫 BOUCHRAKI – Promotrice  
    👨‍🏫 [Nom du Co-promoteur] – Co-promoteur  

    **🤝 En collaboration avec :**  
    🔬 Laboratoire de l’Algérienne des Eaux  

    🏛️ Faculté de Technologie – Département d’Hydraulique  
    Université Abderrahmane Mira de Béjaïa  

    Ce projet s’inscrit dans une dynamique de **recherche scientifique appliquée**, visant à contribuer à l’amélioration de la **santé publique**.
    """)

    st.markdown("*Version 1.0 – Propulsée par la science, l’innovation et la passion pour l’environnement 💙*")


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
