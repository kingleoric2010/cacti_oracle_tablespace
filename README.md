cacti_oracle_tablespace
=======================

A template to monitor oracle database  tablespace in cacti

Install
-------

Put the `get_oracle_tablespace.py` to your `<cacti_path>/scrpits`

and the `oracle_tablespace.xml` to your `<cacti_path>/resources/oracle_tablespace`

the `cacti_graph_template_oracle_tablespace.xml` should be imported into cacti

edit the `oracle_tablespace.xml`

replace the string between &lt;arg_prepend&gt; and &lt;/arg_prepend&gt; at line 4 like this

```xml
<arg_prepend>username password |host_hostname| port(default 1521) oracle_sid</arg_prepend>
```

then you can enjoy it.
