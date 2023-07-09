select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      with relation_columns as (

        
        select
            cast('ID' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('NAME' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CURRENCYISOCODE' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CREATEDDATE' as STRING) as relation_column,
            cast('DATETIME' as STRING) as relation_column_type
        union all
        
        select
            cast('CREATEDBYID' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LASTMODIFIEDDATE' as STRING) as relation_column,
            cast('DATETIME' as STRING) as relation_column_type
        union all
        
        select
            cast('LASTMODIFIEDBYID' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_FACILITY_ID__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_COUNTRY_CODE__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_DATE_OF_BIRTH__C' as STRING) as relation_column,
            cast('DATE' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_EMAIL__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_FIRST_NAME__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_IS_CARD_NEEDED__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_LAST_NAME__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_LEVEL_OF_CONTROL__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_LIMIT__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_MOBILE_NUMBER__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_NUMBER_OF_CARDS__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_TITLE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('_CHANGETYPE' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('_COMMITTIMESTAMP' as STRING) as relation_column,
            cast('INT64' as STRING) as relation_column_type
        union all
        
        select
            cast('LOAD_TIMESTAMP' as STRING) as relation_column,
            cast('DATETIME' as STRING) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CCS_MOBILE_NUMBER__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data
      
    ) dbt_internal_test