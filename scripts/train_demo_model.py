from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def main():
    rng = np.random.default_rng(42)
    sample_count = 1000
    recent_cases = rng.integers(0, 21, size=sample_count)
    coliform_detected = rng.integers(0, 2, size=sample_count)
    turbidity_ntu = rng.uniform(0, 20, size=sample_count)
    features = np.column_stack((recent_cases, coliform_detected, turbidity_ntu))
    review_signal = (
        (recent_cases >= 8)
        | ((coliform_detected == 1) & (turbidity_ntu > 5))
    ).astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        features, review_signal, test_size=0.2, random_state=42, stratify=review_signal
    )
    model = DecisionTreeClassifier(max_depth=3, random_state=42)
    model.fit(x_train, y_train)

    model_path = Path(__file__).resolve().with_name("demo_model.joblib")
    joblib.dump(model, model_path)
    accuracy = accuracy_score(y_test, model.predict(x_test))
    print(f"Saved synthetic demonstration model to {model_path}")
    print(f"Held-out accuracy on synthetic data: {accuracy:.3f}")
    print("This toy model is not validated and must not be used for health decisions.")


if __name__ == "__main__":
    main()