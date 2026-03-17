# ICEY ECOSYSTEMS: Arctic Sea Ice Light Transmission For Ecosystem Dynamics: Analysis with cloud-based ICESat-2 and ERA5 (Earthmover) data

## Overview

This Jupyter Book estimates **under-ice photosynthetically active radiation (PAR)**
across the Arctic Ocean by combining satellite-derived sea ice properties with
atmospheric reanalysis data. Light beneath sea ice is a primary control on
ice-algal and under-ice phytoplankton productivity, yet it is difficult to
observe directly at basin scale. This project bridges that gap by coupling
gridded ICESat-2 sea ice thickness and snow depth with ERA5 cloud cover inside a
physically based Beer-Lambert light transmission model.

The work is part of an NSF-funded DeCODER (Data and Computing Opportunities for
Discovery and Exploration Research) mini research proposal focused on
understanding ecological systems in ice environments, and contributes to the
EarthCube GeoCODES initiative.

## Scientific Approach

The analysis follows a multi-step workflow that traces solar radiation from the
top of the atmosphere down through the cloud layer, snow cover, and sea ice to
estimate the light available beneath the ice pack:

1. **Top-of-atmosphere (TOA) insolation** — daily-mean solar flux computed from
   orbital geometry for a given latitude and day of year.
2. **Cloud attenuation** — TOA flux is reduced to a surface shortwave estimate
   using ERA5 total cloud cover and an empirical power-law parameterisation.
3. **Multi-surface-type Beer-Lambert model** — each ice-covered grid cell is
   partitioned into snow-covered ice, bare ice, and melt-pond sub-areas, each
   with distinct albedo, surface transmittance, and extinction properties.
   Transmitted radiation through each sub-area is computed via exponential decay
   through the snow and ice layers.
4. **Grid-cell PAR** — the ice-area transmittances are weighted by their
   respective fractions, combined with an open-water contribution scaled by sea
   ice concentration, and converted to PAR using a broadband-to-PAR ratio.

The notebook compares results across three Arctic summers (2019–2021) for a
user-selected month (default: June), focusing on pack ice where ICESat-2
provides reliable thickness retrievals (SIC ≥ 0.5 by default).

## Datasets

| Dataset | Variables used | Source | Access method |
|---|---|---|---|
| **ICESat-2 IS2SIT_SUMMER** (monthly, 25 km EASE2 grid) | Sea ice thickness, snow depth, sea ice concentration, freeboard | NSIDC / NASA | S3 Zarr store (`s3://icesat-2-sea-ice-us-west-2/`) |
| **ICESat-2 IS2SITMOGR4 V4** (monthly, 25 km EASE2 grid) | Same variables, winter months (Nov–Apr, 2018–2025) | NSIDC / NASA | S3 Zarr store |
| **ERA5 surface reanalysis** | Total cloud cover (`tcc`) | ECMWF via [Earthmover Arraylake catalog](https://app.earthmover.io/marketplace/695bff20622fd82a1ec88780) | `arraylake` Python client |

All data are accessed directly from cloud storage — no local downloads are
required. Surface shortwave radiation is not read from ERA5 but derived in the
notebook by combining ERA5 cloud cover with a computed TOA insolation field.

## Navigation

- **[Analysis notebook](1_analysis)** — the main notebook: data loading,
  Beer-Lambert model, multi-year comparison maps, high-transmission region
  identification, and summary statistics.

## Future Directions

- Replace broadband extinction with wavelength-dependent coefficients
- Use satellite-derived melt-pond fraction maps (e.g. MODIS) instead of a fixed value
- Extend to a full May–August seasonal cycle to capture the spring bloom window
- Validate modeled under-ice PAR against buoy-based observations
- Differentiate first-year vs. multi-year ice optical properties

## Using the Book

There are three ways to use this Jupyter Book:

1. **Browse** — view the rendered notebooks by clicking through the links on the left.
2. **Binder** — run the notebooks interactively by clicking the **Binder** tab under the rocket ship icon at the top of each notebook.
3. **Local** — clone (or fork) the [GitHub repository](https://github.com/akpetty/icey_ecosystems) and run locally with `uv sync` to set up the environment.

## GeoCODES Integration

This project is integrated with the
[GeoCODES portal](https://geocodes.earthcube.org/#/landing) to make it
discoverable in the EarthCube search interface.

## License

All content in this Jupyter Book is distributed under the MIT license.
