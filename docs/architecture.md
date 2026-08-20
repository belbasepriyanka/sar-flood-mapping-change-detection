# Platform integration architecture

```mermaid
flowchart LR
    A[Sentinel-1 / Aerial Imagery] --> B[Preprocessing]
    B --> C[Pre/Post Change Detection]
    C --> D[Terrain + Permanent-Water Filters]
    D --> E[Flood Probability / Confidence]
    E --> F[Exposure Overlay]
    F --> G[Event Risk Intelligence]
    G --> H[FastAPI Service]
    G --> I[Dashboard]
    H --> J[Disaster Intelligence Platform]
```

The public demo uses synthetic raster values locally and a separate Google Earth Engine template for Sentinel-1 GRD. Operational deployment would add event orchestration, cloud storage, model/version registry, logging, alerting, geospatial tiling, independently validated thresholds/models and human review for uncertain regions.
