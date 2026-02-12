---
trigger: always_on
---

# Rule: Frontend stack Nuxt UI v4 (Vue 3) — conventions obligatoires

## 1) Stack et versions (non négociable)

* UI: **Nuxt UI v4** , **Tailwindcss** uniquement (pas de Vuetify/Element/Quasar).
* Vue: **Vue 3** (Composition API).
* Icons: **@nuxt/icon** (interdit d’utiliser un autre système d’icônes).
* Fonts: **@nuxt/fonts** (interdit de charger des polices manuellement via  ou @import).
* i18n: **vue-i18n v11** (pas d’autre lib i18n).
* State: **Pinia** (pas de Vuex).
* Routing: **vue-router** (si Nuxt: router via pages, et `useRouter/useRoute` côté app).
* Table: **@tanstack/table-core** pour la logique de table (pas de libs “data table” concurrentes).
*  

  ```
  @vee-validate , Zod
  ```

    

## 2) Architecture & dossiers

* Composants UI: `components/` (présentation uniquement).
* Composants “feature”: `features/<feature>/components`, `features/<feature>/composables`, `features/<feature>/stores`.
* Stores Pinia: `stores/` (global) + `features/**/stores` (feature-scoped).
* i18n: `locales/<lang>.json` + clés hiérarchiques (ex: `pos.ticket.total`).
* Tables: logique tanstack dans `features/**/tables/` + render dans des composants dédiés.

## 3) Style de code (Vue 3 + Nuxt)

* Toujours **`<script setup lang="ts">`**.
* Composition API only (pas d’Options API).
* Pas de logique métier dans les composants UI : elle va dans `composables/` ou `services/`.
* Imports triés: externes -> internes -> styles.
* Nommer les composables: `useXxx()` ; stores: `useXxxStore()`.

## 4) Nuxt UI v4 (règles d’usage)

* Utiliser en priorité les composants Nuxt UI (UButton, UInput, UCard, UModal, UDropdown, etc.).
* Toute personnalisation visuelle doit passer par:

  * tokens/props/classes Nuxt UI,
  * ou un seul fichier de style global (pas de styles inline dispersés).
* Interdit: copier/coller du HTML “custom” pour refaire un composant déjà existant dans Nuxt UI.

## 5) @nuxt/icon (règles d’icônes)

* Toutes les icônes via `<Icon name="..." />`.
* Interdit: SVG inline ou packs d’icônes importés manuellement.

## 6) @nuxt/fonts (règles de polices)

* Déclaration des polices via la config Nuxt (@nuxt/fonts).
* Interdit: Google Fonts via CDN, `<link>` dans app.vue, ou `@import` CSS.

## 7) vue-i18n v11 (règles i18n)

* Tout texte visible doit être traduit (sauf noms propres / codes).
* Utiliser `t('...')` (ou `$t`) ; pas de chaînes “hardcodées”.
* Formatage date/nombre via i18n (pas de `.toLocaleString()` direct dans le code métier).

## 8) Pinia (règles de state)

* Stores “feature-first” : un store par domaine (ex: `posCart`, `products`, `auth`).
* Les stores ne font pas de rendu UI.
* Les effets réseau/IO passent par `services/` (ex: `api/*.ts`) puis consommés par store/composables.

## 9) Tables (TanStack Table Core)

* TanStack gère: colonnes, tri, filtrage, pagination, row models.
* Le rendu (table header/body, pagination UI) doit être dans un composant Nuxt UI (ou composants maison minimes).
* Interdit: utiliser une “DataTable” externe qui encapsule tout et bloque la personnalisation.

## 10) Qualité & cohérence

* Aucune dépendance UI additionnelle sans décision explicite (PR + rationale).
* Les nouveaux écrans doivent:

  * utiliser Nuxt UI,
  * être i18n-ready,
  * et respecter le pattern feature-first.
