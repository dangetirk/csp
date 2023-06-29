select 
Id
,LLC_BI__Category__c
,Name
,CreatedById
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
,CurrencyIsoCode
,LastModifiedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
,LLC_BI__lookupKey__c
,OwnerId
from dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_classification_curated