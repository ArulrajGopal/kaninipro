
  
  
  
  create or replace view `kaninipro`.`dev`.`stg_sample`
  
  as (
    select
    *
from kaninipro.dev.employees
where salary > 100000
  )
