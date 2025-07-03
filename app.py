import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from io import BytesIO
import traceback
import plotly.express as px
from fpdf import FPDF

# ✅ Initialisation de la page active
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# =====================================
# ✅ PAGE D'ACCUEIL
# =====================================
if st.session_state.page == "Accueil":
    st.markdown(
        """
        <style>
            .accueil-container {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #dceeff, #ffffff);
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                max-width: 800px;
                margin: auto;
            }
            .accueil-title {
                font-size: 2.5em;
                font-weight: bold;
                color: #0077cc;
                margin-bottom: 0.5rem;
            }
            .accueil-subtitle {
                font-size: 2.0em;
                color: #333;
                margin-bottom: 1.5rem;
            }
            .accueil-info {
                background-color: #f0f8ff;
                padding: 1rem;
                border-radius: 10px;
                display: inline-block;
                text-align: left;
                font-size: 1.1em;
                color: #333;
                margin-top: 1rem;
            }
        </style>

        <div class="accueil-container">
            <div class="accueil-title">💧 Water Quality Application </div>
            <div class="accueil-subtitle">Automation of water quality classification using a weighted index</div>
            <div class="accueil-info">
                🏛️ <b>University of Bejaia</b><br>
                Faculty of Technology,<br>
                Hydraulics Department,<br>
                Laboratory of Applied Hydraulics and Environment Research (LRHAE),<br>
                06000, Bejaia, Algeria
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")
    if st.button("➡️ Go to main menu", help="Click here to enter the main menu."):
        st.session_state.page = "accueil_interne"
        st.rerun()


# =====================================
# ✅ MENU PRINCIPAL
# =====================================
elif st.session_state.page == "accueil_interne":
    st.title("Main Menu")
    st.markdown("Choose an option below:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Data Entry"):
            st.session_state.page = "Data Entry"
            st.rerun()

    with col2:
        if st.button("Water Quality Classification"):
            st.session_state.page = "Water Quality Classification"
            st.rerun()

    with col3:
        if st.button("Data Visualization"):
            st.session_state.page = "Data Visualization"
            st.rerun()

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "Accueil"
        st.rerun()

#################
# BASE DE DONNEE
#################
if st.session_state.page == "Data Entry":
    st.title("Data Entry")


    import pandas as pd
    from datetime import datetime
    from io import BytesIO

    # ✅ Liste initiale des paramètres
    if "parametres_dynamiques" not in st.session_state:
        st.session_state.parametres_dynamiques = [
            "Total Coliform", "Escherichia Coli", "Faecal Streptococci", "Turbidity", "pH", "Temperature",
            "Free Chlorine", "Chlorates", "Sulfate", "Magnesium", "Calcium", "Conductivity", "Dry Residue",
            "Complete Alkaline Title", "Nitrite", "Ammonium", "Phosphate", "Nitrate", "Iron", "Manganese",
            "Colour", "Smell", "Taste"
        ]

    st.markdown("## 📋 Gestion des prélèvements ADE")
    st.info("Ajoutez, visualisez, modifiez et exportez les données de qualité de l’eau.")

    # 🔧 Gestion des paramètres personnalisés
    with st.expander("⚙️ Gérer les paramètres"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_param = st.text_input("➕ Ajouter un paramètre (ex: Fluor)", key="ajout_param")
        with col2:
            if st.button("Ajouter"):
                if new_param and new_param not in st.session_state.parametres_dynamiques:
                    st.session_state.parametres_dynamiques.append(new_param)
                    st.success(f"✅ '{new_param}' ajouté.")
                else:
                    st.warning("⚠️ Paramètre vide ou déjà existant.")

        param_to_remove = st.selectbox("🗑️ Supprimer un paramètre existant", st.session_state.parametres_dynamiques)
        if st.button("Supprimer"):
            if param_to_remove:
                st.session_state.parametres_dynamiques.remove(param_to_remove)
                st.success(f"🗑️ '{param_to_remove}' supprimé.")

    # 📁 Chargement de la base de données
    if "df_prelèvements" not in st.session_state:
        try:
            st.session_state.df_prelèvements = pd.read_pickle("prelevements_sauvegarde.pkl")
        except FileNotFoundError:
            st.session_state.df_prelèvements = pd.DataFrame()

    # ➕ Formulaire d'ajout
    with st.expander("🧾 Ajouter un nouveau prélèvement"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("📅 Date du prélèvement", value=datetime.today())
            heure = st.time_input("⏰ Heure")
            localisation = st.text_input("📍 Localisation")
        with col2:
            entreprise = st.text_input("🏢 Entreprise")
            préleveur = st.text_input("🧪 Préleveur")
            analyste = st.text_input("🧪 Analyste")
            code = st.text_input("🧾 Code échantillon")

        st.markdown("### 🧪 Résultats d'analyse")
        resultats = {}
        for param in st.session_state.parametres_dynamiques:
            resultats[param] = st.number_input(param, value=0.0, format="%.3f", key=f"base_{param}")

        if st.button("💾 Enregistrer le prélèvement"):
            new_row = {
                "Date": date, "Heure": heure, "Localisation": localisation,
                "Entreprise": entreprise, "Préleveur": préleveur, "Analyste": analyste, "Code": code
            }
            new_row.update(resultats)
            st.session_state.df_prelèvements = pd.concat([
                st.session_state.df_prelèvements,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            st.session_state.df_prelèvements.to_pickle("prelevements_sauvegarde.pkl")
            st.success("✅ Prélèvement enregistré avec succès.")

        # 📊 Affichage de la base
    st.markdown("### 📊 Données enregistrées")
    if not st.session_state.df_prelèvements.empty:
        st.dataframe(st.session_state.df_prelèvements, use_container_width=True)

        with st.expander("📤 Exporter les données"):
            # CSV
            csv = st.session_state.df_prelèvements.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Télécharger en CSV", data=csv, file_name="base_donnees.csv", mime="text/csv")

            # Excel
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()

            excel = to_excel(st.session_state.df_prelèvements)
            st.download_button(
                "📥 Télécharger en Excel",
                data=excel,
                file_name="base_donnees.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # 🖨️ Bloc PDF à coller ici, même niveau d'indentation que "with st.expander"
        st.markdown("### 🖨️ Générer un rapport PDF multi-prélèvements")

        if not st.session_state.df_prelèvements.empty:
            df = st.session_state.df_prelèvements.copy()

            # Sélection multiple
            selection = st.multiselect("✅ Sélectionner les prélèvements à inclure (par Code)", options=df["Code"].unique().tolist())

            if selection:
                selection_df = df[df["Code"].isin(selection)]

                normes_pdf = {
                    "Total Coliform": 0, "Escherichia Coli": 0, "Faecal Streptococci": 0, "Turbidity": 5,
                    "pH": (6.5, 8.5), "Temperature": 25, "Free Chlorine": (0.2, 0.5), "Chlorates": 0.7,
                    "Sulfate": 250, "Magnesium": 50, "Calcium": 200, "Conductivity": 2800,
                    "Dry Residue": 1500, "Complete Alkaline Title": (100, 300), "Nitrite": 0.5,
                    "Ammonium": 0.5, "Phosphate": 5, "Nitrate": 50, "Iron": 0.3, "Manganese": 0.1,
                    "Colour": 0, "Smell": 0, "Taste": 0
                }

                pdf_bytes = generer_rapport_prelevements(selection_df, normes_pdf)
                st.download_button(
                    label=" Télécharger le rapport PDF",
                    data=pdf_bytes,
                    file_name="rapport_prelevements.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("📝 Sélectionnez au moins un prélèvement pour générer un rapport.")

    else:
        st.warning("⚠️ Aucune donnée enregistrée.")

    # ... (tout le bloc de gestion de base de données)
        # 🔻 Réinitialisation / Vidage complet de la base de données
    with st.expander("🗑️ Vider complètement la base de données"):
        st.warning("⚠️ Cette action supprimera **toutes** les données enregistrées.")
        if st.button("❌ Vider la base de données"):
            st.session_state.df_prelèvements = pd.DataFrame()
            if os.path.exists("prelevements_sauvegarde.pkl"):
                os.remove("prelevements_sauvegarde.pkl")
            st.success("🧹 Base de données vidée avec succès.")
            st.rerun()


    # Bouton retour à ajouter ici :
    st.markdown("---")
    if st.button("Back"):
        st.session_state.page = "accueil_interne"
        st.rerun()
    pass
elif st.session_state.page == "Water Quality Classification":
    # =========================
    # 🧠 Classification intelligente de la qualité de l’eau (avec alertes)
    # =========================

    import os
    import numpy as np
    import joblib
    import traceback

    # -- Normes algériennes (réutilisées ici pour les alertes)
    normes = {
        "Total Coliform": {"max": 0, "conseil": "Désinfecter le réseau."},
        "Escherichia Coli": {"max": 0, "conseil": "Procéder à une chloration."},
        "Faecal Streptococci": {"max": 0, "conseil": "Analyser les infiltrations."},
        "Turbidity": {"max": 5, "conseil": "Utiliser un préfiltre."},
        "pH": {"min": 6.5, "max": 8.5, "conseil": "Corriger le pH avec des agents adaptés."},
        "Temperature": {"max": 25, "conseil": "Protéger les réservoirs de chaleur."},
        "Free Chlorine": {"min": 0.2, "max": 0.5, "conseil": "Ajuster le dosage de chlore."},
        "Chlorates": {"max": 0.7, "conseil": "Réduire les sous-produits de désinfection."},
        "Sulfate": {"max": 250, "conseil": "Utiliser un traitement adapté."},
        "Magnesium": {"max": 50, "conseil": "Installer un adoucisseur."},
        "Calcium": {"max": 200, "conseil": "Contrôler l’entartrage."},
        "Conductivity": {"max": 2800, "conseil": "Vérifier les sels dissous."},
        "Dry Residue": {"max": 1500, "conseil": "Utiliser osmose inverse."},
        "Complete Alkaline Title": {"min": 100, "max": 300, "conseil": "Ajuster pour stabilité."},
        "Nitrite": {"max": 0.5, "conseil": "Contrôler la pollution organique."},
        "Ammonium": {"max": 0.5, "conseil": "Vérifier la contamination."},
        "Phosphate": {"max": 5, "conseil": "Limiter les rejets agricoles."},
        "Nitrate": {"max": 50, "conseil": "Réduire l’usage d’engrais."},
        "Iron": {"max": 0.3, "conseil": "Filtrer avec oxydation."},
        "Manganese": {"max": 0.1, "conseil": "Filtre catalytique recommandé."},
        "Colour": {"max": 0, "conseil": "Analyser les composés organiques."},
        "Smell": {"max": 0, "conseil": "Rechercher la contamination."},
        "Taste": {"max": 0, "conseil": "Rechercher composés organiques."}
    }

    # -- Fonction pour vérifier les normes
    def verifier_normes(valeurs):
        alertes = []
        for param, val in valeurs.items():
            if param in normes:
                seuil = normes[param]
                if ("min" in seuil and val < seuil["min"]) or ("max" in seuil and val > seuil["max"]):
                    alertes.append(f"🚨 **{param} = {val:.2f}** hors norme ({seuil.get('min', '-')}-{seuil.get('max', '-')}) → {seuil['conseil']}")
        return alertes

    # --- Paramètres officiels
    parametres = list(normes.keys())

    # --- Classes de qualité d’eau
    classes = {
        0: "Bonne",
        1: "Mauvaise",
        2: "Moyenne",
        3: "Très bonne",
        4: "Très mauvaise"
    }

    st.header("🧠 Classification intelligente de la qualité de l’eau")
    st.button("❓ Besoin d’aide ici ?", on_click=lambda: st.session_state.update(page="Assistant"))
    st.markdown("Entrez les valeurs des 23 paramètres pour classer automatiquement la qualité de l’eau potable.")

    # --- Interface utilisateur
    valeurs_class = {}
    col1, col2 = st.columns(2)
    with col1:
        for i, param in enumerate(parametres[:len(parametres)//2]):
            valeurs_class[param] = st.number_input(param, value=0.0, format="%.3f", key=f"class_left_{param}")
    with col2:
        for i, param in enumerate(parametres[len(parametres)//2:]):
            valeurs_class[param] = st.number_input(param, value=0.0, format="%.3f", key=f"class_right_{param}")

    X_input = np.array([valeurs_class[p] for p in parametres]).reshape(1, -1)

    # --- Chargement du modèle et prédiction
    model_path = os.path.join("models", "modele_classification.pkl")
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            st.success("✅ Modèle chargé avec succès.")
            if st.button("📈 Lancer la classification"):
                prediction = model.predict(X_input)[0]
                label = classes.get(prediction, "Inconnue")
                st.success(f"💡 Classe prédite : **{label}**")

                alertes = verifier_normes(valeurs_class)
                if alertes:
                    st.warning("🔔 **Alertes sur les normes détectées :**")
                    for alerte in alertes:
                        st.markdown(f"- {alerte}")
                else:
                    st.info("✅ Tous les paramètres sont conformes aux normes.")
        except Exception as e:
            st.error("❌ Erreur lors de la classification :")
            st.code(traceback.format_exc())
    else:
        st.error(f"❌ Modèle non trouvé à l’emplacement : {model_path}")

    # --- Explication des classes
    with st.expander("ℹ️ Interprétation des classes prédictives"):
        st.markdown("""
- **Très bonne** : Paramètres parfaitement conformes, aucune anomalie détectée.
- **Bonne** : L’eau est potable avec de très légères anomalies sans danger immédiat.
- **Moyenne** : L’eau nécessite un traitement léger avant consommation.
- **Mauvaise** : Plusieurs paramètres sont hors norme, traitement requis.
- **Très mauvaise** : Eau non potable, source fortement contaminée.
""")
    # Bouton retour à ajouter ici :
    st.markdown("---")
    if st.button("Back"):
        st.session_state.page = "accueil_interne"
        st.rerun()
    pass
elif st.session_state.page == "Data Visualization":

    st.header("Data Visualization")
    st.markdown("Explorez les données enregistrées à travers différents graphiques.")

    if "df_prelèvements" in st.session_state and not st.session_state.df_prelèvements.empty:
        df = st.session_state.df_prelèvements

        if "df_prelèvements" in st.session_state and not st.session_state.df_prelèvements.empty:
            df = st.session_state.df_prelèvements.copy()

            st.subheader("📌 Options de sélection")
            params_disponibles = [col for col in df.columns if col not in ["Date", "Heure", "Localisation", "Entreprise","Préleveur", "Analyste", "Code"]]
            param_choisi = st.selectbox("🔍 Choisir un paramètre à visualiser", options=params_disponibles)

            # Ajout de la colonne Datetime
            df["Datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Heure"].astype(str))
            df = df.sort_values("Datetime")

            # Sélecteur de durée
            durees = {
                "1 heure": pd.Timedelta(hours=1),
                "12 heures": pd.Timedelta(hours=12),
                "24 heures": pd.Timedelta(days=1),
                "3 jours": pd.Timedelta(days=3),
                "1 semaine": pd.Timedelta(weeks=1),
                "1 mois": pd.Timedelta(days=30),
                "Tout afficher": None
            }
            choix_duree = st.selectbox("⏳ Sélectionnez la durée :", list(durees.keys()))

            # Application du filtre de temps
            if durees[choix_duree] is not None:
                limite = df["Datetime"].max() - durees[choix_duree]
                df = df[df["Datetime"] >= limite]

            # === Évolution dans le temps
            st.markdown("### 📈 Évolution du paramètre sélectionné")
            fig1 = px.line(df, x="Datetime", y=param_choisi, title=f"Évolution de {param_choisi}", markers=True)
            st.plotly_chart(fig1, use_container_width=True)

            # === Histogramme
            st.markdown("### 📊 Histogramme")
            fig2 = px.histogram(df, x=param_choisi, nbins=30, title=f"Distribution de {param_choisi}")
            st.plotly_chart(fig2, use_container_width=True)

            # === Comparaison avec la norme
            st.markdown("### 📉 Comparaison avec la norme")
            normes_simplifiees = {
            "Total Coliform": 0,
            "Escherichia Coli": 0,
            "Faecal Streptococci": 0,
            "Turbidity": 5,
            "pH": (6.5, 8.5),
            "Temperature": 25,
            "Free Chlorine": (0.2, 0.5),
            "Chlorates": 0.7,
            "Sulfate": 250,
            "Magnesium": 50,
            "Calcium": 200,
            "Conductivity": 2800,
            "Dry Residue": 1500,
            "Complete Alkaline Title": (100, 300),
            "Nitrite": 0.5,
            "Ammonium": 0.5,
            "Phosphate": 5,
            "Nitrate": 50,
            "Iron": 0.3,
            "Manganese": 0.1,
            "Colour": 0,
            "Smell": 0,
            "Taste": 0
            }

            if param_choisi in normes_simplifiees:
                st.info("🔴 Ligne rouge = limite de la norme algérienne")
                fig3 = px.line(df, x="Datetime", y=param_choisi, title=f"{param_choisi} avec Norme", markers=True)

                if isinstance(normes_simplifiees[param_choisi], tuple):
                    min_, max_ = normes_simplifiees[param_choisi]
                    fig3.add_hline(y=min_, line_color="red", line_dash="dash")
                    fig3.add_hline(y=max_, line_color="red", line_dash="dash")
                else:
                    fig3.add_hline(y=normes_simplifiees[param_choisi], line_color="red", line_dash="dash")

                st.plotly_chart(fig3, use_container_width=True)

        else:
            st.warning("⚠️ Aucune donnée enregistrée.")
        
    # Bouton retour
    st.markdown("---")
    if st.button("Back"):
        st.session_state.page = "accueil_interne"
        st.rerun()