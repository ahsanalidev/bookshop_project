with _stg_category as (
    select * from {{ source('raw', 'category') }}
)

select * from _stg_category