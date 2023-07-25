with relation_columns as (

        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CCS_HOW_MUCH_TO_PAY_OFF_EACH_MONTH__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data