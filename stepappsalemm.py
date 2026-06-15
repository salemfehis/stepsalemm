
import streamlit as st
import pandas as pd
import math

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="STEP - Dimensionnement",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS GLOBAL
# =========================================================
st.markdown("""
<style>
/* ======================================================
   FOND GÉNÉRAL
   ====================================================== */
.stApp { background-color: #f0f4f8; }

/* ======================================================
   TOUT LE TEXTE EN NOIR — règle universelle
   ====================================================== */
.stApp *:not([data-testid="stSidebar"]):not([data-testid="stSidebar"] *) {
    color: #111111 !important;
}

/* ======================================================
   INPUTS : valeurs affichées dans les champs
   ====================================================== */
input, textarea, select,
.stNumberInput input,
.stTextInput input,
[data-baseweb="input"] input,
[data-baseweb="select"] *,
[data-baseweb="textarea"] textarea {
    color: #111111 !important;
    background-color: #ffffff !important;
}

/* ======================================================
   SLIDER : valeur courante + labels min/max
   ====================================================== */
[data-testid="stSlider"] *,
[data-testid="stSlider"] span,
[data-testid="stSlider"] div,
[data-testid="stSlider"] p {
    color: #111111 !important;
}

/* ======================================================
   SELECTBOX / DROPDOWN options
   ====================================================== */
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
ul[data-testid="stSelectboxVirtualDropdown"] * {
    color: #111111 !important;
    background-color: #ffffff !important;
}

/* ======================================================
   RADIO buttons texte
   ====================================================== */
.stRadio label p,
.stRadio > label,
[data-testid="stWidgetLabel"] p {
    color: #111111 !important;
}

/* ======================================================
   SIDEBAR — blanc sur fond bleu
   ====================================================== */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d3b66 0%, #1a6496 100%) !important;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
[data-testid="stSidebar"] input {
    color: #111111 !important;
    background: #ffffff !important;
}

/* ======================================================
   TITRES
   ====================================================== */
h1 { color: #0d3b66 !important; font-size: 1.8rem !important; }
h2 { color: #1a6496 !important; border-left: 4px solid #1a9fd4; padding-left: 10px; }
h3 { color: #1a6496 !important; }

/* ======================================================
   METRIC CARDS
   ====================================================== */
[data-testid="stMetric"] {
    background: white !important;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-top: 3px solid #1a9fd4;
}
[data-testid="stMetricValue"] { color: #0d3b66 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #333333 !important; }
[data-testid="stMetricDelta"] { color: #1a9fd4 !important; }

/* ======================================================
   DATAFRAMES
   ====================================================== */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
[data-testid="stDataFrame"] * { color: #111111 !important; }

/* ======================================================
   TABS
   ====================================================== */
[data-baseweb="tab"] * { color: #111111 !important; }
[data-baseweb="tab"][aria-selected="true"] * { color: #0d3b66 !important; font-weight: 700 !important; }

/* ======================================================
   BOUTONS
   ====================================================== */
.stButton > button {
    background: linear-gradient(90deg, #1a6496, #1a9fd4) !important;
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    transition: 0.3s;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

/* ======================================================
   ALERTES
   ====================================================== */
.stSuccess, .stWarning, .stInfo, .stError { border-radius: 8px; }

/* ======================================================
   DIVIDER
   ====================================================== */
.section-divider {
    margin: 32px 0 16px;
    border: none;
    border-top: 2px dashed #c8dff0;
}

/* ======================================================
   BADGE SECTION
   ====================================================== */
.section-badge {
    display: inline-block;
    background: #1a6496;
    color: white !important;
    border-radius: 20px;
    padding: 2px 14px;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("## 💧 STEP Dimensionnement")
    st.markdown("---")
    section = st.radio(
        "Navigation",
        [
            "🏠 Accueil",
            "1 · Démographie & Débits",
            "2 · Ouvrages de prétraitement",
            "3 · Traitement primaire",
            "4 · Traitement biologique",
            "5 · Décanteur secondaire",
            "6 · Bilan & Normes",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<small>Outil de dimensionnement hydraulique et biologique d'une STEP</small>",
        unsafe_allow_html=True
    )

# =========================================================
# HELPER
# =========================================================
def section_header(num, title, icon="🔵"):
    st.markdown(f'<span class="section-badge">ÉTAPE {num}</span>', unsafe_allow_html=True)
    st.header(f"{icon} {title}")

def hline():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# =========================================================
# PAGE : ACCUEIL
# =========================================================
if section == "🏠 Accueil":

    # ---- Bandeau projet ----
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d3b66 0%, #1a6496 60%, #1a9fd4 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(13,59,102,0.18);
    ">
        <div style="display:flex; align-items:center; gap:18px; flex-wrap:wrap;">
            <img src="data:image/png;base64,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" style="width:80px; height:80px; border-radius:50%; border:3px solid rgba(255,255,255,0.5); object-fit:cover; flex-shrink:0;">
            <div>
                <div style="color:#ffffff; font-size:0.82rem; letter-spacing:2px; font-weight:600; opacity:0.85; text-transform:uppercase;">
                    École Nationale Supérieure d'Hydraulique
                </div>
                <div style="color:#ffffff; font-size:1.7rem; font-weight:800; margin:4px 0 2px;">
                    Projet de Fin d'Études
                </div>
                <div style="color:#a8d8f0; font-size:1.05rem; font-weight:500;">
                    Dimensionnement d'une Station d'Épuration des Eaux Usées (STEP)
                </div>
            </div>
            <div style="margin-left:auto; text-align:right;">
                <div style="
                    background: rgba(255,255,255,0.15);
                    border: 1px solid rgba(255,255,255,0.3);
                    border-radius: 10px;
                    padding: 10px 20px;
                    color: white;
                    font-size:0.95rem;
                ">
                    <div style="font-weight:700; font-size:1.1rem;">Promo 2026</div>
                    <div style="opacity:0.85; font-size:0.8rem;">LDL · HV · ENSH</div>
                    <div style="margin-top:8px; padding-top:8px; border-top:1px solid rgba(255,255,255,0.3); font-size:0.82rem; opacity:0.9;">
                        Réalisé par<br><strong>Fehis Salem Abdelhak</strong>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.title("💧 Station d'Épuration des Eaux Usées")
    st.markdown(
        '<p style="color:#111111; font-size:1.15rem; font-weight:600; margin-top:-8px;">'
        'Outil de dimensionnement complet</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="color:#111111; font-size:1rem;">'
        'Bienvenue dans l\'outil de dimensionnement d\'une <strong>STEP</strong> '
        '(Station d\'Épuration des Eaux Usées). '
        'Cet outil vous guide à travers toutes les étapes de calcul, '
        'de l\'étude démographique jusqu\'à la vérification des normes de rejet.'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:3px solid #1a9fd4;">
        <p style="color:#0d3b66; font-size:1rem; font-weight:700; margin-bottom:10px;">📊 Étapes couvertes</p>
        <p style="color:#111111; line-height:1.8; margin:0;">
        • Étude démographique<br>
        • Calcul des débits<br>
        • Dégrillage (Kirschmer)<br>
        • Dessableur / Déshuileur<br>
        • Décanteur primaire &amp; secondaire
        </p></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:3px solid #1a9fd4;">
        <p style="color:#0d3b66; font-size:1rem; font-weight:700; margin-bottom:10px;">⚙️ Traitement biologique</p>
        <p style="color:#111111; line-height:1.8; margin:0;">
        • Bassin biologique<br>
        • Bassin d'anoxie<br>
        • Bassin d'aération<br>
        • Besoins en O₂<br>
        • Déphosphatation
        </p></div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:3px solid #1a9fd4;">
        <p style="color:#0d3b66; font-size:1rem; font-weight:700; margin-bottom:10px;">✅ Vérifications</p>
        <p style="color:#111111; line-height:1.8; margin:0;">
        • Bilans polluants<br>
        • Rendements d'élimination<br>
        • Charges en sortie<br>
        • Conformité aux normes<br>
        • DBO / DCO / MES / P / NO₃
        </p></div>
        """, unsafe_allow_html=True)

    st.info("👈 Utilisez le menu de navigation à gauche pour accéder à chaque section.")
    st.stop()

