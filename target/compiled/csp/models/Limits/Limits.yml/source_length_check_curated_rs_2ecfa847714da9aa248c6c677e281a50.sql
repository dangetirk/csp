
SELECT
  1
FROM
  `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_legal_entities_curated`
WHERE
  LENGTH(LastModifiedById) > 18
