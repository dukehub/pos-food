---
trigger: always_on
---

# Rule: Monorepo 3 apps (Admin / POS / Waiter) + shared packages

## 1) Structure monorepo (obligatoire)

* Monorepo unique (Bun workspace) avec 3 apps et des packages partagés.

Exemple :

* `apps/admin/` : backoffice (produits, plans, users, rapports…)
* `apps/pos/` : caisse (vente, paiement, tickets, clôtures…)
* `apps/waiter/` : tablette/mobile (prise de commande, envoi cuisine, suivi tables…)
* `packages/ui/` : composants UI partagés (wrappers Nuxt UI, design tokens, layouts)
* `packages/core/` : types, utils, validation Zod, i18n helpers, constants métier
* `packages/api/` : client API (fetch wrapper), endpoints, types DTO
* `packages/table/` : helpers TanStack Table (builders colonnes, filtres communs)

Interdit : dupliquer la même logique (types, validation, helpers) dans plusieurs apps.

## 2) Partage UI (Nuxt UI v4 + Tailwind)

* `packages/ui` contient :

  * composants “design system” (Button wrappers, FormField, AppShell, PageHeader, etc.)
  * thèmes/tokens Tailwind (si besoin) et conventions UI
* Chaque app peut avoir **quelques** composants spécifiques, mais tout ce qui est réutilisable va dans `packages/ui`.

## 3) Partage métier (core)

* `packages/core` = source unique de vérité :

  * types TypeScript (ex: `Product`, `Order`, `Table`, `UserRole`)
  * enums/constants (ex: statuts commande, modes paiement)
  * schémas Zod (validation) + inférence des types
  * helpers i18n (keys, namespaces, formatters)
* Interdit : redéfinir les mêmes types dans `apps/*`.

## 4) API & data access (strict)

* Toutes les apps consomment l’API via `packages/api`.
* Un seul wrapper HTTP (fetch/ofetch) avec :

  * gestion token/session
  * erreurs normalisées
  * retry contrôlé (si nécessaire)
* Interdit : appels réseau “ad-hoc” dans les composants.

## 5) Routing (Nuxt)

* Nuxt routing via `pages/` par app.
* Patterns :

  * `apps/admin/pages/...` pour CRUD + dashboards
  * `apps/pos/pages/...` parcours vente (rapide)
  * `apps/waiter/pages/...` parcours service (table/commande)
* Garder les routes **stables** : pas de renommage sans migration + redirections si besoin.

## 6) i18n multi-app (namespaces)

* Chaque app a ses namespaces :

  * `admin.*`, `pos.*`, `waiter.*`
* Les clés communes sont dans `common.*` (dans `packages/core` si possible).
* Règle : une app ne doit pas dépendre de clés d’une autre app (ex: `pos.*` ne doit pas utiliser `admin.*`).

## 7) State management (Pinia) par app

* Chaque app a ses stores dédiés (feature-first).
* Les stores “communs” (auth/session, permissions, settings) peuvent être partagés via `packages/core` (types + helpers) mais le store Pinia reste côté app (car lifecycle/UX diffère).

## 8) Tables (TanStack) : mutualisation intelligente

* Les “patterns” de tables (tri, filtres, pagination, mapping colonnes) vont dans `packages/table`.
* Les colonnes UI et textes restent côté app (car i18n + besoins différents), mais peuvent réutiliser des builders communs.

## 9) Desktop (Tauri) si applicable

* Si `apps/pos` est en Tauri :

  * intégrer les plugins Tauri uniquement dans `apps/pos` (pas dans core/ui)
  * exposer des abstractions côté `packages/core` (ex: `PrinterService` interface) et implémentations côté `apps/pos`.

## 10) Règles de dépendances (anti-spaghetti)

* `apps/*` peuvent dépendre de `packages/*`.
* `packages/ui` peut dépendre de `packages/core`.
* `packages/api` peut dépendre de `packages/core`.
* Interdit : `packages/core` dépend de `apps/*`.
* Interdit : dépendances circulaires entre packages.

## 11) Conventions “feature-first” (dans chaque app)

* `features/<feature>/components|composables|stores|services|tables`
* Les pages importent depuis `features/*` (pas l’inverse).

## 12) Qualité & maintenance

* Toute nouvelle feature :

  1. définir types + Zod dans `packages/core`
  2. endpoints dans `packa
