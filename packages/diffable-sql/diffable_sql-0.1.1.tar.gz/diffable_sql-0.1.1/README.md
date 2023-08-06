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
  --help                          Show this message and exit.
```
