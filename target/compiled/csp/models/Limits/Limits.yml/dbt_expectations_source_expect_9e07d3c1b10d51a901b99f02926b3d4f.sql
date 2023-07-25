with relation_columns as (

        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CCS_SET_UP_A_DIRECT_DEBIT_TO_MANAGE__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data