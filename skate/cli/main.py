import asyncio
import sys

import click

from skate.exporter import export
from skate.judge import run_judge
from skate.renderer import render_run
from skate.runner import run_all
from skate.scorer import compute_similarity


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("prompt", required=False)
@click.option("--models", required=True, help="Comma-separated model identifiers.")
@click.option("--prompt-file", type=click.Path(exists=True), help="Path to a .txt prompt file.")
@click.option("--var", multiple=True, metavar="KEY=VALUE", help="Template variables, repeatable.")
@click.option("--system", default=None, help="System prompt applied to all models.")
@click.option("--temperature", type=float, default=None, help="Sampling temperature.")
@click.option("--max-tokens", type=int, default=None, help="Max output tokens.")
@click.option("--output", default=None, help="Save results to file (.json or .csv).")
@click.option("--score", is_flag=True, default=False, help="Show similarity matrix.")
@click.option("--judge", default=None, help="Model to use as judge.")
@click.option("--judge-criteria", default=None, help="Comma-separated evaluation criteria.")
def run(
    prompt: str | None,
    models: str,
    prompt_file: str | None,
    var: tuple[str, ...],
    system: str | None,
    temperature: float | None,
    max_tokens: int | None,
    output: str | None,
    score: bool,
    judge: str | None,
    judge_criteria: str | None,
) -> None:
    if prompt_file:
        with open(prompt_file) as f:
            prompt_text = f.read().strip()
    elif prompt:
        prompt_text = prompt
    else:
        click.echo("Provide a prompt or --prompt-file.", err=True)
        sys.exit(1)

    if var:
        variables: dict[str, str] = {}
        for item in var:
            if "=" not in item:
                click.echo(f"Invalid --var format: {item!r}. Expected KEY=VALUE.", err=True)
                sys.exit(1)
            key, _, value = item.partition("=")
            variables[key.strip()] = value
        try:
            prompt_text = prompt_text.format_map(variables)
        except KeyError as exc:
            click.echo(f"Missing template variable: {exc}", err=True)
            sys.exit(1)

    model_list = [m.strip() for m in models.split(",") if m.strip()]
    results = asyncio.run(
        run_all(prompt_text, model_list, system=system, temperature=temperature, max_tokens=max_tokens)
    )
    similarity = compute_similarity(results) if score else None

    criteria = [c.strip() for c in judge_criteria.split(",")] if judge_criteria else None
    judge_result = asyncio.run(run_judge(prompt_text, results, judge, criteria)) if judge else None

    render_run(prompt_text, results, similarity=similarity, judge_result=judge_result)

    if output:
        export(results, output)
        click.echo(f"Results saved to {output}")
