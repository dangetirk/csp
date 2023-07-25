with relation_columns as (

        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CCS_SPECIFIC_1_PERIOD_END__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data