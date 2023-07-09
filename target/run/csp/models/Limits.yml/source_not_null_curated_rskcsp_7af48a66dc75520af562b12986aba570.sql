select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select CreatedById
from `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_cardholder_curated`
where CreatedById is null



      
    ) dbt_internal_test