# =========================================================
# ---- CALCULS GLOBAUX (toujours exécutés) ----
# Ces calculs sont nécessaires pour toutes les sections
# =========================================================

# ===== POPULATION =====
with st.sidebar.expander("⚙️ Paramètres de base", expanded=False):
    P0      = st.number_input("Population de référence", value=126971, key="P0_s")
    t       = st.number_input("Taux d'accroissement (%)", value=1.9, key="t_s") / 100
    annee_ref = st.number_input("Année de référence", value=2026, key="yr_s")
    dot0    = st.number_input("Dotation Réf (L/j/hab)", value=150, key="d0_s")
    dot10   = st.number_input("Dotation +10 ans", value=180, key="d10_s")
    dot30   = st.number_input("Dotation +30 ans", value=200, key="d30_s")

def population(P0, t, n):
    return P0 * (1 + t) ** n

def debit(P, dot):
    return (P * dot) / 1000

def total(Qd, Qe, Qi):
    Q_j = Qd + Qe + Qi
    return Q_j, Q_j/24, Q_j/86400, Q_j*1000

def qp(Qs):
    Qls = Qs * 1000
    Kp  = 3 if Qls < 2.8 else 1.5 + 2.5 / (Qls ** 0.5)
    Qp  = Kp * Qs
    return Kp, Qp, Qp * 86400

annee0  = annee_ref
annee10 = annee_ref + 10
annee30 = annee_ref + 30

P0_h  = population(P0, t, 0)
P10_h = population(P0, t, 10)
P30_h = population(P0, t, 30)

Q0  = debit(P0_h,  dot0)
Q10 = debit(P10_h, dot10)
Q30 = debit(P30_h, dot30)

# Coefficient de rejet (sidebar)
with st.sidebar.expander("🔄 Coefficient de rejet", expanded=False):
    mode_rejet = st.radio("Mode K_rejet", ["Auto", "Manuel"], key="krej_mode")
    if mode_rejet == "Auto":
        etat = st.selectbox("État du réseau", ["Bon", "Moyen", "Mauvais"], key="etat_res")
        Krej = {"Bon": 0.9, "Moyen": 0.8, "Mauvais": 0.7}[etat]
    else:
        Krej = st.number_input("Krej (0–1)", value=0.8, key="krej_val")

Q0_k  = Q0  * Krej
Q10_k = Q10 * Krej
Q30_k = Q30 * Krej

# Équipements
with st.sidebar.expander("🏢 Équipements & Industrie", expanded=False):
    mode_eq = st.radio("Mode équipements", ["Auto", "Manuel"], key="eq_mode")
    if mode_eq == "Auto":
        niv_eq = st.selectbox("Niveau équipements", ["Faible", "Moyen", "Fort"], key="niv_eq")
        p_eq   = {"Faible": 0.15, "Moyen": 0.25, "Fort": 0.35}[niv_eq]
    else:
        p_eq = st.number_input("Équip. (%)", value=20.0, step=0.1, format="%.2f", key="peq_v") / 100

    mode_ind = st.radio("Mode industrie", ["Auto", "Manuel"], key="ind_mode")
    if mode_ind == "Auto":
        niv_ind = st.selectbox("Niveau industriel", ["Aucun", "Faible", "Moyen", "Fort"], key="niv_ind")
        p_ind   = {"Aucun": 0.0, "Faible": 0.05, "Moyen": 0.10, "Fort": 0.15}[niv_ind]
    else:
        p_ind = st.number_input("Industrie (%)", value=10.0, step=0.1, format="%.2f", key="pind_v") / 100

Qeq0  = Q0_k  * p_eq;  Qeq10 = Q10_k * p_eq;  Qeq30 = Q30_k * p_eq
Qind0 = Q0_k  * p_ind; Qind10= Q10_k * p_ind;  Qind30= Q30_k * p_ind

T0  = total(Q0_k,  Qeq0,  Qind0)
T10 = total(Q10_k, Qeq10, Qind10)
T30 = total(Q30_k, Qeq30, Qind30)

K0, Qp0, Qpj0   = qp(T0[2])
K10, Qp10, Qpj10 = qp(T10[2])
K30, Qp30, Qpj30 = qp(T30[2])

# Coefficient pluie (sidebar)
with st.sidebar.expander("🌧️ Pluie", expanded=False):
    Cpluie = st.selectbox("Coefficient de pluie", [3, 4, 5], key="cpluie_s")

def q_pluie(Qpts_j):
    Qptp_j = Cpluie * Qpts_j
    return Qptp_j, Qptp_j/24, Qptp_j/86400

Qptp0  = q_pluie(Qpj0)
Qptp10 = q_pluie(Qpj10)
Qptp30 = q_pluie(Qpj30)

# Equivalent habitant
COEFF_REJET = 0.8
def equivalent_habitant(Q_m3j, dotation):
    return (Q_m3j * 1000) / (dotation * COEFF_REJET)

Neq0  = equivalent_habitant(T0[0],  dot0)
Neq10 = equivalent_habitant(T10[0], dot10)
Neq30 = equivalent_habitant(T30[0], dot30)

# Paramètres pollution (sidebar)
with st.sidebar.expander("🧪 Paramètres pollution", expanded=False):
    conductivite = st.number_input("Conductivité (mS/cm)", value=2.88, key="cond_s")
    MES  = st.number_input("MES (mg/L)",       value=378.0,  key="mes_s")
    DCO  = st.number_input("DCO (mg O2/L)",    value=819.0,  key="dco_s")
    DBO5 = st.number_input("DBO5 (mg O2/L)",   value=351.0,  key="dbo5_s")
    P    = st.number_input("Phosphore (mg/L)",  value=7.77,   key="p_s")
    NTK  = st.number_input("NTK (mg/L)",        value=64.0,   key="ntk_s")

def charge_polluante(C, Q):
    return C * Q * 1e-3

Q_2026 = T0[0]; Q_2036 = T10[0]; Q_2056 = T30[0]

L_mes_2036 = charge_polluante(MES,  Q_2036); L_mes_2056 = charge_polluante(MES,  Q_2056)
L_dco_2036 = charge_polluante(DCO,  Q_2036); L_dco_2056 = charge_polluante(DCO,  Q_2056)
L_dbo_2036 = charge_polluante(DBO5, Q_2036); L_dbo_2056 = charge_polluante(DBO5, Q_2056)
L_p_2036   = charge_polluante(P,    Q_2036); L_p_2056   = charge_polluante(P,    Q_2056)
L_ntk_2036 = charge_polluante(NTK,  Q_2036); L_ntk_2056 = charge_polluante(NTK,  Q_2056)

# Décanteur primaire – taux élimination (sidebar)
with st.sidebar.expander("🏗️ Décanteur primaire – rendements", expanded=False):
    taux_mes = st.slider("Rendement MES (%)", 50, 70, 70, 5, key="rend_mes_s") / 100
    taux_dbo = st.slider("Rendement DBO5 (%)", 25, 40, 35, 5, key="rend_dbo_s") / 100

# MES flow through dessableur/déshuileur
def calc_mes_elim(L_mes):
    MM  = L_mes * 0.317; MVS = L_mes * 0.683
    MM_elim  = MM * 0.7
    MM_sortie = MM - MM_elim
    return MVS + MM_sortie

