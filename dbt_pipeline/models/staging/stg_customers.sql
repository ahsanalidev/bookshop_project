with _stg_customers as (
    select * from {{ source('raw', 'customers') }}
)

select * from _stg_customers