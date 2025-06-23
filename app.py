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
from io import BytesIO

def generer_rapport_prelevements(df, normes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Rapport d'analyse de la qualité de l'eau", ln=True)
    pdf.ln(5)

    for idx, row in df.iterrows():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Prelevement : {row.get('Code', 'N/A')}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 10, f"Date : {row.get('Date', '')}  Heure : {row.get('Heure', '')}", ln=True)
        pdf.cell(0, 10, f"Localisation : {row.get('Localisation', '')}", ln=True)
        pdf.cell(0, 10, f"Entreprise : {row.get('Entreprise', '')}", ln=True)
        pdf.cell(0, 10, f"Préleveur : {row.get('Préleveur', '')}", ln=True)
        pdf.cell(0, 10, f"Analyste : {row.get('Analyste', '')}", ln=True)
        pdf.ln(4)

        pdf.set_font("Arial", "B", 11)
        pdf.cell(60, 8, "Paramètre", border=1)
        pdf.cell(30, 8, "Valeur", border=1)
        pdf.cell(40, 8, "Norme", border=1)
        pdf.cell(60, 8, "Conformité", border=1, ln=True)
        pdf.set_font("Arial", "", 11)

        for col in df.columns:
            if col in ["Date", "Heure", "Localisation", "Entreprise", "Préleveur", "Analyste", "Code"]:
                continue

            valeur = row[col]
            norme = normes.get(col)
            if norme is None:
                continue

            if isinstance(norme, tuple):  # norme sous forme (min, max)
                conforme = "Oui" if norme[0] <= valeur <= norme[1] else "Non"
                norme_str = f"{norme[0]} - {norme[1]}"
            else:
                conforme = "Oui" if valeur <= norme else "Non"
                norme_str = f"<= {norme}"

            pdf.cell(60, 8, col, border=1)
            pdf.cell(30, 8, f"{valeur:.2f}", border=1)
            pdf.cell(40, 8, norme_str, border=1)
            pdf.cell(60, 8, conforme, border=1, ln=True)

        pdf.ln(10)

    return pdf.output(dest="S").encode("latin-1")



