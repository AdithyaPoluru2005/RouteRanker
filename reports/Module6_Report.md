
# Module 6: Model Inference and Route Optimization

## 1. Objective
To apply trained machine learning models, identify unusual routes,
generate route review suggestions and simulate possible schedule changes.

## 2. Classification Models
Two classification models were trained:
- Random Forest
- XGBoost

Classification results:

        Model  Accuracy  Precision   Recall  F1_Score
Random Forest  0.497283   0.500425 0.497283  0.496817
      XGBoost  0.518003   0.525031 0.518003  0.518973

The categories Low, Medium and High were derived from scheduled trip
frequency within each city. These are proxy labels, not independently
verified ground-truth labels or passenger-demand categories.

## 3. K-Means Inference
Saved K-Means models were applied to six cities.

     City  Total Routes  Clusters Assigned
    delhi          2403                  2
hyderabad          1031                  2
bengaluru          4434                  2
  chennai          4611                  3
   mumbai          1609                  3
     pune           628                  3

## 4. DBSCAN Inference
Saved DBSCAN models were applied using their core points and eps values.

     City  Total Routes  Clusters Assigned  Unassigned Routes
    delhi          2403                  3                 56
hyderabad          1031                  2                 51
bengaluru          4434                  3                 29
  chennai          4611                  3                  1
   mumbai          1609                  2                 10
     pune           628                  2                 27

Unassigned routes require further investigation. They are not automatically
inefficient routes.

## 5. Unusual Route Analysis
A total of 174 routes were identified as unassigned
by DBSCAN.

Route review suggestions were generated using scheduled trip counts
and stop counts.

## 6. Route Optimization Simulation
A hypothetical 10% scheduled-trip reduction was applied to selected
routes flagged for very high scheduled frequency.

     City  Original_Routes  Simulated_Routes  Original_Scheduled_Trips  Simulated_Scheduled_Trips
    delhi             2403              2403                   89393.0                    89393.0
hyderabad             1031              1031                   44892.0                    42959.0
bengaluru             4434              4434                   57836.0                    57836.0
  chennai             4611              4611                   47047.0                    47047.0
   mumbai             1609              1609                   99080.0                    98947.0
     pune              628               628                   10128.0                    10128.0

This is an illustrative simulation, not a real operational recommendation.
Route merging, splitting and service reductions require further evidence
such as geographical overlap, passenger demand and service coverage.

## 7. Limitations
- GTFS data represents scheduled services, not actual passenger counts.
- No independently verified classification labels were available.
- No actual overcrowding information was available.
- DBSCAN unassigned routes are not necessarily inefficient.
- The simulation does not prove an improvement in service quality.
- Geographical connectivity and passenger demand require further analysis.

## 8. Conclusion
Module 6 demonstrated classification, model inference, unusual route
identification, route review suggestions and hypothetical schedule
simulation across six Indian cities.

## 9. Preprocessing Objects

Six city-specific StandardScaler objects were reconstructed
and verified against the scaled features from Module 4.

Verification results:
- Delhi: True
- Hyderabad: True
- Bengaluru: True
- Chennai: True
- Mumbai: True
- Pune: True

All six scaler objects were saved in:
data/model_results/city_scalers.joblib

## 10. Saved Model Files

- kmeans_models.joblib
- dbscan_models.joblib
- random_forest_model.joblib
- xgboost_model.joblib
- city_scalers.joblib

