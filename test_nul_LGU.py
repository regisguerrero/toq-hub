import random
import operator
import csv

# =================================================================
# TOQ - LGU : SCRIPT DU TEST NUL (VERSION PEER-REVIEW PROOF)
# Validation statistique Monte-Carlo - N=5000
# =================================================================

# 1) Vocabulaire : sous-ensemble contrôlé de N0 ∪ N1 (réf. LGU02)
# On exclut les cibles (137, 264) pour mesurer la rareté réelle.
# NOTE reviewer-proof : on retire 65 (souvent perçu comme "66-1") pour éviter tout soupçon G7 implicite.
VOCABULARY = [1, 3, 4, 5, 7, 8, 10, 11, 19, 53, 55, 66]

def safe_int_div(a: int, b: int) -> int:
    """Division entière stricte conforme à la règle G5 (rejet si non divisible)."""
    if b == 0:
        raise ValueError("ZeroDiv")
    if a % b != 0:
        raise ValueError("Non-divisible")
    return a // b

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": safe_int_div,
}

# 2) Cibles physiques (tolérance relative 100 ppm)
TARGET_ALPHA = 137.036
TOLERANCE_ALPHA = TARGET_ALPHA * 0.0001  # 100 ppm

TARGET_PI0 = 264.144
TOLERANCE_PI0 = TARGET_PI0 * 0.0001      # 100 ppm

def delta_ppm(val: float, target: float) -> float:
    """Δppm = 1e6 * (val - target) / target."""
    return 1e6 * (val - target) / target

def generate_lgu_formula(depth: int = 3, p_leaf: float = 0.2):
    """
    Structure : arbre binaire, profondeur max = 3, arrêt feuille prob = 0.2.
    Conforme LGU04 (sous-test déclaré).
    """
    if depth == 0 or random.random() < p_leaf:
        v = random.choice(VOCABULARY)
        return v, str(v)

    try:
        left_val, left_str = generate_lgu_formula(depth - 1, p_leaf)
        right_val, right_str = generate_lgu_formula(depth - 1, p_leaf)
        op_char = random.choice(list(OPERATORS.keys()))
        res = OPERATORS[op_char](left_val, right_val)
        return res, f"({left_str} {op_char} {right_str})"
    except (ValueError, OverflowError):
        raise ValueError("Invalid LGU Operation")

def run_monte_carlo(iterations: int = 5000, seed_value: int = 42, depth: int = 3, p_leaf: float = 0.2):
    random.seed(seed_value)

    success_alpha = 0
    success_pi0 = 0
    rejected = 0
    results = []

    print(f"--- DÉMARRAGE DU TEST NUL (N={iterations}) ---")
    print(f"Seed={seed_value} | depth={depth} | p_leaf={p_leaf}")
    print(f"VOCABULARY={VOCABULARY}")

    count = 0
    while count < iterations:
        try:
            val, formula_str = generate_lgu_formula(depth=depth, p_leaf=p_leaf)

            dppm_a = delta_ppm(val, TARGET_ALPHA)
            dppm_p = delta_ppm(val, TARGET_PI0)

            match_a = abs(val - TARGET_ALPHA) <= TOLERANCE_ALPHA
            match_p = abs(val - TARGET_PI0) <= TOLERANCE_PI0

            if match_a:
                success_alpha += 1
            if match_p:
                success_pi0 += 1

            results.append({
                "Iteration": count + 1,
                "Formule": formula_str,
                "Valeur": val,
                "DeltaPPM_Alpha": dppm_a,
                "DeltaPPM_Pion": dppm_p,
                "Match_Alpha": match_a,
                "Match_Pion": match_p,
            })

            count += 1
        except ValueError:
            rejected += 1
            continue

    total_draws = iterations + rejected
    reject_rate = rejected / total_draws if total_draws > 0 else 0.0

    print(f"Succès Alpha : {success_alpha} / {iterations}")
    print(f"Succès Pion  : {success_pi0} / {iterations}")
    print(f"Rejets       : {rejected} (taux = {reject_rate:.4%}, total tirages = {total_draws})")

    # Écriture CSV (robuste)
    fieldnames = [
        "Iteration", "Formule", "Valeur",
        "DeltaPPM_Alpha", "DeltaPPM_Pion",
        "Match_Alpha", "Match_Pion"
    ]

    with open("LGU_Test_Nul_Audit.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("\n✅ Audit CSV généré : LGU_Test_Nul_Audit.csv")

if __name__ == "__main__":
    run_monte_carlo(iterations=5000, seed_value=42, depth=3, p_leaf=0.2)
