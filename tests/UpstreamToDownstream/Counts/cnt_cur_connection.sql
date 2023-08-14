WITH RawCounts AS (
  SELECT
    'raw_layer' AS layer,
    COUNT(*) AS count
  FROM
    dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_curated.cur_Connection
  WHERE Relationship||coalesce(UID,'0')  IN (SELECT llc_bi__connected_from__c||coalesce(llc_bi__uid__c,'0') FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_connection_curated)
),
CuratedCounts AS (
  SELECT
    'curated_layer' AS layer,
    COUNT(*) AS count
  FROM
    dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_connection_curated
)
  SELECT 1 FROM (
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
  ) where 1 = case when raw_count = curated_count then 0 else 1 end 
