select 
 Id
,Name
,Type
,RecordTypeId
,ParentId
,BillingStreet
,BillingCity
,BillingState
,BillingPostalCode
,BillingCountry
,ShippingStreet
,ShippingCity
,ShippingState
,ShippingPostalCode
,ShippingCountry
,AccountNumber
,Ownership
,CurrencyIsoCode
,OwnerId
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate
,CreatedById
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate
,LastModifiedById
,LLC_BI__Status__c
,LLC_BI__lookupKey__c
,LLC_BI__Next_Review_Date__c
,Migration_ID__c
,LLC_BI__Is_Non_Customer__c
,LLC_BI__Third_Party__c
,CCS_Total_Current_Bank_Limits__c
,CCS_LendingValue__c
,CCS_Sort_Code__c
,CCS_Risk_Rating__c
,CCS_Account_Type_for_Duplicate_Rule__c
,CCS_TotalHardLBCMLimits__c
,CCS_TotalHardBankLimits__c
,CCS_TotalSoftBankLimits__c
,CCS_TotalSoftLBCMLimits__c
,CCS_TotalHardLBGLimits__c
,CCS_TotalSoftLBGLimits__c
,CCS_TotalCombinedExposure__c
,CCS_RFI_Flag__c
,CCS_Support_Indicator__c
,CCS_DateOfBirth__c
,CCS_Sub_type__c
,CCS_Company_Registration_Number__c
,CCS_Country_of_Incorporation__c
,CCS_Date_Commenced_Trading__c
,CCS_Date_of_Association__c
,CCS_CMDID__c
,CCS_Bank_Entity__c
,CCS_Segment__c
,CCS_BSU_RM_Name__c
,CCS_Credit_Officer__c
,CCS_KYC_Status__c
,CCS_Monthly_Batch_Decision__c
,CCS_DefaultFlag__c
,CCS_RelationshipTradingName__c
,CCS_First_Name__c
,CCS_NPLE_Type_1__c
,CCS_Country_of_Registration__c
,CCS_RM_Name__c
,CCS_Relationship_Record_Type_Name__c
,CCS_RM_FileNumber__c
,CCS_SIC_Code__c
,CCS_SIC_Code_1__c
,CCS_KYB_Status__c
,CCS_Set_up_Actions_by_Profile_for_LG__c
,CCS_SIC_Description__c
,CCS_OUCode__c
,CCS_Last_Name__c
,CCS_RM_Team__c
,CCS_Collections_Indicator__c
,CCS_Support_Needed__c
,CCS_Email__c
,CCS_ARI_Flag__c
,CCS_Available_Overdraft__c
,CCS_Customer_Status__c
,CCS_Final_Slotted_IRDC_Rating__c
,CCS_IRDC_Rating__c
,CCS_Is_part_of_ORG__c
,CCS_Monthly_Loan_Repayment_Limit__c
,CCS_OGSA__c
,CCS_IsCountryOfRiskLinkedWithCustomer__c
,CCS_Registered_Charity_Number__c
,CCS_Relationship_Name_Hyper__c
,CCS_Set_up_Create_OGSA_Profiles__c
,CCS_Total_Lending_Value__c
,CCS_Chat_with_RM__c
,CCS_Profile_check_for_rating_creation__c
,CCS_Average_BDCS_Rating__c
,CCS_BDCS_Default_Flag__c
,CCS_BDCS_Rating__c
,CCS_Basel_Default__c
,CCS_CogLeid__c
,CCS_Customer_Generated_To_last_12_months__c
,CCS_Date_of_Cure__c
,CCS_Date_of_Default__c
,CCS_Default_Comment__c
,CCS_Default_Grade__c
,CCS_Default_Status__c
,CCS_Domicile__c
,CCS_Expiry_Date__c
,CCS_Has_Date_of_Default_been_populated__c
,CCS_Is_Basel_default_true__c
,CCS_Is_Checked__c
,CCS_Is_ORG_Lead__c
,CCS_Legal_Jurisdiction__c
,CCS_Reason_for_Default__c
,CCS_Total_Gross_Value_Amount__c
,CCS_Total_Lending_Value_Amount__c
,Environmental_Social_Comments__c
,Source_of_Customer_Comments__c
,CCS_Average_BDCS_StringRating__c
,CCS_Default_Grade_Rating_Value__c
,CCS_IRDC_Default_Flag__c
,CCS_Policy_Considerations_Comments__c
,CCS_Reason_Codes__c
,CCS_ALIE_Commentary__c
,CCS_Adherence_to_CCD_ILG__c
,CCS_Assessed_financial_impacts_changes__c
,CCS_Attestation__c
,CCS_BSU_Strategy_Phase__c
,CCS_Background_Last_Updated__c
,CCS_Background__c
,CCS_Balance_Sheet__c
,CCS_Borrower_Scope_of_Works_Last_Updated__c
,CCS_Borrower_Scope_of_Works__c
,CCS_Business_Overview__c
,CCS_Cashflow_Serviceability__c
,CCS_Comments__c
,CCS_Companies_Commentary_Last_Updated__c
,CCS_Companies_House_Commentary__c
,CCS_Costs_Amount_Last_Updated__c
,CCS_Costs_Amount__c
,CCS_Country_of_Trading__c
,CCS_Covid19_Loan_Application_Included__c
,CCS_Current_Rating_Model__c
,CCS_Current_Rating__c
,CCS_Customer_s_Vulnerability__c
,CCS_Date_to_BSU__c
,CCS_Decisioning_Codes_Comments__c
,CCS_Declined_Status_Check__c
,CCS_Details_Last_Updated__c
,CCS_DoyouwanttochangetheRatingmodel__c
,CCS_Drawdown_Repayment_Last_Updated__c
,CCS_Drawdown_Repayment__c
,CCS_Emerging_Risks__c
,CCS_Environmental_Comment_last_update__c
,CCS_Event_driven_OKYC_review_confirmed__c
,CCS_External_Professional_Support__c
,CCS_Follow_Regulation_CCA_RMC_Compliance__c
,CCS_Future_Strategy__c
,CCS_Goldmine_ID__c
,CCS_Has_Sanctioned_Rating__c
,CCS_Has_Submitted_Rating__c
,CCS_Headline_Strategy__c
,CCS_Hedging_Risks__c
,CCS_Interim_Review_Date__c
,CCS_Is_KAP_Address_outside_UK__c
,CCS_Key_Management_Background__c
,CCS_Key_Risks_Mitigations__c
,CCS_MonthCalculator__c
,CCS_Performance_Covenants_Commentary__c
,CCS_Product_options_discussion_date__c
,CCS_Profit_and_Loss__c
,CCS_Property_Development_SIC_Code__c
,CCS_Property_Investment_SIC_Code__c
,CCS_Proposed_Rating_Model__c
,CCS_Purpose_Amount_Last_Updated__c
,CCS_Purpose_Amount__c
,CCS_Purpose_Comments__c
,CCS_Rationale__c
,CCS_Repayment_Cashflow_Last_Updated__c
,CCS_Repayment_Cashflow__c
,CCS_Sector_Overview__c
,CCS_Security_Allocation__c
,CCS_Security_Commentary__c
,CCS_Security_Compliance_Last_Updated__c
,CCS_Security_Compliance__c
,CCS_Security_Issues_Last_Updated__c
,CCS_Security_Technical_Issues__c
,CCS_Succession_Considerations__c
,CCS_Support_evaluated_no_new_needs__c
,CCS_Support_needs_assess_recorde_update__c
,CCS_Turnover_Response__c
,CCS_WWID__c
,CCS_Working_Capital_Commentary__c
,CCS_withdrawn_checks__c
,CCS_Active_rating_model__c
,CCS_Country_of_Risk__c
,CCS_Rating_Type__c
,CCS_Is_OGSA_null__c
,CCS_New_To_Bank__c
FROM  dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_account_curated 
