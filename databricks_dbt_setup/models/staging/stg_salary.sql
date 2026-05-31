select 
    *,
    current_timestamp() as updated_time
from kaninipro.dev.raw_employee_salary
where is_active = true