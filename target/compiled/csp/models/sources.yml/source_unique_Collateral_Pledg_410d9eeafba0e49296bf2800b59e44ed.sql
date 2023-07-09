
    
    

with dbt_test__target as (

  select Collateral as unique_field
  from `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_curated`.`Collateral_Pledged_curated`
  where Collateral is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


