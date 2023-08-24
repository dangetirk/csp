SELECT
Id
,Name
,CurrencyIsoCode
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
,CreatedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
,LastModifiedById
,LLC_BI__Account__c
,LLC_BI__Collateral__c
,LLC_BI__End_Date__c
,LLC_BI__Ownership_Percentage__c
,LLC_BI__Pledging_Authority__c
,LLC_BI__Relationship_Type__c
,LLC_BI__Start_Date__c
,LLC_BI__Primary_Owner__c
,LLC_BI__Collateral_Association__c
,LLC_BI__Group_Association__c
,CCS_Perfection_Status__c
,CCS_Security_Hyperlink__c
,CCS_Total_Current_Hard_Limits__c
,CCS_Total_Lending_Value__c
,CCS_Certificate_Type__c
,CCS_No_Of_Concurring_Partners__c
,CCS_No_Of_Non_Property_Owning_Partners__c
,CCS_Partnership_Asset__c
,CCS_Partnership_Type__c
,CCS_Principal__c
FROM  dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_account_collateral_curated
