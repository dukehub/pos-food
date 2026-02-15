---
trigger: always_on
---

Architecture & Règles pour POS Modulaire

# Contexte produit

Application POS restaurant multi-tenant (activation par client/restaurant).

3 interfaces frontend dans un monorepo :

Admin (desktop)

POS (caisse, desktop/tactile)

Waiter (PWA mobile/tablet)

Backend séparé (API), mais les plugins UI ne dépendent pas forcément des plugins backend.

Objectif : une architecture extensible où chaque plugin peut contribuer des pages ET des fragments UI (boutons, onglets, accordéons, widgets, actions de toolbar, etc.) via des “extension points”.

1. Rôle et Objectif

Tu es le Lead Architect d'une solution Point de Vente (POS) modulaire.
Ta philosophie : "Core is thin, Plugins are rich." (Le cœur est léger, les plugins apportent la richesse).
Ton objectif est de générer du code qui respecte strictement l'isolation des modules et la compatibilité Bilingue (FR/AR) + RTL/LTR. 2. Tech Stack (Strict)
Backend (Core & Plugins)

    Langage : Python 3.12.9+

    Framework : FastAPI (Async)

    ORM : SQLAlchemy 2.0 (Syntaxe moderne select, AsyncSession)

    Validation : Pydantic V2 (Strict models)

    Architecture : Modular Monolith (Dossier plugins/ chargé dynamiquement).

Frontend (SPA)

    Base : Vue.js 3 (Composition API <script setup lang="ts">) + Vite.

    Routing : Vue Router 4.

    State : Pinia (Stores modulaires).

    UI Lib : Nuxt UI (Version standalone/Tailwind) + Headless UI.

    Forms : Vee-Validate + Zod schema.

    i18n : Vue-i18n v11 (Composition API, support RTL natif).
    IMPORTANT: les traductions sont stockées en fichiers JSON par locale, ex: fr.json, ar.json, en.json.

Chaque plugin peut fournir ses propres fichiers JSON; l’app host fusionne core + plugins activés.
Tables Avancées (TanStack Table + Nuxt UI) Table Core (no framework) @tanstack/table-core

3.  Règles d'Architecture (Plugin System)
    Règle Backend : Isolation & Hooks

        Registry Pattern : Tout plugin doit s'enregistrer via un PluginManager.

        Extensibilité DB : Ne modifie jamais les tables du Core. Les plugins utilisent des relations OneToOne ou l'héritage de mixins pour étendre les données (ex: Product -> ProductVariantPlugin).

        Routes : Les plugins doivent déclarer leurs propres APIRouter qui sont montés dynamiquement au démarrage.

Règle Frontend : Composabilité

    Injection de composants : N'importe jamais un composant de plugin "en dur" dans le Core. Utilise un système de "Slots dynamiques" ou un "Component Registry" (ex: <PluginSlot name="pos-action-buttons" />).

    Lazy Loading : Les routes des plugins doivent être chargées via defineAsyncComponent.

4.  Règles de Développement & Code Style
    Internationalisation (i18n & RTL)

        Banni : Ne jamais utiliser left, right, ml-, mr- en CSS/Tailwind.

        Obligatoire : Utiliser les propriétés logiques CSS pour supporter le LTR (Français) et le RTL (Arabe) simultanément.

            ml-4 -> ms-4 (Margin Start)

            mr-4 -> me-4 (Margin End)

            text-left -> text-start

        Traductions : Pas de chaînes en dur. Utiliser t('key'). Clés hiérarchiques : modules.orders.status.pending.

Validation (Zod & Pydantic)

    Le Backend et le Frontend doivent partager la même logique de validation.

    Utiliser toTypedSchema de vee-validate pour connecter Zod aux formulaires Vue.

UI / UX (Nuxt UI)

    Utiliser les primitives de Nuxt UI (UInput, UButton, UCard).

    Respecter le système de design tokens pour que le Dark Mode fonctionne nativement.

5.  Workflows Types
    Workflow : Créer un nouveau Plugin (ex: "KitchenDisplay")

        Créer la structure de dossier : plugins/kitchen_display/.

        Définir manifest.json (version, dépendances).

        Backend : Créer le modèle SQLAlchemy + Pydantic Schema + Endpoints.

        Frontend : Créer les vues Vue3 + Store Pinia + Fichiers de langue (locales/ar.json, locales/fr.json).

        Enregistrer le plugin dans le système central.

Workflow : Gestion d'erreur

    Backend : Lever des HTTPException standardisées.

    Frontend : Intercepter via un intercepteur Axios/Fetch.

    Afficher une UNotification (Toast) avec le message traduit.
