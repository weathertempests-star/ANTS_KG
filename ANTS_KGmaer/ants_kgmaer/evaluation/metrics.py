"""Weighted binary metrics with an explicit unresolved prediction column."""

import math


def divide(a, b):
    return a / b if b else None


def mean_defined_pair(a, b):
    return (a + b) / 2 if a is not None and b is not None else None


def from_matrix(matrix):
    if len(matrix) != 2 or any(len(row) != 3 for row in matrix):
        raise ValueError("Expected two truth rows and three prediction columns")
    n0, n1 = map(sum, matrix)
    tn, fp, unresolved0 = matrix[0]
    fn, tp, unresolved1 = matrix[1]
    r0, r1 = divide(tn, n0), divide(tp, n1)
    f0 = divide(2 * tn, 2 * tn + fn + fp + unresolved0)
    f1 = divide(2 * tp, 2 * tp + fp + fn + unresolved1)
    total, decided = n0 + n1, tn + fp + fn + tp
    return {
        "confusion_matrix": matrix,
        "rows": ["benign", "malicious"], "columns": ["benign", "malicious", "unresolved"],
        "support": {"benign": n0, "malicious": n1},
        "BA_all": mean_defined_pair(r0, r1),
        "selective_BA": mean_defined_pair(divide(tn, tn + fp), divide(tp, tp + fn)),
        "macro_F1": mean_defined_pair(f0, f1) if n0 and n1 else None,
        "malicious_recall": r1, "benign_recall": r0, "malicious_precision": divide(tp, tp + fp),
        "FPR": divide(fp, n0), "coverage": divide(decided, total),
        "unresolved": unresolved0 + unresolved1,
    }


class Accumulator:
    def __init__(self):
        self.matrix = [[0.0] * 3 for _ in range(2)]
        self.raw = [[0] * 3 for _ in range(2)]
        self.statuses = {}

    def add(self, truth, prediction, weight=1.0, status="valid"):
        if type(truth) is not int or truth not in (0, 1):
            raise ValueError("An approved binary ground truth is required")
        if prediction is not None and (type(prediction) is not int or prediction not in (0, 1)):
            raise ValueError("Prediction must be 0, 1, or unresolved None")
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or not math.isfinite(weight) or weight <= 0:
            raise ValueError("Sampling weight must be finite and positive")
        column = prediction if prediction is not None else 2
        self.matrix[truth][column] += weight
        self.raw[truth][column] += 1
        self.statuses[status] = self.statuses.get(status, 0) + 1

    def result(self):
        return {**from_matrix(self.matrix), "raw_confusion_matrix": self.raw,
                "raw_events": sum(map(sum, self.raw)), "status_counts": dict(self.statuses)}


def prediction_value(result):
    if not isinstance(result, dict) or result.get("status") != "valid":
        return None
    answer = result.get("answer") or {}
    if not isinstance(answer, dict):
        return None
    return {"benign": 0, "malicious": 1}.get(answer.get("prediction"))
