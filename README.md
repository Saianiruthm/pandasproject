# PANDAS Project

## Medium Documentation

For a detailed overview, analysis insights, and conclusions, please refer to our Medium document [here](https://medium.com/@sai2804aniruth/pandas-project-analysing-netflix-titles-5c81edc3e1cb).

## Overview

This document provides additional context, analysis, and final thoughts on the project.

This repository contains a Python script (`index.py`) for data preprocessing and analysis, along with a dataset file (`data.csv`) sourced from `netflixtitles.csv`.

## Dataset Description

- **data.csv**: This dataset contains Netflix movie and TV show information.

## Code Overview

The `index.py` script performs the following tasks:

1. **Data Preprocessing:**
   - Cleans and processes the Netflix dataset.
   - Handles missing values and converts data types.
   - Separates TV shows and movies for analysis.

2. **Analysis of TV Shows:**
   - Provides insights into TV show data, including counts, ratings, seasons, directors, cast, categories, languages, and more.
   - Presents statistical summaries and distributions.

3. **Analysis of Movies:**
   - Similar analysis as TV shows but specific to movies.

## Instructions

1. **Setup:**
   - Ensure you have Python installed along with the required libraries (`pandas`, `numpy`, etc.).
   - Place the `netflixtitles.csv` file in the repository folder and rename it to `data.csv`.

2. **Execution:**
   - Run `index.py` to execute the data preprocessing and analysis.
   - Review the console output for insights into TV shows and movies on Netflix.

## Requirements

- Python 3.x
- pandas
- numpy

## How to Run

1. Clone the repository:

```
git clone https://github.com/Saianiruthm/pandasproject.git
cd pandasproject
```

2. Install dependencies (if not already installed):

```
pip install pandas numpy
```


3. Run the Python script:

```
python index.py
```

## Note

- The analysis might take some time based on the dataset size.

Feel free to explore and modify the code for further analysis or enhancements.
