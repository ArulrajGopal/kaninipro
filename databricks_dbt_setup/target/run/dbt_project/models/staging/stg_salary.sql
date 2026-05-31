
  
  
  
  create or replace view `kaninipro`.`dev`.`stg_salary`
  
  as (
    select 
    *,
    current_timestamp() as updated_time
from kaninipro.dev.raw_employee_salary
where is_active = true
  )
