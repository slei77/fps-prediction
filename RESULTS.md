# Hardware–Game Generalization Model for FPS Prediction

1. [Project Overview](#project-overview)
2. [Models Tested](#models-tested)
3. [Evaluation Strategy](#evaluation-strategy)
4. [Key Results](#key-results)
5. [Results Summary](#results-summary)
6. [Key Experiments](#key-experiments)
7. [What Matters Most for FPS](#what-matters-most-for-fps)
8. [Residual Analysis](#residual-analysis)
9. [Limitations](#limitations)
10. [Notebooks](#notebooks)

## Project Overview

This project predicts average FPS in PC games using a combination of:

- GPU specs
- game metadata (genre, release date)
- graphics settings (resolution, preset)

The goal is to build a model that generalizes across unseen games and hardware, rather than memorizing specific titles.

Dataset includes:

- 95 games
- 170 GPUs
- ~13,000 benchmark observations

## Models Tested

Evaluated three model families:

- Linear Regression (baseline)
- XGBoost (tree-based boosting)
- Neural Network (MLP)

## Evaluation Strategy

Group-based cross-validation was used to prevent data leakage. The train/test splits were executed at the game level with genre stratification, ensuring the model never encountered test-set games during training and that all genres were represented in the test set.

## Key Results

Final model: 5-fold cross-validated XGBoost ensemble with simple average aggregation.

Evaluation on the held-out test set achieved 16% MAPE, 0.94 R², and 26.6 RMSE.

Ensembling helps mitigate biases caused by fold-specific game distributions, resulting in more stable predictions for underrepresented genres.

## Key Findings

- GPU hardware characteristics are the strongest predictor of FPS.
- Resolution and graphics presets account for most workload variation.
- Game metadata contributes only modest predictive signal.
- XGBoost captures hardware–workload interactions better than linear or neural approaches.
- Cross-validation ensembling improves robustness across unseen games.

## Results Summary

### 5-fold cross-validation result:

|Model|MAPE|R<sup>2</sup>|RMSE|
|---|---|---|---|
|XGBoost|21.68%|0.88|40.55|
|Linear Regression|28.49%|0.76|56.43|

### Fold 1 result:

Fold 1 results are reported due to computational constraints for training the feedforward network across all folds.

|Model|MAPE|R<sup>2</sup>|RMSE|
|---|---|---|---|
|XGBoost|20.85%|0.91|31.48|
|Linear Regression|22.74%|0.87|37.5|
|FNN|24.06%|0.86|39.51|

### Why It Works

The problem is highly interaction-driven:

- GPU power × game settings × resolution all interact nonlinearly

Tree-based models such as XGBoost are well-suited for capturing nonlinear interactions between GPU capabilities, resolution, and game settings.

## Key Experiments

### 1. Feature Engineering

- GPU specs were highly predictive on their own
- Adding game text descriptions (TF-IDF) reduced performance due to sparsity

Conclusion: structured hardware data is far more informative than raw game text for this task.

### 2. Target Transformation

Tested different transformations to handle skewed FPS distribution:

- Power transform (λ = 0.1) performed best
- Improved stability of gradient boosting models

## What Matters Most for FPS

Permutation feature importance analysis shows:

1. GPU specifications
2. Graphics preset
3. Resolution
4. Game release date
5. Genre

### Insight:

FPS is driven primarily by:

hardware capability
rendering workload (resolution + settings)

Game metadata contributes comparatively little signal.

## Residual Analysis

|Original Scale|0.1 Power Scale|
|---|---|
|<img width="583" height="455" alt="image" src="https://github.com/user-attachments/assets/cf6dbde9-734d-4374-8126-354642fc2a53" />|<img width="587" height="455" alt="image" src="https://github.com/user-attachments/assets/d5fc24ac-c7bc-4108-ac6b-fab89719d32b" />|

The residuals in original scale show strong heteroscedasticity, especially at higher FPS values.

After applying the power transform (λ = 0.1), the residual distribution becomes more stable and centered, improving the effectiveness of gradient boosting.

## Limitations

- Dataset is relatively small (95 games, 170 GPUs)
- Some game genres are underrepresented
- Performance varies depending on game distribution in train/test splits

## Notebooks:

[Dev Notebook V2](https://colab.research.google.com/drive/1UguXRdVlS9xsPZTEZlbIyB1gKN4mUZGm?usp=sharing)

[Dev Notebook V1](https://colab.research.google.com/drive/1qLLXqKYXNz56A7DBeDdYQFBECxjI4ktM?usp=sharing)
