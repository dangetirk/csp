
SELECT
  1
FROM
  `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_facility_curated`
WHERE
  LENGTH(CCS_Set_up_a_direct_debit_to_manage__c) > 255
