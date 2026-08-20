# Real Case Study — Pakistan Floods, August 2022

**Data:** Copernicus Sentinel-1 GRD + JRC Global Surface Water + SRTM + WorldPop  
**Region:** Sindh, Pakistan — Larkana / Jacobabad / Dera Murad Jamali corridor  
**Event:** August 2022 monsoon flooding

## Why this event

ESA reported that Copernicus Sentinel-1 imagery acquired on **30 August 2022** was used to map extensive flooding in Pakistan, including the area between Dera Murad Jamali and Larkana. Sentinel-1 SAR is especially useful for flood response because radar can observe through cloud cover and at night.

Official ESA event page: https://www.esa.int/ESA_Multimedia/Images/2022/09/Pakistan_inundated

Official Earth Engine Sentinel-1 GRD catalog: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

## Real-data workflow

1. Define a Sindh flood-event AOI.
2. Build pre-event and post-event Sentinel-1 GRD composites using the same polarization, instrument mode, and orbit direction.
3. Calculate post-minus-pre VV backscatter change.
4. Identify strong negative changes as candidate inundation.
5. Remove persistent surface water using JRC Global Surface Water.
6. Exclude steep terrain using SRTM-derived slope.
7. Calculate candidate flood area.
8. Overlay WorldPop population to estimate exposed population within the mapped flood candidate.
9. Export flood mask, SAR change layer, and event summary for validation and downstream analysis.

## Reproduce in Google Earth Engine

Open [`pakistan_2022_sentinel1.js`](pakistan_2022_sentinel1.js) in the Earth Engine Code Editor and run it. The script is deliberately explicit about date windows, orbit/polarization filtering, permanent-water removal, terrain screening, exposure overlay, and export settings.

> **Important:** the change threshold is a demonstration starting point. A professional flood product must calibrate it using event-specific reference data and report uncertainty and validation metrics.

## What this adds to the portfolio

This case study demonstrates that the repository can move from a controlled synthetic event to a **real public Sentinel-1 disaster event**, while preserving the same processing architecture used by the local Python demo.

## Attribution

Sentinel-1 data: European Union/ESA/Copernicus.  
Historical event reference: ESA, *Pakistan inundated*, September 2022.  
The repository does not claim that its thresholded output reproduces the official ESA/Copernicus flood product exactly.
