with _stg_books as (
    select * from {{ source('raw', 'books') }}
)

select * from _stg_books