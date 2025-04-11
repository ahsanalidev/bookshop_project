with _dim_customers as (
    select
        *,
        "first_name" || ' ' || "last_name" as "nom"
    from {{ ref('stg_customers') }}
)

select * from _dim_customers