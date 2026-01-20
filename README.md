# icey_ecosystems

A research project focused on ice-based ecosystems analysis.

## Overview

This repository contains code and data for analyzing ice-based ecosystems as part of a mini research proposal. The project is organized as a Jupyter Book, providing an interactive and well-indexed collection of analysis notebooks.

## Jupyter Book

This repository is structured as a Jupyter Book. To build and view the book locally, follow the setup instructions below, then:

1. Build the book:
   ```bash
   jb build .
   ```

2. View the book by opening `_build/html/index.html` in your browser.

The book currently contains:
- A homepage with project overview
- An initial analysis notebook

More notebooks and content will be added in the future.

## GeoCODES Integration

This project is integrated with the [GeoCODES portal](https://geocodes.earthcube.org/#/landing) to make it discoverable in the EarthCube search interface. The metadata is embedded in the landing page using JSON-LD format following the Science on Schema (SOS) pattern.

## Setup

### UV Environment Setup

UV is a fast Python package installer and resolver. It's significantly faster than conda and handles Python package management more efficiently.

#### Prerequisites
Install UV first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Creating the UV Environment

UV will automatically create a `.venv` directory in the project root. This is the standard location and is already excluded from Jupyter Book builds.

```bash
# From the icey_ecosystems directory, sync dependencies from pyproject.toml
# This will create .venv automatically and install all dependencies
uv sync

# Activate the environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Verify jupyter-book is installed
uv run jb --help
```

#### Adding as Jupyter Kernel
To use this environment in Jupyter notebooks:
```bash
# Activate the environment first
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install as Jupyter kernel
python -m ipykernel install --user --name icey_ecosystems --display-name "Icey Ecosystems"
```

**Note**: Some geospatial packages (cartopy, rasterio) may require system-level libraries (GEOS, PROJ, GDAL). Install these with your system package manager if needed.

#### Building the Jupyter Book
To build the Jupyter Book using the UV environment:
```bash
# From the icey_ecosystems directory, you can either:

# Option 1: Activate the environment and build
source .venv/bin/activate  # On macOS/Linux
jb build .

# Option 2: Use uv run (no activation needed)
uv run jb build .
```

#### Deploying to GitHub Pages

**First, create the GitHub repository:**
1. Go to [GitHub](https://github.com) and create a new repository named `icey_ecosystems`
2. Initialize and push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/icey_ecosystems.git
   git push -u origin main
   ```

**Then, build and deploy the book:**
```bash
# Make sure the environment is activated
source .venv/bin/activate  # On macOS/Linux

# Build the book
jb build .

# Deploy to GitHub Pages (this pushes to the gh-pages branch)
ghp-import -n -p _build/html

# If you have a custom domain, use the -c flag:
# ghp-import -n -p -c yourdomain.com _build/html
```

The flags mean:
- `-n`: Don't use Jekyll processing
- `-p`: Push to GitHub
- `-c`: Create/update CNAME file for custom domain (optional)

After running this, your book will be available at `https://YOUR_USERNAME.github.io/icey_ecosystems/`

**Note:** Make sure GitHub Pages is enabled in your repository settings (Settings > Pages) and set to use the `gh-pages` branch.

### GeoCODES Integration Setup

This project is integrated with the [GeoCODES portal](https://geocodes.earthcube.org/#/landing) to make it discoverable in the EarthCube search interface. The metadata is embedded in the landing page using JSON-LD format following the Science on Schema (SOS) pattern.

#### Steps to Complete

1. **Update the JSON-LD Metadata**

   Edit `index.html` and update the following fields:
   - Replace `YOUR_USERNAME` with your actual GitHub username in the `url` field
   - Update the `creator` name with your actual name
   - Adjust the `datePublished` if needed
   - Modify the `description` to match your specific research proposal

2. **Enable GitHub Pages**

   1. Go to your repository on GitHub
   2. Navigate to **Settings** > **Pages**
   3. Under "Source", select the branch (usually `main` or `master`)
   4. Select the folder (usually `/ (root)`)
   5. Click **Save**
   6. Your site will be available at `https://YOUR_USERNAME.github.io/icey_ecosystems/`

3. **Update the Repository URL**

   After enabling GitHub Pages, update the `url` field in `index.html` to match your actual GitHub Pages URL.

4. **Register with GeoCODES**

   Once your landing page is live:
   1. Visit the [EarthCube Resource Registry](https://www.earthcube.org/geocodes)
   2. Register your resource by providing your GitHub Pages URL
   3. The GeoCODES crawler will index your metadata

5. **Validate Your Metadata**

   Before submitting, validate your JSON-LD:
   - Use [Google Rich Results Test](https://search.google.com/test/rich-results)
   - Use [Schema.org Validator](https://validator.schema.org/)

#### Required Schema.org Properties

The JSON-LD in `index.html` includes the minimum required properties:
- `@context`: Schema.org context
- `@type`: Dataset (or SoftwareSourceCode if it's primarily code)
- `name`: Project name
- `description`: Project description
- `url`: Landing page URL
- `keywords`: Relevant search terms
- `creator`: Author information
- `license`: License information

#### Additional Resources

- [GeoCODES Portal](https://geocodes.earthcube.org/#/landing)
- [Schema.org Documentation](https://schema.org/)
- [EarthCube GeoCODES Info](https://www.earthcube.org/geocodes)

## Usage

[Add usage instructions here]

## License

[Add license information here]
