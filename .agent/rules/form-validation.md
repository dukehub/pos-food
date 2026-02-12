---
trigger: always_on
---

# Rule #3: Forms, validation, toasts, permissions — (vee-validate + Zod) + patterns Admin/POS/Waiter

## 1) Validation (source unique = Zod)

* Tous les modèles de formulaires doivent avoir un **schéma Zod** dans `packages/core/schemas/*`.
* Les types TS doivent être dérivés de Zod : `type X = z.infer<typeof XSchema>`.
* Interdit : validation “à la main” dispersée dans les composants (if/else partout).

## 2) Formulaires (vee-validate)

* Tous les formulaires utilisent vee-validate :

  * `useForm()` + `defineField()` (ou `Field`/`Form` si tu préfères un style)
  * binding standard sur Nuxt UI (`UInput`, `USelect`, `UTextarea`, etc.)
* Règle UX : afficher l’erreur **au niveau du champ** + un message global si erreur serveur.
* Interdit : gérer `errors`/`touched` manuellement dans chaque page.

## 3) “Form adapter” Zod → vee-validate (obligatoire)

* Créer un helper unique dans `packages/core/forms/` :

  * `toTypedSchema(ZodSchema)` ou équivalent
* Toutes les pages importent cet adapter au lieu de refaire l’intégration.

## 4) Erreurs API (standardisées)

* Toute réponse d’erreur doit être normalisée dans `packages/api` :

  * `code` (ex: `VALIDATION_ERROR`, `UNAUTHORIZED`, `CONFLICT`, `UNKNOWN`)
  * `message` (i18n key ou message fallback)
  * `fieldErrors?: Record<string, string>` (mapping champs -> i18n keys)
* Les formulaires doivent :

  * mapper `fieldErrors` vers vee-validate (`setFieldError`)
  * afficher un toast global si non “field error”.

## 5) Notifications / toasts (convention)

* Utiliser le système de notifications Nuxt UI (ou un wrapper `useAppToast()` dans `packages/ui`).
* Niveaux :

  * success (opération OK)
  * error (échec)
  * warning (non bloquant)
  * info (feedback)
* Règle : pas de `alert()` / pas de console-only.

## 6) Patterns par type d’interface

### Admin (CRUD + backoffice)

* Pattern : List → Create/Edit → Details
* Tables : tri/filtre/pagination (TanStack core) + actions par ligne.
* Formulaires : validations strictes + confirmations pour delete.

### POS (flux rapide / caisse)

* Objectif : **zéro friction**
* Validation : minimale mais sûre (ex: quantité > 0, paiement valide).
* Feedback : toasts courts + erreurs lisibles, jamais de modals bloquants inutiles.
* Offline/latence : prévoir états “pending” et reprise (si c’est dans le scope).

### Waiter (mobile/tablet)

* UI : boutons larges, actions rapides, navigation simple.
* Formulaires : étapes courtes (ex: sélectionner table → items → envoyer cuisine).
* Erreurs réseau : mode “retry” simple + statut clair.

## 7) Permissions & rôles (RBAC)

* Définir rôles/capabilités dans `packages/core/auth/permissions.ts` :

  * ex: `can('products:write')`, `can('orders:close')`
* Chaque route/page doit déclarer son besoin :

  * middleware/guard (Nuxt route middleware)
  * et masquage UI cohérent (boutons/actions)
* Interdit : “cacher juste le bouton” sans guard côté routing.

## 8) Middlewares (Nuxt)

* `auth` : redirection login si non authentifié
* `role/permission` : blocage/redirect si interdit
* `tenant/client` (si multi-client) : vérifier contexte actif

## 9) Conventions d’internationalisation des erreurs

* Les messages d’erreurs doivent être des **clés i18n** (ex: `errors.required`, `errors.email_invalid`)
* Les schémas Zod doivent référencer ces clés (ou les mapper via adapter).

## 10) Définition du “Done” pour un écran

Un écran est “done” si :

* i18n complet
* validation Zod + vee-validate
* erreurs API mappées (field + global)
* permissions respectées (guard + UI)
* toasts success/error présents
