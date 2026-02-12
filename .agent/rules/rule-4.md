---
trigger: always_on
---

# Rule #4: Environment, config Nuxt, qualité (Bun) — repo ready-to-scale

## 1) Runtime & package manager (Bun only)

* Utiliser **Bun** pour installer, exécuter, et builder.
* Interdit : `npm`, `yarn`, `pnpm` dans le repo.
* Le repo doit contenir :

  * `bun.lockb` (ou lock Bun)
  * des scripts Bun uniques (pas de doublons “dev2/dev3”).

## 2) Monorepo workspaces (3 apps + packages)

* Workspaces déclarés dans le root (Bun workspaces).
* Chaque app `apps/*` a ses scripts :

  * `dev`, `build`, `lint`, `typecheck`, `test` (si tests)
* Chaque package `packages/*` doit être “lean” :

  * pas de dépendances UI lourdes inutilement
  * exports propres (barrel exports) + types.

## 3) TypeScript & alias (obligatoire)

* TS strict (recommandé) + pas de `any` “facile”.
* Aliases cohérents :

  * `@ui/*` → `packages/ui/*`
  * `@core/*` → `packages/core/*`
  * `@api/*` → `packages/api/*`
  * `@table/*` → `packages/table/*`
* Interdit : imports relatifs profonds du style `../../../../`.

## 4) Nuxt config standard (par app)

* Chaque app a son `nuxt.config.ts` clair et minimal.
* Modules attendus :

  * `@nuxt/ui`
  * `@nuxt/icon`
  * `@nuxt/fonts`
  * `@pinia/nuxt`
  * i18n (selon ton choix : intégration Nuxt + vue-i18n v11)
* Règle : toute config “commune” entre apps doit être factorisée (helper `createNuxtConfig()` dans `packages/core/nuxt/` si utile).

## 5) Tailwind / styling

* Tailwind activé via Nuxt UI (ou config dédiée si nécessaire).
* Un seul point d’entrée CSS par app (ex: `assets/css/main.css`).
* Interdit : multiplier les fichiers globaux, ou mettre des styles globaux dans des composants au hasard.

## 6) ESLint + formatting (obligatoire)

* ESLint doit être activé sur tout le repo (apps + packages).
* `lint` ne doit jamais être “optionnel” dans CI.
* Formatage :

  * soit Prettier,
  * soit ESLint format,
  * mais **une seule** source de vérité (pas les deux en conflit).
* Interdit : règles différentes par app sans raison.

## 7) Qualité CI (definition of done)

* Le CI (ou check local) doit au minimum exécuter :

  * `lint`
  * `typecheck`
  * `build` (au moins pour apps)
* Une PR est “mergeable” seulement si ces checks passent.

## 8) Gestion des environnements (env)

* Utiliser `.env` + `.env.example` (jamais de secrets committés).
* Les variables doivent être préfixées et documentées :

  * `NUXT_PUBLIC_*` pour ce qui est exposé client
  * variables privées sans `PUBLIC`
* Interdit : accéder à `process.env` directement dans les composants sans passer par `runtimeConfig`.

## 9) Logging & erreurs

* Pas de `console.log` en prod (autoriser `console.warn/error` si utile).
* Erreurs applicatives :

  * normalisées côté `packages/api`
  * affichées via toasts (Nuxt UI) côté apps

## 10) Scripts root (conventions)

Au root, fournir des scripts simples :

* `bun run dev:admin`
* `bun run dev:pos`
* `bun run dev:waiter`
* `bun run build:all`
* `bun run lint`
* `bun run typecheck`

Interdit : des scripts ambigus ou “magiques” non documentés.
