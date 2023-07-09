select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      select 1 from dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_downstream_raw.rskcsp_ds_account_copy
where length(AccountNumber)<=0
      
    ) dbt_internal_test