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
            cast('LLC_BI__CODE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__COLLATERAL_MGMT__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__COVENANT_MGMT__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__LOAN__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__MITIGATION_REASON_1__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__MITIGATION_REASON_2__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__MITIGATION_REASON_3__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__RELATIONSHIP__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__SEVERITY_VALUE__C' as STRING) as relation_column,
            cast('NUMERIC' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__SEVERITY__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__STATUS__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__TYPE__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('LLC_BI__AUTOMATICALLY_ADDED__C' as STRING) as relation_column,
            cast('BOOLEAN' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_LBG_ENTITY__C' as STRING) as relation_column,
            cast('STRING' as STRING) as relation_column_type
        union all
        
        select
            cast('CCS_LBG_ENTITY_FACILITY__C' as STRING) as relation_column,
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
            relation_column = 'CCS_LBG_ENTITY_FACILITY__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data