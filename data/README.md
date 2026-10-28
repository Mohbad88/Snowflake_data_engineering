# Données sources

Les fichiers CSV chargés dans Snowflake se trouvent dans `raw/`. Chaque fichier comporte une ligne d’en-tête; les colonnes suivent l’ordre des tables de staging créées par `sql/ddl/ddl.sql`.

| Fichier | Table Snowflake | Colonnes |
|---|---|---|
| `bookings.csv` | `AIRBNB.STAGING.BOOKINGS` | `booking_id`, `listing_id`, `booking_date`, `nights_booked`, `booking_amount`, `cleaning_fee`, `service_fee`, `booking_status`, `created_at` |
| `hosts.csv` | `AIRBNB.STAGING.HOSTS` | `host_id`, `host_name`, `host_since`, `is_superhost`, `response_rate`, `created_at` |
| `listings.csv` | `AIRBNB.STAGING.LISTINGS` | `listing_id`, `host_id`, `property_type`, `room_type`, `city`, `country`, `accommodates`, `bedrooms`, `bathrooms`, `price_per_night`, `created_at` |

Ces fichiers sont les données d’exemple du projet source. Vérifie leurs conditions d’utilisation avant toute redistribution en dehors de ce dépôt.
