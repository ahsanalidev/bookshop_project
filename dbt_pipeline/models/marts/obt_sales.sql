with ventes as (
    select * from {{ ref('fact_ventes') }}
),

factures as (
    select * from {{ ref('fact_factures') }}
),

books as (
    select * from {{ ref('dim_books') }}
),

category as (
    select * from {{ ref('dim_category') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
)

select
    v."id",
    v."annees",
    v."mois",
    v."jour",
    v."pu",
    v."qte",
    f."id" as "facture_id",
    f."code" as "facture_code",
    f."qte_totale",
    f."total_amount",
    f."total_paid",
    c."intitule" as "category_intitule",
    b."code" as "book_code",
    b."intitule" as "book_intitule",
    b."isbn_10",
    b."isbn_13",
    cust."code" as "customer_code",
    cust."nom" as "customer_nom"
from ventes v
join factures f on v."factures_id" = f."id"
join books b on v."books_id" = b."id"
join category c on b."category_id" = c."id"
join customers cust on f."customers_id" = cust."id"