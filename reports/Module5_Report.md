# Module 5 – Machine Learning Model Development and Evaluation

## 1. Objective
The objective of this module was to apply machine learning clustering algorithms to identify groups of similar public transit routes using the preprocessed GTFS datasets of six Indian cities.

## 2. Algorithms Implemented
- **K-Means:** Grouped routes into a selected number of clusters.
- **DBSCAN:** Grouped nearby routes and identified noise points.

Random Forest and XGBoost classification were not implemented because the available dataset does not contain genuine labelled target data.

## 3. Evaluation Methods
K-Means was evaluated using:
- Elbow Method
- Silhouette Score
- Davies-Bouldin Index

DBSCAN was evaluated using:
- Silhouette Score
- Davies-Bouldin Index
- Number of clusters
- Noise-point analysis

## 4. Key Observations
- K-Means produced clusters for all six cities.
- Hyderabad achieved the highest K-Means Silhouette Score of 0.816.
- DBSCAN identified different numbers of clusters depending on its `eps` parameter.
- Chennai achieved the highest DBSCAN Silhouette Score of 0.783.
- Bengaluru achieved the lowest DBSCAN Davies-Bouldin Index of 0.342.
- DBSCAN identified 56 noise points in Delhi and only 1 in Chennai.

## 5. Limitations
- The dataset contains scheduled transit information, not actual passenger counts.
- The clusters represent similarities in total trips and total stops, not actual passenger overcrowding.
- DBSCAN noise points do not automatically indicate inefficient routes.
- Classification algorithms were not applicable because genuine target labels were unavailable.
- Clustering results depend on algorithm parameters and selected features.

## 6. Possible Route Optimization Suggestions
- Study routes belonging to different clusters to identify differences in scheduled trips and stops.
- Review routes identified as DBSCAN noise points for unusual characteristics.
- Use clustering results as an initial analysis to support route planning.
- Collect actual passenger demand and occupancy data before making decisions about overcrowding, merging routes or changing service frequency.

## 7. Conclusion
Both K-Means and DBSCAN were successfully implemented and evaluated using six city datasets. The results demonstrate how clustering can group similar transit routes and identify unusual data points. These findings can support further public transit analysis and route planning.