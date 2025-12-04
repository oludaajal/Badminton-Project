#import necessary phython libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *


#Womens Analysis
#read women's doubles csv
womens_db = pd.read_csv("wd.csv")
#clean up the data and remove player IDs
womens_db = delete_playerIDs(womens_db)
#rename team 1 and 2 nationality
womens_db = womens_db.rename(columns={
    'team_one_player_one_nationality': 'team_one_nationality',
    'team_two_player_one_nationality': 'team_two_nationality'
})
#change country codes to full names
womens_db = change_country_names(womens_db, country_map)

#function to determine if the teams have the same nationality as country of play and
# produce a 0 or 1 in new columns to determine the winner
womens_db = check_home_country(womens_db)
#print(womens_db['team_one_nationality'].unique())


#to remove (away and away) matches to remove skew and have matches with at least 1 home team
womens_db_home = keep_matches_with_home_team(womens_db)

#check nationality
number_of_countries = print("Number of match country locations: ", womens_db_home['country'].nunique())
number_of_nationalities = print("Number of Nationalities present within the teams: ", womens_db_home['team_one_nationality'].nunique())

print(womens_db_home.columns)
# now compute win rates, point diff, chi-square on womesd_db_home

#checking the matches with home team
matches_with_home_team = ((womens_db_home['team_one_nationality'] == womens_db_home['country']) |
                          (womens_db_home['team_two_nationality'] == womens_db_home['country'])).sum()

print("Matches with at least one home team:", matches_with_home_team)
print("Total matches:", len(womens_db_home))

#double checking to see which nationalities match the county of play
matching_nationalities = womens_db_home.loc[
    (womens_db_home['team_one_nationality'] == womens_db_home['country']) |
    (womens_db_home['team_two_nationality'] == womens_db_home['country']),
    'country'
].nunique()
print("Countries where home teams exist:", matching_nationalities)




#Analysis 1 - Win Rates
#In matches where at least one home team is present, what fraction are won by the home team?
womens_home_win_rates = home_win_rates(womens_db_home)
womens_away_win_rates = away_win_rates(womens_db_home)

#chi-square test
chi_square_home_away_test(womens_db_home)


#Analysis 2 - Point Differential
womens_average_home_point_differential = point_differential_average(womens_db_home)

#Analysis 3 - Tournament Importance, Percentage of winners/tournament type
winners, win_percentages = winner_tournament(womens_db_home)
#print(win_percentages)

#Analysis 4 - Home advantage by natonality
#print the nationality results of the table
womens_nationality_results = nationality_home_advantage(womens_db_home)
print(womens_nationality_results)

#possibillity of playing in the home country
possibility_home_play = (matching_nationalities/(womens_db_home['team_one_nationality'].nunique()))*100
print(f"Possibility of playing in home country {possibility_home_play:.2f}%" )

#list of to 5 countries
top_host_countries(womens_db_home, 5)
#pie chart to visualize the top 5 countries
plot_top5_countries(womens_db_home)



