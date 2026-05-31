select
    id,
    name,
    age,
    case 
        when age < 30 then 'Young'
        when age between 30 and 40 then 'Mid'
        else 'Senior'
    end as age_group
from hive_metastore.dev.sample_table