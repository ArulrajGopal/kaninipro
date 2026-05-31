
  
    
        create or replace table `kaninipro`.`dev`.`employee_object`
      
      
    using delta
  
      
      
      
      
      
      
      
      
      as
      select 
 A.id,
    A.name,
    A.dept,
    A.joined as joined_date,
    B.salary,
    B.start_date as salary_updated_time
from `kaninipro`.`dev`.`stg_employees` A  
join `kaninipro`.`dev`.`stg_salary` B ON A.id = B.id
  