MES_entree_2036 = calc_mes_elim(L_mes_2036)
MES_entree_2056 = calc_mes_elim(L_mes_2056)

DBO5_entree_2036 = L_dbo_2036; DBO5_entree_2056 = L_dbo_2056

DBO5_sortie_2036 = DBO5_entree_2036 * (1 - taux_dbo)
DBO5_sortie_2056 = DBO5_entree_2056 * (1 - taux_dbo)
MES_sortie_DP_2036 = MES_entree_2036 * (1 - taux_mes)
MES_sortie_DP_2056 = MES_entree_2056 * (1 - taux_mes)

# Bassin biologique
DBO_entree_2036 = DBO5_sortie_2036; DBO_entree_2056 = DBO5_sortie_2056
Cf = 30
DBO_sortie_2036 = Cf * Q10 * 1e-3; DBO_sortie_2056 = Cf * Q30 * 1e-3

L0_2036 = DBO_entree_2036; Lf_2036 = DBO_sortie_2036; Le_2036 = L0_2036 - Lf_2036
L0_2056 = DBO_entree_2056; Lf_2056 = DBO_sortie_2056; Le_2056 = L0_2056 - Lf_2056

R_2036 = (Le_2036 / L0_2036) * 100
R_2056 = (Le_2056 / L0_2056) * 100

# Cm / Cv (sidebar)
with st.sidebar.expander("🔬 Bassin biologique – Cm/Cv", expanded=False):
    def classify(R):
        if R > 90: return "Faible charge"
        elif 80 <= R <= 90: return "Moyenne charge"
        elif 60 <= R < 80: return "Forte charge"
        else: return "Indéterminé"
    mode_bassin = st.selectbox("Type de fonctionnement", ["Faible charge", "Moyenne charge", "Forte charge"], key="mode_b")
    if mode_bassin == "Faible charge":
        Cm = st.slider("Cm", 0.1, 0.2, 0.15, 0.01, key="cm_f"); Cv = st.slider("Cv", 0.3, 0.8, 0.6, 0.05, key="cv_f")
    elif mode_bassin == "Moyenne charge":
        Cm = st.slider("Cm", 0.2, 0.5, 0.3, 0.01, key="cm_m"); Cv = st.slider("Cv", 0.8, 1.8, 1.2, 0.05, key="cv_m")
    else:
        Cm = st.slider("Cm", 0.5, 1.0, 0.7, 0.01, key="cm_s"); Cv = st.slider("Cv", 1.8, 2.5, 2.0, 0.05, key="cv_s")

# Déphosphatation
P_norme = 2
P_in_2036  = charge_polluante(P, Q_2036); P_in_2056  = charge_polluante(P, Q_2056)
P_norm_2036 = charge_polluante(P_norme, Q_2036); P_norm_2056 = charge_polluante(P_norme, Q_2056)
P_elim_2036 = max(P_in_2036 - P_norm_2036, 0); P_elim_2056 = max(P_in_2056 - P_norm_2056, 0)

Fe_P_ratio=1.2; MFe=56; MP=31; MFeOH3=107; MFePO4=150
Fe_2036 = Fe_P_ratio*(MFe/MP)*P_elim_2036; Fe_2056 = Fe_P_ratio*(MFe/MP)*P_elim_2056
FePO4_2036=(MFePO4/MP)*P_elim_2036; FePO4_2056=(MFePO4/MP)*P_elim_2056
Fe_exces_2036=Fe_2036-(MFe/MP)*P_elim_2036; Fe_exces_2056=Fe_2056-(MFe/MP)*P_elim_2056
FeOH3_2036=(MFeOH3/MFe)*Fe_exces_2036; FeOH3_2056=(MFeOH3/MFe)*Fe_exces_2056
Boues_2036=FePO4_2036+FeOH3_2036; Boues_2056=FePO4_2056+FeOH3_2056

# Bilan azote
NTK_entree_2036 = NTK*Q_2036*1e-3; NTK_entree_2056 = NTK*Q_2056*1e-3
Nopr_2036=0.02*NTK_entree_2036; Nopr_2056=0.02*NTK_entree_2056
Nass_2036=0.05*L0_2036; Nass_2056=0.05*L0_2056
NH4_conc=2
NH4_rejet_2036=NH4_conc*Q_2036*1e-3; NH4_rejet_2056=NH4_conc*Q_2056*1e-3
N_nitrifie_2036=NTK_entree_2036-Nopr_2036-Nass_2036-NH4_rejet_2036
N_nitrifie_2056=NTK_entree_2056-Nopr_2056-Nass_2056-NH4_rejet_2056
NO3_conc=30
NO3_rejet_2036=NO3_conc*Q_2036*1e-3; NO3_rejet_2056=NO3_conc*Q_2056*1e-3
N_denitrifie_2036=N_nitrifie_2036-NO3_rejet_2036
N_denitrifie_2056=N_nitrifie_2056-NO3_rejet_2056
Xa_2036=L0_2036/Cm; Xa_2056=L0_2056/Cm
V_bio_2036=L0_2036/Cv; V_bio_2056=L0_2056/Cv
CMVS_2036=L0_2036/(Cm*V_bio_2036); CMVS_2056=L0_2056/(Cm*V_bio_2056)

# Anoxie (pour besoins O2)
Va_default = 2.7
Va_j_default = (Va_default * 24) / 1000
Vanox_2036 = N_denitrifie_2036 / (Va_j_default * CMVS_2036) if CMVS_2036 > 0 else 0
Vanox_2056 = N_denitrifie_2056 / (Va_j_default * CMVS_2056) if CMVS_2056 > 0 else 0
Vanox = Vanox_2036  # par défaut horizon 2036

# Débits pluie pour décanteur secondaire
Qptp_2036 = Qptp10[1]; Qptp_2056 = Qptp30[1]


