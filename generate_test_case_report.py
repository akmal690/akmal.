import json
import glob
import os
import csv
from datetime import datetime


def find_latest_report() -> str | None:
    candidates = glob.glob('accuracy_report_*.json')
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def main():
    report_path = find_latest_report()
    if not report_path:
        print('No accuracy_report_*.json found.')
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)

    # Determine the source of custom test in the report
    custom = report.get('custom_test') or {}
    metrics = custom.get('metrics') or {}
    preds = (custom.get('predictions') or {})
    predicted_labels = preds.get('predicted_labels') or []
    prediction_probabilities = preds.get('prediction_probabilities') or []

    # Attempt to also fetch original test cases used in the script (not saved by default)
    # We'll infer by count only; per-case inputs are not stored in the report, so we only export predictions.
    timestamp = report.get('timestamp', datetime.now().isoformat())

    out_file = 'test_case_report.csv'
    with open(out_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['timestamp', 'report_file', 'case_index', 'predicted_label', 'fraud_probability'])
        # Rows
        for idx, (label, prob) in enumerate(zip(predicted_labels, prediction_probabilities), start=1):
            writer.writerow([timestamp, os.path.basename(report_path), idx, label, prob])

    # Write a small metrics summary file as well
    summary_file = 'test_case_report_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Report: {report_path}\n")
        f.write(f"Timestamp: {timestamp}\n")
        if metrics:
            f.write(f"Accuracy: {metrics.get('accuracy')}\n")
            f.write(f"Precision: {metrics.get('precision')}\n")
            f.write(f"Recall: {metrics.get('recall')}\n")
            f.write(f"F1-Score: {metrics.get('f1_score')}\n")
            f.write(f"Total Samples: {metrics.get('total_samples')}\n")
            cm = metrics.get('confusion_matrix') or {}
            f.write(f"Confusion Matrix (TN,FP,FN,TP): {cm.get('true_negatives')},{cm.get('false_positives')},{cm.get('false_negatives')},{cm.get('true_positives')}\n")

    print(f"test_case_report saved to: {out_file}")
    print(f"summary saved to: {summary_file}")


if __name__ == '__main__':
    main()


