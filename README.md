# esilv-agentic-ai-td1
# Trustworthy Generative AI : TD1 à TD3

**Classe :** DIA5 · **Sous-groupe :** DIA5-G3 · **Membres :** Diaila DIALLO, Meriam BOUMEDIENE, Lina ZAAQ, Imane BOUNA MOCTAR, Arthur GAUCHÉ, Jean VASSEUR, Simeon SIMEONOV

## Présentation du projet
Ce dépôt contient le travail du sous-groupe pour les trois TD du cours Next Generation AI à l'ESILV (thème « Trustworthy Generative AI »). Le TD1 teste et compare cinq modèles d'IA générative gratuits sur 20 questions text-to-SQL. Le TD2 fait voter ces modèles et écrit la règle de routage. Le TD3 chiffre les configurations et choisit l'une d'elles pour un cas d'usage.

## Organisation du dépôt

```
.
├── README.md
├── td1/                 TD1 (21/10) : références, traces des cinq modèles, tableaux de synthèse
│   └── README.md
├── td2/                 TD2 (18/11) : un dossier par binôme
│   ├── README.md
│   ├── A-quorum/        binôme A : vote k-sur-n (Step 1)
│   │   ├── README.md
│   │   ├── review-1.md  review par le binôme B
│   │   ├── review-2.md  review par le binôme C
│   │   └── ...
│   ├── B-consensus/     binôme B : faux consensus (Step 2)
│   │   ├── README.md
│   │   ├── review-1.md  review par le binôme A
│   │   ├── review-2.md  review par le binôme C
│   │   └── ...
│   └── C-routing/       binôme C : règle de routage (Step 3)
│       ├── README.md
│       ├── review-1.md  review par le binôme A
│       ├── review-2.md  review par le binôme B
│       └── ...
├── td3/                 TD3 (11/12)
│   └── README.md
└── reports/
    ├── td1.md
    ├── td2.md
    └── td3.md
```

Chaque TD a son `README.md` (contenu, fichiers, commandes pour rejouer) et son rapport dans `reports/`. Au TD2, chaque binôme a son dossier avec son `README.md` et les deux reviews reçues des autres binômes : `review-1.md` et `review-2.md`, dans l'ordre alphabétique des binômes relecteurs.

## Rejouer

Python 3 (bibliothèque standard), sans clé ni réseau, depuis la racine du dépôt : voir les commandes de [`td2/README.md`](td2/README.md). Les scripts du TD2 lisent les traces du TD1 dans `td1/`.

## Informations
Cours : Next Generation AI · École : ESILV · Rendus : commit enregistré sur Moodle le dimanche qui suit chaque TD, à 23:59.
