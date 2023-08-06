Target_options = {
  "datalake": {
      "globally_unique_keys": {"type": "boolean", "editable": False, "optional": True},
      "storage_connection": {"type": "identifier", "editable": False, "optional": True},
      "storage_location": {"type": "text", "editable": False, "optional": True},
      "compute_cluster": {"type": "identifier", "editable": True, "optional": True},
      "compression": {"type": "value", "editable": True, "optional": True},
      "compaction_processes": {"type": "integer", "editable": True, "optional": True},
      "disable_compaction": {"type": "boolean", "editable": True, "optional": True},
      "retention_date_partition": {"type": "text", "editable": True, "optional": True},
      "table_data_retention": {"type": "text", "editable": True, "optional": True},
      "column_data_retention": {"type": "text", "editable": True, "optional": True},
      "comment": {"type": "text", "editable": True, "optional": True}
  },
  "materialized_view": {
      "storage_connection": {"type": "identifier", "editable": False, "optional": True},
      "storage_location": {"type": "text", "editable": False, "optional": True},
      "max_time_travel_duration": {"type": "integer", "editable": True, "optional": True},
      "compute_cluster": {"type": "identifier", "editable": True, "optional": True},
  },
  "snowflake": {
        "column_transformations": {"type": "dict", "editable": False, "optional": True},
        "deduplicate_with": {"type": "dict", "editable": False, "optional": True},
        "exclude_columns": {"type": "list", "editable": False, "optional": True},
        "create_table_if_missing": {"type": "boolean", "editable": False, "optional": True},
        "write_interval": {"type": "integer", "editable": False, "optional": True},
  }
}