# =========================================================
# SECTION 1 : DÉMOGRAPHIE & DÉBITS
# =========================================================
if section == "1 · Démographie & Débits":

    section_header(1, "Étude démographique & Débits", "📈")

    # Population
    st.subheader("Population projetée")
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Population {annee0}",  f"{P0_h:,.0f} hab")
    c2.metric(f"Population {annee10}", f"{P10_h:,.0f} hab", f"+{P10_h-P0_h:,.0f}")
    c3.metric(f"Population {annee30}", f"{P30_h:,.0f} hab", f"+{P30_h-P0_h:,.0f}")

    df_pop = pd.DataFrame({"Année": [annee0, annee10, annee30], "Population (hab)": [P0_h, P10_h, P30_h]})
    st.dataframe(df_pop.round(0), use_container_width=True, hide_index=True)

    hline()

    # Débits domestiques
    st.subheader("💧 Débit domestique moyen journalier")
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Q {annee0}",  f"{Q0:,.1f} m³/j")
    c2.metric(f"Q {annee10}", f"{Q10:,.1f} m³/j")
    c3.metric(f"Q {annee30}", f"{Q30:,.1f} m³/j")

    hline()

    # Débit rejeté
    st.subheader("🔄 Débit de rejet (Krej = {:.2f})".format(Krej))
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Q0 corrigé",  f"{Q0_k:,.1f} m³/j")
    c2.metric(f"Q10 corrigé", f"{Q10_k:,.1f} m³/j")
    c3.metric(f"Q30 corrigé", f"{Q30_k:,.1f} m³/j")

    hline()

    # Débits totaux
    st.subheader("📊 Débit total rejeté (Domestique + Équipements + Industrie)")
    df_total = pd.DataFrame({
        "Horizon": [annee0, annee10, annee30],
        "Domestique (m³/j)": [Q0_k, Q10_k, Q30_k],
        "Équipements (m³/j)": [Qeq0, Qeq10, Qeq30],
        "Industrie (m³/j)": [Qind0, Qind10, Qind30],
        "Q total (m³/j)": [T0[0], T10[0], T30[0]],
        "Q total (m³/h)": [T0[1], T10[1], T30[1]],
        "Q total (m³/s)": [T0[2], T10[2], T30[2]],
    })
    st.dataframe(df_total.round(4), use_container_width=True, hide_index=True)

    hline()

    # Débit de pointe
    st.subheader("⚡ Débit de pointe (Temps sec)")
    df_peak = pd.DataFrame({
        "Horizon":        ["Réf",  "+10",   "+30"],
        "Kp":             [K0,     K10,     K30],
        "Q pointe (m³/s)":[Qp0,   Qp10,   Qp30],
        "Q pointe (m³/j)":[Qpj0,  Qpj10,  Qpj30],
    })
    st.dataframe(df_peak.round(4), use_container_width=True, hide_index=True)

    st.subheader("🌧️ Débit de pointe (Temps de pluie) — Coefficient = {}".format(Cpluie))
    df_pluie = pd.DataFrame({
        "Horizon":     ["Réf",        "+10",        "+30"],
        "Qptp (m³/j)": [Qptp0[0],  Qptp10[0],  Qptp30[0]],
        "Qptp (m³/h)": [Qptp0[1],  Qptp10[1],  Qptp30[1]],
        "Qptp (m³/s)": [Qptp0[2],  Qptp10[2],  Qptp30[2]],
    })
    st.dataframe(df_pluie.round(4), use_container_width=True, hide_index=True)

    hline()

    # Capacité STEP
    st.subheader("🏭 Capacité de la STEP")
    df_cap = pd.DataFrame({
        "Horizon":                 ["Réf",  "+10",   "+30"],
        "Capacité STEP (m³/j)":   [T0[0],  T10[0],  T30[0]],
        "Équivalent habitant":     [Neq0,   Neq10,   Neq30],
    })
    st.dataframe(df_cap.round(0), use_container_width=True, hide_index=True)

    hline()

    # Paramètres de pollution
    st.subheader("🧪 Paramètres de pollution (eaux brutes)")
    K_ratio = DCO / DBO5
    c1, c2 = st.columns([2, 1])
    with c1:
        df_poll = pd.DataFrame({
            "Paramètre":    ["Conductivité", "MES", "DCO", "DBO5", "Phosphore", "NTK"],
            "Unité":        ["mS/cm", "mg/L", "mg O₂/L", "mg O₂/L", "mg/L", "mg/L"],
            "Valeur":       [conductivite, MES, DCO, DBO5, P, NTK],
        })
        st.dataframe(df_poll, use_container_width=True, hide_index=True)
    with c2:
        st.metric("Rapport K = DCO/DBO5", f"{K_ratio:.2f}")
        if K_ratio <= 1:
            st.success("Facilement biodégradable")
        elif K_ratio < 2.5:
            st.success("Traitement biologique possible")
        elif K_ratio < 3.2:
            st.warning("Bio + physico-chimique recommandé")
        else:
            st.error("Traitement biologique difficile")

    hline()

    # Charges polluantes
    st.subheader("📦 Charges polluantes (kg/j)")
    df_load = pd.DataFrame({
        "Paramètre": ["MES", "DCO", "DBO5", "P", "NTK"],
        "2026 (kg/j)": [charge_polluante(MES,Q_2026), charge_polluante(DCO,Q_2026),
                         charge_polluante(DBO5,Q_2026), charge_polluante(P,Q_2026), charge_polluante(NTK,Q_2026)],
        "2036 (kg/j)": [L_mes_2036, L_dco_2036, L_dbo_2036, L_p_2036, L_ntk_2036],
        "2056 (kg/j)": [L_mes_2056, L_dco_2056, L_dbo_2056, L_p_2056, L_ntk_2056],
    })
    st.dataframe(df_load.round(2), use_container_width=True, hide_index=True)


