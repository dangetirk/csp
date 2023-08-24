SELECT
 Id
,LLC_BI__Classification__c
,CreatedById
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') CreatedDate
,CurrencyIsoCode
,LastModifiedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000')  LastModifiedDate
,LLC_BI__lookupKey__c
,OwnerId
,Name
,LLC_BI__Spread_Projections_Template__c
,LLC_BI__Spread_Statement_Record__c
,LLC_BI__Spread_Statement_Record_Value__c
,LLC_BI__Type__c
,LLC_BI__Value__c
FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_spread_projections_driver_curated
