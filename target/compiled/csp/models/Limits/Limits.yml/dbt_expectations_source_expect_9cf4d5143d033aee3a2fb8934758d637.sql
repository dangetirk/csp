with relation_columns as (

        
        select
            cast('ID' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('OWNERID' as STRING) as relation_column,
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
            cast('LLC_BI__ACTIVE__C' as STRING) as relation_column,
            cast('BOOLEAN' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__CODE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__DESCRIPTION__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__END_DATE__C' as STRING) as relation_column,
            cast('DATE' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__SEVERITIES__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__START_DATE__C' as STRING) as relation_column,
            cast('DATE' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__TYPE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__LOOKUPKEY__C' as STRING) as relation_column,
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
            relation_column = 'LLC_BI__CODE__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data