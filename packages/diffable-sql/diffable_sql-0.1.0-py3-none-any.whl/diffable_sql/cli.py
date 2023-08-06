from __future__ import annotations

import click
import sqlalchemy
from sqlalchemy import ForeignKeyConstraint, MetaData
from sqlalchemy.schema import AddConstraint, CreateIndex, CreateTable


@click.command()
@click.option("--no-rename-indexes", help="Don't rename indexes")
@click.option("--no-rename-constraints", help="Don't rename constraints")
@click.option("--no-ignore-deferrable-constraints", help="Include deferrable constraint information")
@click.option("--no-ignore-identity-columns", help="Don't ignore identity column information")
@click.argument("dsn_list", metavar="[dsn]...", nargs=-1)
def cli(
    no_rename_indexes,
    no_rename_constraints,
    no_ignore_deferrable_constraints,
    no_ignore_identity_columns,
    dsn_list,
):
    tables = []
    for dsn in dsn_list:
        engine = sqlalchemy.create_engine(dsn)
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=engine)
        tables.extend((engine, table) for table in metadata_obj.tables.values())

    sorted_tables = sorted(tables, key=lambda t: t[1].name)

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
            constraints.append(str(AddConstraint(constraint).compile(engine)))

        indexes = []
        for index in table.indexes:
            if not no_rename_indexes:
                index.name = "i"
            indexes.append(str(CreateIndex(index).compile(engine)))

        create_table_ddl = CreateTable(table)
        create_table_ddl.columns = sorted(create_table_ddl.columns, key=lambda c: c.element.name)
        print((str(create_table_ddl.compile(engine)).strip() + ";\n"))
        print("\n".join(f"{constraint};" for constraint in sorted(constraints)))
        print("\n".join(f"{index};" for index in sorted(indexes)))
        print()


if __name__ == "__main__":
    cli()
