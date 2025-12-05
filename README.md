# Home Advantage in Women’s Doubles Badminton  
Analysis of BWF World Tour (2018–2021)

This project investigates whether a home-country advantage exists in professional women’s doubles badminton. Using match data from the BWF World Tour (2018–2021), the analysis evaluates win rates, point differentials, and tournament-level performance for home vs. away teams.

---

## Dataset

The dataset used in this project comes from Kaggle:

**Badminton BWF World Tour Dataset – SanderP (2024)**  
https://www.kaggle.com/datasets/sanderp/badminton-bwf-world-tour/data

Only **completed matches** were used. Retired or unfinished matches were removed.

---

## Key Metrics

The analysis computes:

### 1. **Home vs. Away Win Rates**
- Identifies whether each team is competing in its home country.
- Calculated win rate: percentage of wins per team type

### 2. **Point Differential**
Difference between points scored and points conceded:

### 3. **Tournament-Level Performance**
Compares results across:
- World Tour Finals  
- Super 1000  
- Super 750  
- Super 500  
- Super 300  
- Super 100  

### 4. **Statistical Tests**
- **Chi-square test** for independence of home/away and win/loss  
- **Welch’s t-test** comparing point differentials

---

## Running the Project

### 1. **Install Dependencies**
Run: requirements.txt

### 2. **Load Dataset**
Place `wd.csv` (women’s doubles data) in the project folder.

### 3. **Run Analysis**
In the notebook or script:
```python
from functions import (
    delete_playerIDs,
    change_country_names,
    check_home_country,
    keep_matches_with_home_team,
    home_win_rates,
    away_win_rates,
    chi_square_home_away_test,
    point_differential_average,
    plot_top5_countries
)

# Load dataset
df = pd.read_csv("wd.csv")

# Apply the cleaning and analysis steps...
#for example
plot_top5_countries(df)

