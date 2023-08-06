{% materialization incremental, adapter='upsolver' %}

  {%- set identifier = model['alias'] -%}
  {%- set model_config = model['config'] -%}
  {%- set incremental_strategy = adapter.get(model_config, 'incremental_strategy', False) -%}
  {%- set sync = adapter.get(model_config, 'sync', False) -%}
  {%- set options = adapter.get(model_config, 'options', {}) -%}
  {%- set source = adapter.get(model_config, 'source') -%}
  {%- set target_type = adapter.get(model_config, 'target_type', 'datalake').lower() -%}
  {%- set target_table_alias = adapter.get(model_config, 'target_table_alias', identifier) -%}
  {%- set delete_condition = adapter.get(model_config, 'delete_condition', False) -%}
  {%- set partition_by = adapter.get(model_config, 'partition_by', []) -%}
  {%- set primary_key = adapter.get(model_config, 'primary_key', []) -%}
  {%- set map_columns_by_name = adapter.get(model_config, 'map_columns_by_name', False) -%}
  {%- set job_identifier = identifier + '_job' %}

  {%- set old_relation = adapter.get_relation(identifier=job_identifier,
                                              schema=schema,
                                              database=database) -%}
  {%- set target_relation = api.Relation.create(identifier=job_identifier,
                                                schema=schema,
                                                database=database,
                                                type='incremental') -%}


  {{ run_hooks(pre_hooks, inside_transaction=False) }}
  {{ run_hooks(pre_hooks, inside_transaction=True) }}
  {{ log("model[config]: " ~ model['config'] ) }}


  {% if target_type  == 'datalake' %}
    {%- set target_connection = adapter.get(model_config, 'target_connection', database) -%}
    {%- set target_schema = adapter.get(model_config, 'target_schema', schema) -%}
    {%- set table_relation = api.Relation.create(identifier=target_table_alias,
                                                 schema=target_schema,
                                                 database=target_connection,
                                                 type='table') -%}
    {%- set into_relation = table_relation -%}
    {%- call statement('create_table_if_not_exists') -%}
      {{ get_create_table_if_not_exists_sql(table_relation, partition_by, primary_key, options) }}
    {%- endcall -%}
  {%- else -%}
    {%- set target_schema = adapter.require(model_config, 'target_schema') -%}
    {% set target_connection = adapter.require(model_config, 'target_connection') %}
    {%- set into_relation = target_connection + '.' + target_schema + '.' + target_table_alias -%}
  {%- endif %}

  {%- if old_relation -%}
    {%- call statement('main') -%}
      {{ get_alter_job_sql(job_identifier, options, incremental_strategy, source) }}
    {%- endcall %}
  {%- else -%}
    {%- call statement('main') -%}
      {%- if incremental_strategy == 'merge' -%}
        {{ get_create_merge_job_sql(job_identifier, into_relation, sync,
                                    options, primary_key, delete_condition,
                                    target_type) }}
      {%- elif incremental_strategy == 'insert' -%}
        {{ get_create_insert_job_sql(job_identifier,
                                    into_relation, sync, options,
                                    map_columns_by_name, target_type) }}

      {%- else  -%}
        {{ get_create_copy_job_sql(job_identifier, sql,
                                   into_relation, sync, options, source,
                                   target_type) }}

      {%- endif -%}
    {%- endcall -%}
  {%- endif -%}

  {%- do persist_docs(target_relation, model) -%}
  {%- do persist_docs(table_relation, model) -%}

  {{ run_hooks(post_hooks, inside_transaction=False) }}
  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {%- if target_type  == 'datalake' -%}
    {{ return({'relations': [target_relation, table_relation]}) }}
  {%- else  -%}
    {{ return({'relations': [target_relation]}) }}
  {%- endif -%}
{%- endmaterialization -%}
