# ==============================================================================
# Nom du fichier : validation_croisee_dual_c.py
# Description   : Validation croisée Leave-One-Out (LOO) du modèle A-CORE / Dual-C
# Objectif      : Tester la robustesse et le pouvoir prédictif du modèle
#
# IMPORTANT — CONVENTION DE SIGNE :
# --------------------------------------------------------------------------
# Dans ce script, la densité est écrite sous la forme :
#     Φ = 1 + β·n_eff² − γ·n_eff³   avec γ > 0
#
# Cette écriture est STRICTEMENT ÉQUIVALENTE à la convention utilisée dans HAL11 :
#     Φ = 1 + β·n_eff² + γ'·n_eff³  avec γ' < 0
#
# Les deux formulations décrivent le même mécanisme de saturation cubique.
# --------------------------------------------------------------------------
# Auteur : Régis Music / TOQ Project
# Date   : Janvier 2026
# ==============================================================================

import numpy as np
from scipy.optimize import minimize

# ==============================================================================
# 1. STRUCTURE FIXE : FONCTION Dt(n)
# ==============================================================================

# Paramètres structurels (figés, non ajustés)
A1 = -0.04136; K1 = 4.493; PHI1 = 0.785
A2 = 0.00424;  K2 = 13.48; PHI2 = -1.2

A_N_AMP = -0.32; A_N_CENTER = np.log(2.5)
E_N_LOW = -15.0; E_N_HIGH = -0.45
C_N_AMP = -0.0008; C_N_DECAY = -2.0; C_N_CENTER = 4.0


def Dt(n_ideal):
    """Fonction de métrique temporelle Dt(n) — structure figée."""
    ln_n = np.log(n_ideal)

    f1 = A1 * np.sin(K1 * ln_n + PHI1)
    f2 = A2 * np.sin(K2 * ln_n + PHI2)

    A_n = np.exp(A_N_AMP * (ln_n - A_N_CENTER)**2)

    term_low = (1 - np.exp(E_N_LOW * (n_ideal - 1)))
    term_high = (1 - np.exp(E_N_HIGH * (16.5 - n_ideal)))
    E_n = term_low * term_high

    C_n = C_N_AMP * np.exp(C_N_DECAY * (n_ideal - C_N_CENTER)**2) \
          * np.sin(2 * np.pi * n_ideal)

    return 1 + f1 + (f2 * A_n * E_n) + C_n


# ==============================================================================
# 2. MODÈLE DE MASSE (PARAMÈTRES DYNAMIQUES)
# ==============================================================================

def predict_mass(n_ideal, famille, params):
    """
    Calcule la masse prédite d'un quark.

    params = [C_impair, C_pair, beta, gamma]
    Convention : Φ = 1 + β·n_eff² − γ·n_eff³  (gamma > 0)
    """
    C_impair, C_pair, beta, gamma = params

    n_eff = n_ideal * Dt(n_ideal)

    phi = 1 + beta * n_eff**2 - gamma * n_eff**3

    C_val = C_impair if famille == "impair" else C_pair

    return C_val * (phi - 1)**2


# ==============================================================================
# 3. DONNÉES EXPÉRIMENTALES (PDG)
# ==============================================================================

quarks_db = [
    {"name": "u", "n": 1.0,  "fam": "impair", "m_pdg": 2.16},
    {"name": "d", "n": 1.25, "fam": "pair",   "m_pdg": 4.67},
    {"name": "s", "n": 2.50, "fam": "impair", "m_pdg": 93.0},
    {"name": "c", "n": 5.0,  "fam": "pair",   "m_pdg": 1270.0},
    {"name": "b", "n": 6.5,  "fam": "impair", "m_pdg": 4180.0},
    {"name": "t", "n": 16.5, "fam": "pair",   "m_pdg": 172760.0},
]


# ==============================================================================
# 4. VALIDATION CROISÉE LEAVE-ONE-OUT
# ==============================================================================

def run_cross_validation():
    print(">>> VALIDATION CROISÉE Leave-One-Out — Modèle A-CORE / Dual-C <<<")
    print("-" * 78)
    print(f"{'Quark caché':^12} | {'Masse réelle':^15} | {'Masse prédite':^15} | {'Erreur':^10}")
    print("-" * 78)

    global_errors = []

    # Point de départ (paramètres du modèle calibré)
    x0 = [192.15, 188.40, 0.0948, 0.00055]  # gamma > 0 ici (voir convention)

    for q_hidden in quarks_db:
        train_set = [q for q in quarks_db if q["name"] != q_hidden["name"]]

        def loss_function(params):
            if params[0] < 0 or params[1] < 0:
                return 1e9  # pénalité non-physique

            err = 0.0
            for q in train_set:
                m_pred = predict_mass(q["n"], q["fam"], params)
                err += (np.log(m_pred) - np.log(q["m_pdg"]))**2
            return err

        res = minimize(loss_function, x0, method="Nelder-Mead", tol=1e-5)
        best_params = res.x

        m_pred = predict_mass(q_hidden["n"], q_hidden["fam"], best_params)
        rel_err = 100 * (m_pred - q_hidden["m_pdg"]) / q_hidden["m_pdg"]
        global_errors.append(abs(rel_err))

        if m_pred > 1000:
            pred_str = f"{m_pred/1000:.3f} GeV"
            real_str = f"{q_hidden['m_pdg']/1000:.3f} GeV"
        else:
            pred_str = f"{m_pred:.2f} MeV"
            real_str = f"{q_hidden['m_pdg']:.2f} MeV"

        print(f"{q_hidden['name']:^12} | {real_str:^15} | {pred_str:^15} | {rel_err:+.2f}%")

    print("-" * 78)
    print(f"ERREUR MOYENNE ABSOLUE (MAPE) : {np.mean(global_errors):.2f}%")

    if np.mean(global_errors) < 15:
        print("\n✅ CONCLUSION : Modèle robuste et prédictif.")
    else:
        print("\n⚠️  CONCLUSION : Instabilité détectée.")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    run_cross_validation()
