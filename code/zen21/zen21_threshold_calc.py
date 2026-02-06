#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOR726 — ZEN21 (Code de référence)

Objectif (niveau Licence)
------------------------
Ce script calcule les deux valeurs "figées" du package ZEN21 :
  - E*   = 726.0 GeV  (borne / seuil)
  - Epeak ≈ 747.9 GeV (pic de structure "froide")

Ce dépôt/artefact sert à la reproductibilité et à la traçabilité.

Comment citer
------------
- ZEN21-0 (Index / package) : DOI = 10.5281/zenodo.18510570
- ZEN21-A (Méthode / protocole) : DOI = 10.5281/zenodo.18510305
- ZEN21-B (Paramètres figés) : DOI = 10.5281/zenodo.18510350
- (Optionnel) Archive logicielle Zenodo (Software DOI) : [à renseigner si activé]

Licence
-------
Code : MIT (recommandé) ou selon le choix du dépôt GitHub/Zenodo.
Documents (PDF) : CC BY 4.0 (voir Zenodo records).
"""

import numpy as np

def calculate_thresholds():
    # 1. CONSTANTES FONDAMENTALES (NIST/CODATA 2022)
    me = 0.51099895069  # Masse de l'électron en MeV
    
    # 2. PARAMÈTRES STRUCTURELS TOQ
    n = 11               # Rang de nivation maîtresse
    t11 = 66             # Volume triangulaire de saturation (n*(n+1)/2)
    pivot_geom = 21      # Rang de complétude (T6)
    
    # 3. MODULES DE LA LOI DE L'APEX (66/65)
    module_froid = 4 * 66 # 264 (Pion - ZEN17)
    module_chaud = 4 * 65 # 260 (Top/Tau - ZEN12/19)

    # =========================================================================
    # CALCULS AXIOMATIQUES
    # =========================================================================

    # A. La Frontière de Synchronisation (Borne de 726)
    # Définition : Produit du rang par son volume de saturation
    E_star_gev = (n * t11) 
    
    # B. Le Pic de Structure Froide (L'anomalie de 2015)
    # Définition : Énergie de structure du pivot géométrique en régime froid
    E_peak_mev = pivot_geom * (module_froid**2) * me
    E_peak_gev = E_peak_mev / 1000

    return E_star_gev, E_peak_gev

if __name__ == "__main__":
    e_star, e_peak = calculate_thresholds()
    
    print("="*60)
    print("🔬 AUDIT AXIOMATIQUE ZEN21-B")
    print("="*60)
    print(f"Borne de synchronisation théorique (E*) : {e_star:.1f} GeV")
    print(f"Pic de structure froide prédit (E_peak) : {e_peak:.2f} GeV")
    print("-"*60)
    print("INTERPRÉTATION :")
    print(f"1. La valeur {e_star:.1f} GeV est la borne de saturation du rang n=11.")
    print(f"2. L'excès diphoton de 2015 (~750 GeV) est le reflet du pic à {e_peak:.1f} GeV.")
    print("="*60)
