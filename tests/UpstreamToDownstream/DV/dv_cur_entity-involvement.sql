select 1 from (
SELECT
id
,createddate
,createdbyid
,lastmodifieddate
,lastmodifiedbyid
,llc_bi__account__c
,llc_bi__borrower_type__c
,llc_bi__contingent_type__c
,llc_bi__contingent_amount__c
,recordtypeid
,llc_bi__loan__c
,llc_bi__product_package__c
,name
,currencyisocode
FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_legal_entities_curated
except distinct
SELECT
	Id	id
,	Created_Date	createddate
,	Created_By	createdbyid
,	Last_Modified_Date	lastmodifieddate
,	Last_Modified_By	lastmodifiedbyid
,	Relationship_Name	llc_bi__account__c
,	Borrower_Type	llc_bi__borrower_type__c
,	Contingent_Type	llc_bi__contingent_type__c
,	Contingent_Amount	llc_bi__contingent_amount__c
,	Record_Type	recordtypeid
,	Facility	llc_bi__loan__c
,	Product_Package	llc_bi__product_package__c
,	Entity_Auto_Number	name
,	Currency	currencyisocode

FROM  `dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_curated.cur_entity-involvement`
where id in (select id from  dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_legal_entities_curated))
union all

select 1 from (

SELECT
	Id	id
,	Created_Date	createddate
,	Created_By	createdbyid
,	Last_Modified_Date	lastmodifieddate
,	Last_Modified_By	lastmodifiedbyid
,	Relationship_Name	llc_bi__account__c
,	Borrower_Type	llc_bi__borrower_type__c
,	Contingent_Type	llc_bi__contingent_type__c
,	Contingent_Amount	llc_bi__contingent_amount__c
,	Record_Type	recordtypeid
,	Facility	llc_bi__loan__c
,	Product_Package	llc_bi__product_package__c
,	Entity_Auto_Number	name
,	Currency	currencyisocode

FROM  `dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_curated.cur_entity-involvement`
where id in (select id from  dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_legal_entities_curated)
except distinct
SELECT
id
,createddate
,createdbyid
,lastmodifieddate
,lastmodifiedbyid
,llc_bi__account__c
,llc_bi__borrower_type__c
,llc_bi__contingent_type__c
,llc_bi__contingent_amount__c
,recordtypeid
,llc_bi__loan__c
,llc_bi__product_package__c
,name
,currencyisocode
FROM dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_ds_curation.rskcsp_ds_legal_entities_curated


)

