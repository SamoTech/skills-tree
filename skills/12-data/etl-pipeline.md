# ETL Pipeline

**Category:** `data`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Build Extract-Transform-Load pipelines to move and reshape data between sources and destinations.

### Example

```python
# Airflow DAG skeleton
with DAG('etl_pipeline', schedule_interval='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_fn)
    transform = PythonOperator(task_id='transform', python_callable=transform_fn)
    load = PythonOperator(task_id='load', python_callable=load_fn)
    extract >> transform >> load
```

### Frameworks

- Apache Airflow, Prefect, Dagster
- dbt (transform layer)
- Fivetran, Airbyte (managed ETL)

### Related Skills

- [Data Cleaning](data-cleaning.md)
- [Data Joining](data-joining.md)
- [SQL Query Execution](sql-execution.md)
