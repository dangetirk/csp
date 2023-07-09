




    with grouped_expression as (
    select
        
        
    
  Id is not null as expression


    from `dmn01-rsksoi-bld-01-2017`.`dmn01_rsksoi_euwe2_rsk_csp_ds_staging`.`rskcsp_ds_cardholder_staging`
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors



