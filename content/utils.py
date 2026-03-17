"""Shared utility functions for the icey_ecosystems analysis notebooks.

Includes data readers for ICESat-2 and ERA5, regridding helpers,
solar geometry, and Arctic map plotting utilities.
"""

import numpy as np
import xarray as xr
import pandas as pd
import s3fs
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import RegularGridInterpolator


# ---------------------------------------------------------------------------
# Data readers
# ---------------------------------------------------------------------------

def read_is2sitmogr4_v4(
    zarr_path="s3://icesat-2-sea-ice-us-west-2/IS2SITMOGR4_V4/zarr/IS2SITMOGR4_V4_201811-202504.zarr",
    persist=True,
):
    """Read IS2SITMOGR4 V4 monthly gridded sea ice thickness from S3 Zarr.

    Opens the dataset, drops the time dimension from static variables
    (grid_cell_area, longitude, latitude, region_mask), promotes lat/lon
    to coordinates, and normalises timestamps to the 1st of each month.

    Args:
        zarr_path: S3 path to the Zarr store.
        persist: If True, load lazy arrays into memory.

    Returns:
        xr.Dataset with dimensions (time, y, x).
    """
    s3 = s3fs.S3FileSystem(anon=True)
    store = s3fs.S3Map(root=zarr_path, s3=s3, check=False)
    ds = xr.open_zarr(store=store)

    for var in ("grid_cell_area", "longitude", "latitude", "region_mask"):
        if var in ds.data_vars:
            ds[var] = ds[var].isel(time=0, drop=True)

    ds = ds.assign_coords(
        longitude=(["y", "x"], ds.longitude.values),
        latitude=(["y", "x"], ds.latitude.values),
    )

    time_pd = pd.to_datetime(ds.time.values)
    ds = ds.assign_coords(
        time=pd.to_datetime([f"{t.year}-{t.month:02d}-01" for t in time_pd])
    )

    if persist:
        ds = ds.persist()

    return ds


def read_is2sit_summer(
    zarr_path="s3://icesat-2-sea-ice-us-west-2/is2sit_summer/zarr/IS2SIT_SUMMER_01_201905-202108.zarr",
    persist=True,
):
    """Read the IS2SIT summer monthly gridded sea ice thickness from S3 Zarr.

    Covers May 2019 – August 2021 on the same 25 km EASE2 grid as the
    winter product.

    Args:
        zarr_path: S3 path to the Zarr store.
        persist: If True, load lazy arrays into memory.

    Returns:
        xr.Dataset with dimensions (time, y, x).
    """
    s3 = s3fs.S3FileSystem(anon=True)
    store = s3fs.S3Map(root=zarr_path, s3=s3, check=False)
    ds = xr.open_zarr(store=store)

    for var in ("grid_cell_area", "longitude", "latitude", "region_mask"):
        if var in ds.data_vars:
            if "time" in ds[var].dims:
                ds[var] = ds[var].isel(time=0, drop=True)

    ds = ds.assign_coords(
        longitude=(["y", "x"], ds.longitude.values),
        latitude=(["y", "x"], ds.latitude.values),
    )

    time_pd = pd.to_datetime(ds.time.values)
    ds = ds.assign_coords(
        time=pd.to_datetime([f"{t.year}-{t.month:02d}-01" for t in time_pd])
    )

    if persist:
        ds = ds.persist()

    return ds


def read_era5_earthmover(group="spatial"):
    """Open the Earthmover ERA5 surface dataset from Arraylake.

    Requires ``arraylake`` to be installed and the user to be logged in
    (``arraylake login``).

    Args:
        group: Zarr sub-group — ``"spatial"`` (one global map per hour,
            good for map queries) or ``"temporal"`` (one year of hourly
            data per chunk, good for time-series).

    Returns:
        Lazy xr.Dataset backed by dask.
    """
    from arraylake import Client

    client = Client()
    repo = client.get_repo("earthmover-public/era5-surface-aws")
    session = repo.readonly_session("main")

    ds = xr.open_dataset(
        session.store,
        engine="zarr",
        consolidated=False,
        zarr_format=3,
        chunks={},
        group=group,
    )
    return ds


# ---------------------------------------------------------------------------
# Regridding
# ---------------------------------------------------------------------------

def regrid_era5_to_is2(era5_da, is2_lat, is2_lon, method="linear"):
    """Bilinearly interpolate a 2-D ERA5 field onto the IS2 EASE2 grid.

    Args:
        era5_da: xr.DataArray on a regular (latitude, longitude) grid.
            Latitude may be ascending or descending; longitude is assumed
            0–360.
        is2_lat: 2-D array of IS2 latitudes.
        is2_lon: 2-D array of IS2 longitudes (−180 to 180).
        method: Interpolation method passed to RegularGridInterpolator.

    Returns:
        2-D numpy array on the IS2 grid.
    """
    era5_lat = era5_da.latitude.values
    era5_lon = era5_da.longitude.values
    data = era5_da.values

    # RegularGridInterpolator needs ascending axes
    if era5_lat[0] > era5_lat[-1]:
        era5_lat = era5_lat[::-1]
        data = data[::-1, :]

    # Convert IS2 longitudes from (−180, 180) to (0, 360)
    is2_lon_360 = np.where(is2_lon < 0, is2_lon + 360, is2_lon)

    interp = RegularGridInterpolator(
        (era5_lat, era5_lon), data,
        method=method, bounds_error=False, fill_value=np.nan,
    )
    return interp(
        np.column_stack([is2_lat.ravel(), is2_lon_360.ravel()])
    ).reshape(is2_lat.shape)


# ---------------------------------------------------------------------------
# Solar geometry
# ---------------------------------------------------------------------------

def daily_mean_toa_insolation(lat_deg, day_of_year):
    """Daily-mean top-of-atmosphere insolation (W/m²).

    Uses the standard Milankovitch/Berger formulation with a simplified
    Spencer (1971) solar declination.

    Args:
        lat_deg: Latitude(s) in degrees (scalar or array).
        day_of_year: Day of year (1–365).

    Returns:
        Insolation array of the same shape as *lat_deg* (W/m²).
    """
    S0 = 1361.0
    lat = np.deg2rad(lat_deg)
    decl = np.deg2rad(23.45 * np.sin(np.deg2rad(360.0 / 365.0 * (day_of_year - 81))))
    cos_h0 = np.clip(-np.tan(lat) * np.tan(decl), -1, 1)
    h0 = np.arccos(cos_h0)
    Q = (S0 / np.pi) * (
        h0 * np.sin(lat) * np.sin(decl)
        + np.cos(lat) * np.cos(decl) * np.sin(h0)
    )
    return np.maximum(Q, 0.0)


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

def add_arctic_features(ax, extent=(-179, 179, 55, 90)):
    """Add coastlines, land, and gridlines to a polar-projection axes."""
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.coastlines(linewidth=0.3, zorder=3)
    ax.add_feature(cfeature.LAND, color="0.93", zorder=2)
    ax.gridlines(linewidth=0.2, color="gray", alpha=0.5, linestyle="--")


def arctic_map_panel(
    lon2d, lat2d, data, *,
    ax=None, cmap="viridis", vmin=None, vmax=None,
    title="", extend="max", cbar_label="",
    extent=(-180, 180, 55, 90),
):
    """Plot a single polar-stereographic panel with colorbar.

    Args:
        lon2d, lat2d: 2-D coordinate arrays.
        data: 2-D data array to plot.
        ax: Existing GeoAxes (created if None).
        cmap, vmin, vmax: Colormap settings.
        title: Panel title string.
        extend: Colorbar extend setting.
        cbar_label: Colorbar label.
        extent: Map extent (lon_min, lon_max, lat_min, lat_max).

    Returns:
        (ax, im) tuple.
    """
    proj = ccrs.NorthPolarStereo(central_longitude=-45)
    if ax is None:
        _, ax = plt.subplots(subplot_kw={"projection": proj})

    im = ax.pcolormesh(
        lon2d, lat2d, data,
        transform=ccrs.PlateCarree(),
        cmap=cmap, vmin=vmin, vmax=vmax,
    )
    add_arctic_features(ax, extent=extent)
    ax.set_title(title, fontsize=9)
    plt.colorbar(im, ax=ax, shrink=0.7, pad=0.04, extend=extend, label=cbar_label)
    return ax, im
