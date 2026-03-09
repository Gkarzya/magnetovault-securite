import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from google import genai
from streamlit_paste_button import paste_image_button
import os
import base64

# =========================================================
# CONFIGURATION DE LA PAGE & PLEIN ÉCRAN (UI CLEANUP)
# =========================================================
st.set_page_config(layout="wide", page_title="Sécurité IRM & DMI", page_icon="🛡️", initial_sidebar_state="expanded")

# CSS pour simuler un vrai logiciel
css_fullscreen_et_onglets = """
<style>
#MainMenu {visibility: hidden;}
.stDeployButton {display: none;}
footer {visibility: hidden;}
header {background-color: transparent !important;}
.block-container {padding-top: 2rem; padding-bottom: 0rem;}

/* Cibler le texte à l'intérieur des boutons d'onglets Streamlit */
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size: 24px !important;
    font-weight: bold !important;
    padding: 5px 10px !important;
}
</style>
"""
st.markdown(css_fullscreen_et_onglets, unsafe_allow_html=True)

# Initialisation de l'IA avec la clé cachée
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ Clé API introuvable. Vérifiez votre fichier .streamlit/secrets.toml")

# Gestion des variables de session (Langue et Authentification)
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def T(fr, en):
    return fr if st.session_state.lang == 'fr' else en

# Fonction infaillible pour centrer les drapeaux
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# =========================================================
# ÉCRAN DE CONNEXION (MUR DE SÉCURITÉ)
# =========================================================
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("") # Espace
        st.write("")
        if os.path.exists("logo_mia.jpg"):
            st.image("logo_mia.jpg", use_container_width=True)
            
        st.markdown("<h2 style='text-align: center;'>🔒 Accès Restreint</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Identifiant (ID)")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit:
                # Dictionnaire des utilisateurs autorisés
                utilisateurs_valides = {
                    "Franck": "Dumiairm2023",
                    "seb": "Dumiairm2023"
                }
                
                if username in utilisateurs_valides and utilisateurs_valides[username] == password:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Identifiant ou mot de passe incorrect.")
    
    # On stoppe la lecture du code ici si l'utilisateur n'est pas connecté !
    st.stop()


# =========================================================
# NAVIGATION (MENU LATÉRAL) & TRADUCTION
# =========================================================
# Si le code arrive ici, c'est que l'utilisateur est connecté !

if os.path.exists("logo_mia.jpg"):
    st.sidebar.image("logo_mia.jpg", use_container_width=True)
else:
    st.sidebar.error("Logo introuvable (logo_mia.jpg)")

st.sidebar.title("Navigation")

# --- BOUTONS DE TRADUCTION AVEC IMAGES CENTRÉES ---
c_lang1, c_lang2 = st.sidebar.columns(2)
with c_lang1:
    if os.path.exists("flag_fr.png"):
        img_b64 = get_base64_image("flag_fr.png")
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_b64}" width="40"></div>', unsafe_allow_html=True)
    if st.button("FR", use_container_width=True):
        st.session_state.lang = 'fr'
        st.rerun()
        
with c_lang2:
    if os.path.exists("flag_uk.png"):
        img_b64 = get_base64_image("flag_uk.png")
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_b64}" width="40"></div>', unsafe_allow_html=True)
    if st.button("EN", use_container_width=True):
        st.session_state.lang = 'en'
        st.rerun()

st.sidebar.divider()

# --- SÉLECTION DE LA PAGE ---
page = st.sidebar.radio(
    T("Choisissez un module :", "Choose a module:"), 
    [T("🏠 Accueil & Mentions Légales", "🏠 Home & Legal Notice"), 
     T("🛡️ Module Sécurité DMI", "🛡️ DMI Safety Module")]
)

st.sidebar.divider()
st.sidebar.info(T("💡 **Astuce :** Appuyez sur **F11** sur votre clavier pour passer en mode Plein Écran (et F11 pour en sortir).", 
                  "💡 **Tip:** Press **F11** on your keyboard to toggle Full Screen mode."))

