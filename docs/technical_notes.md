# Flood Remote Sensing Technical Notes

## Sentinel-1 for flood mapping
Sentinel-1 SAR can observe day or night and is much less constrained by cloud cover than optical imagery. Open water commonly produces low backscatter, so pre/post SAR analysis is useful for rapid event mapping.

## Avoiding false flood detections
Low backscatter can also occur over permanent water, smooth surfaces, radar shadow and other land-cover conditions. The workflow therefore uses pre/post change, permanent-water screening and terrain filtering rather than relying on a single post-event threshold.

## Threshold calibration
Operational thresholds should be calibrated with event- and region-specific reference data. Useful evaluation metrics include precision, recall, F1 and IoU, together with threshold-sensitivity analysis.

## Common false positives
Potential sources include permanent water, wet soil, irrigated agriculture, radar shadow, layover, smooth urban surfaces and acquisition differences.

## Validation
Flood is often a minority class, so overall accuracy alone can be misleading. IoU, F1, recall and precision provide more information about the mapped flood class.

## Uncertainty
Useful products include confidence/probability layers, threshold or model sensitivity, known failure modes, provenance information and areas flagged for analyst review.

## Exposure and risk
Flood hazard layers can be combined with population, roads, buildings and critical infrastructure to generate response-priority information.

## Scaling
A larger operational system would use cloud-native storage and tiling, event orchestration, parallel processing, cached baselines, metadata controls, region-specific calibration, automated QA/QC, APIs and analyst review for uncertain events.

## Platform integration
Processing and delivery can be separated by generating versioned event products and summary metrics, exposing them through APIs, and adding logging, monitoring, model/version metadata, alerting and failure recovery.

## Future extensions
Potential extensions include adaptive thresholds, Sentinel-1/Sentinel-2 fusion, validated segmentation models, object-level filtering, hydrologic context, near-real-time exposure updates and cross-event generalization testing.

## Project limitation
The committed local demonstration event is synthetic, so its numerical validation metrics are not evidence of real-world flood-mapping performance. Operational claims require independent event-specific validation.
