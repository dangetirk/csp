select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
SELECT
  1
FROM
  `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_limit_curated`
WHERE
  LENGTH(CCS_Facility__c) > 18

      
    ) dbt_internal_test