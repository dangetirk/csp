SELECT
Id
,Name
,CurrencyIsoCode
,CreatedDate
,CreatedById
,LastModifiedDate
,LastModifiedById
,LLC_BI__Collateral__c
,LLC_BI__Active__c
,LLC_BI__Collateral_Type_SubType__c
,LLC_BI__Comments__c
,LLC_BI__Primary__c
,LLC_BI__Source__c
,LLC_BI__Type__c
,LLC_BI__Value__c
,LLC_BI__Valuation_Details__c
,LLC_BI__Valuation_Description__c
,LLC_BI__Original_Value__c
,LLC_BI__Raw_Valuation_Details__c
,CCS_Date_of_Valuation__c
,CCS_Existing_Use_Valuation_EUV_SH__c
,CCS_MVSTT__c
,CCS_Market_Rent_Value_OMRV__c
,CCS_Market_Value__c
,CCS_Open_Market_Value_Closed_MV2__c
,CCS_Goodwill_Applicable__c
,CCS_Other_Valuation_Comments__c
,CCS_Other_Valuation__c
,CCS_Reinstatement_Value__c
,CCS_Vacant_Possession_Closed_Value_MV3__c
,CCS_Valuation_Method__c
,CCS_Valuer_Email__c
,CCS_Valuer_Name__c
,CCS_Gross_Development_Value_GDV__c
,CCS_Valuer_Telephone_Number__c
,CCS_Google_Valuer_Address__Street__s
,CCS_Google_Valuer_Address__City__s
,CCS_Google_Valuer_Address__PostalCode__s
,CCS_Google_Valuer_Address__StateCode__s
,CCS_Google_Valuer_Address__CountryCode__s
,CCS_Google_Valuer_Address__c
,CCS_Goodwill_Value__c
,CCS_Proposed_Goodwill_Value__c
,CCS_Proposed_valuation__c
FROM   LLC_BI__Collateral_Valuation__c
where CreatedDate >=2023-08-24T10:04:00.000Z
