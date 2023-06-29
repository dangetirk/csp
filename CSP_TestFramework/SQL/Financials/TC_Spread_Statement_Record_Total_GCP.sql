SELECT
Id
,CreatedById
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
,CurrencyIsoCode
,LLC_BI__Debit__c
,LLC_BI__Global_Analysis_Type__c
,LLC_BI__Color__c
,LLC_BI__Group_Type__c
,LLC_BI__Hide_All_Records__c
,LLC_BI__Hide_Column_Totals__c
,LLC_BI__KPI_Type__c
,LLC_BI__Include_In_Total__c
,LLC_BI__Is_Balance_Check__c
,LLC_BI__Is_Summary_Group__c
,LastModifiedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
,LLC_BI__lookupKey__c
,LLC_BI__Publish_On_Init_Event__c
,LLC_BI__Publish_On_Update_Event__c
,LLC_BI__Row_Number__c
,LLC_BI__Show_Math__c
,LLC_BI__Source_Group__c
,Name
,LLC_BI__Spread_Statement_Type__c
,LLC_BI__Title__c
,LLC_BI__Total_Type__c
FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_spread_statement_record_total_curated 