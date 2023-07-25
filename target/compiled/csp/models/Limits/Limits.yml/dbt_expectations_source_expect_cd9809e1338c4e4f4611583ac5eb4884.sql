with relation_columns as (

        
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