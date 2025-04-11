with _dim_books as (
  select * from {{ ref('stg_books') }}
)

select * from _dim_books