# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

from IPython.core.getipython import get_ipython
import iql

import logging
import argparse
from typing import Optional
from jinja2 import Template


from traitlets.config.configurable import Configurable
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.core.magic import (
    Magics,
    cell_magic,
    line_magic,
    magics_class,
    no_var_expand,
    needs_local_scope,
)

from duckdb import DuckDBPyConnection

logger = logging.getLogger(__name__)

connection: Optional[DuckDBPyConnection] = None


def _get_obj_from_name(name: str) -> Optional[object]:
    ip = get_ipython()
    return ip.ev(name) if ip is not None else None


def execute_iql(
    query_string: str,
    connection: Optional[DuckDBPyConnection],
    export_function: Optional[str] = None,
):
    return iql.execute(query_string, connection)


@magics_class
class IqlMagic(Magics, Configurable):
    # database connection object
    # created via -d (default), -cn (connection string) or -co (connection object)

    # selected via -t. None = Pandas.
    export_function = None

    def __init__(self, shell):
        Configurable.__init__(self, config=shell.config)
        Magics.__init__(self, shell=shell)

        # Add ourself to the list of module configurable via %config
        self.shell.configurables.append(self)  # type: ignore

    def connect_by_objectname(self, connection_object):
        con: DuckDBPyConnection = _get_obj_from_name(connection_object)  # type: ignore
        if not isinstance(con, DuckDBPyConnection):
            raise ValueError(f"{connection_object} is not a DuckDBPyConnection")
        if con is None:
            raise ValueError(f"Couldn't find {connection_object}")
        else:
            logger.info(f"Using existing connection: {connection_object}")

        global connection
        connection = con

    @no_var_expand
    @needs_local_scope
    @line_magic("iql")
    @cell_magic("iql")
    @line_magic("bql")
    @cell_magic("bql")
    @magic_arguments()
    @argument(
        "-co",
        "--connection_object",
        help="Connect to a database using the connection object",
        nargs=1,
        type=str,
        action="store",
    )
    @argument(
        "-o",
        "--output",
        help="Write the output to the specified variable",
        nargs=1,
        type=str,
        action="store",
    )
    @argument(
        "-q",
        "--quiet",
        help="Don't return an object, similar to %%capture",
        nargs=1,
        type=str,
        action="store",
    )
    @argument("-j", "--jinja2", help="Apply Jinja2 Template", action="store_true")
    @argument("rest", nargs=argparse.REMAINDER)
    def execute(self, line: str = "", cell: str = "", local_ns=None):
        global connection

        args = parse_argstring(self.execute, line)
        # Grab rest of line
        rest = " ".join(args.rest)
        query = f"{rest}\n{cell}".strip()

        logger.debug(f"Query = {query}, {len(query)}")

        if args.jinja2:  # Replace any {var}'s with the string values
            query = Template(query).render(get_ipython().user_ns)  # type: ignore

        if args.connection_object:
            self.connect_by_objectname(args.connection_object[0])

        if query is None or len(query) == 0:
            logger.debug("Nothing to execute")
            return

        try:
            o = execute_iql(
                query_string=query,
                connection=connection,
                export_function=self.export_function,
            )
        except Exception as e:
            raise ValueError(f"Error executing {query} in DuckDB") from e

        if args.output:
            self.shell.user_ns[args.output[0]] = o  # type: ignore

        if args.quiet:
            return None
        else:
            return o


def apply_template(sql: str, user_ns) -> str:
    t = Template(sql)
    return t.render(user_ns)


def load_ipython_extension(ip):
    ip = get_ipython()

    ip.register_magics(IqlMagic)  # type: ignore
