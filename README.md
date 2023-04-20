Welcome to your new dbt project!

### Using the starter project

Try running the following commands:

- dbt run
- dbt test

Connection Test:

dbt debug --profiles-dir ./profiles --profile csp

To test the Sources:

1. To execute all the tests defined in the project

    dbt test --profiles-dir ./profiles --profile csp

2. To execute the tests for particular sources

    dbt test -s source:Product_curated.Product_curated  --profiles-dir ./profiles --profile csp

3. To execute the own sigular test (refer the test folder )

    dbt test --profiles-dir ./profiles --profile csp  --select sampletest

### Resources:

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
