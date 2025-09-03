# Flight-Data-Analyzer

A Python-based application that ingests live flight telemetry from the OpenSky Network API, stores it in a SQLite database, and provides tools for visualization and anomaly detection.

- Key Features

    - Real-Time Data Ingestion – Collects aircraft callsigns, altitude, velocity, and geographic position from the OpenSky API.

    - Database Integration – Saves telemetry into a local SQLite database for persistence and structured querying.

    - Interactive Visualization – Generates flight maps with Plotly to explore positions, altitudes, and speeds by origin country.

    - Anomaly Detection – Uses a scikit-learn Isolation Forest model to flag irregular climb and descent rates.

    - Console & Map Outputs – Provides both command-line anomaly reports and an interactive map dashboard.

- Tech Stack

    - Languages/Libraries: Python, Pandas, scikit-learn, Plotly Express

    - Database: SQLite

    - Data Source: OpenSky Network REST API
