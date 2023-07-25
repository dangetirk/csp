with relation_columns as (

        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CCS_SEND_QUOTE_TO_CLIENT_BEFORE_SANCTION__C'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data