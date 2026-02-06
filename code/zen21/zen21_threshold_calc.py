#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOR726 — ZEN21 (code de référence)

Ce script calcule deux valeurs figées associées au package ZEN21 :
  - E*   = 726.0 GeV  (borne / seuil)
  - Epeak ≈ 747.91 GeV (pic de structure "froide")

DOI (références)
- ZEN21-0 (Index / package) : 10.5281/zenodo.18510570
- ZEN21-A (Méthode / protocole) : 10.5281/zenodo.18510305
- ZEN21-B (Paramètres figés) : 10.5281/zenodo.18510350
"""

# Constante : masse de l'électron (CODATA 2022) en MeV
M_E_MEV = 0.51099895069

def calculate_thresholds():
    """
    Retourne (E_star_GeV, E_peak_GeV).

    Définitions (ZEN21-B) :
      - n = 11 ; T_11 = 66  => E* = n * T_11 = 726 GeV
      - pivot = T_6 = 21 ; module_froid = 4*T_11 = 264
        E_peak(MeV) = pivot * module_froid^2 * m_e
        E_peak(GeV) = E_peak(MeV)/1000
    """
    n = 11
    t11 = 66
    pivot = 21
    module_froid = 4 * t11  # 264

    e_star_gev = n * t11
    e_peak_mev = pivot * (module_froid ** 2) * M_E_MEV
    e_peak_gev = e_peak_mev / 1000.0

    return e_star_gev, e_peak_gev


def main():
    e_star, e_peak = calculate_thresholds()

    print("=" * 60)
    print("AUDIT ZEN21-B — TOR726 (valeurs figées)")
    print("=" * 60)
    print(f"E* (borne / seuil)     : {e_star:.1f} GeV")
    print(f"E_peak (pic attendu)   : {e_peak:.2f} GeV")
    print("=" * 60)


if __name__ == "__main__":
    main()
