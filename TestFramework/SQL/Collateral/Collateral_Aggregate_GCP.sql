select 
 Id
,OwnerId
,Name
,CurrencyIsoCode
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
,CreatedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
,LastModifiedById
,LLC_BI__lookupKey__c
,LLC_BI__Current_Total_Lendable_Value__c
,LLC_BI__Total_Collateral_Pledged__c
,LLC_BI__Total_Collateral_Value__c
,LLC_BI__Total_Current_Lien_Amount__c
,LLC_BI__Total_Superior_Lien_Amount__c
,LLC_BI__Collateral_Pledged_Count__c
FROM  dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_loan_collateral_aggregate_curated 
