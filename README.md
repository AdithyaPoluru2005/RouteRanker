# RouteRanker: AI-Powered Public Transit Route Optimization

## 1. Project Goal

RouteRanker aims to analyze public transit data and support route analysis and optimization using data science and machine learning techniques.

The first module focuses on collecting, organizing, inspecting, and documenting public transit datasets from six Indian cities.

## 2. Project Structure

```text
RouteRanker/
├── data/
│   ├── raw/
│   │   ├── delhi/
│   │   ├── Hyderabad/
│   │   ├── bengaluru/
│   │   ├── chennai/
│   │   ├── mumbai/
│   │   └── pune/
│   └── processed/
├── notebooks/
│   ├── 01_dataset_understanding.ipynb
│   ├── 02_hyderabad_dataset_understanding.ipynb
│   ├── 03_bengaluru_dataset_understanding.ipynb
│   ├── 04_chennai_dataset_understanding.ipynb
│   ├── 05_mumbai_dataset_understanding.ipynb
│   └── 06_pune_dataset_understanding.ipynb
├── reports/
├── .gitignore
└── README.md
```

Folder names and notebook names should match the actual project files.

## 3. Dataset Sources

The project uses GTFS or GTFS-style public transit data obtained from publicly accessible online sources.

| City | Dataset source |
|---|---|
| Delhi | [Delhi GTFS bus dataset](https://ethanc8.github.io/delhi-gtfs/bus.zip) |
| Hyderabad | [Telangana State Road Transport Corporation Open Data](https://www.tgsrtc.telangana.gov.in/open-data) |
| Bengaluru | [BMTC GTFS repository](https://github.com/Vonter/bmtc-gtfs) |
| Chennai | [Chennai GTFS repository](https://github.com/ungalsoththu/ChennaiGTFS) |
| Mumbai | [Mumbai GTFS repository](https://github.com/croyla/mumbai-gtfs) |
| Pune | [PMPML GTFS repository](https://github.com/croyla/pmpml-gtfs) |

Check each source for its publisher, available files, licence, and update date. Community-maintained data should not be described as an official agency feed unless the source confirms this.

## 4. How to Obtain the Datasets

1. Open the relevant source link in the table above.
2. Download the available GTFS files or archive using the source's instructions.
3. Extract each dataset into its corresponding city folder under `data/raw/`.
4. Locate the directory containing the GTFS text files, such as `routes.txt`, `stops.txt`, `trips.txt`, and `stop_times.txt`.
5. Check whether additional files, such as `calendar.txt` and `calendar_dates.txt`, are available.

Keep the original downloaded data unchanged. The raw datasets are stored locally and are excluded from GitHub where configured in `.gitignore`. Anyone cloning the repository may need to download the datasets separately.

## 5. Dataset Inventory and Quality Checks

Each city has a Jupyter notebook for examining its downloaded dataset.

The notebooks record the available files, row counts, column counts, column names, missing values, duplicate identifiers, and selected relationships between GTFS files.

Observed issues should be documented using the actual notebook results. Missing values in optional GTFS fields do not necessarily indicate invalid records.

## 6. GTFS File Relationships

- `routes.txt` identifies transit routes using `route_id`.
- `trips.txt` connects scheduled trips to routes through `route_id` and identifies their service schedules using `service_id`.
- `stop_times.txt` connects to trips through `trip_id` and to stops through `stop_id`. It also records stop sequence and scheduled times.
- `stops.txt` contains stop names and available location information.
- `calendar.txt`, when present, defines regular operating days and service periods.
- `calendar_dates.txt`, when present, records service-date additions and exceptions.

The relationship checks help identify references to missing routes, trips, or stops and trips without stop-time records. Calendar availability is checked separately for each city's feed.

## 7. Software Requirements

- Python 3
- Jupyter Notebook support
- pandas

Install the required Python packages from a terminal:

```bash
python -m pip install pandas jupyter
```

Open the project folder in VS Code and ensure that the Python and Jupyter extensions are installed.

## 8. How to Run the Notebooks

1. Clone or open the RouteRanker project folder.
2. Download the required city datasets and place them in the expected `data/raw/` directories.
3. Open the `notebooks/` folder in VS Code.
4. Open the notebook for the city you want to inspect.
5. Select a Python kernel.
6. Run the cells from top to bottom.
7. Review the dataset inventory, missing values, and relationship validation results.
8. Save the notebook after completing the analysis.

The notebook paths and data paths must match the actual local folder structure.

## 9. Current Module

Module 1 covers dataset acquisition, folder organization, dataset inventory, initial data-quality assessment, GTFS relationship documentation, and instructions for running the notebooks.

## 10. Future Work

Later modules can build on the inspected data for data cleaning, feature engineering, transit network analysis, and route optimization.
