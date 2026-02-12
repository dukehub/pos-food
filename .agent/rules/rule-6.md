---
trigger: always_on
---

# Rule #6: UI/UX POS & Waiter — speed, ergonomie, impression, perf

## 1) Règle d’or: “Fast path” toujours prioritaire

* Toute action fréquente doit être faisable en **≤ 2 interactions** quand c’est possible.
* L’UI doit favoriser :

  * clics courts
  * clavier (POS)
  * touch (Waiter)
* Interdit : workflows longs pour encaisser / envoyer cuisine / changer table.

## 2) POS (desktop) — clavier & productivité

* Supporter navigation clavier :

  * focus visible
  * `Enter` pour valider / ajouter
  * `Esc` pour fermer modal / annuler
  * raccourcis (ex: nouvelle vente, paiement, impression)
* Les champs “quantité”, “remise”, “paiement” doivent être optimisés clavier (pas de popup compliquées).
* Interdit : dépendre uniquement du mouse pour la caisse.

## 3) POS — codes-barres / recherche produit

* Recherche produit :

  * input toujours accessible (ou via raccourci)
  * ajout instant au panier
* Barcode :

  * traiter les scans comme une saisie rapide dans un champ dédié
  * comportement déterministe (si produit introuvable → message clair + beep/feedback)
* Interdit : scan qui déclenche des modals bloquants.

## 4) POS — impression ticket (pattern)

* Impression doit être :

  * déclenchable en 1 clic (ou auto selon config)
  * avec état “printing / done / failed”
* En cas d’échec :

  * bouton “Réimprimer”
  * conserver l’ID ticket + contenu
* Interdit : perdre un ticket après paiement.

## 5) POS — flux paiement (simple & robuste)

* UI paiement :

  * montants clairs (total, taxes, remise, rendu)
  * modes paiement visibles (cash, carte, mixte si supporté)
* Validation :

  * empêcher paiement incohérent (ex: montant négatif)
  * confirmer uniquement quand nécessaire (ex: annulation vente payée)
* Interdit : confirmations inutiles partout.

## 6) Waiter (tablet/mobile) — ergonomie touch

* Boutons minimum “touch-friendly” :

  * grandes cibles, spacing, pas de menus trop denses
* Navigation :

  * 3 niveaux max (Salle → Table → Commande)
* Actions rapides :

  * ajouter item
  * envoyer cuisine
  * demander addition / clôturer
* Interdit : pages longues avec scroll excessif pour des actions fréquentes.

## 7) Waiter — statuts visibles & temps réel (si possible)

* Chaque commande/ligne doit afficher un statut simple :

  * brouillon / envoyé / en préparation / servi / annulé
* Rafraîchissement :

  * polling léger ou websockets si dispo
* Interdit : “on ne sait pas si c’est parti en cuisine”.

## 8) Performance front (critique)

* Listes (produits, tables, commandes) :

  * pagination ou virtualisation si grosse volumétrie
  * éviter re-renders inutiles
* Images produits :

  * lazy-load
  * placeholders
* Interdit : charger tout le catalogue en mémoire sans stratégie.

## 9) Accessibilité minimale (même en POS)

* Focus ring visible
* Contrastes corrects (Nuxt UI + tokens)
* États disabled/loading clairs
* Interdit : actions sans feedback.

## 10) UI states standard

Tout écran doit gérer :

* `loading` (squelette/spinner)
* `empty` (message + action)
* `error` (retry)
* `success` (toast)
* `offline` (badge + file d’attente si actif)

## 11) “Design consistency”

* Une seule barre de navigation par app (AppShell).
* Même pattern pour :

  * modals
  * confirm dialogs
  * toasts
  * forms
* Interdit : inventer un nouveau style par écran.
