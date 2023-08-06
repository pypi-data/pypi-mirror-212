from __future__ import annotations

import json

import click
import sqlalchemy
from sqlalchemy import ForeignKeyConstraint, MetaData
from sqlalchemy.schema import AddConstraint, CreateColumn, CreateIndex, CreateTable
from sqlalchemy.sql.schema import Column, Index


@click.command(no_args_is_help=True)
@click.version_option()
@click.option("--no-rename-indexes", help="Don't rename indexes")
@click.option("--no-rename-constraints", help="Don't rename constraints")
@click.option("--no-ignore-deferrable-constraints", help="Include deferrable constraint information")
@click.option("--no-ignore-identity-columns", help="Don't ignore identity column information")
@click.option("--output-format", type=click.Choice(["sql", "json"]), default="sql")
@click.argument("dsn_list", metavar="[dsn]...", nargs=-1)
def cli(
    no_rename_indexes,
    no_rename_constraints,
    no_ignore_deferrable_constraints,
    no_ignore_identity_columns,
    output_format,
    dsn_list,
):
    tables = []
    for dsn in dsn_list:
        engine = sqlalchemy.create_engine(dsn)
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=engine)
        tables.extend((engine, table) for table in metadata_obj.tables.values())

    sorted_tables = sorted(tables, key=lambda t: t[1].name)

    no_rename_constraints = output_format == "json" or no_rename_constraints
    no_rename_indexes = output_format == "json" or no_rename_indexes

    for engine, table in sorted_tables:
        for column in table.columns:
            if column.primary_key and not no_ignore_identity_columns:
                column.identity = None
                column.type = sqlalchemy.BigInteger()

        # Rename all constraints
        constraints = []
        for constraint in table.constraints:
            if not no_rename_constraints:
                constraint.name = "c"
            if not no_ignore_deferrable_constraints and isinstance(constraint, ForeignKeyConstraint):
                constraint.deferrable = None
                constraint.initially = None

            if output_format == "json":
                constraints.append(
                    {
                        "name": constraint.name,
                        "type": constraint.__class__.__name__,
                        "sql": str(AddConstraint(constraint).compile(engine)),
                        "columns": constraint.columns.keys(),
                        "expression": str(constraint.sqltext.compile(engine))
                        if hasattr(constraint, "sqltext")
                        else None,
                    }
                )
            else:
                constraints.append(str(AddConstraint(constraint).compile(engine)))

        indexes = []
        for index in table.indexes:
            if not no_rename_indexes:
                index.name = "i"
            index: Index

            if output_format == "json":
                indexes.append(
                    {
                        "name": index.name,
                        "type": index.__class__.__name__,
                        "sql": str(CreateIndex(index).compile(engine)),
                        "columns": index.columns.keys(),
                        "expressions": [
                            str(expression.compile(engine))
                            for expression in index.expressions
                            if not isinstance(expression, Column)
                        ],
                    }
                )
            else:
                indexes.append(str(CreateIndex(index).compile(engine)))

        if output_format == "json":
            output = {
                "name": table.name,
                "database": engine.url.database,
                "columns": {
                    column.name: {
                        "type": str(column.type.compile(engine.dialect)),
                        "sql": str(CreateColumn(column).compile(engine)),
                        "nullable": column.nullable,
                    }
                    for column in table.columns
                },
                "indexes": indexes,
                "constraints": constraints,
            }
            print(json.dumps(output))
        else:
            # sql
            create_table_ddl = CreateTable(table)
            create_table_ddl.columns = sorted(create_table_ddl.columns, key=lambda c: c.element.name)
            print((str(create_table_ddl.compile(engine)).strip() + ";\n"))
            print("\n".join(f"{constraint};" for constraint in sorted(constraints)))
            print("\n".join(f"{index};" for index in sorted(indexes)))
            print()


if __name__ == "__main__":
    cli()
