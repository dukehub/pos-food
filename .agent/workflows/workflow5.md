---
description: menu header
---

OBJECTIF (PHASE ESSENTIELLE)
Construire l’interface Admin (Vuejs + Nuxt UI) avec :
1) Socle (shell) : layout dashboard, navigation, routing, auth, RBAC, i18n (FR/AR + RTL), gestion erreurs API.
2) Features internes (pas de UI plugins) :
   - Login + session (refresh si nécessaire)
   - Settings : app_settings
   - Business Profile : business_profile
   - Users : CRUD + roles + activation + reset password
   - Catalog Product (+ i18n) : liste + create/edit (minimum)
   - Orders : listing + détails (lecture)
   - Customers : listing + fiche
   - Devices/Printer : listing + assignations (minimum)
   - Floor plan : CRUD basique (sans drag&drop pour v1)

CONTRAINTES TECHNIQUES
- Monorepo avec Bun (bun workspaces)
- Pinia (stores)
- Vue-router
- Nuxt UI v4
- i18n via vue-i18n@11 OU module Nuxt UI i18n (au choix), mais :
  - ressources en JSON (fr.json, ar.json) dans packages/i18n
  - switch langue + support RTL automatique pour AR
- Tables : @tanstack/table-core
- packages/api : client HTTP unique (fetch/ofetch) + interceptors (401), baseURL via runtime config, gestion d’erreurs normalisée
- packages/core : auth (token/session), RBAC (roles + permissions), tenant (tenant_id) + helpers
- packages/validations : schémas (vee-validate/zod) pour formulaires
- packages/ui : composants partagés (ex: AppPage, DataTable wrapper, ConfirmDialog, FormField…), basés sur Nuxt UI
- pas de système de plugins UI maintenant. Le dossier /plugins doit rester “réservé” (phase PRO) mais ne pilote pas l’essentiel.
- Qualité : ESLint + Prettier + type-safe, structure claire, zéro “spaghetti”

SÉCURITÉ / MULTI-TENANT / RBAC
- Multi-tenant : toutes les requêtes doivent inclure tenant_id (header recommandé : X-Tenant-Id) + prévoir où il est stocké (session)
- RBAC : rôles minimum (ADMIN, WAITER, CASHIER) + permissions fines (ex: users.read, users.write, catalog.read…)
- Guards :
  - middleware global auth
  - middleware permission par page
  - sidebar n’affiche que ce que l’utilisateur a le droit de voir

UX MINIMALE OBLIGATOIRE
- Sidebar + topbar, breadcrumb optionnel
- États : loading, empty, error
- Toasts succès/erreurs
- Tables : search + pagination + tri
- Forms : validation, disabled state, erreurs serveur affichées proprement

LIVRABLES DEMANDÉS (DANS CET ORDRE)
A) Plan d’implémentation en 12–15 étapes max (priorités réalistes)
B) Arborescence complète des dossiers/fichiers (en respectant la structure imposée)
C) Code des fichiers clés COMPLETS (pas des extraits) pour pouvoir lancer l’Admin :
   - apps/admin/nuxt.config.ts
   - apps/admin/app.vue + layout dashboard (Nuxt UI)
   - apps/admin/middleware/auth.global.ts + middleware permission
   - packages/api (client http + error model + auth headers)
   - packages/core (auth store/composable + RBAC + tenant)
   - packages/i18n (fr.json/ar.json + loader + RTL toggle)
   - 2–3 features minimum prêtes (vertical slice) :
     1) Login
     2) Settings (app_settings ou business_profile)
     3) Users (list + create/edit)
D) Commandes Bun pour install/dev/build au niveau monorepo

HYPOTHÈSES
- Si les endpoints exacts ne sont pas fournis, crée une couche API avec fonctions stub + TODO, mais l’app doit tourner.
- Runtime config : NUXT_PUBLIC_API_BASE_URL (et autres si besoin)
- Ne pas inventer un plugin system pour l’essentiel.

STYLE DE RÉPONSE
- Sois concret, orienté code exécutable.
- Utilise Nuxt UI (UButton, UCard, UInput, UForm, UTable, UModal, UNotifications si dispo).
- N’écris pas de texte inutile : donne le plan, l’arborescence, puis le code.


dans sidebar regrouper parametre application, profile entriprise et utilisateurs dans paramètres.
réorganoser le munu:
Dashboard
plan de salle (renome: Plan Restaurant)
Catalogue
appareils & imprimantes
clients
commandes
et en bas: paramètres
mettre profile aAdmin User dans UDropdownMenu avec le menu suivant: profile, theme, apparence(light, dark), deconnexion
dans le header ajouter Notification (USlideover)


Commence maintenant.
