import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from io import BytesIO
import traceback
import plotly.express as px
# ✅ Liste officielle des 23 paramètres utilisés dans l'application
parametres = [
    "Total Coliform", "Escherichia Coli", "Faecal Streptococci", "Turbidity",
    "pH", "Temperature", "Free Chlorine", "Chlorates", "Sulfate", "Magnesium",
    "Calcium", "Conductivity", "Dry Residue", "Complete Alkaline Title",
    "Nitrite", "Ammonium", "Phosphate", "Nitrate", "Iron", "Manganese",
    "Colour", "Smell", "Taste"
]


# ✅ Initialisation de la page active dans la session
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if st.session_state.page == "Accueil":
    st.markdown("""
        <style>
            .accueil-container {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(145deg, #d6f0ff, #ffffff);
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
            .accueil-title {
                font-size: 3em;
                font-weight: bold;
                color: #0077cc;
            }
            .accueil-subtitle {
                font-size: 1.5em;
                color: #333;
            }
            .accueil-description {
                font-size: 1.1em;
                margin-top: 1.5rem;
                color: #444;
                line-height: 1.6;
            }
            .accueil-footer {
                margin-top: 2rem;
                color: #888;
            }
        </style>

        <div class="accueil-container">
            <h1 class="accueil-title">💧 Water Quality App</h1>
            <p class="accueil-subtitle">Analyse intelligente de la qualité de l'eau potable en Algérie</p>
            <div class="accueil-description">
                Bienvenue sur l'application dédiée à la surveillance et à l'amélioration de la qualité de l’eau potable.<br><br>
                Grâce à cette application, vous pouvez :
                <ul style="text-align: left; max-width: 600px; margin: auto;">
                    <li>🔍 Classer la qualité de l’eau selon les normes algériennes</li>
                    <li>📊 Gérer une base de données complète de prélèvements</li>
                    <li>🧠 Prédire les paramètres manquants avec IA</li>
                    <li>🚨 Détecter automatiquement le type de pollution</li>
                    <li>📁 Exporter vos résultats en PDF ou Excel</li>
                </ul>
            </div>
            <div class="accueil-footer">
                Version 1.0 – Développé avec ❤️ pour l’environnement et la santé publique
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

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Base de données"):
            st.session_state.page = "Base de données"
            st.rerun()
        if st.button("🔍 Prédiction"):
            st.session_state.page = "Prédiction"
            st.rerun()
    with col2:
        if st.button("🧠 Classification"):
            st.session_state.page = "Classification"
            st.rerun()
        if st.button("☣️ Détection Pollution"):
            st.session_state.page = "Pollution"
            st.rerun()
    with col3:
        if st.button("📊 Visualisation"):
            st.session_state.page = "Visualisation"
            st.rerun()
        if st.button("💬 Assistant IA"):
            st.session_state.page = "Assistant"
            st.rerun()
    # 🔚 Bouton de retour à l’accueil (page d’introduction)
    st.markdown("---")
    if st.button("🔚 Retour à l’accueil"):
        st.session_state.page = "accueil"
        st.rerun()
  

# Afficher la bonne section selon la page
#################
# BASE DE DONNEE
#################
if st.session_state.page == "Base de données":

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
            analyste = st.text_input("🧪 Analyste")
            code = st.text_input("🧾 Code échantillon")

        st.markdown("### 🧪 Résultats d'analyse")
        resultats = {}
        for param in st.session_state.parametres_dynamiques:
            resultats[param] = st.number_input(param, value=0.0, format="%.3f", key=f"base_{param}")

        if st.button("💾 Enregistrer le prélèvement"):
            new_row = {
                "Date": date, "Heure": heure, "Localisation": localisation,
                "Entreprise": entreprise, "Analyste": analyste, "Code": code
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
    else:
        st.warning("⚠️ Aucune donnée enregistrée.")

    # ... (tout le bloc de gestion de base de données)
    
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

        # Sélection des options
        st.subheader("📌 Options de sélection")
        params_disponibles = [col for col in df.columns if col not in ["Date", "Heure", "Localisation", "Entreprise", "Analyste", "Code"]]
        param_choisi = st.selectbox("🔍 Choisir un paramètre à visualiser", options=params_disponibles)

        st.markdown("### 📈 Évolution du paramètre sélectionné")
        fig1 = px.line(df, x="Date", y=param_choisi, title=f"Évolution de {param_choisi}", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### 📊 Histogramme")
        fig2 = px.histogram(df, x=param_choisi, nbins=30, title=f"Distribution de {param_choisi}")
        st.plotly_chart(fig2, use_container_width=True)

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
            st.info("Ligne rouge = limite de la norme algérienne")
            fig3 = px.line(df, x="Date", y=param_choisi, title=f"{param_choisi} avec Norme")
            if isinstance(normes_simplifiees[param_choisi], tuple):
                min_, max_ = normes_simplifiees[param_choisi]
                fig3.add_hline(y=min_, line_color="red", line_dash="dash")
                fig3.add_hline(y=max_, line_color="red", line_dash="dash")
            else:
                fig3.add_hline(y=normes_simplifiees[param_choisi], line_color="red", line_dash="dash")
            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.warning("⚠️ Aucune donnée enregistrée. Veuillez d’abord ajouter des prélèvements dans la base de données.")

    # Bouton retour
    st.markdown("---")
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()

elif st.session_state.page == "Assistant":
    st.header("🤖 Assistant IA – Aide & Visualisation des Données")
    st.markdown("Posez votre question à l’assistant sur la qualité de l’eau, l’analyse ou les visualisations disponibles.")

    question = st.text_input("💬 Votre question :", placeholder="Ex : Comment visualiser l’évolution du pH ?")

    if question:
        # Réponses prédéfinies en fonction de mots-clés détectés
        question_lower = question.lower()

        if "graphique" in question_lower or "visualiser" in question_lower or "courbe" in question_lower:
            st.info("📊 Vous pouvez visualiser l’évolution d’un paramètre dans le menu **Visualisation**.\n\nVoici ce que vous pouvez faire :")
            st.markdown("""
            - **Tracer une courbe** de l'évolution d’un paramètre (ex : pH, nitrate, etc.) dans le temps.
            - **Comparer plusieurs paramètres** ensemble.
            - **Détecter des anomalies visuelles** (pics de turbidité, baisses du chlore libre, etc.).
            - **Filtrer les données** par date, localisation ou entreprise pour une analyse ciblée.
            - **Exporter les visualisations** au format image (via clic droit ou capture).
            - **Utiliser différents types de graphes** : lignes, barres, nuages de points.

            ℹ️ Conseil : veillez à avoir au moins quelques prélèvements enregistrés dans la **Base de Données** pour que les graphiques s’affichent !
            """)

        elif "paramètre" in question_lower:
            st.info("💡 Tous les paramètres mesurés sont disponibles pour la visualisation.")
            st.markdown("Voici la **liste complète des 23 paramètres** que vous pouvez analyser :")
            for p in parametres:
                st.markdown(f"- {p}")

        elif "erreur" in question_lower or "pas de graphique" in question_lower:
            st.warning("❌ Vérifiez que vous avez bien **enregistré des prélèvements** dans la base de données.\nSans données, aucun graphique ne peut être généré.")
            st.markdown("📍 Astuce : utilisez la section **Base de Données** pour saisir ou importer vos premiers prélèvements.")

        elif "comparaison" in question_lower:
            st.markdown("""
            📈 Vous pouvez comparer plusieurs paramètres dans la section **Visualisation** :
            - Sélectionnez **deux ou plusieurs paramètres** dans le filtre.
            - Un graphique multi-trace apparaîtra pour comparer les tendances.
            - Cela permet de repérer des **corrélations**, comme entre nitrate et conductivité.
            """)

        else:
            st.info("🤖 Je suis encore en cours d’apprentissage. Essayez une question sur la visualisation ou sur les paramètres !")
            st.markdown("🔍 Exemples de questions :\n- Comment afficher le graphique du pH ?\n- Peut-on comparer les paramètres ?\n- Pourquoi je ne vois pas de graphique ?")

    # Retour
    st.markdown("---")
    if st.button("🔙 Retour au menu principal"):
        st.session_state.page = "accueil_interne"
        st.rerun()





