---
trigger: manual
---

# Prompt Antigravity: lancer le projet (Nuxt UI v4 + Bun monorepo)

Tu es Agent sur un monorepo Bun avec 3 apps Nuxt :

* apps/admin
* apps/pos
* apps/waiter
  et des packages partagés dans /packages.

Objectif: démarrer le projet en mode développement **maintenant**.

1. Vérifie au root la présence de:

* bun.lockb
* package.json (workspaces)
* apps/*/package.json

2. Si les dépendances ne sont pas installées:

* exécute `bun install` au root.

3. Assure-toi que chaque app a un script `dev` valide.

* Si une app n’a pas `dev`, ajoute-le dans son package.json (ex: `"dev": "nuxt dev"`).
* Assure-toi que Nuxt est bien installé (localement via deps), et que `nuxt.config.ts` existe.

4. Ajoute des scripts au root (si absents) :

* `dev:admin` -> lancer `apps/admin`
* `dev:pos` -> lancer `apps/pos`
* `dev:waiter` -> lancer `apps/waiter`

5. Lance l’app demandée (par défaut POS) et confirme:

* URL locale affichée
* aucune erreur bloquante au démarrage

Commandes attendues (ordre recommandé):

* `bun install`
* `bun run dev:pos` (ou dev:admin / dev:waiter)

Contraintes:

* Utiliser Bun uniquement (pas npm/yarn/pnpm)
* Ne pas modifier l’architecture; uniquement scripts/config nécessaires au démarrage
* Si erreur, propose la correction minimale et relance
* À la fin, affiche la commande exacte pour lancer chaque app
