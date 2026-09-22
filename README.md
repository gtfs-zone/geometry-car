# Geometry Car

Dagster pipeline that inventories the world of GTFS. It ingests the Transitland
Atlas DMFR corpus and the Mobility Database daily, checks whether each feed
endpoint still answers, keeps the history in Postgres, and publishes public JSON
artifacts to object storage at `data.gtfs.zone`.

## Overview

Every consumer used to ship its own copy of a build-time feed catalog with no
liveness signal. This replaces that: one pipeline produces `sources.json`,
`status.json`, `examples.json`, `summary.json` and a `manifest.json` consumers
poll to decide whether to refetch, plus deduplicated dated snapshots.

Reachability is checked with a HEAD request, falling back to a ranged GET when
the origin rejects HEAD. No feed bodies are downloaded or stored.

`globe-of-contents` (`list.gtfs.zone`) is the frontend for these artifacts.

## Running Locally

```bash
make env             # creates .env from .env.example
uv sync
uv run dagster dev
```

Fill `MOBILITY_DB_REFRESH_TOKEN` in `.env`, and point `TRANSITLAND_ATLAS_PATH`
at a sibling checkout of `transitland/transitland-atlas` so runs read the DMFR
corpus from disk rather than the GitHub API.

Trigger the first run from the Dagster UI rather than waiting for the schedule.

## Development

```bash
uv sync              # install dependencies
ruff check .         # lint
ruff format .        # format
uv run pytest        # tests
pre-commit install   # install git hooks (run once after clone)
```

Tests run against no services: `respx` for the catalog APIs and the endpoint
checks, `moto` for the bucket, SQLite for the history tables.
