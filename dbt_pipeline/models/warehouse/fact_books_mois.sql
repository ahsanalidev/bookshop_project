with _fact_books_mois as (
  select 
    {{ get_french_month('"date_edit"') }} as "mois",
    "books_id",
    sum("qte") as "total_sold"
  from {{ ref('stg_ventes') }}
  group by "mois", "books_id" 
  order by "mois", "books_id"
)

select * from _fact_books_mois