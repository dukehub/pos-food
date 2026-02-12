---
trigger: always_on
---

# Rule #5: API, DTO, auth/session, caching, offline — (POS/Waiter first)

## 1) DTO & contrats API (obligatoire)

* Tous les DTO (request/response) doivent être définis dans `packages/core/dto/*` (+ schémas Zod si possible).
* `packages/api` doit exposer des fonctions “endpoint-first” (ex: `products.list()`, `orders.create()`, `tickets.print()`).
* Interdit : construire des payloads “free-form” dans les composants/pages.

## 2) Validation runtime des réponses

* Les réponses API importantes doivent être validées (Zod parse/safeParse) au moins sur :

  * auth/session
  * commandes/ventes
  * paiements
  * tickets/clôtures
* Si invalid : erreur normalisée `UNKNOWN` + log contrôlé.

## 3) Auth/session (standard)

* Un seul mécanisme d’auth côté frontend :

  * `packages/api/auth` gère login/refresh/logout
  * token/refresh stockés selon ta stratégie (cookie httpOnly recommandé si possible)
* Toutes les requêtes passent par le client HTTP unique (interceptors/handlers).
* Interdit : gérer un token à la main dans chaque feature.

## 4) RBAC côté API + UI

* Le backend est la source de vérité (le frontend masque mais ne “sécurise” pas).
* Le frontend doit :

  * afficher/masquer actions via `can(...)`
  * bloquer la navigation via middleware
  * gérer `403` avec écran/redirect propre

## 5) Caching & invalidation (pragmatique)

* Caching local autorisé pour :

  * produits
  * plan de salle/tables
  * paramètres (taxes, imprimantes, etc.)
* Invalidation déclenchée par :

  * versioning (ex: `settingsVersion`)
  * timestamps “updatedAt”
  * ou endpoint “changes since…”
* Interdit : “cache infini” sans invalidation.

## 6) Offline mode (POS/Waiter)

* Objectif : l’app reste utilisable même si réseau instable (au minimum lecture + file d’attente).
* Règle : toute action critique doit être conçue comme “command” :

  * créer commande
  * ajouter item
  * envoyer cuisine
  * encaisser
* Si offline :

  * on écrit une “queue” locale (IndexedDB ou storage adapté)
  * on marque l’état UI “pending”
  * on resynchronise quand la connexion revient

## 7) Conflits de sync (règles simples)

* Définir une stratégie claire :

  * “last write wins” pour certaines entités
  * “server wins” pour d’autres
  * ou résolution manuelle (rare)
* Toujours afficher un état compréhensible côté Waiter (ex: “Envoyé”, “En attente”, “Échec – Réessayer”).

## 8) Gestion des erreurs réseau (UX)

* Timeout + retry contrôlé uniquement dans `packages/api`.
* Messages utilisateurs via i18n keys :

  * `errors.network`
  * `errors.timeout`
  * `errors.server_unavailable`
* Interdit : afficher des stack traces.

## 9) Observabilité minimale

* Créer une couche `packages/core/telemetry` (même simple) :

  * events (ex: `order_created`, `payment_failed`)
  * erreurs normalisées (code + contexte)
* POS : log local possible (utile pour debug offline) mais jamais de données sensibles en clair.

## 10) Multi-tenant (si plugins par client)

* Chaque requête API doit inclure le contexte client/tenant (header ou param) si ton backend le demande.
* Les “plugins” activés doivent venir d’un endpoint `features.enabled` et être stockés dans un store “settings”.
* Interdit : activer/désactiver des plugins par simple “flag” hardcodé dans le frontend.