# =========================================================
# SECTION 2 : OUVRAGES DE PRÉTRAITEMENT
# =========================================================
elif section == "2 · Ouvrages de prétraitement":

    section_header(2, "Ouvrages de prétraitement", "🔩")

    tab1, tab2, tab3 = st.tabs(["📐 Dégrillage", "🪨 Dessableur", "🛢️ Déshuileur"])

    # ---- DÉGRILLAGE ----
    with tab1:
        st.subheader("Dégrillage — Méthode de Kirschmer")

        c1, c2 = st.columns(2)
        with c1:
            horizon_deg = st.selectbox("Horizon", ["2026", "2036", "2056"], key="h_deg")
            if horizon_deg == "2026": Q_deg = Qptp0[2];  N_deg = Neq0
            elif horizon_deg == "2036": Q_deg = Qptp10[2]; N_deg = Neq10
            else:                       Q_deg = Qptp30[2]; N_deg = Neq30
            st.info(f"Qptp = {Q_deg:.4f} m³/s")

        with c2:
            alpha_deg = math.radians(st.slider("Angle α (°)", 60, 80, 60, key="alpha_d"))
            v_deg     = st.number_input("Vitesse V (m/s)", value=1.2, key="v_deg")
            hmax_deg  = st.number_input("Hmax (m)", value=1.0, key="hmax_d")

        c1, c2 = st.columns(2)
        with c1:
            type_grille = st.radio("Type de grille", ["Manuelle", "Mécanique"], key="tg")
            C_grill = 0.25 if type_grille == "Manuelle" else 0.45
        with c2:
            mode_deg = st.radio("Type", ["Grossier", "Fin"], key="mode_deg")

        if mode_deg == "Grossier": d_deg=2; e_deg=5; Vret_min,Vret_max=2,5
        else:                      d_deg=1; e_deg=2; Vret_min,Vret_max=5,10

        beta_deg = d_deg / (d_deg + e_deg)
        L_raw    = (Q_deg * math.sin(alpha_deg)) / (hmax_deg * v_deg * (1 - beta_deg) * C_grill)
        L_grill  = max(0.3, min(L_raw, 3.0))
        L0_grill = hmax_deg / math.sin(alpha_deg)
        L_total  = L0_grill + 0.5
        S_grill  = Q_deg / v_deg
        delta_g  = 2.42; g = 9.81
        Dh_grill = delta_g * ((d_deg/e_deg)**(4/3)) * (v_deg**2/(2*g)) * math.sin(alpha_deg)
        Vmin_g   = (N_deg * Vret_min * 1e-3) / 365
        Vmax_g   = (N_deg * Vret_max * 1e-3) / 365

        longueur_g = st.number_input("Longueur bassin (m)", value=2.0, key="lg_g")
        largeur_g  = S_grill / longueur_g
        hauteur_g  = st.number_input("Hauteur bassin (m)", value=hmax_deg, key="hg_g")

        df_grill = pd.DataFrame({
            "Paramètre": ["Débit Qptp", "Surface hydraulique", "Largeur grille",
                          "Longueur mouillée", "Longueur totale", "Perte de charge ΔH",
                          "Volume refus min", "Volume refus max",
                          "Bassin (L × l × h)"],
            "Valeur": [round(Q_deg,4), round(S_grill,2), round(L_grill,2),
                       round(L0_grill,2), round(L_total,2), round(Dh_grill,4),
                       round(Vmin_g,4), round(Vmax_g,4),
                       f"{longueur_g:.2f} × {largeur_g:.2f} × {hauteur_g:.2f}"],
            "Unité": ["m³/s","m²","m","m","m","m","m³/an","m³/an","m"]
        })
        st.dataframe(df_grill, use_container_width=True, hide_index=True)
        st.success(f"✔ Largeur retenue grille = {L_grill:.2f} m")

    # ---- DESSABLEUR ----
    with tab2:
        st.subheader("Dessableur Rectangulaire")
        horizon_dss = st.selectbox("Horizon", ["+10", "+30"], key="h_dss")
        Q_dss = Qptp10[2] if horizon_dss == "+10" else Qptp30[2]
        st.info(f"Qptp = {Q_dss:.4f} m³/s")

        c1, c2 = st.columns(2)
        with c1:
            Ve_dss = st.slider("Vitesse horizontale Ve (m/s)", 0.1, 0.3, 0.3, key="ve_dss")
            Vs_dss = st.slider("Vitesse sédimentation Vs (m³/m²/h)", 40, 70, 65, key="vs_dss")
        with c2:
            Ts_dss = st.slider("Temps de séjour (min)", 3, 5, 4, key="ts_dss")
            H_dss  = st.slider("Profondeur H (m)", 1.0, 3.0, 3.0, key="h_dss2")

        V_dss  = Q_dss * (Ts_dss * 60)
        Sh_dss = V_dss / H_dss
        L_dss  = 10 * H_dss
        l_dss  = Sh_dss / L_dss
        ratio_dss = L_dss / H_dss

        if not (10 <= ratio_dss <= 15): st.warning(f"⚠️ L/H = {ratio_dss:.2f} (doit être 10–15)")
        if not (0.1 <= Ve_dss <= 0.3):  st.warning("⚠️ Ve hors plage recommandée")

        df_dss = pd.DataFrame({
            "Paramètre": ["Qptp (m³/s)","Ve (m/s)","Vs (m³/m²/h)","Ts (min)","H (m)",
                          "Volume V (m³)","Surface Sh (m²)","Longueur L (m)","Largeur l (m)","L/H"],
            "Valeur": [Q_dss, Ve_dss, Vs_dss, Ts_dss, H_dss, V_dss, Sh_dss, L_dss, l_dss, ratio_dss]
        })
        st.dataframe(df_dss.round(3), use_container_width=True, hide_index=True)

    # ---- DÉSHUILEUR ----
    with tab3:
        st.subheader("Déshuileur")
        horizon_deh = st.selectbox("Horizon", ["+10", "+30"], key="h_deh")
        Q_deh = Qptp10[2] if horizon_deh == "+10" else Qptp30[2]
        st.info(f"Qptp = {Q_deh:.4f} m³/s")

        c1, c2 = st.columns(2)
        with c1:
            Vasc_deh = st.slider("Vasc (m/h)", 5, 15, 15, key="vasc_d")
            Ts_deh   = st.slider("Ts (min)", 8, 15, 10, key="ts_deh")
        with c2:
            Vair_deh    = st.slider("Air (m³/m³)", 1.0, 1.5, 1.2, key="vair_d")
            type_deh    = st.radio("Forme", ["Rectangulaire", "Circulaire"], key="td")

        V_deh  = Q_deh * (Ts_deh * 60)
        Sh_deh = (Q_deh * 3600) / Vasc_deh
        H_deh  = V_deh / Sh_deh
        Qair_deh = Q_deh * Vair_deh

        if Vasc_deh > 15: st.warning("⚠️ Vasc > 15 m/h")
        if not (8 <= Ts_deh <= 15): st.warning("⚠️ Ts hors norme")

        geo = {}
        if type_deh == "Rectangulaire":
            geo = {"Longueur L (m)": 10*H_deh, "Largeur B (m)": Sh_deh/(10*H_deh), "Hauteur H (m)": H_deh}
        else:
            D_deh = math.sqrt(4*Sh_deh/math.pi)
            geo = {"Diamètre D (m)": D_deh, "Hauteur H (m)": H_deh}

        data_deh = {"Qptp (m³/s)":Q_deh,"Vasc (m/h)":Vasc_deh,"Ts (min)":Ts_deh,
                    "Volume V (m³)":V_deh,"Surface Sh (m²)":Sh_deh,"Débit air (m³/s)":Qair_deh}
        data_deh.update(geo)
        df_deh = pd.DataFrame(list(data_deh.items()), columns=["Paramètre","Valeur"])
        st.dataframe(df_deh.round(3), use_container_width=True, hide_index=True)

        hline()
        st.subheader("MES : Entrée – Éliminée – Sortie (Dessableur / Déshuileur)")
        def calc_mes_full(Q_m3j):
            MES_in = MES * Q_m3j * 1e-3
            MVS = MES_in * 0.683; MM = MES_in * 0.317
            MM_elim = MM * 0.7; MM_sortie = MM - MM_elim
            return [MES_in, MVS, MM, MM_elim, MM_sortie, MVS + MM_sortie]

        df_mes_out = pd.DataFrame({
            "Paramètre": ["MES entrée","MVS (entrée)","MM (entrée)","MM éliminées","MM sortie","MES sortie"],
            "2026 (kg/j)": calc_mes_full(Q_2026),
            "2036 (kg/j)": calc_mes_full(Q_2036),
            "2056 (kg/j)": calc_mes_full(Q_2056),
        })
        st.dataframe(df_mes_out.round(2), use_container_width=True, hide_index=True)


# =========================================================
# SECTION 3 : TRAITEMENT PRIMAIRE
# =========================================================
elif section == "3 · Traitement primaire":

    section_header(3, "Décanteur Primaire", "🏗️")

    c1, c2 = st.columns(2)
    with c1:
        horizon_dp = st.selectbox("Horizon", ["2036 (+10 ans)", "2056 (+30 ans)"], key="h_dp")

    if horizon_dp == "2036 (+10 ans)":
        Kpts_dp, Qpts_s_dp, _ = qp(T10[2])
        Qpts_dp   = Qpts_s_dp * 3600
        Qptp_dp   = Qptp10[1]
        Qmoy_h_dp = Q10 / 24
    else:
        Kpts_dp, Qpts_s_dp, _ = qp(T30[2])
        Qpts_dp   = Qpts_s_dp * 3600
        Qptp_dp   = Qptp30[1]
        Qmoy_h_dp = Q30 / 24

    st.info(f"Qpts = {Qpts_dp:.2f} m³/h")

    K_dp = Qpts_dp / Qmoy_h_dp
    st.subheader("Rapport K")
    st.write(f"Qpts = {Qpts_dp:.2f} m³/h")
    st.write(f"Qmoy,h = {Qmoy_h_dp:.2f} m³/h")
    st.success(f"K = {K_dp:.2f}")

    if   K_dp <= 2.5: Vlim_dp = 2
    elif K_dp <= 3:   Vlim_dp = 2.5
    elif K_dp <= 5:   Vlim_dp = 3.75
    elif K_dp <= 8:   Vlim_dp = 5
    else:             Vlim_dp = 6

    st.success(f"Vlim = {Vlim_dp} m/h")

    Sh_dp_total = Qptp_dp / Vlim_dp
    nb_dp = st.number_input("Nombre de décanteurs", 1, 2, 2, key="nb_dp")
    Sh_dp_unit  = Sh_dp_total / nb_dp

    ts_dp      = st.slider("Temps de séjour (h)", 1.0, 2.0, 1.5, key="ts_dp_s")
    V_dp_total = Qptp_dp * ts_dp
    V_dp_unit  = V_dp_total / nb_dp
    H_dp       = V_dp_unit / Sh_dp_unit
    Ht_dp      = H_dp + 0.75
    D_dp       = math.sqrt((4 * V_dp_unit) / (math.pi * Ht_dp))

    df_dp = pd.DataFrame({
        "Paramètre": [
            "Qpts (m³/h)", "Qptp (m³/h)", "Qmoy,h (m³/h)",
            "K", "Vlim (m/h)",
            "Surface totale (m²)", "Surface unitaire (m²)",
            "Volume unitaire (m³)",
            "Hauteur eau (m)", "Revanche (m)", "Hauteur totale (m)",
            "Diamètre (m)"
        ],
        "Valeur": [
            Qpts_dp, Qptp_dp, Qmoy_h_dp,
            K_dp, Vlim_dp,
            Sh_dp_total, Sh_dp_unit,
            V_dp_unit,
            H_dp, 0.75, Ht_dp,
            D_dp
        ]
    })
    st.dataframe(df_dp.round(3), use_container_width=True, hide_index=True)

    hline()
    st.subheader("Charges éliminées – Décantation primaire")
    st.info(f"Rendement MES = {taux_mes*100:.0f}%   |   Rendement DBO5 = {taux_dbo*100:.0f}%")

    df_dp_charges = pd.DataFrame({
        "Paramètre": ["DBO5 entrée (kg/j)","MES entrée (kg/j)",
                      "DBO5 éliminée (kg/j)","MES éliminée (kg/j)",
                      "DBO5 sortie (kg/j)","MES sortie (kg/j)"],
        "2036": [round(DBO5_entree_2036,2), round(MES_entree_2036,2),
                 round(DBO5_entree_2036*taux_dbo,2), round(MES_entree_2036*taux_mes,2),
                 round(DBO5_sortie_2036,2), round(MES_sortie_DP_2036,2)],
        "2056": [round(DBO5_entree_2056,2), round(MES_entree_2056,2),
                 round(DBO5_entree_2056*taux_dbo,2), round(MES_entree_2056*taux_mes,2),
                 round(DBO5_sortie_2056,2), round(MES_sortie_DP_2056,2)],
    })
    st.dataframe(df_dp_charges, use_container_width=True, hide_index=True)


