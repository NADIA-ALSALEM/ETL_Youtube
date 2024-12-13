# ETL YouTube Data Project

This project extracts, transforms, and loads (ETL) data from YouTube using Dagster for data pipelines.

## Features
- Extracts video metadata from YouTube using the YouTube Data API.
- Cleans and transforms the data for analysis.
- Stores the cleaned data into an SQLite database.

## Prerequisites
1. Python 3.10 or higher.
2. Required libraries:
   - `dagster`
   - `dagit`
   - `sqlite3`
3. SQLite database browser for inspecting the data.

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/NADIA-ALSALEM/ETL_Youtube
   cd ETL-Youtube-Data
