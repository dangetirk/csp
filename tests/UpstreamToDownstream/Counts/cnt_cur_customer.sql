WITH RawCounts AS (
  SELECT
    'raw_layer' AS layer,
    COUNT(*) AS count
  FROM
    dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_curated.cur_customer
  WHERE RelationshipName  IN (SELECT name FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_account_curated)
),
CuratedCounts AS (
  SELECT
    'curated_layer' AS layer,
    COUNT(*) AS count
  FROM
    dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_account_curated
)
  
SELECT
  raw.layer,
  raw.count AS raw_count,
  curated.count AS curated_count,
  CASE
    WHEN raw.count = curated.count THEN 'Pass'
    ELSE 'Fail'
  END AS result
FROM RawCounts raw
left JOIN CuratedCounts curated ON raw.count = curated.count
