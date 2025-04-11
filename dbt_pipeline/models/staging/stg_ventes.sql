with _stg_ventes as (
    select
        "id",
        "code",
        to_date("date_edit", 'YYYYMMDD') as "date_edit",
        "factures_id",
        "books_id",
        "pu",
        "qte",
        "created_at"
    from {{ source('raw', 'ventes') }}
)

select * from _stg_ventes