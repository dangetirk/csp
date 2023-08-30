    SELECT
    Id
    ,OwnerId
    ,Name
    ,CurrencyIsoCode
    ,CreatedDate
    ,CreatedById
    ,LastModifiedDate
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
    FROM CCS_ORG_Approval__c
    where CreatedDate >=2023-08-29T00:00:00.000Z