with _stg_factures as (
    select
        "id",
        "code",
        to_date("date_edit", 'YYYYMMDD') as "date_edit",
        "customers_id",
        "qte_totale",
        "total_amount",
        "total_paid",
        "created_at"
    from {{ source('raw', 'factures') }}
)

select * from _stg_factures