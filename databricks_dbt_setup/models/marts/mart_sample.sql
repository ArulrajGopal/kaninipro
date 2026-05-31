with base as (
    select * from {{ ref('stg_sample') }}
)

select
    dept,
    count(id)       as employee_count
from base
group by dept