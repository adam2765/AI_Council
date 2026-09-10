# Conseil des IAs

Poser une question à quatre intelligences artificielles à la fois, les faire
débattre entre elles, puis demander à une cinquième de trancher.

## Le problème

Quand on pose une question à une IA, elle répond toujours sur le même ton
assuré — qu'elle ait raison ou qu'elle invente. Rien dans sa réponse ne
permet de faire la différence.

L'idée ici : si on pose la même question à plusieurs IA conçues par des
équipes différentes, les endroits où elles se contredisent sont justement
les endroits où la question est réellement incertaine. Là où elles tombent
toutes d'accord, on peut être un peu plus tranquille.

Le but n'est donc pas d'obtenir une réponse unanime, mais de rendre les
désaccords visibles au lieu de les cacher derrière une réponse lisse.

## Comment ça marche

Le fonctionnement est calqué sur celui d'un jury.

1. **Chacun répond seul.** Les quatre IA reçoivent la question sans savoir
   ce que les autres ont répondu. Personne n'est influencé. Si un membre en
   a besoin, il peut chercher sur le web avant de répondre — utile pour une
   question qui dépend d'une information récente.
2. **Tout le monde lit tout le monde.** On renvoie à chaque IA les réponses
   des autres, en anonyme (« Membre 1 », « Membre 2 »…), et on lui demande
   soit de corriger son avis, soit de le maintenir en expliquant pourquoi.
3. **Un président tranche.** Une cinquième IA, qui n'a pas participé au
   débat, lit les avis révisés, dit sur quoi les membres divergent vraiment,
   et donne la réponse finale.

L'anonymat du tour 2 est volontaire : une IA qui sait qu'elle relit un
concurrent — ou sa propre réponse — ne réagit pas de la même façon.

## Qui siège au conseil

Quatre IA de familles différentes, développées sur des continents différents :

- `gpt-5-mini` (OpenAI, États-Unis)
- `deepseek-r1` (DeepSeek, Chine)
- `qwen3` (Alibaba, Chine)
- `kimi-k2.5` (Moonshot, Chine)

Le président est `claude-sonnet-4.6` (Anthropic, États-Unis), qui ne fait
pas partie des quatre.

Ce choix n'est pas décoratif. Des IA entraînées de façon similaire ont
tendance à se tromper de la même façon : si elles sont d'accord entre elles,
ça ne prouve rien. En mélangeant les origines, un accord a plus de valeur.

## Exemple

On lance le programme, il pose une question :

    Question : Vaut-il mieux éteindre son ordinateur le soir ou le laisser en veille ?

Le débat entre les IA se déroule en coulisses. Seule la conclusion du
président s'affiche — voici à quoi elle ressemble :

    Les membres sont d'accord sur l'essentiel : la veille consomme peu et
    l'usure liée aux allumages répétés est négligeable sur du matériel
    récent. Ils divergent réellement sur deux points :

    1. La consommation en veille. Deux membres l'estiment négligeable,
       un troisième rappelle qu'un ordinateur de bureau avec plusieurs
       périphériques peut consommer bien davantage qu'un portable.
    2. Les mises à jour. Un membre considère que le redémarrage régulier
       est le vrai argument, les autres n'en parlent pas.

    Réponse finale : pour un portable, la veille est très bien au quotidien,
    avec un redémarrage complet une fois par semaine. Pour une tour avec
    écran et périphériques, éteindre le soir reste plus pertinent. [...]

*(exemple reconstitué pour illustrer le format, pas une vraie sortie)*

## Installation

Il faut **Python** installé sur la machine ([python.org](https://www.python.org/downloads/)),
et un compte sur **OpenRouter** ([openrouter.ai](https://openrouter.ai)) — un
service qui donne accès à toutes ces IA via un seul abonnement, au lieu
d'ouvrir un compte chez chaque fournisseur.

Installer les bibliothèques nécessaires :

    pip install -r requirements.txt

Créer un fichier nommé `.env` à côté du programme, contenant la clé
personnelle fournie par OpenRouter :

    OPENROUTER_API_KEY=votre_clé_ici

Ce fichier n'est jamais partagé : il est exclu du dépôt.

## Utilisation

    python conseil.py

Le programme demande la question, réfléchit un moment, puis affiche la
synthèse finale.

**À savoir :** une seule question déclenche au moins 9 échanges avec les IA
(4 au premier tour, 4 au second, 1 pour le président) — davantage si un
membre décide de chercher sur le web, ce qui lui coûte un échange
supplémentaire. C'est facturé par OpenRouter, en général quelques
centimes, mais ce n'est pas gratuit — et c'est aussi pour ça que la
réponse met du temps à arriver.

## Ce qui reste à faire

Le programme fonctionne, mais c'est un prototype. Dans l'ordre d'importance :

- **Accélérer.** Les IA sont interrogées une par une, alors qu'elles
  pourraient l'être en même temps. C'est ce qui rend l'attente aussi longue.
- **Encaisser les pannes.** Si une IA ne répond pas, sa case reste vide et
  les autres reçoivent un avis vide au lieu d'un avis manquant. Il faut
  l'écarter proprement, et abandonner si trop de membres tombent.
- **Montrer le débat.** Aujourd'hui tout est jeté sauf la conclusion, donc
  impossible de vérifier ce qui s'est réellement dit. Prévoir une option
  pour afficher les deux tours et les enregistrer.
- **Mieux informer le président.** Il ne lit que les avis révisés. Si une IA
  avait raison au départ et s'est laissé convaincre, l'information est
  perdue. Il faudrait au moins lui signaler qui a changé d'avis.
- **Laisser débattre plus longtemps.** Le nombre de tours est figé à un.
  Le rendre réglable, et s'arrêter tout seul quand plus personne ne bouge.
- **Poser la question directement** en ligne de commande, pour pouvoir
  automatiser des séries de questions.
- **Afficher le coût** de chaque question.
- **Supprimer l'appel de test** resté en fin de fichier, qui consomme un
  échange inutile à chaque lancement.

## État

Prototype. Code écrit avec assistance IA, architecture et choix de conception personnels.
