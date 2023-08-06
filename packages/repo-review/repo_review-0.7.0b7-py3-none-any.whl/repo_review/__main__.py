from __future__ import annotations

import itertools
import json
import sys
import typing
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

if typing.TYPE_CHECKING:
    import click
else:
    import rich_click as click

import rich.console
import rich.markdown
import rich.syntax
import rich.terminal_theme
import rich.text
import rich.traceback
import rich.tree

from ._compat.importlib.resources.abc import Traversable
from ._compat.typing import assert_never
from .families import Family
from .ghpath import GHPath
from .html import to_html
from .processor import Result, _collect_all, as_simple_dict, process

rich.traceback.install(suppress=[click, rich], show_locals=True, width=None)


def rich_printer(
    families: Mapping[str, Family],
    processed: list[Result],
    *,
    svg: bool = False,
    stderr: bool = False,
) -> None:
    console = rich.console.Console(
        record=svg, quiet=svg, stderr=stderr, color_system=None if stderr else "auto"
    )

    for family, results_list in itertools.groupby(processed, lambda r: r.family):
        family_name = families[family].get("name", family)
        tree = rich.tree.Tree(f"[bold]{family_name}[/bold]:")
        for result in results_list:
            color = (
                "yellow"
                if result.result is None
                else "green"
                if result.result
                else "red"
            )
            description = (
                f"[link={result.url}]{result.description}[/link]"
                if result.url
                else result.description
            )
            msg = rich.text.Text()
            msg.append(result.name, style="bold")
            msg.append(" ")
            msg.append(rich.text.Text.from_markup(description, style=color))
            if result.result is None:
                msg.append(" [skipped]", style="yellow bold")
                tree.add(msg)
            elif result.result:
                msg.append(rich.text.Text.from_markup(" :white_check_mark:"))
                tree.add(msg)
            else:
                msg.append(rich.text.Text.from_markup(" :x:"))
                detail = rich.markdown.Markdown(result.err_msg)
                msg_grp = rich.console.Group(msg, detail)
                tree.add(msg_grp)

        console.print(tree)
        console.print()

    if len(processed) == 0:
        console.print("[bold red]No checks ran")

    if svg:
        str = console.export_svg(theme=rich.terminal_theme.DEFAULT_TERMINAL_THEME)
        if stderr:
            print(str, file=sys.stderr)
        else:
            rich.print(rich.syntax.Syntax(str, lexer="xml"))


def display_output(
    families: Mapping[str, Family],
    processed: list[Result],
    *,
    format_opt: Literal["rich", "json", "html", "svg"],
    stderr: bool,
) -> None:
    match format_opt:
        case "rich" | "svg":
            rich_printer(families, processed, svg=format_opt == "svg", stderr=stderr)
        case "json":
            j = json.dumps(
                {"families": families, "checks": as_simple_dict(processed)}, indent=2
            )
            if stderr:
                print(j, file=sys.stderr)
            else:
                rich.print_json(j)
        case "html":
            html = to_html(families, processed)
            if stderr:
                print(html, file=sys.stderr)
            else:
                rich.print(rich.syntax.Syntax(html, lexer="html"))
        case _:
            assert_never(format_opt)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("package", type=click.Path(dir_okay=True, path_type=Path))
@click.option(
    "--format",
    "format_opt",
    type=click.Choice(["rich", "json", "html", "svg"]),
    default="rich",
    help="Select output format.",
)
@click.option(
    "--stderr",
    type=click.Choice(["rich", "json", "html", "svg"]),
    help="Select additional output format for stderr. Will not use terminal escape codes.",
)
@click.option(
    "--select",
    help="Only run certain checks, comma separated. All checks run if empty.",
    default="",
)
@click.option(
    "--ignore",
    help="Ignore a check or checks, comma separated.",
    default="",
)
@click.option(
    "--package-dir",
    "-p",
    help="Path to python package.",
    default="",
)
@click.option(
    "--list/--no-list",
    "list_opt",
    help="List all checks and exit",
    default=False,
)
def main(
    package: Traversable,
    format_opt: Literal["rich", "json", "html"],
    stderr: Literal["rich", "json", "html"] | None,
    select: str,
    ignore: str,
    package_dir: str,
    list_opt: bool,
) -> None:
    """
    Pass in a local Path or gh:org/repo@branch.
    """
    ignore_list = {x.strip() for x in ignore.split(",") if x}
    select_list = {x.strip() for x in select.split(",") if x}

    _, checks, families = _collect_all(package, subdir=package_dir)
    if len(checks) == 0:
        msg = "No checks registered. Please install a repo-review plugin."
        raise click.ClickException(msg)

    if list_opt:
        for family, grp in itertools.groupby(checks.items(), key=lambda x: x[1].family):
            rich.print(f'  [dim]# {families[family].get("name", family)}')
            for code, check in grp:
                rich.print(f'  "{code}",  [dim]# {check.__doc__}')

        raise SystemExit(0)

    if str(package).startswith("gh:"):
        _, org_repo_branch, *p = str(package).split(":", maxsplit=2)
        org_repo, branch = org_repo_branch.split("@", maxsplit=1)
        package = GHPath(repo=org_repo, branch=branch, path=p[0] if p else "")
        if format_opt == "rich":
            rich.print(f"[bold]Processing [blue]{package}[/blue] from GitHub\n")

    families, processed = process(
        package, select=select_list, ignore=ignore_list, subdir=package_dir
    )

    display_output(families, processed, format_opt=format_opt, stderr=False)
    if stderr:
        display_output(families, processed, format_opt=stderr, stderr=True)

    if any(p.result is False for p in processed):
        raise SystemExit(2)
    if len(processed) == 0:
        raise SystemExit(2)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