# =========================================================
# SECTION 4 : TRAITEMENT BIOLOGIQUE
# =========================================================
elif section == "4 · Traitement biologique":

    section_header(4, "Traitement biologique", "🦠")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌿 Bassin bio", "♻️ Anoxie", "💨 Aération",
        "🔵 O₂", "🧫 Déphosphatation"
    ])

    # ---- BASSIN BIOLOGIQUE ----
    with tab1:
        st.subheader("Bassin biologique")
        c1, c2 = st.columns(2)
        c1.metric("Rendement 2036", f"{R_2036:.1f}% → {classify(R_2036)}")
        c2.metric("Rendement 2056", f"{R_2056:.1f}% → {classify(R_2056)}")

        df_bio_tab = pd.DataFrame({
            "Paramètre": ["DBO entrée (kg/j)","DBO sortie (kg/j)","DBO éliminée (kg/j)","Rendement (%)","Type"],
            "2036": [round(L0_2036,2), round(Lf_2036,2), round(Le_2036,2), round(R_2036,1), classify(R_2036)],
            "2056": [round(L0_2056,2), round(Lf_2056,2), round(Le_2056,2), round(R_2056,1), classify(R_2056)],
        })
        st.dataframe(df_bio_tab, use_container_width=True, hide_index=True)
        st.info(f"Mode sélectionné : **{mode_bassin}**   |   Cm = {Cm}   |   Cv = {Cv}")

        hline()
        st.subheader("Dimensionnement du bassin biologique")
        c1, c2 = st.columns(2)
        with c1:
            N_bio = st.number_input("Nombre de bassins", min_value=1, value=2, key="N_bio")
        with c2:
            H_bio = st.slider("Hauteur H (m)", 3.0, 5.0, 5.0, 0.5, key="H_bio")

        V_bio2036=L0_2036/Cv; V_bio2056=L0_2056/Cv
        Vu_b36=V_bio2036/N_bio; Vu_b56=V_bio2056/N_bio
        Sh_b36=V_bio2036/H_bio; Sh_b56=V_bio2056/H_bio
        Shu_b36=Sh_b36/N_bio; Shu_b56=Sh_b56/N_bio
        L_b36=math.sqrt(2*Shu_b36); L_b56=math.sqrt(2*Shu_b56)
        l_b36=L_b36/2; l_b56=L_b56/2

        df_bassin = pd.DataFrame({
            "Paramètre": ["Volume total (m³)","Volume unitaire (m³)",
                          "Surface totale (m²)","Surface unitaire (m²)",
                          "Longueur L (m)","Largeur l (m)"],
            "2036": [round(V_bio2036,2),round(Vu_b36,2),round(Sh_b36,2),round(Shu_b36,2),round(L_b36,2),round(l_b36,2)],
            "2056": [round(V_bio2056,2),round(Vu_b56,2),round(Sh_b56,2),round(Shu_b56,2),round(L_b56,2),round(l_b56,2)],
        })
        st.dataframe(df_bassin, use_container_width=True, hide_index=True)

    # ---- BASSIN ANOXIE ----
    with tab2:
        st.subheader("Bassin d'anoxie")
        c1, c2 = st.columns(2)
        with c1:
            Va_anox  = st.number_input("Va (g N/kg MVS/h)", value=2.7, key="va_anox")
            N_anox   = st.number_input("Nombre de bassins", value=2, key="N_anox")
        with c2:
            H_anox   = st.slider("Hauteur H (m)", 3.0, 5.0, 5.0, key="H_anox")
            l_anox   = st.number_input("Largeur (m)", value=5.0, key="l_anox")

        horizon_anox = st.selectbox("Horizon", ["2036", "2056"], key="h_anox")
        Nd_anox = N_denitrifie_2036 if horizon_anox == "2036" else N_denitrifie_2056
        CMVS_anox = CMVS_2036 if horizon_anox == "2036" else CMVS_2056

        if Nd_anox <= 0:
            st.warning("⚠️ Pas de dénitrification nécessaire pour cet horizon.")
        else:
            Va_j_anox = (Va_anox * 24) / 1000
            Vanox_calc = Nd_anox / (Va_j_anox * CMVS_anox)
            Vu_anox  = Vanox_calc / N_anox
            Sh_anox  = Vanox_calc / H_anox
            Shu_anox = Sh_anox / N_anox
            L_anox   = Shu_anox / l_anox

            df_anox = pd.DataFrame({
                "Paramètre": ["N dénitrifié (kg/j)","CMVS (kg/m³)","Va (g/kg/h)",
                              "Volume total (m³)","Volume unitaire (m³)",
                              "Surface totale (m²)","Surface unitaire (m²)","Longueur (m)"],
                "Valeur": [round(Nd_anox,2), round(CMVS_anox,2), Va_anox,
                           round(Vanox_calc,2), round(Vu_anox,2),
                           round(Sh_anox,2), round(Shu_anox,2), round(L_anox,2)]
            })
            st.dataframe(df_anox, use_container_width=True, hide_index=True)
            st.success(f"✔ Volume anoxique = {Vanox_calc:.2f} m³")

    # ---- BASSIN AÉRATION ----
    with tab3:
        st.subheader("Bassin d'aération")
        c1, c2 = st.columns(2)
        with c1:
            H_aer  = st.slider("Hauteur H (m)", 3.0, 5.0, 5.0, key="H_aer2")
            N_aer  = st.number_input("Nombre de bassins", value=2, key="N_aer2")
        with c2:
            l_aer  = st.number_input("Largeur (m)", value=5.0, key="l_aer2")
            h_aer2 = st.selectbox("Horizon", ["2036", "2056"], key="hz_aer")

        V_bio_sel  = V_bio_2036 if h_aer2 == "2036" else V_bio_2056
        Nd_aer     = N_denitrifie_2036 if h_aer2 == "2036" else N_denitrifie_2056
        CMVS_aer   = CMVS_2036 if h_aer2 == "2036" else CMVS_2056
        Va_j2      = (Va_default * 24) / 1000
        V_anox_aer = Nd_aer / (Va_j2 * CMVS_aer) if CMVS_aer > 0 else 0
        V_aer_calc = max(V_bio_sel - V_anox_aer, 0)
        Vu_aer2    = V_aer_calc / N_aer
        Sh_aer2    = V_aer_calc / H_aer
        Shu_aer2   = Sh_aer2 / N_aer
        L_aer2     = Shu_aer2 / l_aer

        df_aer2 = pd.DataFrame({
            "Paramètre": ["Volume bio (m³)","Volume anoxique (m³)","Volume aération (m³)",
                          "Volume unitaire (m³)","Surface totale (m²)","Surface unitaire (m²)",
                          "Longueur (m)"],
            "Valeur": [round(V_bio_sel,2), round(V_anox_aer,2), round(V_aer_calc,2),
                       round(Vu_aer2,2), round(Sh_aer2,2), round(Shu_aer2,2), round(L_aer2,2)]
        })
        st.dataframe(df_aer2, use_container_width=True, hide_index=True)

    # ---- BESOINS O2 ----
    with tab4:
        st.subheader("Besoins en oxygène")
        c1, c2 = st.columns(2)
        with c1:
            hz_o2 = st.selectbox("Horizon", ["2036", "2056"], key="hz_o2")
            type_o2 = st.selectbox("Type de charge", ["Forte charge","Moyenne charge","Faible charge","Aération prolongée"], key="to2")
        with c2:
            st.markdown("")

        params_o2 = {"Forte charge":(0.52,0.11),"Moyenne charge":(0.57,0.08),
                     "Faible charge":(0.60,0.07),"Aération prolongée":(0.64,0.07)}
        a_prime, b_prime = params_o2[type_o2]

        Le_o2   = Le_2036  if hz_o2=="2036" else Le_2056
        Nnit_o2 = N_nitrifie_2036 if hz_o2=="2036" else N_nitrifie_2056
        Nden_o2 = N_denitrifie_2036 if hz_o2=="2036" else N_denitrifie_2056
        V_bio_o2 = V_bio_2036 if hz_o2=="2036" else V_bio_2056
        CMVS_o2  = CMVS_2036 if hz_o2=="2036" else CMVS_2056
        V_anox_o2= Vanox_2036 if hz_o2=="2036" else Vanox_2056
        V_aer_o2 = max(V_bio_o2 - V_anox_o2, 0)
        Xa_o2    = CMVS_o2 * V_aer_o2

        qO2 = a_prime*Le_o2 + b_prime*Xa_o2 + 4.57*Nnit_o2 - 2.85*Nden_o2
        qO2_h = qO2/24
        qO2_vol = qO2/V_aer_o2 if V_aer_o2>0 else 0
        Td=16; qO2p = (a_prime*Le_o2/Td) + (b_prime*Xa_o2/24)
        alpha_o2=0.8; beta_o2=0.8
        qO2_reel = qO2 / (alpha_o2*beta_o2*24)

        c1, c2, c3 = st.columns(3)
        c1.metric("qO₂ total (kg/j)", f"{qO2:.2f}")
        c2.metric("qO₂/h (kg/h)",     f"{qO2_h:.3f}")
        c3.metric("qO₂ réel (kg/h)",  f"{qO2_reel:.3f}")

        df_o2 = pd.DataFrame({
            "Paramètre": ["a'","b'","Le","Xa","Nnit","Ndenit","V anox","V bio","V aer",
                          "qO₂ (kg/j)","qO₂/h (kg/h)","qO₂ volumique","qO₂ diurne","qO₂ réel (kg/h)"],
            "Valeur": [a_prime,b_prime,Le_o2,Xa_o2,Nnit_o2,Nden_o2,V_anox_o2,V_bio_o2,V_aer_o2,
                       qO2,qO2_h,qO2_vol,qO2p,qO2_reel]
        })
        st.dataframe(df_o2.round(4), use_container_width=True, hide_index=True)

    # ---- DÉPHOSPHATATION ----
    with tab5:
        st.subheader("Déphosphatation chimique (FeCl₃)")
        c1, c2, c3 = st.columns(3)
        c1.metric("P entrée 2036 (kg/j)",   f"{P_in_2036:.2f}")
        c1.metric("P entrée 2056 (kg/j)",   f"{P_in_2056:.2f}")
        c2.metric("P à éliminer 2036 (kg/j)", f"{P_elim_2036:.2f}")
        c2.metric("P à éliminer 2056 (kg/j)", f"{P_elim_2056:.2f}")
        c3.metric("Boues chimiques 2036 (kg/j)", f"{Boues_2036:.2f}")
        c3.metric("Boues chimiques 2056 (kg/j)", f"{Boues_2056:.2f}")

        df_phos = pd.DataFrame({
            "Paramètre": ["P entrée (kg/j)","P norme (kg/j)","P à éliminer (kg/j)",
                          "Fer ajouté (kg/j)","Solution FeCl₃ (L/j)","Boues chimiques (kg/j)"],
            "2036": [round(P_in_2036,3), round(P_norm_2036,3), round(P_elim_2036,3),
                     round(Fe_2036,3), round(Fe_2036/0.2,1), round(Boues_2036,3)],
            "2056": [round(P_in_2056,3), round(P_norm_2056,3), round(P_elim_2056,3),
                     round(Fe_2056,3), round(Fe_2056/0.2,1), round(Boues_2056,3)],
        })
        st.dataframe(df_phos, use_container_width=True, hide_index=True)
        st.success("✔ Déphosphatation — bilan massique complet")


