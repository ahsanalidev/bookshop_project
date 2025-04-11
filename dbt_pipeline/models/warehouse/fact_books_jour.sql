with _fact_books_jour as (
  select 
    {{ get_french_day('"date_edit"') }} as "jour",
    "books_id",
    sum("qte") as "total_sold"
  from {{ ref('stg_ventes') }}
  group by "jour", "books_id" 
  order by "jour", "books_id"
)

select * from _fact_books_jour