st.sidebar.divider()
if st.sidebar.button(T("🚪 Se déconnecter", "🚪 Logout"), use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# =========================================================
# PAGE 1 : ACCUEIL & MENTIONS LÉGALES
# =========================================================
if page == T("🏠 Accueil & Mentions Légales", "🏠 Home & Legal Notice"):
    st.title(T("Bienvenue sur Magnetovault - Sécurité Clinique", "Welcome to Magnetovault - Clinical Safety"))
    
    st.markdown(T("### 🎯 Objectif du Logiciel", "### 🎯 Software Objective"))
    st.write(T(
        "Ce logiciel a été conçu spécifiquement pour assister les manipulateurs en électroradiologie médicale (MERM) et les médecins radiologues dans la gestion quotidienne de la sécurité IRM. Il permet de centraliser la recherche de compatibilité des Dispositifs Médicaux Implantables (DMI) grâce à l'intelligence artificielle, et d'estimer théoriquement les contraintes physiques (SAR, B1+rms) liées aux séquences.",
        "This software was specifically designed to assist radiographers (MRI Techs) and radiologists in the daily management of MRI safety. It centralizes compatibility research for Active Implantable Medical Devices (AIMD) using artificial intelligence, and theoretically estimates physical constraints (SAR, B1+rms) related to sequences."
    ))
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(T("### ⚖️ Cadre Législatif & Responsabilité", "### ⚖️ Legislative Framework & Liability"))
        st.warning(T(
            "**Ce logiciel n'est PAS un Dispositif Médical certifié (marquage CE).**\n\n* **Aide à la décision uniquement :** Les résultats générés par le module IA et les estimations physiques sont donnés à titre purement indicatif.\n* **Responsabilité humaine :** L'utilisateur final reste seul responsable de la validation des données, de la consultation des manuels officiels des constructeurs, et de la décision finale.\n* **Aucune garantie :** L'auteur décline toute responsabilité en cas d'incident résultant de l'utilisation de cet outil.",
            "**This software is NOT a certified Medical Device (CE marking).**\n\n* **Decision support only:** Results generated by the AI module and physical estimations are for informational purposes only.\n* **Human responsibility:** The end user remains solely responsible for validating data, consulting official manufacturer manuals, and making the final decision.\n* **No warranty:** The author declines all responsibility for incidents resulting from the use of this tool."
        ))
        
    with c2:
        st.markdown(T("### © Droits d'Auteur & Propriété", "### © Copyright & Ownership"))
        st.info(T(
            "**Propriété Intellectuelle :**\n* Ce logiciel, son code source, son interface et son architecture sont la propriété exclusive de son auteur.\n* **Toute reproduction, distribution, revente ou modification** sans l'accord explicite de l'auteur est strictement interdite.\n* L'utilisation de ce logiciel est strictement limitée au cadre interne du service pour lequel il a été déployé.\n\n*Contact et propriété : magnetovault@gmail.com*",
            "**Intellectual Property:**\n* This software, its source code, interface, and architecture are the exclusive property of its author.\n* **Any reproduction, distribution, resale, or modification** without the author's explicit agreement is strictly prohibited.\n* The use of this software is strictly limited to the internal framework of the department for which it was deployed.\n\n*Contact and ownership: magnetovault@gmail.com*"
        ))
        
    st.divider()
    st.success(T("👈 **Sélectionnez le 'Module Sécurité DMI' dans le menu de gauche pour commencer.**", "👈 **Select the 'DMI Safety Module' in the left menu to start.**"))

# =========================================================
# PAGE 2 : MODULE SÉCURITÉ (L'application principale)
# =========================================================
elif page == T("🛡️ Module Sécurité DMI", "🛡️ DMI Safety Module"):
    st.title(T("🛡️ Module Clinique : Sécurité RF & Compatibilité DMI", "🛡️ Clinical Module: RF Safety & DMI Compatibility"))
    
    tab_rf, tab_dmi = st.tabs([
        T("📊 1. Moniteurs Physiques (SAR & B1+rms)", "📊 1. Physical Monitors (SAR & B1+rms)"),
        T("🦿 2. Assistant IA DMI & Rapports", "🦿 2. AI DMI Assistant & Reports")
    ])

    # =========================================================
    # ONGLET 1 : SÉCURITÉ PHYSIQUE
    # =========================================================
    with tab_rf:
        st.warning(T(
            "⚠️ **Simulateur Théorique :** Module reproduisant les contraintes de la norme (IEC 60601-2-33). **Ce module est éducatif et ne remplace pas les moniteurs réels du constructeur.**",
            "⚠️ **Theoretical Simulator:** Module reproducing the norm constraints (IEC 60601-2-33). **This module is educational and does not replace the manufacturer's real monitors.**"
        ))

        # --- 1. CONFIGURATION ---
        SAR_CALIB_FACTOR = 0.005
        k_sinc = T("Sinc (Standard 2D)", "Sinc (Standard 2D)")
        k_rect = T("Rect (Hard Pulse 3D)", "Rect (Hard Pulse 3D)")
        k_gauss = T("Gauss (Sélectif)", "Gauss (Selective)")

        PULSE_LIBRARY = {
            k_sinc:  {"factor": 1.0, "desc": T("Pour coupes 2D nettes", "For sharp 2D slices")},
            k_rect:  {"factor": 1.4, "desc": T("Pour volumes 3D rapides", "For fast 3D volumes")},
            k_gauss: {"factor": 0.7, "desc": T("Pour Saturation ou Inversion", "For Saturation or Inversion")}
        }
        
        RF_MODES = {"Low SAR": 0.8, "Normal": 1.0, "High Power": 1.2}

        # --- 2. ENTRÉES UTILISATEUR ---
        c_pat, c_seq, c_scan = st.columns(3)
        
        with c_pat:
            st.markdown(f"#### {T('👤 Patient', '👤 Patient')}")
            weight = st.number_input(T("Poids (kg)", "Weight (kg)"), 30.0, 150.0, 75.0, 5.0)
            height = st.number_input(T("Taille (m)", "Height (m)"), 1.0, 2.2, 1.75, 0.05)

        with c_seq:
            st.markdown(f"#### {T('📡 Séquence', '📡 Sequence')}")
            seq_type = st.selectbox(T("Type Séquence", "Sequence Type"), ["Spin Echo (SE)", "Turbo Spin Echo (TSE)", "Echo de Gradient (GRE)"])
            b0_val = st.radio(T("Champ Magnétique (B0)", "Magnetic Field (B0)"), [1.5, 3.0], horizontal=True)
            pulse_shape = st.selectbox(T("Forme Onde", "Waveform"), list(PULSE_LIBRARY.keys()), index=0)
            
            if "GRE" in seq_type:
                def_etl, def_ang = 0, 20
                label_angle = T("Angle d'Excitation (α)", "Excitation Angle (α)")
            elif "TSE" in seq_type: 
                def_etl, def_ang = 3, 180
                label_angle = T("Angle de Refoc (°)", "Refoc Angle (°)")
            else: 
                def_etl, def_ang = 0, 180
                label_angle = T("Angle de Refoc (°)", "Refoc Angle (°)")

            angle = st.slider(label_angle, 5, 180, def_ang)
            
            if "TSE" in seq_type:
                etl = st.slider(T("ETL (Facteur Turbo)", "ETL (Turbo Factor)"), 2, 64, def_etl)
            else:
                etl = 0
                st.slider("ETL", 0, 1, 0, disabled=True)

        with c_scan:
            st.markdown(f"#### {T('⚙️ Paramètres Scan', '⚙️ Scan Settings')}")
            tr = st.number_input("TR (ms)", 20, 10000, 600, 50)
            nb_slices = st.slider(T("Nombre de Coupes", "Number of Slices"), 1, 60, 20)
            rf_mode_name = st.select_slider("Mode RF", options=list(RF_MODES.keys()), value="Normal")
            rf_intensity = RF_MODES[rf_mode_name]

        st.divider()

        # --- 3. MOTEUR PHYSIQUE ---
        factor_b0 = (b0_val / 1.5) ** 2 
        energy_90 = 1.0 
        energy_angle_slider = (angle / 90.0) ** 2 
        
        if "GRE" in seq_type: total_energy_per_slice = energy_angle_slider 
        elif "TSE" in seq_type: total_energy_per_slice = energy_90 + (etl * energy_angle_slider) 
        else: total_energy_per_slice = energy_90 + (1 * energy_angle_slider) 
        
        total_energy_per_tr = total_energy_per_slice * nb_slices
        power_factor = total_energy_per_tr / (tr / 1000.0)
        factor_weight = 75.0 / weight
        factor_shape = PULSE_LIBRARY[pulse_shape]["factor"]
        
        sar_val = SAR_CALIB_FACTOR * factor_b0 * power_factor * factor_weight * rf_intensity * factor_shape
        
        peak_angle = angle 
        b1_peak_est = (peak_angle / 90.0) * 4.0 * rf_intensity 
        
        if "GRE" in seq_type: p_count = 1
        elif "TSE" in seq_type: p_count = 1 + etl
        else: p_count = 2
        
        duty_cycle = (p_count * nb_slices * 2.5) / tr 
        duty_cycle = min(duty_cycle, 1.0)
        b1_rms_ut = b1_peak_est * np.sqrt(duty_cycle) * factor_shape

        # --- 4. VISUALISATION ---
        st.subheader(T("📊 Moniteurs de Sécurité", "📊 Safety Monitors"))
        
        c_visu_g, c_visu_d = st.columns([1, 1])
        
        with c_visu_g:
            st.markdown(f"##### {T('📉 Profil RF & Charge', '📉 RF Profile & Load')}")
            fig_p, ax_p = plt.subplots(figsize=(5, 2.5))
            t_axis = np.linspace(-1, 1, 200)
            if "Rect" in pulse_shape: y_pulse = np.where(np.abs(t_axis)<0.5, 1, 0)
            elif "Sinc" in pulse_shape: y_pulse = np.sinc(t_axis * 3)
            else: y_pulse = np.exp(-t_axis**2 * 5)
                
            y_pulse = y_pulse * b1_peak_est
            ax_p.plot(t_axis, y_pulse, color='#8e44ad', lw=2)
            ax_p.fill_between(t_axis, y_pulse, color='#8e44ad', alpha=0.2)
            ax_p.set_ylim(0, max(10, b1_peak_est * 1.3))
            ax_p.set_yticks([]); ax_p.set_xticks([])
            ax_p.set_ylabel("B1 (µT)")
            ax_p.set_title(T(f"Pic B1: {b1_peak_est:.1f} µT (x{factor_b0:.0f} énergie à {b0_val}T)", f"B1 Peak: {b1_peak_est:.1f} µT"), fontsize=9, color='gray')
            st.pyplot(fig_p); plt.close(fig_p)
            
            if b0_val == 3.0:
                st.error(T("⚠️ **ATTENTION 3T** : Énergie x4 par rapport à 1.5T.", "⚠️ **WARNING 3T**: Energy x4."))

        with c_visu_d:
            def draw_gauge_cursor(value, label, limit_norm, limit_first, max_scale=6.0):
                fig, ax = plt.subplots(figsize=(6, 2))
                ax.add_patch(plt.Rectangle((0, 0), limit_norm, 1, color='#2ecc71', alpha=0.9))
                ax.text(limit_norm/2, 0.5, "NORMAL", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
                ax.add_patch(plt.Rectangle((limit_norm, 0), limit_first-limit_norm, 1, color='#f1c40f', alpha=0.9))
                ax.text((limit_norm+limit_first)/2, 0.5, "LEVEL 1", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
                ax.add_patch(plt.Rectangle((limit_first, 0), max_scale-limit_first, 1, color='#e74c3c', alpha=0.9))
                ax.text((limit_first+max_scale)/2, 0.5, "STOP", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
                
                cursor_pos = min(value, max_scale - 0.1)
                ax.plot([cursor_pos, cursor_pos], [-0.2, 1.2], color='black', linewidth=4)
                ax.text(cursor_pos, 1.35, f"{value:.2f}", ha='center', fontweight='bold', fontsize=12, color='black')
                ax.set_xlim(0, max_scale); ax.set_ylim(0, 1.6); ax.axis('off')
                ax.set_title(label, loc='left', fontweight='bold')
                return fig

            st.pyplot(draw_gauge_cursor(sar_val, T("SAR Global (W/kg)", "Global SAR (W/kg)"), 2.0, 4.0))
            st.pyplot(draw_gauge_cursor(b1_rms_ut, "B1+rms (µT)", 2.8, 4.0))

        st.divider()
        
        # --- 5. FORMULES & GLOSSAIRES ---
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.markdown(f"#### {T('🌡️ Calcul du SAR', '🌡️ SAR Calculation')}")
            st.latex(r"SAR \propto B_0^2 \times E_{totale} \times \frac{1}{TR \cdot Poids}")
        with c_f2:
            st.markdown(f"#### {T('⚡ Calcul du B1+rms', '⚡ B1+rms Calculation')}")
            st.latex(r"B_{1}^{+rms} \propto B_{1,peak} \times \sqrt{DC}")

        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            with st.expander(T("📖 Facteurs SAR (Détails)", "📖 SAR Factors (Details)")):
                 st.info(T(
                     "**Pourquoi le SAR est CALCULÉ ?**\nLe SAR (Débit d'Absorption Spécifique) mesure l'échauffement des tissus. Il est mathématiquement **calculé** car il est impossible à mesurer directement in vivo. Ce calcul dépend obligatoirement de la morphologie du patient (poids), du champ statique (B0) et du modèle thermique du constructeur.",
                     "**Why is SAR CALCULATED?**\nSAR measures tissue heating. It is mathematically **calculated** because it's impossible to measure directly in vivo. This calculation strictly depends on patient morphology (weight), static field (B0), and the manufacturer's thermal model."
                 ))
                 if "GRE" in seq_type:
                    st.markdown(T("""
                    * **Type** : Écho de Gradient (GRE).
                    * **Énergie** : Une seule impulsion d'excitation (Angle variable de **5° à 90°**).
                    * **Analyse** : Le SAR est réduit car il n'y a **pas de train d'impulsions de refocalisation**.
                    """, """
                    * **Type**: Gradient Echo (GRE).
                    * **Energy**: Single excitation pulse (Variable angle **5° to 90°**).
                    * **Analysis**: SAR is low because there is **no refocusing pulse train**.
                    """))
                 else:
                    st.markdown(T(f"""
                    * **Type** : Spin Echo / TSE.
                    * **Énergie** : Excitation 90° (Fixe) + Refocalisations {angle}° (Variable).
                    * **Poids du 180°** : Un pulse 180° chauffe **4x** plus qu'un 90°.
                    """, f"""
                    * **Type**: Spin Echo / TSE.
                    * **Energy**: Excitation 90° (Fixed) + Refocusing {angle}° (Variable).
                    * **Weight of 180°**: A 180° pulse heats **4x** more than a 90°.
                    """))
                    
        with c_exp2:
            with st.expander(T("📖 Facteurs B1+rms (Détails)", "📖 B1+rms Factors (Details)")):
                 st.info(T(
                     "**Pourquoi le B1+rms est ESTIMÉ ?**\nLe B1+rms représente l'amplitude moyenne du champ magnétique RF. Il est **estimé** car c'est une grandeur physique pure (en µT) générée par l'antenne. **Il est indépendant du poids ou de l'anatomie du patient**.",
                     "**Why is B1+rms ESTIMATED?**\nB1+rms represents the average amplitude of the RF magnetic field. It is **estimated** because it's a pure physical quantity (in µT) generated by the coil. **It is independent of patient weight or anatomy**."
                 ))
                 if "GRE" in seq_type:
                    st.markdown(T("""
                    * **B1 Peak** : Dépend de l'angle d'excitation.
                    * **Duty Cycle** : Très faible (1 pulse par TR).
                    """, """
                    * **B1 Peak**: Depends on excitation angle.
                    * **Duty Cycle**: Very low (1 pulse per TR).
                    """))
                 else:
                    st.markdown(T("""
                    * **B1 Peak** : Intensité des pulses de refocalisation.
                    * **Duty Cycle** : Élevé en TSE (mitraillage).
                    """, """
                    * **B1 Peak**: Refocusing pulse intensity.
                    * **Duty Cycle**: High in TSE (rapid firing).
                    """))
        
        st.divider()
        
        with st.expander(T("📝 Seuils & Paramètres IEC", "📝 IEC Thresholds & Parameters"), expanded=False):
            st.markdown(T("""
            * 🟢 :green[**Mode Normal**] : **< 2.0 W/kg** (Routine Clinique, aucun risque).
            * 🟠 :orange[**Mode Contrôlé (Niveau 1)**] : **2.0 - 4.0 W/kg** (Surveillance médicale requise).
            * 🔴 :red[**Mode Restreint (Niveau 2)**] : **> 4.0 W/kg** (Blocage logiciel, risque d'échauffement > 1°C).
            """, """
            * 🟢 :green[**Normal Mode**]: **< 2.0 W/kg** (Clinical Routine, no risk).
            * 🟠 :orange[**First Level Mode**]: **2.0 - 4.0 W/kg** (Medical supervision required).
            * 🔴 :red[**Second Level Mode**]: **> 4.0 W/kg** (Software lockout, heating risk > 1°C).
            """))

        with st.expander(T("🏥 Clinique : Formes d'Impulsions & Séquences", "🏥 Clinical: Pulse Shapes & Sequences"), expanded=False):
            st.markdown(T("""
            | Forme | Usage Principal | Avantage | Risque / Inconvénient |
            | :--- | :--- | :--- | :--- |
            | **Sinc** | **TSE, SE (2D)** | Profil de coupe rectangulaire (Pas de croisement). | **SAR Élevé** (Impulsions longues & nombreuses). |
            | **Rectangulaire** | **MP-RAGE (3D)** | Ultra-rapide (TR court). | Coupe "sale" (bords flous) - corrigé par encodage 3D. |
            | **Gaussienne** | **Fat Sat** | Très sélectif en fréquence. | **Pic B1 Élevé** (Stress sur l'ampli RF). |
            """, """
            | Shape | Main Usage | Advantage | Risk / Drawback |
            | :--- | :--- | :--- | :--- |
            | **Sinc** | **TSE, SE (2D)** | Rectangular slice profile (No crosstalk). | **High SAR** (Long & numerous pulses). |
            | **Rectangular** | **MP-RAGE (3D)** | Ultra-fast (Short TR). | "Dirty" slice (blurred edges) - corrected by 3D encoding. |
            | **Gaussian** | **Fat Sat** | Highly frequency selective. | **High B1 Peak** (RF Amp Stress). |
            """))

        with st.expander(T("🎯 Guide Pratique : Impact des Paramètres", "🎯 Quick Guide: Parameters Impact"), expanded=True):
            st.markdown(T("""
            Ce tableau résume le comportement des paramètres d'acquisition sur les deux moniteurs de sécurité.
            
            | Paramètre | Action | Impact sur le SAR (Chaleur) | Impact sur le B1+rms (Implant) |
            | :--- | :--- | :--- | :--- |
            | ⚖️ **Poids (Weight)** | ⬆️ Augmentation | ⬇️ **Baisse** (Énergie diluée dans la masse) | ➖ **Aucun effet** (Grandeur matérielle) |
            | 📏 **Taille (Height)** | ⬆️ Augmentation | ➖ **Aucun effet direct** | ➖ **Aucun effet direct** |
            | 📡 **Type Séquence** | GRE ➔ SE ➔ TSE | ⬆️ **Forte Augmentation** (Nb d'impulsions ↗) | ⬆️ **Augmentation** (Duty Cycle ↗) |
            | 🧲 **Champ B0** | 1.5T ➔ 3.0T | ⬆️ **Quadruple (x4)** | ➖ **Aucun effet direct** (Le seuil reste en µT) |
            | 〰️ **Forme Onde** | Rect ➔ Sinc ➔ Gauss | ⬆️ **Augmentation** (Énergie de l'impulsion ↗) | ⬆️ **Augmentation** (Pic B1 ↗) |
            | 📐 **Angle (α)** | ⬆️ Augmentation | ⬆️ **Forte Augmentation (x²)** | ⬆️ **Augmentation directe** |
            | 🚀 **ETL (Turbo)** | ⬆️ Augmentation | ⬆️ **Augmentation** (Mitraillage RF) | ⬆️ **Augmentation** (Duty Cycle ↗) |
            | ⏱️ **TR** | ⬆️ Augmentation | ⬇️ **Baisse** (Plus de temps de refroidissement)| ⬇️ **Baisse** (Duty Cycle ↘) |
            | 🍕 **Nb Coupes** | ⬆️ Augmentation | ⬆️ **Augmentation** (Plus d'impulsions par TR) | ⬆️ **Augmentation** (Duty Cycle ↗) |
            | 🔋 **Mode RF** | Low ➔ Normal ➔ High | ⬆️ **Augmentation** | ⬆️ **Augmentation** |
            
            *💡 **L'astuce du Manipulateur :** Pour faire baisser le **B1+rms** d'une séquence TSE récalcitrante, le moyen le plus efficace est d'augmenter le **TR** ou de baisser l'angle de refocalisation (ex: 120° au lieu de 180°).*
            """, """
            This table summarizes the behavior of acquisition parameters on both safety monitors.
            
            | Parameter | Action | Impact on SAR (Heating) | Impact on B1+rms (Implant) |
            | :--- | :--- | :--- | :--- |
            | ⚖️ **Weight** | ⬆️ Increase | ⬇️ **Decreases** (Energy diluted in mass) | ➖ **No effect** (Hardware quantity) |
            | 📏 **Height** | ⬆️ Increase | ➖ **No effect directly** | ➖ **No effect directly** |
            | 📡 **Sequence Type**| GRE ➔ SE ➔ TSE | ⬆️ **Strong Increase** (Nb of pulses ↗) | ⬆️ **Increases** (Duty Cycle ↗) |
            | 🧲 **B0 Field** | 1.5T ➔ 3.0T | ⬆️ **Quadruples (x4)** | ➖ **No effect directly** (Threshold stays in µT) |
            | 〰️ **Waveform** | Rect ➔ Sinc ➔ Gauss | ⬆️ **Increases** (Pulse energy ↗) | ⬆️ **Increases** (B1 Peak ↗) |
            | 📐 **Angle (α)** | ⬆️ Increase | ⬆️ **Strong Increase (x²)** | ⬆️ **Direct Increase** |
            | 🚀 **ETL (Turbo)** | ⬆️ Increase | ⬆️ **Increases** (RF rapid firing) | ⬆️ **Increases** (Duty Cycle ↗) |
            | ⏱️ **TR** | ⬆️ Increase | ⬇️ **Decreases** (More cooling time) | ⬇️ **Decreases** (Duty Cycle ↘) |
            | 🍕 **Nb Slices** | ⬆️ Increase | ⬆️ **Increases** (More pulses per TR) | ⬆️ **Increases** (Duty Cycle ↗) |
            | 🔋 **RF Mode** | Low ➔ Normal ➔ High | ⬆️ **Increases** | ⬆️ **Increases** |
            
            *💡 **Tech Tip:** To lower the **B1+rms** of a stubborn TSE sequence, the most effective way is to increase the **TR** or lower the refocusing angle (e.g., 120° instead of 180°).*
            """))

    # =========================================================
    # ONGLET 2 : ASSISTANT IA & DMI
    # =========================================================
    with tab_dmi:
        st.error(T(
            "⚠️ **AVERTISSEMENT CLINIQUE :** Ce module exige votre validation humaine. L'IA facilite la recherche, mais **VOUS** êtes responsable de la vérification finale et de la saisie des données.",
            "⚠️ **CLINICAL WARNING:** This module requires human validation. The AI facilitates research, but **YOU** are responsible for final verification and data entry."
        ))
        
        if "etape_dmi" not in st.session_state: st.session_state.etape_dmi = 0
        if "nom_dmi_memoire" not in st.session_state: st.session_state.nom_dmi_memoire = ""
        if "sources_ia" not in st.session_state: st.session_state.sources_ia = ""
        
        # --- ÉTAPE 1 : IDENTIFICATION ---
        st.markdown(T("### 1️⃣ Identification du dispositif", "### 1️⃣ Device Identification"))
        nom_dmi = st.text_input(T("Saisissez un Nom, Modèle ou Réf/Lot :", "Enter a Name, Model, or Ref/Lot:"), placeholder="Ex: Medtronic Advisa, Nucleus 7...", key="input_nom_dmi")
        
        st.markdown(T("**📄 Preuve visuelle de la carte (Optionnel) :**", "**📄 Visual proof of the card (Optional):**"))
        
        onglets_img1, onglets_img2, onglets_img3 = st.tabs([T("📁 Parcourir", "📁 Browse"), T("📸 Appareil Photo", "📸 Camera"), T("📋 Coller (Presse-papier)", "📋 Paste (Clipboard)")])
        
        with onglets_img1:
            fichier_preuve = st.file_uploader(T("Glissez ou sélectionnez une image :", "Drag or select an image:"), type=['png', 'jpg', 'jpeg'], key="input_file_dmi")
        
        with onglets_img2:
            st.info(T("🔒 Pour des raisons de confidentialité, la caméra est désactivée par défaut.", "🔒 For privacy reasons, the camera is disabled by default."))
            activer_camera = st.toggle(T("🎥 Activer l'appareil photo", "🎥 Enable camera"), key="toggle_cam")
            photo_camera = None
            if activer_camera:
                photo_camera = st.camera_input(T("Prendre une photo de la carte du patient :", "Take a picture of the patient's card:"), key="camera_dmi")

        with onglets_img3:
            st.info(T("Copiez une image (Ctrl+C) puis cliquez sur le bouton ci-dessous :", "Copy an image (Ctrl+C) then click the button below:"))
            image_collee = paste_image_button(
                label="📋 Coller l'image" if st.session_state.lang == 'fr' else "📋 Paste image",
                background_color="#4A86e8",
                hover_background_color="#205b9f",
                text_color="#ffffff"
            )
            if image_collee.image_data is not None:
                st.success(T("✅ Image collée avec succès !", "✅ Image pasted successfully!"))
                st.image(image_collee.image_data, width=250)

        image_fournie = None
        if fichier_preuve:
            image_fournie = fichier_preuve
        elif photo_camera:
            image_fournie = photo_camera
        elif image_collee.image_data is not None:
            image_fournie = image_collee.image_data

        if nom_dmi != st.session_state.nom_dmi_memoire:
            st.session_state.nom_dmi_memoire = nom_dmi
            st.session_state.etape_dmi = 0

        if st.button(T("🔍 1. Rechercher le constructeur et les accès", "🔍 1. Search manufacturer & access"), use_container_width=True):
            if nom_dmi or image_fournie:
                st.session_state.etape_dmi = 1
                with st.spinner(T("Analyse approfondie et recherche en cours...", "In-depth analysis and search in progress...")):
                    
                    prompt_sources = f"""
                    Agis comme un moteur de recherche ultra-précis spécialisé en dispositifs médicaux implantables (DMI). 
                    Nom saisi : "{nom_dmi if nom_dmi else "Aucun texte saisi. LIS L'IMAGE CI-JOINTE."}"
                    
                    MISSION :
                    1. Extraire Fabricant et Modèle.
                    2. Générer une stratégie de recherche "anti-lien mort" en 3 options (Portail IRM, Accueil, Recherche Google).
                    """
                    
                    contenu_etape1 = [prompt_sources]
                    
                    if image_fournie:
                        try:
                            if isinstance(image_fournie, Image.Image):
                                img = image_fournie
                            else:
                                image_fournie.seek(0)
                                img = Image.open(image_fournie)
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            contenu_etape1.append(img)
                        except Exception as e:
                            st.error(f"Erreur image : {e}")

                    try:
                        reponse_src = client.models.generate_content(model='gemini-2.5-flash', contents=contenu_etape1)
                        st.session_state.sources_ia = reponse_src.text
                    except Exception as e:
                        st.error(f"Erreur IA : {e}")
            else:
                st.warning(T("Veuillez saisir un nom ou fournir une photo.", "Please enter a name or provide a photo."))
                
        if st.session_state.etape_dmi >= 1:
            st.markdown(st.session_state.sources_ia)
            st.divider()