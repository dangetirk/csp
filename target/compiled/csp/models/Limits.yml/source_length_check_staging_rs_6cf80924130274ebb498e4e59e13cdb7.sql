
SELECT
  1
FROM
  `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_staging`.`rskcsp_ds_cardholder_staging`
WHERE
  LENGTH(Name) > 45
