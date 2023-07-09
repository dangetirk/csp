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
            cast('RECORDTYPEID' as STRING) as relation_column,
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
            cast('LLC_BI__ACCOUNT__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__BORROWER_TYPE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__CONTINGENT_TYPE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__LOAN__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__OWNERSHIP__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__PRODUCT_PACKAGE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__CONTINGENT_AMOUNT__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('MIGRATION_ID__C' as STRING) as relation_column,
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
            relation_column = 'LLC_BI__PRODUCT_PACKAGE__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data