# ✅ Liste officielle des 23 paramètres utilisés dans l'application
parametres = [
    "Total Coliform", "Escherichia Coli", "Faecal Streptococci", "Turbidity",
    "pH", "Temperature", "Free Chlorine", "Chlorates", "Sulfate", "Magnesium",
    "Calcium", "Conductivity", "Dry Residue", "Complete Alkaline Title",
    "Nitrite", "Ammonium", "Phosphate", "Nitrate", "Iron", "Manganese",
    "Colour", "Smell", "Taste"
]
# ✅ Initialisation de la page active
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if st.session_state.page == "Accueil":
    st.markdown("""
        <style>
            .accueil-container {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #e6f7ff, #f0faff);
                border-radius: 20px;
                box-shadow: 0 6px 20px rgba(0, 123, 255, 0.2);
                font-family: 'Segoe UI', sans-serif;
            }
            .accueil-title {
                font-size: 3em;
                font-weight: bold;
                color: #0077cc;
            }
            .accueil-subtitle {
                font-size: 1.7em;
                color: #1a1a1a;
                margin-bottom: 1rem;
            }
            .accueil-description {
                font-size: 1.1em;
                margin-top: 1.5rem;
                color: #444;
                line-height: 1.8;
                max-width: 750px;
                margin-left: auto;
                margin-right: auto;
            }
            .accueil-footer {
                margin-top: 2rem;
                color: #666;
                font-size: 0.95em;
            }
        </style>

        <div class="accueil-container">
            <h1 class="accueil-title">💧 Water Quality App</h1>
            <p class="accueil-subtitle">Application intelligente pour l’analyse de la qualité de l’eau potable</p>

            <div class="accueil-description">
                <b>Initiateurs :</b><br>
                👨‍🎓 <b>Yanis FETHI</b> – Étudiant chercheur<br>
                👨‍🎓 <b>[Nom Étudiant 2]</b> – Étudiant chercheur<br><br>

                <b>Encadrement :</b><br>
                👩‍🏫 <b>[Nom Promotrice]</b> – Promotrice<br>
                👨‍🏫 <b>[Nom Co-promoteur]</b> – Co-promoteur<br><br>

                <b>En collaboration avec :</b><br>
                🔬 <b>Laboratoire de l’Algérienne des Eaux</b><br><br>

                <b>Faculté de Technologie</b> – Département d’Hydraulique<br>
                <b>Université Abderrahmane Mira de Béjaïa</b><br><br>

                Ce projet s’inscrit dans une dynamique de <b>recherche scientifique appliquée</b>, 
                visant à contribuer à l’amélioration de la santé publique et de la gestion des ressources en eau en Algérie.
            </div>

            <div class="accueil-footer">
                Version 1.0 – Propulsée par la science, l’innovation et la passion pour l’environnement 💙
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Action bouton → entrée dans l'application
    if st.button("➡️ Entrer dans le menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()

if st.session_state.page == "accueil_interne":
    st.title("📚 Menu principal")
    st.markdown("Choisissez une fonctionnalité ci-dessous :")

    if st.button("1-📘 Présentation de l’application"):
        st.session_state.page = "Présentation"
        st.rerun()


    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("2-📋 Base de données"):
            st.session_state.page = "Base de données"
            st.rerun()
        if st.button("3-🔍 Prédiction"):
            st.session_state.page = "Prédiction"
            st.rerun()
    with col2:
        if st.button("4-🧠 Classification"):
            st.session_state.page = "Classification"
            st.rerun()
        if st.button("5-☣️ Détection Pollution"):
            st.session_state.page = "Pollution"
            st.rerun()
    with col3:
        if st.button("6-📊 Visualisation"):
            st.session_state.page = "Visualisation"
            st.rerun()
        if st.button("7-💬 Assistant IA"):
            st.session_state.page = "Assistant"
            st.rerun()
    # 🔚 Bouton de retour à l’accueil (page d’introduction)
    st.markdown("---")
    if st.button("🔚 Retour à l’accueil"):
        st.session_state.page = "Accueil"
        st.rerun()
  

# Afficher la bonne section selon la page
if st.session_state.page == "Présentation":
    st.title("📘 Présentation de Water Quality App")

    # Ajout de l’image (assure-toi que "eau.jpg" existe dans le dossier de ton app)
    st.image("eau.jpg", use_column_width=True)

    st.markdown("""
    ---
    ### 💧 Description générale
    Water Quality App est une application professionnelle conçue pour analyser et surveiller la qualité de l’eau potable en utilisant des techniques d’intelligence artificielle.

    ---
    ### ⚙️ Fonctionnalités principales
    - 📥 Ajout de prélèvements manuellement ou via fichier Excel
    - 🔍 Prédiction de paramètres manquants avec IA (Random Forest)
    - 🧠 Classification intelligente de la qualité (NORME, EXCÈS CHLORE…)
    - ☣️ Détection automatique du type de pollution
    - 📊 Visualisations interactives
    - 📤 Export PDF et Excel
    - 🤖 Assistant IA intégré pour guider les utilisateurs

    ---
    ### 🧪 Paramètres analysés
    23 paramètres selon les normes algériennes (pH, Chlore, Nitrate, Coliformes, etc.)

    ---
    ### 🧠 Technologies utilisées
    Python, Pandas, Scikit-learn, Plotly, Streamlit

    ---
    ### 👥 Public cible
    - Laboratoires de contrôle de qualité
    - Services d’eau potable
    - Universitaires
    - Institutions de santé publique

    ---
    ### 🌐 Hébergement
    Application hébergée via GitHub + Render ou OVH, avec mises à jour automatiques pour tous les utilisateurs.

    ---
    """, unsafe_allow_html=True)

    # Bouton retour
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()
    pass
#################
# BASE DE DONNEE
#################
elif st.session_state.page == "Base de données":

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
    st.button("❓ Besoin d’aide ici ?", on_click=lambda: st.session_state.update(page="Assistant"))
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
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()
    pass
###########################
# Prediction d'un paramètre ######
############################
elif st.session_state.page == "Prédiction":
    import os
    import joblib
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    st.header("📊 Prédiction d’un paramètre de qualité de l’eau")
    st.markdown("Anticipez une valeur manquante grâce à un modèle IA intelligent, visualisez les résultats et recevez des recommandations.")

    # 🔹 Liste officielle des 23 paramètres selon les normes algériennes
    parametres = [
        "Total Coliform", "Escherichia Coli", "Faecal Streptococci", "Turbidity",
        "pH", "Temperature", "Free Chlorine", "Chlorates", "Sulfate", "Magnesium",
        "Calcium", "Conductivity", "Dry Residue", "Complete Alkaline Title",
        "Nitrite", "Ammonium", "Phosphate", "Nitrate", "Iron", "Manganese",
        "Colour", "Smell", "Taste"
    ]

    # 🔹 Normes algériennes simplifiées
    normes = {
        "pH": (6.5, 8.5), "Turbidity": 5, "Temperature": 25, "Free Chlorine": (0.2, 0.5),
        "Sulfate": 250, "Magnesium": 50, "Calcium": 200, "Conductivity": 2800,
        "Dry Residue": 1500, "Nitrite": 0.5, "Ammonium": 0.5, "Phosphate": 5,
        "Nitrate": 50, "Iron": 0.3, "Manganese": 0.1, "Chlorates": 0.7,
        "Complete Alkaline Title": (100, 300), "Total Coliform": 0, "Escherichia Coli": 0,
        "Faecal Streptococci": 0, "Colour": 0, "Smell": 0, "Taste": 0
    }

    # 🔸 Choix du paramètre cible à prédire
    param_cible = st.selectbox("🎯 Paramètre à prédire :", parametres)
    model_name = f"modele_{param_cible.replace(' ', '_')}.pkl"
    model_path = os.path.join("models", model_name)

    # 🧪 Saisie des autres paramètres
    st.markdown("### 🧪 Entrez les autres paramètres mesurés :")
    valeurs = {}
    for param in parametres:
        if param != param_cible:
            valeurs[param] = st.number_input(param, value=0.0, format="%.3f", key=f"pred_{param}")

    if st.button("🔮 Lancer la prédiction"):
        try:
            if not os.path.exists(model_path):
                st.warning("🚫 Modèle introuvable.")
                st.stop()

            modele = joblib.load(model_path)
            X_input = np.array([valeurs[p] for p in valeurs]).reshape(1, -1)
            prediction = modele.predict(X_input)[0]
            st.success(f"✅ **{param_cible} prédit :** `{round(prediction, 3)}`")

            # 🔍 Visualisation avec normes
            if param_cible in normes:
                st.markdown("### 📊 Comparaison avec la norme")
                fig, ax = plt.subplots(figsize=(6, 1.5))
                ax.barh([param_cible], [prediction], color="skyblue")
                if isinstance(normes[param_cible], tuple):
                    ax.axvline(normes[param_cible][0], color="green", linestyle="--", label="Min")
                    ax.axvline(normes[param_cible][1], color="red", linestyle="--", label="Max")
                else:
                    ax.axvline(normes[param_cible], color="red", linestyle="--", label="Norme")
                ax.legend()
                st.pyplot(fig)

                # 💬 Commentaire automatique
                commentaire = "✅ Valeur conforme."
                if isinstance(normes[param_cible], tuple):
                    if prediction < normes[param_cible][0]:
                        commentaire = "⬇️ Valeur trop basse (non conforme)."
                    elif prediction > normes[param_cible][1]:
                        commentaire = "⬆️ Valeur trop élevée (non conforme)."
                else:
                    if prediction > normes[param_cible]:
                        commentaire = "⚠️ Valeur au-dessus de la norme."
                    elif prediction < normes[param_cible]:
                        commentaire = "⚠️ Valeur anormalement basse."
                st.info(commentaire)

            # 📋 Valeurs utilisées
            with st.expander("📋 Voir les valeurs utilisées pour cette prédiction"):
                for k, v in valeurs.items():
                    st.markdown(f"- **{k}** : {v}")

            # 💾 Option de sauvegarde
            if st.checkbox("💾 Sauvegarder cette prédiction"):
                save_path = "historique_predictions.pkl"
                ligne = {"Paramètre": param_cible, "Valeur prédite": prediction}
                ligne.update(valeurs)
                if os.path.exists(save_path):
                    df_old = pd.read_pickle(save_path)
                else:
                    df_old = pd.DataFrame()
                df_new = pd.concat([df_old, pd.DataFrame([ligne])], ignore_index=True)
                df_new.to_pickle(save_path)
                st.success("📁 Résultat enregistré avec succès.")

        except Exception as e:
            st.error("❌ Une erreur est survenue pendant la prédiction.")
            st.code(str(e))

    # 🔙 Retour
    st.markdown("---")
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()

    pass
elif st.session_state.page == "Classification":
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
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()
    pass
elif st.session_state.page == "Pollution":
    # ===============================
    # ⚠️ DÉTECTION DU TYPE DE POLLUTION
    # ===============================
    st.header("⚠️ Détection du type de pollution")
    st.button("❓ Besoin d’aide ici ?", on_click=lambda: st.session_state.update(page="Assistant"))

    st.markdown("Remplissez les paramètres pour identifier automatiquement le type de pollution présent.")

    # Liste des 23 paramètres utilisés dans l’application (normes algériennes)
    parametres = [
        "Total Coliform", "Escherichia Coli", "Faecal Streptococci", "Turbidity",
        "pH", "Temperature", "Free Chlorine", "Chlorates", "Sulfate", "Magnesium",
        "Calcium", "Conductivity", "Dry Residue", "Complete Alkaline Title",
        "Nitrite", "Ammonium", "Phosphate", "Nitrate", "Iron", "Manganese",
        "Colour", "Smell", "Taste"
    ]

    # 🔬 Détection manuelle du type de pollution selon les 23 paramètres
    def detecter_pollution(parametres_valeurs):
        pollutions = {
            "Pollution Bactériologique": ["Total Coliform", "Escherichia Coli", "Faecal Streptococci"],
            "Pollution Physico-chimique": ["pH", "Temperature", "Free Chlorine", "Chlorates"],
            "Pollution Minérale": ["Sulfate", "Magnesium", "Calcium", "Conductivity", "Dry Residue"],
            "Pollution Organique": ["Nitrite", "Ammonium", "Phosphate", "Nitrate"],
            "Métaux et Élémentaires": ["Iron", "Manganese"],
            "Pollution Organoleptique": ["Colour", "Smell", "Taste"],
            "Problème d'Alcalinité": ["Complete Alkaline Title"]
        }

        # Normes algériennes simplifiées
        normes = {
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

        type_pollutions_detectees = []

        for type_pollution, params in pollutions.items():
            for param in params:
                if param in parametres_valeurs and param in normes:
                    valeur = parametres_valeurs[param]
                    norme = normes[param]
                    if isinstance(norme, tuple):  # plage min-max
                        if valeur < norme[0] or valeur > norme[1]:
                            type_pollutions_detectees.append(type_pollution)
                            break
                    else:
                        if valeur > norme:
                            type_pollutions_detectees.append(type_pollution)
                            break

        return list(set(type_pollutions_detectees))  # enlever les doublons

    # 🛠 Recommandations selon type de pollution
    def recommandation(pollution_type):
        recs = {
            "Pollution Bactériologique": "💡 Désinfecter le réseau, renforcer la chloration, surveiller les infiltrations fécales.",
            "Pollution Physico-chimique": "💡 Limiter les rejets industriels, contrôler le chlore et la température.",
            "Pollution Minérale": "💡 Envisager un traitement par osmose inverse, surveiller les sels dissous.",
            "Pollution Organique": "💡 Contrôler la matière organique, améliorer le traitement des eaux usées.",
            "Métaux et Élémentaires": "💡 Utiliser des filtres spécifiques pour fer et manganèse.",
            "Pollution Organoleptique": "💡 Traiter l’eau pour goût, couleur, odeur (filtration, aération).",
            "Problème d'Alcalinité": "💡 Ajuster l’équilibre chimique pour stabiliser l’eau."
        }
        return recs.get(pollution_type, "✅ Aucun traitement nécessaire.")

    # === Formulaire de saisie
    pollution_vals = {}
    for p in parametres:
        pollution_vals[p] = st.number_input(p, value=0.0, format="%.4f", key=f"poll_{p}")

    # === Détection
    if st.button("🔎 Détecter la pollution"):
        types_detectes = detecter_pollution(pollution_vals)
        if not types_detectes:
            st.success("✅ Eau conforme : aucune pollution détectée.")
        else:
            st.error("⚠️ Types de pollution détectés :")
            for t in types_detectes:
                st.markdown(f"- **{t}**")
                st.info(recommandation(t))

    # === Bouton retour
    st.markdown("---")
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()

elif st.session_state.page == "Visualisation":

    st.header("📊 Visualisation des données de qualité de l’eau")
    st.button("❓ Besoin d’aide ici ?", on_click=lambda: st.session_state.update(page="Assistant"))
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
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()

elif st.session_state.page == "Assistant":
    st.header("🤖 Assistant IA – Aide & Explications sur l’application")
    st.markdown("Posez une question sur l’utilisation de l’application, l’analyse de l’eau, les normes ou les fonctionnalités disponibles.")

    question = st.text_input("💬 Votre question :", placeholder="Ex : Comment classifier un prélèvement ?")

    if question:
        question_lower = question.lower()
        
        # --- Réponses intelligentes à base de mots-clés ---
        if "prélèvement" in question_lower or "ajouter" in question_lower:
            st.info("🧪 Pour **ajouter un nouveau prélèvement**, rendez-vous dans le menu **Base de Données**.\nRemplissez les champs obligatoires comme la date, l’heure, le lieu, et les valeurs des paramètres. Cliquez ensuite sur **💾 Enregistrer le prélèvement**.")

        elif "classer" in question_lower or "classification" in question_lower:
            st.info("🧠 Pour **classifier la qualité de l’eau**, allez dans la section **Classification**.\nSaisissez les 23 paramètres, puis cliquez sur **📈 Lancer la classification**. L’algorithme affichera une des 5 classes (Très bonne, Bonne, Moyenne, Mauvaise, Très mauvaise) avec les alertes associées.")

        elif "pollution" in question_lower or "pollu" in question_lower:
            st.info("⚠️ Pour **détecter le type de pollution**, ouvrez la page **Pollution**.\nEntrez les valeurs des 23 paramètres et cliquez sur **🔎 Détecter la pollution**. L’IA identifiera automatiquement s’il y a une pollution bactérienne, minérale, organique, etc.")

        elif "norme" in question_lower:
            st.info("📏 Les **normes algériennes** sont intégrées dans l’application.\nChaque paramètre est comparé à sa norme pour signaler les dépassements et proposer une action : chloration, désinfection, adoucisseur, etc.")

        elif "visualiser" in question_lower or "graphe" in question_lower or "graphique" in question_lower:
            st.info("📊 Pour **visualiser l’évolution des paramètres**, allez dans **Visualisation**.\nVous pouvez y tracer des courbes dans le temps, voir des histogrammes, ou comparer les valeurs à la norme.")

        elif "export" in question_lower or "excel" in question_lower or "pdf" in question_lower:
            st.info("📤 Pour **exporter la base de données**, utilisez le menu **Base de Données**.\nVous y trouverez des boutons pour exporter au format CSV ou Excel.")

        elif "vider" in question_lower or "supprimer" in question_lower or "reset" in question_lower:
            st.info("🗑️ Pour **vider la base de données**, ouvrez la section **Base de Données** et cliquez sur le bouton **❌ Vider la base de données** dans la zone d’expansion prévue.")

        elif "paramètre" in question_lower or "liste" in question_lower:
            st.markdown("📋 Voici la **liste complète des 23 paramètres** utilisés dans l’application :")
            for p in [
                "Total Coliform", "Escherichia Coli", "Faecal Streptococci", "Turbidity", "pH",
                "Temperature", "Free Chlorine", "Chlorates", "Sulfate", "Magnesium", "Calcium",
                "Conductivity", "Dry Residue", "Complete Alkaline Title", "Nitrite", "Ammonium",
                "Phosphate", "Nitrate", "Iron", "Manganese", "Colour", "Smell", "Taste"
            ]:
                st.markdown(f"- {p}")
        elif "chlore" in question_lower:
            st.info("💧 Le **chlore libre** doit être maintenu entre **0.2 et 0.5 mg/L** pour garantir une désinfection efficace.\nEn dessous, il y a un risque microbiologique. Au-dessus, il peut y avoir un goût désagréable ou des effets secondaires.")

        elif "ph" in question_lower:
            st.info("🧪 Le **pH idéal de l’eau potable** est entre **6.5 et 8.5**.\nUn pH trop acide (<6.5) favorise la corrosion des tuyaux, un pH trop basique (>8.5) peut affecter le goût et réduire l'efficacité du chlore.")

        elif "conductivité" in question_lower:
            st.info("⚡ La **conductivité** mesure la concentration en sels dissous dans l’eau.\nUne conductivité supérieure à **2800 µS/cm** peut indiquer une eau trop minéralisée (souvent en lien avec des infiltrations salines ou industrielles).")

        elif "goût" in question_lower or "odeur" in question_lower or "couleur" in question_lower:
            st.info("👃👅👁️ Le **goût, l’odeur et la couleur** sont des indicateurs organoleptiques.\nToute anomalie dans ces paramètres peut signaler une contamination organique ou chimique, même si les autres paramètres sont normaux.")

        elif "résultat parfait" in question_lower or "eau parfaite" in question_lower:
            st.info("✅ Une eau potable parfaite aura :\n- **Coliformes, E. coli, Streptocoques** = 0\n- **pH entre 6.5 et 8.5**, **Turbidité < 5**\n- **Chlore libre entre 0.2 et 0.5 mg/L**\n- Tous les autres paramètres sous les normes maximales.")

        elif "analyse complète" in question_lower or "tous les paramètres" in question_lower:
            st.info("🔬 L’analyse complète repose sur **23 paramètres**, classés en catégories :\n- Bactériologiques : Coliformes, E. coli, Streptocoques\n- Physico-chimiques : pH, température, chlore, etc.\n- Minéraux : sulfate, calcium, magnésium, etc.\n- Métaux : fer, manganèse\n- Organoleptiques : goût, odeur, couleur")

        elif "quelle est la meilleure eau" in question_lower:
            st.info("💧 L’eau de **classe Très bonne** est la meilleure :\nTous les paramètres sont conformes, sans dépassement ni alerte.\nElle est **immédiatement potable**, sans besoin de traitement.")

        elif "nitrate" in question_lower:
            st.info("🌿 Le **nitrate** ne doit pas dépasser **50 mg/L**. Il provient souvent des engrais agricoles.\nUn excès peut provoquer des problèmes de santé, surtout chez les nourrissons.")

        elif "fer" in question_lower or "manganèse" in question_lower:
            st.info("🧲 Le **fer** et le **manganèse** sont naturellement présents dans le sol.\nIls doivent être filtrés si leurs concentrations dépassent **0.3 mg/L** pour le fer et **0.1 mg/L** pour le manganèse.\nIls peuvent colorer l’eau et endommager les canalisations.")
        elif "turbidité" in question_lower:
            st.info("🌫️ La **turbidité** reflète la clarté de l’eau.\nElle ne doit pas dépasser **5 NTU**.\nUn excès peut indiquer la présence de matières en suspension ou de micro-organismes. Un filtre ou une décantation est souvent conseillé.")

        elif "température" in question_lower:
            st.info("🌡️ Une eau potable doit rester en dessous de **25°C**.\nUne température élevée favorise le développement bactérien et réduit l’efficacité du chlore.")

        elif "chlorates" in question_lower:
            st.info("🧪 Les **chlorates** sont des sous-produits de la désinfection.\nIls doivent rester inférieurs à **0.7 mg/L**. Un excès signifie souvent un dosage excessif ou un vieillissement du chlore utilisé.")

        elif "alcalinité" in question_lower or "titre alcalin" in question_lower:
            st.info("⚖️ Le **titre alcalin complet** mesure la capacité de l’eau à neutraliser l’acidité.\nIl doit rester entre **100 et 300 mg/L** pour assurer une bonne stabilité chimique de l’eau.")

        elif "résidu sec" in question_lower or "dry residue" in question_lower:
            st.info("🧂 Le **résidu sec** indique la teneur totale en sels dissous.\nIl ne doit pas dépasser **1500 mg/L**. Un excès signale une forte minéralisation.")

        elif "analyse rapide" in question_lower or "analyse simple" in question_lower:
            st.info("⏱️ Pour une **analyse rapide**, concentrez-vous sur :\n- **Coliformes**, **E. coli** (sécurité microbio)\n- **pH**, **chlore libre**, **turbidité** (sécurité physico-chimique)\n- **Nitrate**, **fer**, **manganèse** (sécurité minérale et métal)")

        elif "pollution" in question_lower:
            st.info("⚠️ Votre application détecte automatiquement 7 types de pollution :\n- **Bactériologique** : coliformes, E. coli, streptocoques\n- **Physico-chimique** : chlore, pH, température, chlorates\n- **Minérale** : sulfate, magnésium, etc.\n- **Organique** : nitrate, phosphate...\n- **Métaux** : fer, manganèse\n- **Organoleptique** : goût, odeur, couleur\n- **Alcalinité**")

        elif "problème courant" in question_lower or "problèmes fréquents" in question_lower:
            st.info("🧾 Les problèmes les plus fréquents en Algérie sont :\n- pH trop bas (<6.5)\n- chlore libre absent\n- présence de coliformes\n- nitrate élevé dans les zones agricoles\n- eau calcaire (calcium et magnésium élevés)")

        elif "comment corriger" in question_lower:
            st.info("🔧 Votre application donne automatiquement des conseils pour chaque paramètre hors norme.\nPar exemple :\n- **pH bas** → ajouter des agents alcalins\n- **Chlore faible** → réajuster la chloration\n- **Nitrate élevé** → améliorer le traitement ou changer de source\n- **Fer/manganèse** → filtre catalytique")

        elif "que faire si" in question_lower:
            st.info("❓ En cas d’anomalie détectée :\n- Consultez les alertes affichées après la classification\n- Suivez les conseils pour chaque paramètre\n- Vérifiez le type de pollution dans l’onglet **Pollution**\n- Exportez vos données pour les partager avec un laboratoire")

        elif "exporter" in question_lower or "télécharger" in question_lower:
            st.info("📤 Vous pouvez exporter les données de prélèvement dans l’onglet **Base de Données**.\nFormats disponibles : **CSV** (tableur) et **Excel** (analyses, partage, archivage).")

        elif "modèle" in question_lower or "intelligence artificielle" in question_lower:
            st.info("🤖 L’application utilise plusieurs modèles d’intelligence artificielle :\n- **Random Forest Classifier** pour classer la qualité de l’eau\n- **Détection manuelle intelligente** pour identifier le type de pollution\nLes modèles sont pré-entraînés à partir de normes algériennes et de données d’analyses.")

        elif "comment fonctionne" in question_lower:
            st.info("⚙️ L’application fonctionne par étapes :\n1. Vous entrez les résultats de votre prélèvement\n2. Le modèle IA classe la qualité (Très bonne → Très mauvaise)\n3. Les paramètres sont vérifiés automatiquement\n4. Des alertes sont générées si nécessaire\n5. L’origine de la pollution est identifiée")

        elif "norme" in question_lower:
            st.info("📏 Les normes utilisées sont les **normes algériennes** en vigueur (ex : décret exécutif n° 11-219).\nChaque paramètre a une limite maximale (et parfois minimale) fixée par les autorités sanitaires.")

        elif "ajouter un paramètre" in question_lower:
            st.info("➕ Vous pouvez ajouter/supprimer des paramètres via la section **Base de Données**.\nL’interface permet de sélectionner dynamiquement les paramètres mesurés.")

        elif "base de données" in question_lower:
            st.info("📂 Tous les prélèvements sont stockés dans un fichier `prelevements_sauvegarde.pkl`.\nVous pouvez le vider, l’exporter, ou l’analyser dans l’application.")

        elif "version mobile" in question_lower:
            st.info("📱 L’application peut être déployée comme site web responsive, utilisable sur smartphone.\nVous pouvez aussi envisager une conversion en APK avec des outils comme Streamlit-to-APK ou Flutter WebView.")

        elif "mémoire" in question_lower or "présentation" in question_lower:
            st.info("📝 Cette application peut être présentée dans un mémoire comme un outil d’aide à la décision pour les analyses d’eau potable.\nElle combine l’IA, les normes nationales, la visualisation interactive et la détection automatisée de pollution.")


        elif "erreur" in question_lower or "ne fonctionne pas" in question_lower or "problème" in question_lower:
            st.warning("❌ Assurez-vous d’avoir bien **enregistré au moins un prélèvement**.\nSinon, les fonctionnalités comme la visualisation ou l’export ne fonctionneront pas correctement.")
        
        elif "conseil" in question_lower or "améliorer" in question_lower:
            st.markdown("""💡 Quelques **bons conseils** pour une bonne qualité de l’eau :
- Maintenir le **chlore libre entre 0.2 et 0.5 mg/L**.
- Garder la **turbidité sous 5 NTU** pour une bonne clarté.
- S’assurer que les **coliformes et E. coli soient à 0**.
- Éviter les nitrates > 50 mg/L pour prévenir les risques chez les nourrissons.
- Surveiller **l’odeur, la couleur et le goût** pour détecter les anomalies invisibles.""")

        elif "classe" in question_lower or "interprétation" in question_lower:
            st.markdown("""🧠 **Interprétation des classes prédictives de qualité :**
- **Très bonne** : Tous les paramètres sont conformes.
- **Bonne** : Légères anomalies sans danger.
- **Moyenne** : Traitement recommandé avant consommation.
- **Mauvaise** : Non potable sans traitement.
- **Très mauvaise** : Source très contaminée.""")

        else:
            st.info("🤖 Je suis encore en cours d’apprentissage.\nEssayez une question sur les prélèvements, la classification, les normes ou les visualisations.")
            st.markdown("📍 *Exemples de questions :*\n- Comment classifier un prélèvement ?\n- Que signifie la classe « Mauvaise » ?\n- Comment exporter mes résultats ?")
        st.markdown("---")
        st.subheader("📚 Foire Aux Questions (FAQ)")

        with st.expander("🔍 Comment visualiser un paramètre ?"):
            st.markdown("""
            - Allez dans le menu **Visualisation**.
            - Sélectionnez un paramètre (pH, nitrate...).
            - Consultez les courbes, histogrammes et seuils réglementaires.
            """)

        with st.expander("📈 Comment fonctionne la classification intelligente ?"):
            st.markdown("""
            - Entrez les 23 paramètres d’un échantillon dans **Classification**.
            - L’IA vous donne une **classe de qualité** (Très bonne à Très mauvaise).
            - Si des normes sont dépassées, des **alertes et conseils** s’affichent automatiquement.
            """)

        with st.expander("⚠️ Que faire si l’eau n’est pas conforme ?"):
            st.markdown("""
            - Consultez les alertes sur chaque paramètre.
            - Utilisez l’onglet **Pollution** pour identifier le type de pollution.
            - Appliquez les recommandations proposées automatiquement.
            """)

        with st.expander("📤 Puis-je exporter mes données ?"):
            st.markdown("""
            - Oui, dans **Base de Données**, vous pouvez exporter au format **CSV** ou **Excel**.
            - Cela permet d’archiver, d’analyser ou de transmettre les résultats.
            """)

        with st.expander("🧪 Quels sont les paramètres analysés ?"):
            if "parametres_dynamiques" in st.session_state:
                st.markdown(", ".join(st.session_state.parametres_dynamiques))
            else:
                st.info("⚠️ Les paramètres dynamiques ne sont pas encore chargés. Veuillez d’abord accéder à la base de données.")

    # Bouton retour
    st.markdown("---")
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()





