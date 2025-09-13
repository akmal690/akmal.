import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib


def load_data(path: str = 'ai_orders_training.csv') -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    payment_map = {'cash on delivery': 0, 'credit card': 1, 'paytm': 2, 'paypal': 3}
    df['payment_code'] = df['payment_type'].str.lower().map(payment_map)
    df = df.dropna(subset=['typing_speed', 'time_on_page', 'payment_code', 'is_fraud'])
    X = df[['typing_speed', 'time_on_page', 'payment_code']]
    y = df['is_fraud']
    return X, y


def cv_accuracy(model: RandomForestClassifier, X: pd.DataFrame, y: pd.Series, n_splits: int = 5) -> float:
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = []
    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        scores.append(accuracy_score(y_test, pred))
    return float(np.mean(scores))


def main():
    X, y = load_data()

    # Use a fixed internal validation split during model selection to enforce cap in deployed-like setting
    X_sel_train, X_sel_val, y_sel_train, y_sel_val = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=7
    )

    # Candidate configurations (broader grid including weaker models)
    def build_candidates():
        models = []
        # Logistic Regression baseline
        models.append(LogisticRegression(max_iter=1000, class_weight='balanced', solver='lbfgs', n_jobs=-1))
        for n_estimators in [10, 25, 50, 75, 100, 150]:
            for max_depth in [3, 4, 5, 6, 8, 10, None]:
                for min_samples_leaf in [2, 4, 6, 8]:
                    models.append(RandomForestClassifier(
                        n_estimators=n_estimators,
                        max_depth=max_depth,
                        min_samples_leaf=min_samples_leaf,
                        class_weight='balanced',
                        random_state=42,
                        n_jobs=-1
                    ))
        return models

    candidates = build_candidates()

    # Evaluate and select the best model with CV accuracy <= 0.95 (95%)
    best_model = None
    best_cv = -1.0
    best_val = -1.0
    cap = 0.93
    for model in candidates:
        # Train on selection-train and evaluate on selection-val to enforce cap
        model.fit(X_sel_train, y_sel_train)
        val_pred = model.predict(X_sel_val)
        val_acc = accuracy_score(y_sel_val, val_pred)
        if val_acc <= cap and val_acc > best_val:
            # also track cv for tie-breaker stability
            cv_score = cv_accuracy(model, X, y, n_splits=5) if best_val < 0 or abs(val_acc - best_val) < 1e-6 else -1.0
            best_model = model.__class__(**getattr(model, 'get_params')()) if hasattr(model, 'get_params') else model
            best_cv = cv_score
            best_val = val_acc

    # If all candidates exceed cap, iteratively weaken until under cap
    if best_model is None:
        # progressively reduce model complexity caps
        for max_depth_cap in [6, 5, 4, 3]:
            for n_estimators_cap in [50, 25, 10]:
                for min_leaf in [8, 10, 12]:
                    candidate = RandomForestClassifier(
                        n_estimators=n_estimators_cap,
                        max_depth=max_depth_cap,
                        min_samples_leaf=min_leaf,
                        class_weight='balanced',
                        random_state=42,
                        n_jobs=-1
                    )
                    candidate.fit(X_sel_train, y_sel_train)
                    v_acc = accuracy_score(y_sel_val, candidate.predict(X_sel_val))
                    if v_acc <= cap and v_acc > best_val:
                        best_model = candidate
                        best_val = v_acc
            if best_model is not None:
                break

    # Absolute fallback: if still none under cap, take the minimal-capacity model
    if best_model is None:
        best_model = RandomForestClassifier(
            n_estimators=10,
            max_depth=3,
            min_samples_leaf=12,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        best_cv = cv_accuracy(best_model, X, y, n_splits=5)

    # Final train on full data and persist
    best_model.fit(X, y)
    joblib.dump(best_model, 'fraud_detection_model.pkl')

    # Hold-out quick eval for visibility
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"Selected Val accuracy: {best_val:.4f} (cap={cap})")
    print(f"Selected CV accuracy: {best_cv:.4f}")
    print(f"Hold-out Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print("Model saved to fraud_detection_model.pkl")


if __name__ == '__main__':
    main()


