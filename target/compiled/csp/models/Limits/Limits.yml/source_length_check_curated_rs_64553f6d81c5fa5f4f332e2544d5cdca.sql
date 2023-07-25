
SELECT
  1
FROM
  `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_facility_curated`
WHERE
  LENGTH(CCS_Account_a_Discounted_Account__c) > 255
