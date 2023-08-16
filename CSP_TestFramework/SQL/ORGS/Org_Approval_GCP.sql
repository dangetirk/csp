    SELECT
    Id
    ,OwnerId
    ,Name
    ,CurrencyIsoCode
    ,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
    ,CreatedById
    ,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
    ,LastModifiedById
    ,CCS_Approval_for__c
    ,CCS_Comments__c
    ,CCS_Connection__c
    ,CCS_Lending_Group__c
    ,CCS_ORG_Lead__c
    ,CCS_ORG_Members__c
    ,CCS_ORG_Status__c
    ,CCS_Request_Reviewer__c
    ,CCS_Review_Date__c
    ,CCS_Reviewer_Comments__c
    FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_org_approval_curated