# =========================================================
# SECTION 5 : DÉCANTEUR SECONDAIRE
# =========================================================
elif section == "5 · Décanteur secondaire":

    section_header(5, "Décanteur Secondaire", "🌀")

    c1, c2, c3 = st.columns(3)
    with c1:
        Ts_ds = st.slider("Temps de séjour Ts (h)", 1.5, 2.0, 1.5, 0.1, key="ts_ds")
    with c2:
        H_ds  = st.slider("Hauteur H (m)", 3.0, 5.0, 5.0, 0.5, key="H_ds")
    with c3:
        N_ds  = st.number_input("Nombre de décanteurs", value=2, key="N_ds")

    V_ds_2036 = Ts_ds * Qptp_2036; V_ds_2056 = Ts_ds * Qptp_2056
    Vu_ds_2036= V_ds_2036/N_ds;    Vu_ds_2056= V_ds_2056/N_ds
    Sh_ds_2036= V_ds_2036/H_ds;    Sh_ds_2056= V_ds_2056/H_ds
    Shu_ds_2036=Sh_ds_2036/N_ds;   Shu_ds_2056=Sh_ds_2056/N_ds
    r_ds_2036 = math.sqrt(Shu_ds_2036/math.pi)
    r_ds_2056 = math.sqrt(Shu_ds_2056/math.pi)
    D_ds_2036 = 2*r_ds_2036; D_ds_2056 = 2*r_ds_2056

    c1, c2, c3 = st.columns(3)
    c1.metric("Diamètre 2036 (m)", f"{D_ds_2036:.2f}")
    c2.metric("Diamètre 2056 (m)", f"{D_ds_2056:.2f}")
    c3.metric("Volume unitaire 2036 (m³)", f"{Vu_ds_2036:.1f}")

    df_ds = pd.DataFrame({
        "Paramètre": ["Qptp (m³/h)","Volume total (m³)","Volume utile (m³)",
                      "Surface horizontale (m²)","Surface unitaire (m²)",
                      "Rayon (m)","Diamètre (m)"],
        "2036": [Qptp_2036, V_ds_2036, Vu_ds_2036, Sh_ds_2036, Shu_ds_2036, r_ds_2036, D_ds_2036],
        "2056": [Qptp_2056, V_ds_2056, Vu_ds_2056, Sh_ds_2056, Shu_ds_2056, r_ds_2056, D_ds_2056],
    })
    st.dataframe(df_ds.round(3), use_container_width=True, hide_index=True)
    st.success("✔ Décanteur secondaire dimensionné avec cohérence des unités")

    hline()

    # Bilan azote
    st.subheader("📋 Bilan de l'azote et des boues biologiques")
    df_azote = pd.DataFrame({
        "Paramètre": ["Masse boues Xa (kg)","CMVS (kg/m³)","Volume bassin bio (m³)",
                      "NTK entrée (kg/j)","N organique réfractaire (kg/j)",
                      "N assimilé (kg/j)","NH₄ rejeté (kg/j)","N nitrifié (kg/j)",
                      "NO₃ rejeté (kg/j)","N dénitrifié (kg/j)"],
        "2036": [Xa_2036, CMVS_2036, V_bio_2036, NTK_entree_2036, Nopr_2036,
                 Nass_2036, NH4_rejet_2036, N_nitrifie_2036, NO3_rejet_2036, N_denitrifie_2036],
        "2056": [Xa_2056, CMVS_2056, V_bio_2056, NTK_entree_2056, Nopr_2056,
                 Nass_2056, NH4_rejet_2056, N_nitrifie_2056, NO3_rejet_2056, N_denitrifie_2056],
    })
    st.dataframe(df_azote.round(2), use_container_width=True, hide_index=True)


