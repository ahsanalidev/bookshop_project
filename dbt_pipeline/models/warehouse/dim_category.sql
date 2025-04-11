with _dim_category as (
  select * from {{ ref('stg_category') }}
)

select * from _dim_category