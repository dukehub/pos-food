---
description: correction env + ExtensionPoint component
---

corriger et utiliser les versions suivantes:
"vite": "^7.3.1",
"typescript": "~5.9.3",
"vue-tsc": "^3.1.5"
"@vee-validate/zod": "^4.15.1",
"vee-validate": "^4.15.1",
"vue-i18n": "^11.2.8",
"zod": "^4.3.6"
"@nuxt/ui": "^4.4.0",
"tailwindcss": "^4.1.18",
"@types/node": "^24.10.1",
"@vitejs/plugin-vue": "^6.0.2",

ExtensionPoint component (packages/ui ou app)

Un composant Vue 3 <ExtensionPoint name="..." :ctx="..."/> qui :

récupère la liste des contributions depuis le registry (inject/provide ou store)

rend une liste de composants async

passe les props via resolveProps(ctx)

gère un fallback “empty” et un fallback “loading”

Montrer comment l’app fournit le registry au runtime (provide/inject ou Pinia store)

Exemples concrets

Exemple 1 : sur Admin Products page, un plugin injecte un bouton dans la toolbar (mountPoint="admin.products.toolbar.actions")

Exemple 2 : un plugin injecte un onglet dans la fiche produit (mountPoint="admin.product.tabs")

Exemple 3 : Waiter injecte un widget “infos table” dans la vue table (mountPoint="waiter.table.sidebar.widgets")

Organisation monorepo

Où placer :

extension points génériques (packages/ui)
types/registry (packages/core)
contributions dans plugins (packages/plugins/\*)
Donner l’arborescence recommandée + conventions de nommage (mountPoint)