# =========================================================
# SECTION 6 : BILAN & NORMES
# =========================================================
elif section == "6 · Bilan & Normes":

    section_header(6, "Bilan polluant & Vérification des normes", "✅")

    st.subheader("Rendement d'élimination des charges polluantes")

    type_charge_b = st.selectbox("Type de charge", ["Forte charge","Moyenne charge","Faible charge"], key="tc_b")
    ranges = {
        "Forte charge":   {"DBO":(60,80,70),"DCO":(50,70,60),"MES":(50,70,60)},
        "Moyenne charge": {"DBO":(80,90,85),"DCO":(70,85,78),"MES":(70,90,80)},
        "Faible charge":  {"DBO":(90,98,95),"DCO":(80,95,90),"MES":(85,98,92)},
    }[type_charge_b]

    c1, c2, c3 = st.columns(3)
    with c1:
        rend_DBO = st.slider("Rendement DBO5 (%)", *ranges["DBO"], key="rdbo")
    with c2:
        rend_DCO = st.slider("Rendement DCO (%)",  *ranges["DCO"], key="rdco")
    with c3:
        rend_MES = st.slider("Rendement MES (%)",  *ranges["MES"], key="rmes")

    R_DBO=rend_DBO/100; R_DCO=rend_DCO/100; R_MES=rend_MES/100

    DBO_sortie_final_2036 = DBO_entree_2036*(1-R_DBO); DBO_sortie_final_2056 = DBO_entree_2056*(1-R_DBO)
    DCO_sortie_2036 = L_dco_2036*(1-R_DCO);              DCO_sortie_2056 = L_dco_2056*(1-R_DCO)
    MES_sortie_final_2036= MES_sortie_DP_2036*(1-R_MES); MES_sortie_final_2056 = MES_sortie_DP_2056*(1-R_MES)

    DBO_mgl_2036 = (DBO_sortie_final_2036/Q10)*1000; DBO_mgl_2056 = (DBO_sortie_final_2056/Q30)*1000
    DCO_mgl_2036 = (DCO_sortie_2036/Q10)*1000;       DCO_mgl_2056 = (DCO_sortie_2056/Q30)*1000
    MES_mgl_2036 = (MES_sortie_final_2036/Q10)*1000;  MES_mgl_2056 = (MES_sortie_final_2056/Q30)*1000
    P_mgl_2036   = (P_norm_2036/Q10)*1000;             P_mgl_2056   = (P_norm_2056/Q30)*1000

    hline()
    st.subheader("Charges polluantes sortie décanteur secondaire")

    df_sortie = pd.DataFrame({
        "Paramètre": ["DBO sortie (kg/j)","DBO sortie (mg/L)",
                      "DCO sortie (kg/j)","DCO sortie (mg/L)",
                      "MES sortie (kg/j)","MES sortie (mg/L)",
                      "P sortie (kg/j)","P sortie (mg/L)"],
        "2036": [DBO_sortie_final_2036, DBO_mgl_2036, DCO_sortie_2036, DCO_mgl_2036,
                 MES_sortie_final_2036, MES_mgl_2036, P_norm_2036, P_mgl_2036],
        "2056": [DBO_sortie_final_2056, DBO_mgl_2056, DCO_sortie_2056, DCO_mgl_2056,
                 MES_sortie_final_2056, MES_mgl_2056, P_norm_2056, P_mgl_2056],
    })
    st.dataframe(df_sortie.round(3), use_container_width=True, hide_index=True)

    hline()
    st.subheader("✅ Vérification des normes de rejet")

    norme = {"MES":30, "DBO5":30, "DCO":120, "NO3":30, "P":5}
    NO3_mgl = 30

    def check(v, n): return "✔ Conforme" if v <= n else "⚠ Traitement tertiaire nécessaire"
    def check_p(v, n): return "✔ Conforme" if v <= n else "⚠ Bassin anaérobie ou tertiaire nécessaire"

    df_normes = pd.DataFrame({
        "Paramètre": ["MES","DBO5","DCO","NO₃⁻","Phosphore total"],
        "Norme (mg/L)": [norme["MES"],norme["DBO5"],norme["DCO"],norme["NO3"],norme["P"]],
        "2036 (mg/L)": [round(MES_mgl_2036,2),round(DBO_mgl_2036,2),round(DCO_mgl_2036,2),NO3_mgl,round(P_mgl_2036,2)],
        "2036 État": [check(MES_mgl_2036,norme["MES"]), check(DBO_mgl_2036,norme["DBO5"]),
                      check(DCO_mgl_2036,norme["DCO"]), check(NO3_mgl,norme["NO3"]),
                      check_p(P_mgl_2036,norme["P"])],
        "2056 (mg/L)": [round(MES_mgl_2056,2),round(DBO_mgl_2056,2),round(DCO_mgl_2056,2),NO3_mgl,round(P_mgl_2056,2)],
        "2056 État": [check(MES_mgl_2056,norme["MES"]), check(DBO_mgl_2056,norme["DBO5"]),
                      check(DCO_mgl_2056,norme["DCO"]), check(NO3_mgl,norme["NO3"]),
                      check_p(P_mgl_2056,norme["P"])],
    })
    st.dataframe(df_normes, use_container_width=True, hide_index=True)

    hline()
    non_conformes = [r for r in ["2036 État","2056 État"] if "nécessaire" in " ".join(df_normes[r].tolist())]
    if non_conformes:
        st.warning("⚠ Certains paramètres nécessitent un traitement complémentaire.")
    else:
        st.success("✔ Toutes les normes de rejet sont respectées.")

    # Récap final
    hline()
    st.subheader("📋 Récapitulatif général")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Population & Débits**")
        st.markdown(f"- Population 2056 : **{P30_h:,.0f} hab**")
        st.markdown(f"- Q total 2056 : **{T30[0]:,.1f} m³/j**")
        st.markdown(f"- Kp : **{K30:.2f}**  |  Qptp : **{Qptp30[0]:,.1f} m³/j**")
    with c2:
        st.markdown("**Traitement biologique**")
        st.markdown(f"- Mode : **{mode_bassin}**")
        st.markdown(f"- Rendement DBO5 : **{rend_DBO}%**")
        st.markdown(f"- Rendement DCO : **{rend_DCO}%**  |  MES : **{rend_MES}%**")
