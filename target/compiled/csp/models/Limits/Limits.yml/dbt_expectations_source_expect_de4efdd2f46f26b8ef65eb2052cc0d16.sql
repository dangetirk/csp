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
            cast('CCS_FACILITY__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_AMOUNT__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_EXPIRY_DATE__C' as STRING) as relation_column,
            cast('DATE' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_IS_THIS_A_TEMPORARY_AMENDMENT__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_START_DATE__C' as STRING) as relation_column,
            cast('DATE' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_CURRENT_LIMIT__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_PROPOSED_LIMIT__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_TENOR__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_UTILISATION__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
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
            relation_column = 'CURRENCYISOCODE'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data