with _fact_books_annees as (
  select 
    {{ get_year('"date_edit"') }} as "annees",
    "books_id",
    sum("qte") as "total_sold"
  from {{ ref('stg_ventes') }}
  group by "annees", "books_id" 
  order by "annees", "books_id"
)

select * from _fact_books_annees