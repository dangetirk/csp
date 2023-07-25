with relation_columns as (

        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'PRIMARY_SOURCE_OF_REPAYMENT__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data