with _fact_factures as (
    select *,
        {{ get_year('"date_edit"') }} as "annees",
        {{ get_french_month('"date_edit"') }} as "mois",
        {{ get_french_day('"date_edit"') }} as "jour"
    from {{ ref('stg_factures') }}
)

select * from _fact_factures