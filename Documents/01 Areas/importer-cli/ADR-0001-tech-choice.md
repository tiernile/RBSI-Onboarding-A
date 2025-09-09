# ADR-0001: Importer CLI Technology Choice

## Status
Accepted

## Context
We already have Python scripts (`scripts/*.py`) that parse XLSX, perform mapping, and generate schema and reports using `pandas`, `beautifulsoup4`, and `pyyaml`. We need a CLI with smart defaults, solid error messages, and auditable outputs.

## Decision
Build the importer as a Python CLI (argparse + logging) that composes the existing scripts and adds:
- strict argument parsing and helpful `--help`
- tolerant header resolution and mapping validation
- summary and decisions reports under `data/generated/importer-cli/`
- exit codes and clear errors for CI use

## Alternatives Considered
- Node/TS CLI: Consistency with Nuxt app, but would duplicate XLSX/CSV parsing work and slow delivery.
- Shell scripts: Too brittle for header normalisation and reporting.

## Consequences
- Reuse existing Python ecosystem and code, faster delivery.
- Keep Node footprint minimal in the Nuxt app; importer remains an external tool.
- Ensure Python deps documented; prefer `requirements.txt` kept small.

