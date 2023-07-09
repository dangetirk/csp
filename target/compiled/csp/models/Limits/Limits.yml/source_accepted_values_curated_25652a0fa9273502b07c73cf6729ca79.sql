
    
    

with all_values as (

    select
        CurrencyIsoCode as value_field,
        count(*) as n_records

    from `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_curation`.`rskcsp_ds_cardholder_curated`
    group by CurrencyIsoCode

)

select *
from all_values
where value_field not in (
    'G2BP'
)


