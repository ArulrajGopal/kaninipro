
  
  
  
  create or replace view `kaninipro`.`dev`.`stg_employees`
  
  as (
    select 
    *,
    current_timestamp() as updated_time
from kaninipro.dev.raw_employees
  )
