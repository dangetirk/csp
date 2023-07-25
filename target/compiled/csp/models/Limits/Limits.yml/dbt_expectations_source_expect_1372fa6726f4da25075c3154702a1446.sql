with relation_columns as (

        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CCS_OVERDRAFT_REQUEST_TYPE__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data