# Sentinel-1 SAR Flood Mapping and Change Detection

A reproducible demonstration of pre/post-event SAR change detection for rapid flood screening.

## Skills demonstrated
- Sentinel-1 SAR
- Pre/post-event change detection
- Backscatter interpretation
- Binary flood classification
- Accuracy, precision, recall, F1 and IoU
- Google Earth Engine and Python

## Project design
The Earth Engine script creates a real-data workflow using Sentinel-1 GRD. The Python demo generates synthetic raster arrays so anyone can run the project without credentials or a large geospatial download.

## Run
```bash
pip install -r requirements.txt
python src/demo.py
pytest -q
```

## Method
Potential inundation is identified from a strong decrease in radar backscatter between pre-event and post-event composites. In a production workflow, the result should be refined with permanent-water masks, terrain/slope constraints, speckle treatment, orbit consistency, and independent validation.

## Data note
The local Python example is synthetic and is not a flood map of a real event.

## Author
Priyanka Belbase | Remote Sensing | Hydrology | SAR | GIS
