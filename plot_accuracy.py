import json
import glob
import os
from datetime import datetime
import matplotlib.pyplot as plt


def parse_timestamp(ts_str: str, fallback_name: str) -> datetime:
    try:
        return datetime.fromisoformat(ts_str)
    except Exception:
        # Try parse from filename like accuracy_report_YYYYMMDD_HHMMSS.json
        base = os.path.basename(fallback_name)
        try:
            parts = base.replace('accuracy_report_', '').replace('.json', '')
            return datetime.strptime(parts, '%Y%m%d_%H%M%S')
        except Exception:
            # Fallback to file mtime
            return datetime.fromtimestamp(os.path.getmtime(fallback_name))


def extract_accuracy(report: dict) -> float | None:
    # Preferred: top-level basic_accuracy.accuracy from our test script
    try:
        if report.get('basic_accuracy') and isinstance(report['basic_accuracy'], dict):
            acc = report['basic_accuracy'].get('accuracy')
            if isinstance(acc, (int, float)):
                return float(acc)
    except Exception:
        pass

    # Alternate: performance_summary.accuracy_evaluation.accuracy
    try:
        perf = report.get('performance_summary')
        if perf and isinstance(perf, dict):
            acc_eval = perf.get('accuracy_evaluation')
            if acc_eval and isinstance(acc_eval, dict):
                acc = acc_eval.get('accuracy')
                if isinstance(acc, (int, float)):
                    return float(acc)
    except Exception:
        pass

    # Alternate older formats: direct keys
    for key_path in [
        ['accuracy'],
        ['metrics', 'accuracy'],
        ['detailed_accuracy', 'accuracy'],
    ]:
        ref = report
        ok = True
        for k in key_path:
            if isinstance(ref, dict) and k in ref:
                ref = ref[k]
            else:
                ok = False
                break
        if ok and isinstance(ref, (int, float)):
            return float(ref)
    return None


def main():
    # Collect report files from root and 'af' directory
    report_paths = []
    report_paths.extend(glob.glob('accuracy_report_*.json'))
    report_paths.extend(glob.glob(os.path.join('af', 'accuracy_report_*.json')))

    if not report_paths:
        print('No accuracy report files found.')
        return

    points = []
    for path in report_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            ts = parse_timestamp(data.get('timestamp', ''), path)
            acc = extract_accuracy(data)
            if acc is not None:
                points.append((ts, acc, path))
        except Exception as e:
            print(f'Skip {path}: {e}')

    if not points:
        print('No accuracy values found in reports.')
        return

    # Sort by timestamp
    points.sort(key=lambda x: x[0])
    times = [p[0] for p in points]
    accs = [p[1] for p in points]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(times, [a * 100 for a in accs], marker='o', linewidth=2, color='#1f77b4')
    plt.title('Model Accuracy Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Accuracy (%)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    out_path = 'accuracy_trend.png'
    plt.savefig(out_path, dpi=150)
    print(f'Accuracy line chart saved to: {out_path}')


if __name__ == '__main__':
    main()


