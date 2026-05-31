with base as (
    select * from {{ ref('stg_sample') }}
)

select
    age_group,
    count(id)       as total_people,
    avg(age)        as avg_age,
    min(age)        as min_age,
    max(age)        as max_age
from base
group by age_group