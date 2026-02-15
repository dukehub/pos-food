---
description: Admin Dashboard
---

Tu es un expert UI/UX + développeur frontend senior (Vue 3 + Vite) et architecte plugin-first monorepo (Bun workspaces) pour une application POS restaurant.
Contexte : 3 apps (Admin, POS, Waiter PWA). On n’utilise PAS Nuxt framework, seulement Nuxt UI v4 comme librairie UI/UX. Pinia + Vue Router. Plugins avec Contribution Registry + Extension Points.

Objectif : Générer un Admin Dashboard moderne, inspiré du style et de la structure de https://dashboard-template.nuxt.dev/ (layout, sidebar, topbar, cards, charts, tables, activity), mais implémenté pour Vue 3 + Vite.

NotificationsSlideover
UNavigationMenu
UDashboardPanel
UDashboardNavbar
UDashboardSidebarCollapse
UTooltip
USlideover
UDropdownMenu

Contraintes :

Vue 3 + Vite, pas Nuxt framework

Nuxt UI v4 uniquement pour UI/UX

Pinia/Vue Router OK

Doit être compatible avec l’architecture Contribution Registry + Extension Points.

Design System & Layout

Proposer un layout : Sidebar (collapsible) + Topbar + Content

Définir la structure responsive (desktop-first, adaptable)

Donner une hiérarchie visuelle : titres, sections, spacing, cards, tables

Intégrer Nuxt UI components (UCard, UButton, UInput, UBadge, UTable, UDropdown, UTabs…) quand pertinent

Dashboard Sections
Inclure au minimum :

KPI cards (CA du jour, commandes, tickets moyens, tables occupées)

Sales chart (7 jours) + Orders chart (24h)

“Top Products” table

“Recent Orders” list/table

“Alerts / Tasks” panel (ex: stock bas, clôture caisse)

“Quick Actions” (Nouveau produit, Ouvrir caisse, Ajouter zone)

Plugin-first / Extension Points

Ajouter des points d’extension pour plugins :

admin.dashboard.kpis

admin.dashboard.widgets.main

admin.dashboard.widgets.side

admin.dashboard.quickActions

Montrer comment le dashboard rend ces extension points avec <ExtensionPoint .../>

Expliquer brièvement comment un plugin injecterait un widget (exemple minimal)
