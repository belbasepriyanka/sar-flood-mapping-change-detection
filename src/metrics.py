import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, jaccard_score

def flood_metrics(reference, predicted):
    reference = np.asarray(reference).ravel().astype(int)
    predicted = np.asarray(predicted).ravel().astype(int)
    return {
        "accuracy": accuracy_score(reference, predicted),
        "precision": precision_score(reference, predicted, zero_division=0),
        "recall": recall_score(reference, predicted, zero_division=0),
        "f1": f1_score(reference, predicted, zero_division=0),
        "iou": jaccard_score(reference, predicted, zero_division=0),
    }
