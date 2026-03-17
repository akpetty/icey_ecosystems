# ICEY ECOSYSTEMS: Arctic Sea Ice Light Transmission For Ecosystem Dynamics: Analysis with cloud-based ICESat-2 and ERA5 (Earthmover) data

## Overview

This Jupyter Book has been created to showcase new estimates of **under-ice photosynthetically active radiation (PAR)**
across the Arctic Ocean by combining satellite-derived sea ice thickness observations with
atmospheric reanalysis data. Light beneath sea ice is a primary control on
ice-algal and under-ice phytoplankton productivity, yet it is difficult to
observe directly at basin scale. This project bridges that gap by coupling
gridded ICESat-2/NSESOSIM sea ice thickness and snow depth estimates with ERA5 cloud cover inside a
physically based Beer-Lambert light transmission model.

The work is part of an NSF-funded DeCODER (Data and Computing Opportunities for
Discovery and Exploration Research) mini research proposal focused on
understanding ecological systems in ice environments, and contributes to the
EarthCube GeoCODES initiative. A key additional focus is thus on incorporating appropriate schema into the html files to increase discoverability. 

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
   with distinct albedo, surface transmittance, and extinction properties that can be tweaked by the user.
   Transmitted radiation through each 25 km x 25 km grid-cell ea is computed via exponential decay
   through the snow and ice.
4. **Grid-cell PAR** — the ice-area transmittances are weighted by their
   respective fractions, combined with an open-water contribution scaled by sea
   ice concentration, and converted to PAR using a broadband-to-PAR ratio.

The notebook compares results across three Arctic summers (2019–2021) for a
user-selected month (default: June), focusing on pack ice where ICESat-2
provides reliable thickness retrievals (SIC ≥ 0.5 by default).

## Datasets

| Dataset | Variables used | Source | Access method |
|---|---|---|---|
| **ICESat-2 IS2SIT_SUMMER** (monthly, 25 km x 25 km North Polar Stereographic grid, Petty et al., 2025a, 2025b) | Sea ice thickness, snow depth, sea ice concentration, freeboard | NSIDC / NASA | S3 Zarr store (`s3://icesat-2-sea-ice-us-west-2/`) |
| **ICESat-2 IS2SITMOGR4 V4** (monthly, 25 km x 25 km North Polar Stereographic grid, Petty et al., 2023, 2025c) | Same variables, winter months (Nov–Apr, 2018–2025) | NSIDC / NASA | S3 Zarr store |
| **ERA5 surface reanalysis** | Total cloud cover (`tcc`) | ECMWF via [Earthmover Arraylake catalog](https://app.earthmover.io/marketplace/695bff20622fd82a1ec88780) | `arraylake` Python client |

All data are accessed directly from cloud storage — no local downloads are
required. Surface shortwave radiation is not read from ERA5 but derived in the
notebook by combining ERA5 cloud cover with a computed TOA insolation field.

## Navigation

- **[Analysis notebook](1_analysis)** — the main notebook: data loading,
  Beer-Lambert model, multi-year comparison maps, high-transmission region
  identification, and summary statistics.

## Potential Future Directions

- Replace broadband extinction with wavelength-dependent coefficients.
- Use satellite-derived melt-pond fraction or albedo estimates from remote sensing estimates, instead of a fixed value.
- Extend to a full May–August seasonal cycle to capture the spring bloom window.
- Validate modeled under-ice PAR against buoy-based observations.
- Differentiate first-year vs. multi-year ice optical properties.

## Using the Book

There are three ways to use this Jupyter Book:

1. **Browse** — view the rendered notebook/s by clicking through the links on the left.
2. **Binder** — run the notebooks interactively by clicking the **Binder** tab under the rocket ship icon at the top of each notebook.
3. **Local** — clone (or fork) the [GitHub repository](https://github.com/akpetty/icey_ecosystems) and run locally with `uv sync` to set up the environment (see GitHub README for more information on UV and environments).

## Discoverability & GeoCODES Integration

This project follows [Science on Schema.org (SOS)](https://github.com/ESIPFed/science-on-schema.org)
best practices to increase discoverabilty through search engines and the
[GeoCODES portal](https://geocodes.earthcube.org/#/landing).

Every page of this Jupyter Book includes structured
[JSON-LD](https://json-ld.org/) metadata (via a custom Sphinx template) using the
`SoftwareSourceCode` schema type. The metadata includes:

- Project description, URL, and code repository link
- Domain-specific keywords (Arctic, sea ice, ICESat-2, ERA5, under-ice PAR,
  Beer-Lambert, melt ponds, phytoplankton, ice algae, etc.)
- Creator, publisher (EarthCube), and funder (NSF)
- License (MIT)

After deploying the book to GitHub Pages, the metadata can be validated with:

- [Google Rich Results Test](https://search.google.com/test/rich-results) —
  checks whether Google can parse the structured data
- [Schema.org Validator](https://validator.schema.org/) — checks full
  conformance against the Schema.org specification

See the [GitHub README](https://github.com/akpetty/icey_ecosystems) for
instructions on maintaining the JSON-LD when the project scope or datasets
change.

## References

Petty, A. A., A. Cabaj, J. Landy (2025a), Initial assessment of all-season Arctic sea ice thickness from ICESat-2, Journal of Glaciology, 1-39, doi: 10.1017/jog.2025.10119.

Petty, A. A. (2025b), Monthly gridded summer Arctic sea ice thickness from ICESat-2, v1 [Data set], Zenodo, doi: 10.5281/zenodo.15375596.

Petty, A. A., N. Kurtz, R. Kwok, T. Markus, T. A. Neumann, N. Keeney and A. Cabaj (2025c), ICESat-2 L4 Monthly Gridded Sea Ice Thickness, Version 4. [Indicate subset used]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. doi: 10.5067/TXDHDJ1JT0CG.

Petty A. A., N. Keeney, A. Cabaj, P. Kushner, M. Bagnardi (2023), Winter Arctic sea ice thickness from ICESat-2: upgrades to freeboard and snow loading estimates and an assessment of the first three winters of data collection, The Cryosphere, 17, 127–156, doi: 10.5194/tc-17-127-2023.

McHenry K, Bobak M, Coakley K, Fils D, Gatzke L, Zhang B, Kooper R, Richard S, Valentine D, Zaslavsky I, Shepherd, A & Lingerfelt E. (2021). GeoCODES. EarthCube. https://geocodes.earthcube.org.

## License

All content in this Jupyter Book is distributed under the MIT license.
