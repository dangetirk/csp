select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select LastModifiedById
from `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_legal_entities_curated`
where LastModifiedById is null



      
    ) dbt_internal_test