# Diffable SQL

This is a small tool that outputs SQL from a number of databases in a sorted, diff-friendly order.

## Install

The tool supports any database [that SQLAlchemy supports](https://docs.sqlalchemy.org/en/20/dialects/index.html).
You must install the correct connector for your database:

```
$ pip install diffable-sql
$ pip install psycopg2-binary # postgres
$ pip install mysqlclient # mysql
```

## Usage

You can pass any number of DSNs as arguments, for example `postgresql:///db-name`. The tool will output normalised SQL
DDL statements for each DSN.

```shell
$ diffable-sql sqlite:///db.sqlite3
CREATE TABLE sometable (
	foo VARCHAR,
	id BIGINT NOT NULL
);

ALTER TABLE sometable ADD CONSTRAINT c PRIMARY KEY (id);
ALTER TABLE sometable ADD CONSTRAINT c UNIQUE (foo);
CREATE INDEX i ON sometable (foo);
```

Specifically:
- The tables and columns will be sorted by name
- Indexes and constraints will be renamed as `i` and `c`
- Deferrable constraint information will be hidden
- Identity columns will be hidden

These allow schemas to be more easily diffed.

## JSON output

Passing `--output-format=json` will output a json structure for each table, containing information on the column
types, SQL, nullability, indexes and constraints:

```shell
$ poetry run diffable-sql sqlite:///tools/db.sqlite3 --output-format=json | jq
```

Outputs:
```json
{
  "name": "sometable",
  "database": "tools/db.sqlite3",
  "columns": {
    "id": {
      "type": "BIGINT",
      "sql": "id BIGINT NOT NULL",
      "nullable": false
    },
    "foo": {
      "type": "VARCHAR",
      "sql": "foo VARCHAR",
      "nullable": true
    }
  },
  "indexes": [
    {
      "name": "foobar",
      "type": "Index",
      "sql": "CREATE INDEX foobar ON sometable (foo)",
      "columns": [
        "foo"
      ],
      "expressions": []
    }
  ],
  "constraints": [
    {
      "name": null,
      "type": "PrimaryKeyConstraint",
      "sql": "ALTER TABLE sometable ADD PRIMARY KEY (id)",
      "columns": [
        "id"
      ],
      "expression": null
    },
    {
      "name": null,
      "type": "UniqueConstraint",
      "sql": "ALTER TABLE sometable ADD UNIQUE (foo)",
      "columns": [
        "foo"
      ],
      "expression": null
    }
  ]
}
```

## Args

```console
$ diffable-sql --help
Usage: diffable-sql [OPTIONS] [dsn]...

Options:
  --no-rename-indexes TEXT        Don't rename indexes
  --no-rename-constraints TEXT    Don't rename constraints
  --no-ignore-deferrable-constraints TEXT
                                  Include deferrable constraint information
  --no-ignore-identity-columns TEXT
                                  Don't ignore identity column information
  --output-format [sql|json]
  --help                          Show this message and exit.

```
