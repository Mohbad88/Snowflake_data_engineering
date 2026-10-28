# Projet d’ingénierie de données Airbnb

Projet d’apprentissage qui transforme des fichiers CSV de réservations, d’hôtes et d’annonces avec Snowflake et dbt. Les modèles suivent une architecture en couches **Bronze → Silver → Gold**; dbt gère également des snapshots pour historiser les changements.


1. Les CSV sont chargés dans les tables de staging Snowflake.
2. Les modèles Bronze reprennent les données sources.
3. Les modèles Silver nettoient et enrichissent les données.
4. Les modèles Gold produisent les tables d’analyse et les snapshots.

Le chargement des fichiers est manuel. Le projet fournit un stage interne Snowflake et des commandes `COPY INTO`; aucun compte AWS ni identifiant AWS n’est nécessaire pour le parcours de démarrage décrit ici.

## Arborescence

```text
.
├── data/
│   ├── README.md
│   └── raw/                         # CSV d’origine
├── scripts/validate_data.py          # Vérification des fichiers CSV
├── tests/test_validate_data.py       # Tests du vérificateur
├── dbt/                             # Projet dbt
│   ├── models/
│   │   ├── sources/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── macros/
│   ├── snapshots/
│   ├── tests/
│   └── dbt_project.yml
├── docs/architecture.png
├── sql/ddl/                         # Tables de staging et chargement
├── .python-version
├── pyproject.toml
└── README.md
```

## Prérequis

- Un compte Snowflake et un rôle autorisé à créer/lire les tables, les schémas et le warehouse utilisés.
- Python 3.12 ou plus récent.
- [uv](https://docs.astral.sh/uv/) pour installer les dépendances Python et dbt.

## Installation et configuration

Depuis la racine du dépôt, dans PowerShell :

```powershell
uv sync --python 3.12

New-Item -ItemType Directory -Force "$env:USERPROFILE\.dbt"
Copy-Item .\dbt\profiles.example.yml "$env:USERPROFILE\.dbt\profiles.yml"

$env:SNOWFLAKE_ACCOUNT = "votre_identifiant_de_compte"
$env:SNOWFLAKE_USER = "votre_utilisateur"
$env:SNOWFLAKE_PASSWORD = "votre_mot_de_passe"
$env:SNOWFLAKE_ROLE = "votre_role"
$env:SNOWFLAKE_WAREHOUSE = "votre_warehouse"
```

Les variables définies avec `$env:` ne durent que le temps de la session PowerShell. Le fichier `profiles.yml` les lit au lancement de dbt; ne mets pas de mot de passe dans le dépôt.

## Préparer Snowflake et charger les CSV

1. Exécuter `sql/ddl/ddl.sql` pour créer la base `AIRBNB`, le schéma `STAGING` et les tables.
2. Exécuter `sql/ddl/resources.sql` pour créer le format CSV et le stage interne.
3. Déposer les trois fichiers de `data/raw/` dans le stage `AIRBNB.STAGING.AIRBNB_FILES` avec Snowsight.
4. Exécuter les trois commandes `COPY INTO` à la fin de `sql/ddl/resources.sql` pour charger les données dans les tables de staging.

Les scripts sont réexécutables sans remplacer les tables déjà créées. Snowflake peut afficher les clés primaires comme contraintes informatives; elles ne remplacent pas les tests de qualité dbt.

## Vérifier et exécuter dbt

Depuis la racine du dépôt :

```powershell
uv run --project . dbt debug --project-dir .\dbt --profiles-dir "$env:USERPROFILE\.dbt"
uv run --project . dbt parse --project-dir .\dbt --profiles-dir "$env:USERPROFILE\.dbt"
uv run --project . dbt build --project-dir .\dbt --profiles-dir "$env:USERPROFILE\.dbt"
```

`dbt build` exécute les modèles, tests et snapshots. Une connexion Snowflake configurée et les tables de staging chargées sont nécessaires pour l’exécution complète. Pour reconstruire les modèles incrémentaux depuis zéro, utiliser `dbt build --full-refresh` avec les mêmes options.

## Données incluses

| Fichier | Contenu | Lignes de données |
|---|---|---:|
| `data/raw/bookings.csv` | Réservations | 5 000 |
| `data/raw/hosts.csv` | Hôtes | 200 |
| `data/raw/listings.csv` | Annonces | 500 |

Le détail des colonnes et des noms de tables se trouve dans [`data/README.md`](data/README.md).

Pour contrôler les en-têtes et le nombre de colonnes des fichiers CSV avant leur chargement dans Snowflake :

```powershell
uv run --project . python .\scripts\validate_data.py
uv run --project . python -m unittest discover -s tests
```

Le script lit `data/raw/` par défaut. Un autre répertoire peut être vérifié avec `--data-dir`.

## Identifiants et sécurité

- `dbt/profiles.example.yml` ne contient que des références aux variables d’environnement.
- Ne committe jamais `profiles.yml`, un fichier `.env` ou des identifiants Snowflake/AWS.
- Le stage utilisé par le parcours de démarrage est interne à Snowflake. Si tu configures un stage S3 séparément, utilise une intégration de stockage Snowflake plutôt que des clés AWS dans le SQL.
