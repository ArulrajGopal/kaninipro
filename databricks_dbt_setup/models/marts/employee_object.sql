
select 
 A.id,
    A.name,
    A.dept,
    A.joined as joined_date,
    B.salary,
    B.start_date as salary_updated_time
from {{ ref('stg_employees') }} A  
join {{ ref('stg_salary') }} B ON A.id = B.id