import random
import operator
import csv
from datetime import datetime

# =================================================================
# TOQ - LGU : SCRIPT DU TEST NUL (Protocole Anti-P-Hacking)
# Auteur : Régis Guerrero
# Cibles : Alpha (137.036) et Pion pi0 (264.144)
# Tolérance : 100 ppm
# =================================================================

# 1. Dictionnaire LGU autorisé (Niveau 0 et Niveau 1 basique)
VOCABULARY = [1, 3, 4, 5, 7, 8, 10, 11, 12, 13, 19, 53, 55, 65, 66, 137, 264, 277]

# 2. Opérations autorisées
OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# 3. Cibles physiques et tolérances (100 ppm)
TARGET_ALPHA = 137.036
TOLERANCE_ALPHA = TARGET_ALPHA * 0.0001  # 0.0137

TARGET_PI0 = 264.144
TOLERANCE_PI0 = TARGET_PI0 * 0.0001      # 0.0264

def generate_random_tree(depth=3):
    """
    Génère récursivement un arbre mathématique (profondeur max).
    Retourne un tuple : (valeur_calculee, formule_en_texte)
    """
    # Arrêt de la profondeur ou chance aléatoire de stopper (20%)
    if depth == 0 or random.random() < 0.2:
        val = random.choice(VOCABULARY)
        return val, str(val)
    else:
        left_val, left_str = generate_random_tree(depth - 1)
        right_val, right_str = generate_random_tree(depth - 1)
        
        op_char = random.choice(list(OPERATORS.keys()))
        op_func = OPERATORS[op_char]
        
        # Protection contre la division par zéro
        if op_char == '/' and right_val == 0:
            raise ValueError("Division par zero")
            
        try:
            val = op_func(left_val, right_val)
            return val, f"({left_str} {op_char} {right_str})"
        except OverflowError:
            raise ValueError("Overflow")

def run_monte_carlo(iterations=5000, seed_value=42):
    """Exécute le test nul sur N itérations et exporte en CSV"""
    random.seed(seed_value) # Garantit la reproductibilité absolue
    
    success_alpha = 0
    success_pi0 = 0
    results = []
    
    print(f"--- DÉMARRAGE DU TEST NUL ({iterations} itérations) ---")
    
    i = 0
    while i < iterations:
        try:
            val, formula_str = generate_random_tree(depth=3)
        except ValueError:
            # Si division par zéro ou overflow, on relance un tirage (on ignore)
            continue
            
        # Test contre Alpha
        alpha_match = abs(val - TARGET_ALPHA) <= TOLERANCE_ALPHA
        if alpha_match: success_alpha += 1
            
        # Test contre Pion
        pi0_match = abs(val - TARGET_PI0) <= TOLERANCE_PI0
        if pi0_match: success_pi0 += 1
            
        # Sauvegarde pour le CSV
        results.append({
            'Iteration': i + 1,
            'Formule_Generee': formula_str,
            'Valeur_Calculee': val,
            'Match_Alpha': alpha_match,
            'Match_Pion': pi0_match
        })
        i += 1

    print("--- RÉSULTATS ---")
    print(f"Succès pour Alpha (tolérance 100 ppm) : {success_alpha} / {iterations}")
    print(f"Succès pour Pion pi0 (tolérance 100 ppm) : {success_pi0} / {iterations}")
    
    # Export CSV ZENODO-Ready
    filename = "LGU_Test_Nul_Resultats.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✅ Fichier d'audit sauvegardé : {filename}")
    return success_alpha, success_pi0

if __name__ == "__main__":
    run_monte_carlo(iterations=5000, seed_value=42)