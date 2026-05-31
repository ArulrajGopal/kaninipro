
  
    
        create or replace table `kaninipro`.`dev`.`mart_sample`
      
      
    using delta
  
      
      
      
      
      
      
      
      
      as
      with base as (
    select * from `kaninipro`.`dev`.`stg_sample`
)

select
    dept,
    count(id)       as employee_count
from base
group by dept
  