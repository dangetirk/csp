SELECT
Id
,OwnerId
,Name
,CurrencyIsoCode
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
,CreatedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
,LastModifiedById
,CCS_Primary_Security__c
,CCS_Security__c

FROM  dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_ccs_multi_charge_form_asset_curated