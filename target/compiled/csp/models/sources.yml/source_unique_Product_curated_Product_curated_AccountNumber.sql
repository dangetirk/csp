
    
    

with dbt_test__target as (

  select AccountNumber as unique_field
  from `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_curated`.`Product_curated`
  where AccountNumber is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


