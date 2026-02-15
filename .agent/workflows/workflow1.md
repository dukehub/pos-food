---
description: Monorepo avec Bun workspaces
---

Frontend: Vue 3 + Vite + TypeScript + Pinia + Vue Router.

Nuxt UI v4 utilisé uniquement comme librairie UI.

Le Vite plugin Nuxt UI doit être appliqué dans chaque app (vite.config.ts), mais la config est factorisée dans packages/ui.

Styles, tokens, fonts, icons centralisés dans packages/ui.

i18n: vue-i18n@11 dans packages/i18n (plugins fournissent leurs messages).

Validation: zod + vee-validate + @vee-validate/zod dans packages/validation (schémas partagés).

Les libs runtime (vue-i18n, vee-validate, zod) doivent être déclarées en peerDependencies dans les packages concernés et installées côté apps (ou root) pour éviter les soucis de résolution Vite (dependency scan).

Arborescence cible

apps/
admin/
pos/
waiter/
packages/
core/ (contrats plugin, registry, permissions, router injection, contribution points)
ui/ (Nuxt UI setup, styles globales, thème/tokens, wrappers UI, config Vite exportée)
api/ (client HTTP, interceptors, typed endpoints)
i18n/ (createAppI18n, mergeMessages, loader messages plugins)
validation/ (schemas zod, asVeeSchema, helpers)
plugins/
product/
zones/
etc...
