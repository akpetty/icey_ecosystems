# icey_ecosystems

Estimating under-ice light availability across the Arctic using ICESat-2 and ERA5.

## Overview

This repository estimates **under-ice photosynthetically active radiation (PAR)**
by coupling NASA ICESat-2 sea ice thickness and snow depth with ERA5 cloud cover
inside a Beer-Lambert light transmission model. The goal is to identify where and
when enough light penetrates the pack ice to support ice-algal and under-ice
phytoplankton productivity.

The project is part of an NSF-funded DeCODER mini research proposal and is
organised as a Jupyter Book.

### Datasets

| Dataset | Source | Access |
|---|---|---|
| ICESat-2 IS2SIT_SUMMER (monthly, 25 km EASE2) | NSIDC / NASA | S3 Zarr store |
| ICESat-2 IS2SITMOGR4 V4 (monthly, 25 km EASE2) | NSIDC / NASA | S3 Zarr store |
| ERA5 surface reanalysis (total cloud cover) | ECMWF / [Earthmover catalog](https://app.earthmover.io/marketplace/695bff20622fd82a1ec88780) | `arraylake` client |

All data are accessed directly from cloud storage — no local downloads required.
Surface shortwave radiation is derived from ERA5 cloud cover combined with a
computed TOA insolation field.

### Analysis workflow

1. Compute daily-mean TOA insolation from solar geometry
2. Attenuate through ERA5 cloud cover to get surface shortwave
3. Partition ice-covered grid-cells into snow-covered, bare-ice, and melt-pond
   sub-areas with distinct albedo and extinction properties
4. Apply two-layer (snow + ice) Beer-Lambert decay to estimate transmittance
5. Weight by sea ice concentration and convert to PAR
6. Compare across three Arctic summers (2019–2021) for a user-selected month

## Jupyter Book

This repository is structured as a Jupyter Book. To build and view the book
locally, follow the setup instructions below, then:

```bash
uv run jb build .
```

Open `_build/html/index.html` in your browser to view the book.

The book contains:
- **Home** (`content/0_home.md`) — project summary, dataset descriptions, and
  scientific approach
- **Analysis notebook** (`content/1_analysis.ipynb`) — data loading, Beer-Lambert
  model, multi-year comparison maps, high-transmission region identification, and
  summary statistics
- **Utilities** (`content/utils.py`) — reusable helper functions (TOA insolation,
  ERA5 regridding, Arctic map styling)

More notebooks and content will be added in the future.

## Setup

All dependencies are managed with [uv](https://docs.astral.sh/uv/) via `pyproject.toml`. There is no `requirements.txt` — uv handles everything through its lock file (`uv.lock`).

### Prerequisites

Install uv (one-time):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install and activate

```bash
# Clone the repo and cd into it
git clone https://github.com/akpetty/icey_ecosystems.git
cd icey_ecosystems

# Create .venv and install all dependencies (one command)
uv sync

# Activate the environment
source .venv/bin/activate   # macOS / Linux
```

That's it. `uv sync` reads `pyproject.toml`, resolves versions, creates `.venv/`, and installs everything.

### Register the Jupyter kernel

So notebooks can find the environment:

```bash
source .venv/bin/activate
python -m ipykernel install --user --name icey_ecosystems --display-name "Icey Ecosystems"
```

Then select **"Icey Ecosystems"** as the kernel in Jupyter or VS Code / Cursor.

### Running commands without activating

You can skip `source .venv/bin/activate` and prefix any command with `uv run`:

```bash
uv run jupyter lab
uv run jb build .
uv run python my_script.py
```

## Managing dependencies

### Add a package

```bash
uv add <package>            # e.g. uv add seaborn
uv add "<package>>=1.2.0"   # with a version constraint
```

This updates `pyproject.toml` and `uv.lock` in one step.

### Remove a package

```bash
uv remove <package>
```

### Update all packages to latest compatible versions

```bash
uv lock --upgrade
uv sync
```

### Update a single package

```bash
uv lock --upgrade-package <package>
uv sync
```

### Regenerate the lock file from scratch

If things get tangled:

```bash
rm uv.lock
uv sync
```

### Export a requirements.txt (for collaborators not using uv)

```bash
uv export --format requirements-txt > requirements.txt
```

## Building and deploying the Jupyter Book

```bash
# Build
uv run jb build .

# Deploy to GitHub Pages
uv run ghp-import -n -p _build/html
```

The book will be available at `https://akpetty.github.io/icey_ecosystems/`.

Make sure GitHub Pages is enabled in your repository settings (Settings > Pages) using the `gh-pages` branch.

## Discoverability & GeoCODES Integration

This project follows [Science on Schema.org (SOS)](https://github.com/ESIPFed/science-on-schema.org)
best practices to make the analysis discoverable through search engines and the
[GeoCODES portal](https://geocodes.earthcube.org/#/landing).

### What we embed

Structured [JSON-LD](https://json-ld.org/) metadata is injected into every page
of the Jupyter Book (via `_templates/layout.html`) and into the standalone
landing page (`index.html`). The metadata uses the `SoftwareSourceCode` schema
type and includes:

- Project name, description, and URL
- Domain-specific keywords (Arctic, sea ice, ICESat-2, ERA5, under-ice PAR,
  Beer-Lambert, melt ponds, etc.)
- Creator, publisher (EarthCube), and funder (NSF)
- License (MIT)
- Link to the GitHub repository

### Validation tools

After deploying to GitHub Pages, validate the metadata with:

| Tool | What it checks |
|---|---|
| [Google Rich Results Test](https://search.google.com/test/rich-results) | Whether Google can parse the structured data and generate rich search results |
| [Schema.org Validator](https://validator.schema.org/) | Full conformance against the Schema.org specification |

Paste `https://akpetty.github.io/icey_ecosystems/` into either tool after
deployment.

### Maintaining the metadata

When the project scope or datasets change:

1. Update the JSON-LD in both `index.html` and `_templates/layout.html` (keep
   them in sync).
2. Bump `dateModified` to the current date.
3. Re-run the validation tools above after deploying.
4. If registering for the first time, submit the GitHub Pages URL at the
   [EarthCube Resource Registry](https://www.earthcube.org/geocodes).

## License

MIT — see the [home page](content/0_home.md) for details.
