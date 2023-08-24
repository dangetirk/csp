SELECT		
Id		
,OwnerId		
,Name		
,CurrencyIsoCode		
,RecordTypeId		
,CONCAT(REPLACE(CAST(CreatedDate AS STRING ),' ','T'),'.000+0000') AS CreatedDate	
,CreatedById		
,CONCAT(REPLACE(CAST(LastModifiedDate AS STRING ),' ','T'),'.000+0000') AS LastModifiedDate	
,LastModifiedById		
,LLC_BI__Agricultural_Use__c		
,LLC_BI__Appraisal_Date__c		
,LLC_BI__Assessment_Method__c		
,LLC_BI__Book_Entry__c		
,LLC_BI__City__c		
,LLC_BI__Collateral_Insurance_Company__c		
,LLC_BI__Collateral_Insurance_Policy_Number__c		
,LLC_BI__Collateral_Type__c		
,LLC_BI__Combined_Percent_Pledged__c		
,LLC_BI__Commercial_Use__c		
,LLC_BI__Description__c		
,LLC_BI__Dwelling__c		
,LLC_BI__Insurance_Type__c		
,LLC_BI__Leasehold__c		
,LLC_BI__Number_of_Shares__c		
,LLC_BI__Owner_Occupied__c		
,LLC_BI__Principal_Dwelling__c		
,LLC_BI__Purchase_Money__c		
,LLC_BI__Refinance__c		
,LLC_BI__Remaining_Lendable_Value__c		
,LLC_BI__Residential_Property__c		
,LLC_BI__State__c		
,LLC_BI__UCC_Financing_Statement__c		
,LLC_BI__Year_Built__c		
,LLC_BI__Zip_Code__c		
,LLC_BI__Total_Lien_Amount__c		
,LLC_BI__Total_Pledge_Amount__c		
,Migration_ID__c		
,LLC_BI__Maturity_Date__c		
,LLC_BI__Rental_Income__c		
,cm_Abundance_of_Caution__c		
,cm_Condo_Project_Name_if_master_policy__c		
,cm_In_Flood_Zone__c		
,cm_Insurance_Coverage_Amount__c		
,cm_Insurance_Effective_Date__c		
,cm_Insurance_Reviewed__c		
,CCS_IsThisFacilityLBCM__c		
,CCS_Type__c		
,CCS_Subtype1__c		
,CCS_Account_Number__c		
,CCS_Account_Title__c		
,CCS_Acreage__c		
,CCS_All_Monies__c		
,CCS_Amount_Limited_To__c		
,CCS_Are_there_any_existing_Debentures__c		
,CCS_Asset_Insured__c		
,CCS_Bank_Entity__c		
,CCS_Basis_of_Valuation__c		
,CCS_Commercial_Property_Type__c		
,CCS_Date_of_Charge__c		
,CCS_Date_of_Debenture__c		
,CCS_Date_of_Deed_of_Priority__c		
,CCS_Date_of_Factoring_Agreement__c		
,CCS_Date_of_Guarantee__c		
,CCS_Date_of_Property_Occupancy__c		
,CCS_Date_of_Registration__c		
,CCS_Date_of_Registration_at_Companies__c		
,CCS_Deed_of_Priority_Details__c		
,CCS_Description_of_Stock_Portfolio__c		
,CCS_Document_Storage_Location__c		
,CCS_EPC_Assessment_Date__c		
,CCS_EPC_Expiry_Date__c		
,CCS_EPC_Rating__c		
,CCS_EPC_Reference_Number__c		
,CCS_Factoring_Agreement_Details__c		
,CCS_Factoring_Agreement__c		
,CCS_Form_Used__c		
,CCS_HMLR_Title_Number__c		
,CCS_HMO_Housing_Model__c		
,CCS_Hull_Insurance_Amount__c		
,CCS_Independent_Legal_Advice_Taken__c		
,CCS_Insurance_Type__c		
,CCS_Insurance_Value__c		
,CCS_Is_this_Debenture_to_remain__c		
,CCS_Jurisdiction__c		
,CCS_LBCM_Ranking__c		
,CCS_LBCM_Shared__c		
,CCS_Lease_End_Date__c		
,CCS_Limitation__c		
,CCS_Machinery_Insurance_Amount__c		
,CCS_Maturity_Expiry_Date__c		
,CCS_Minimum_Death_Benefit__c		
,CCS_Name_of_Boat__c		
,CCS_Name_of_Stock_Portfolio__c		
,CCS_Occupancy__c		
,CCS_Perfected_Alert_Comments__c		
,CCS_Perfection_Status__c		
,CCS_Ranking_of_Charge__c		
,CCS_Reference_Number__c		
,CCS_Renewal_Date__c		
,CCS_Residential_Property_Type__c		
,CCS_Safe_to_Lend_Alert_Comments__c		
,CCS_Single_Farm_Payments__c		
,CCS_Sort_Code__c		
,CCS_Square_Footage__c		
,CCS_Stocks_and_Shares_Type__c		
,CCS_Sum_Assured__c		
,CCS_Supporting_Security_Held__c		
,CCS_Type_of_Ship__c		
,CCS_Value_As_At__c		
,CCS_Deed_of_Priority__c		
,CCS_Life_Policy_Type__c		
,CCS_Other_Life_Policy_Details__c		
,CCS_Professional_Valuation__c		
,CCS_Unexpired_Lease_Term_Years__c		
,CCS_Application__c		
,CCS_Other_Security_Description__c		
,CCS_Surrender_Value__c		
,CCS_Gross_Value_Amount__c		
,CCS_LendingValue_Percentage__c		
,CCS_Lending_Value__c		
,CCS_Security_Name_Hyper__c		
,CCS_Set_up_Add_Remove_OGSA_Profiles__c		
,CCS_IsFirstChargeDuplicate__c		
,CCS_IsThirdChargeDuplicate__c		
,CCS_SecondChargeDuplicate__c		
,CCS_Security_Case__c		
,CCS_Valuation_Report_Uploaded__c		
,CCS_Status1__c		
,CCS_Outstanding_Amount_Latest__c		
,CCS_Google_Address__Street__s		
,CCS_Google_Address__City__s		
,CCS_Google_Address__PostalCode__s		
,CCS_Google_Address__StateCode__s		
,CCS_Google_Address__CountryCode__s		
,CCS_Google_Address__c		
,CCS_Gross_Value_Amount_SecVal__c		
,CCS_Ready_for_Dentons_Instruction__c		
,CCS_Security_Workflow_Model__c		
,CCS_Case_Check_All_required_Document__c		
,CCS_CheckSignaturesSolicitorNotWitness__c		
,CCS_Account_Number_Funds_Credited_To__c		
,CCS_OGSA_Gross_Value_Amount__c		
,CCS_OGSA_Lending_Value_Amount__c		
,CCS_Multi_Charge_Form_Asset__c		
,CCS_Facility_SAA__c		
,CCS_Sort_Code_Funds_Credited_To__c		
,CCS_Bypass_Validation_Rule_Check__c		
,CCS_Check_and_upload_Final_IPRS_SAM_toDM__c		
,CCS_CompaniesHouseRegistrationComplete__c		
,CCS_Companies_House_Regd_Cert_Held__c		
,CCS_CompleteCompaniesHouseSearchforDeben__c		
,CCS_Complete_Document_Redaction__c		
,CCS_Consent_to_Lease_Required_Land_o_ROT__c		
,CCS_Indemnity_Policies_Required__c		
,CCS_Packet_Sent_To_Iron_Mountain__c		
,CCS_Registered_Land_Registry_Correct__c		
,CCS_ReviewReturnedDocumentsCorrespondenc__c		
,CCS_Send_SIO_to_Solicitors_Land_only__c		
,CCS_Update_Security_Status__c		
,CCS_Update_Security_fields_in_PP_check__c		
,CCS_Update_Security_fields_in_nCino__c		
,CCS_Update_nCino_status_to_Perfected__c		
,CCS_UpdatenCinoWithPacketNumber__c		
,CCS_Upload_completed_documents_to_nCino__c		
,CCS_Security_Order__c		
,CCS_BranchAddressInclPostcode__Street__s		
,CCS_BranchAddressInclPostcode__City__s		
,CCS_BranchAddressInclPostcode__PostalCode__s		
,CCS_BranchAddressInclPostcode__StateCode__s		
,CCS_BranchAddressInclPostcode__CountryCode__s		
,CCS_BranchAddressInclPostcode__c		
,CCS_InsurerAddressInclPostcode__Street__s		
,CCS_InsurerAddressInclPostcode__City__s		
,CCS_InsurerAddressInclPostcode__PostalCode__s		
,CCS_InsurerAddressInclPostcode__StateCode__s		
,CCS_InsurerAddressInclPostcode__CountryCode__s		
,CCS_InsurerAddressInclPostcode__c		
,CCS_Collateral_Valuation_Estimated__c		
,CCS_Are_Adult_Occupiers_Living_in_the_Pr__c		
,CCS_Are_all_Partners_Titleholders__c		
,CCS_Confirm_Commercial_Consideration_Ben__c		
,CCS_Do_We_Require_Collateral_Warranties__c		
,CCS_Does_CCA_Apply__c		
,CCS_Does_Etridge_Apply__c		
,CCS_Financial_Assistance_Required__c		
,CCS_Is_Provider_a_Charity_IPC__c		
,CCS_Is_The_Charge_Indirect__c		
,CCS_Is_This_An_Uplift__c		
,CCS_Is_This_For_Property_Development__c		
,CCS_Is_the_Security_Provider_a_Pension__c		
,CCS_Is_this_Policy_held_in_Trust__c		
,CCS_Is_this_a_Partnership_Asset__c		
,CCS_Is_this_a_Professional_Partnership__c		
,CCS_Is_this_a_Purchase__c		
,CCS_Life_Policy_Holder__c		
,CCS_Only_One_Company_Official_Registered__c		
,CCS_Purchase_Price_2__c		
,CCS_Security_is_not_MCOB_Regulated__c		
,CCS_Term_Date_2__c		
,CCS_Which_Entity_is_the_Lead_or_Parent__c		
,CCS_Flag_to_disable_action_on_security__c		
,CCS_Account_Type__c		
,CCS_If_Other_Detail__c		
FROM 	dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_collateral_curated