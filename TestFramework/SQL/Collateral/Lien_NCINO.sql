
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
,LLC_BI__Amount__c
,LLC_BI__Expire_Date__c
,LLC_BI__Institution__c
,LLC_BI__Is_Excluded__c
,LLC_BI__Is_Internal__c
,LLC_BI__Loan_Number__c
,LLC_BI__Loan__c
,LLC_BI__Position__c
,LLC_BI__Is_Created_From_Collateral__c
,CCS_Date_of_Charge__c
,CCS_Lender__c
,CCS_Account_Number__c
,CCS_Action_Required__c
,CCS_Email_Address__c
,CCS_Outstanding_Balance__c
,CCS_AddressInclPostcode__Street__s
,CCS_AddressInclPostcode__City__s
,CCS_AddressInclPostcode__PostalCode__s
,CCS_AddressInclPostcode__StateCode__s
,CCS_AddressInclPostcode__CountryCode__s
,CCS_AddressInclPostcode__c
FROM  LLC_BI__Lien__c
where CreatedDate >=2023-08-24T10:04:00.000Z