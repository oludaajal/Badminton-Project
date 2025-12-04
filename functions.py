import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind

#function to delete the columns of player ID
def delete_playerIDs(df):
    df = df.copy() #copy the original data
    df = df.drop(columns=[
        "city",
        "date",
        "tournament",
        "retired",
        "discipline",
        "team_one_player_one",
        "team_one_player_two",
        "team_two_player_one",
        "team_two_player_two",
        "game_1_score",
        "game_2_score",
        "game_3_score",
        "game_1_scores",
        "game_2_scores",
        "game_3_scores",
        "game_2_scores",
        "team_one_game_points",
        "team_two_game_points",
        "team_one_game_points_game_1",
        "team_one_game_points_game_2",
        "team_one_game_points_game_3",
        "team_two_game_points_game_1",
        "team_two_game_points_game_2",
        "team_two_game_points_game_3",
        "team_one_most_consecutive_points",
        "team_two_most_consecutive_points",
        "team_one_most_consecutive_points_game_1",
        "team_two_most_consecutive_points_game_1",
        "team_one_most_consecutive_points_game_2",
        "team_two_most_consecutive_points_game_2",
        "team_one_most_consecutive_points_game_3",
        "team_two_most_consecutive_points_game_3",
        "team_one_player_two_nationality",
        "team_two_player_two_nationality"
        ])
    return df


#create a map to change the country from codes to the full country names
country_map = {
    'THA': 'Thailand',
    'INA': 'Indonesia',
    'SWE': 'Sweden',
    'MAS': 'Malaysia',
    'GER': 'Germany',
    'SGP': 'Singapore',
    'HKG': 'Hong Kong',
    'IND': 'India',
    'AUS': 'Australia',
    'CHN': 'China',
    'DEN': 'Denmark',
    'TPE': 'Chinese Taipei',
    'JPN': 'Japan',
    'KOR': 'South Korea',
    'BEL': 'Belgium',
    'NED': 'Netherlands',
    'SUI': 'Switzerland',
    'CZE': 'Czech Republic',
    'FRA': 'France',
    'ENG': 'England',
    'BUL': 'Bulgaria',
    'RUS': 'Russia',
    'UKR': 'Ukraine',
    'FIN': 'Finland',
    'NZL': 'New Zealand',
    'USA': 'United States',
    'CAN': 'Canada',
    'PHI': 'Philippines',
    'VIE': 'Vietnam',
    'MAC': 'Macau',
    'LAT': 'Latvia',
    'TUR': 'Turkey',
    'ITA': 'Italy',
    'IRL': 'Ireland',
    'SCO': 'Scotland',
    'POR': 'Portugal',
    'EST': 'Estonia',
    'HUN': 'Hungary',
    'CRO': 'Croatia',
    'EGY': 'Egypt',
    'DOM': 'Dominican Republic',
    'PER': 'Peru',
    'POL': 'Poland',
    'AUT': 'Austria'
}

#update the country names
def change_country_names(df, country_map):

    df['team_one_nationality'] = df['team_one_nationality'].map(country_map)
    df['team_two_nationality'] = df['team_two_nationality'].map(country_map)

    return df

#function to determine if the teams have the same nationality as country of play and
# produce a 0 or 1 in new columns to determine the winner
def check_home_country(df):
    #They play in their home country
    df['team_one_home'] = (
        df['team_one_nationality'] ==
        df['country']
    ).astype(int) #convert the boolean to integer 1 for win, 0 for los

    df['team_two_home'] = (
        df['team_two_nationality'] ==
        df['country']
    ).astype(int) #convert the boolean to integer  1 for win, 0 for los

    return df

#take away matches with no home teams to remove skew.(DOUBLE CHECK AGAIN)
def keep_matches_with_home_team(df):
    """
    matches
    where at least one team is playing at home.
    
    Assumes:
        - df['team_one_home'] is 1 if team 1 is home, else 0
        - df['team_two_home'] is 1 if team 2 is home, else 0
    """
    hide = (df['team_one_home'] == 1) | (df['team_two_home'] == 1)
    return df[hide].copy()


#Analysis 1 - Win rates and chi-square test
#win rates of home plays
def home_win_rates(df):
    team1_home_wins = ((df['team_one_home'] == 1) & (df['winner'] == 1)).sum()
    team2_home_wins = ((df['team_two_home'] == 1) & (df['winner'] == 2)).sum()
    #how many games are the home teams winning in general
    home_wins = team1_home_wins + team2_home_wins

    
    team1_home_total = (df['team_one_home'] == 1).sum()
    team2_home_total = (df['team_two_home'] == 1).sum()
    #how many teams are playing in their home countries
    home_total = team1_home_total + team2_home_total

    #home win rate
    home_win_rate = (home_wins / home_total)*100
    result = print(f"Home win rate: {home_win_rate:.2f}%")

    return result

#win rates of away plays
def away_win_rates(df):
    team1_away_wins = ((df['team_one_home'] == 0) & (df['winner'] == 1)).sum()
    team2_away_wins = ((df['team_two_home'] == 0) & (df['winner'] == 2)).sum()
     #how many games are the away teams winning in general
    away_wins = team1_away_wins + team2_away_wins

    team1_away_total = (df['team_one_home'] == 0).sum()
    team2_away_total = (df['team_two_home'] == 0).sum()
     #how many teams are playing in an away countries
    away_total = team1_away_total + team2_away_total

    #away win rate
    away_win_rate = (away_wins / away_total)*100

    result = print(f"Away win rate: {away_win_rate:.2f}%")
    return result


#Chi-square test for significance

def chi_square_home_away_test(df):
    # Home wins and losses
    home_wins = (
        ((df['team_one_home'] == 1) & (df['winner'] == 1)).sum() +
        ((df['team_two_home'] == 1) & (df['winner'] == 2)).sum()
    )
    home_total = (df['team_one_home'] == 1).sum() + (df['team_two_home'] == 1).sum()
    #print(home_total)
    home_losses = home_total - home_wins

    # Away wins and losses
    away_wins = (
        ((df['team_one_home'] == 0) & (df['winner'] == 1)).sum() +
        ((df['team_two_home'] == 0) & (df['winner'] == 2)).sum()
    )
    away_total = (df['team_one_home'] == 0).sum() + (df['team_two_home'] == 0).sum()
    #print(away_total)
    away_losses = away_total - away_wins

    # Contingency table
    contingency = pd.DataFrame({
        'Win': [home_wins, away_wins],
        'Loss': [home_losses, away_losses]
    }, index=['Home', 'Away'])

    # Chi-square test
    chi2, p, dof, expected = chi2_contingency(contingency)

    # Print the information inside function
    print("\n\nChi-Square Test for Home vs Away Win Rates\n")
    print("Relationship Between Home and Away:")
    print(contingency)
    print("\nChi-square value:", round(chi2, 2))
    print("Degrees of freedom:", dof)
    print(f"p-value:, {p:.2e}")
    print("\nExpected frequencies if there was no relationship:")
    print(pd.DataFrame(expected, index=['Home', 'Away'], columns=['Win', 'Loss'])
          .round(2))
    
    #Side by Side Bar plot
    contingency.plot(kind='bar', figsize=(10,8))

    plt.title('Wins and Losses: Home vs Away Teams')
    plt.ylabel('Number of Matches')
    plt.xticks(rotation=0)


    # Add labels above bars
    for i, (idx, row) in enumerate(contingency.iterrows()):
        plt.text(i - 0.15, row['Win'] + 10, str(row['Win']), color='blue')
        plt.text(i + 0.05, row['Loss'] + 10, str(row['Loss']), color='orange')

    # Compute win rates inside the plot
    home_win_rate = (contingency.loc['Home', 'Win'] /
                    contingency.loc['Home'].sum()) * 100

    away_win_rate = (contingency.loc['Away', 'Win'] /
                    contingency.loc['Away'].sum()) * 100

    # Add text inside the square plot
    plt.text(
        0.02, 0.95,   # X, Y position (0–1 axis coordinates)
        f"Home win rate: {home_win_rate:.2f}%\nAway win rate: {away_win_rate:.2f}%",
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='black')
    )

    plt.tight_layout()
    plt.show() 
    #end of plot

    # Still return values in case you need them later
    return contingency, chi2, p, expected

    

#Analysis 2 - Point differential
#difference in total points scored by both teams
def point_differential_average(df):
    #point differential for team 1, both away and home
    df['team_one_point_diff'] = df['team_one_total_points'] - df['team_two_total_points']
    # Team 1: home vs away
    team1_home_points = df.loc[df['team_one_home'] == 1, 'team_one_point_diff']
    team1_away_points = df.loc[df['team_one_home'] == 0, 'team_one_point_diff']

    #point differential for team 2, away and home
    df['team_two_point_diff'] = df['team_two_total_points'] - df['team_one_total_points']
    # Team 2: home vs away
    team2_home_points = df.loc[df['team_two_home'] == 1, 'team_two_point_diff']
    team2_away_points = df.loc[df['team_two_home'] == 0, 'team_two_point_diff']

    #combination of the home and away differentials
    home_point_diff = pd.concat([team1_home_points, team2_home_points], ignore_index=True)
    away_point_diff = pd.concat([team1_away_points, team2_away_points], ignore_index=True)

    average_home_point_diff = print(f"\nAverage home point differential: {home_point_diff.mean():.2f}%")
    average_away_point_diff = print(f"Average away point differential: {away_point_diff.mean():.2f}%")
    #its not ok to not return anything as when return is taken away, the function breaks.

    #check the variance to determine the type of T- test to use
    home_var = home_point_diff.var()
    away_var = away_point_diff.var()

    #Print the resunlt of the variance 
    print(f"Home variance: {home_var:.2f}")
    print(f"Away variance: {away_var:.2f}")

    #Two sample T-test significance for the point difference (Welches test as the variances are not the equal)
    t_stat, p_value = ttest_ind(home_point_diff, away_point_diff, equal_var=False)
    print(f"T-statistic: {t_stat:.2f}")
    print(f"P-value: {p_value:.2e}") 

    
    return average_home_point_diff, average_away_point_diff, t_stat, p_value


#Analysis 3
#Tournament importance, Table with% of wins by home teams and away teams
def winner_tournament(df):
    # Team 1 winners
    team1 = df[df['winner'] == 1][['tournament_type', 'team_one_home']]
    team1 = team1.rename(columns={'team_one_home': 'home'})
    
    # Team 2 winners
    team2 = df[df['winner'] == 2][['tournament_type', 'team_two_home']]
    team2 = team2.rename(columns={'team_two_home': 'home'})
    
    # Combine winners
    winners = pd.concat([team1, team2], ignore_index=True)
    #the percentage
    win_percentages = winners.groupby("tournament_type")["home"].mean() * 100
    
    #print the sumary table 
    summary = pd.DataFrame({
    'Home Win %': win_percentages,
    'Away Win %': 100 - win_percentages
    })
    print(summary.round(2))
    #return the new table of home and away winners and the win percentages
    return winners, win_percentages

#build a table to show the nationality and winners of home and away games
def team_nationality_table(df):
    # Team 1 rows
    team1 = pd.DataFrame({
        'nationality': df['team_one_nationality'],
        'home': df['team_one_home'],
        'won': (df['winner'] == 1).astype(int)
    })

    # Team 2 rows
    team2 = pd.DataFrame({
        'nationality': df['team_two_nationality'],
        'home': df['team_two_home'],
        'won': (df['winner'] == 2).astype(int)
    })

    team_df = pd.concat([team1, team2], ignore_index=True)
    return team_df

#ANALYSIS 4
#Win rates per nationality using the table, checking home advantage depending on if they win at home or away
def nationality_home_advantage(df):
    team_df = team_nationality_table(df)

    # Group by nationality
    results = team_df.groupby('nationality').apply(
        lambda x: pd.Series({ #use series to hold data of int types.
            "Home_matches %": (x['home'] == 1).sum(),
            "Away_matches %": (x['home'] == 0).sum(),
            "Home_win_rate %": x.loc[x['home'] == 1, 'won'].mean()* 100,
            "Away_win_rate %": x.loc[x['home'] == 0, 'won'].mean()* 100
        })
    )

    #rounding up only the percentages for a cleaner table
    

    return (results.round(2))

#to determine, top n host countries
def top_host_countries(df, top_n=None):
    """
    Returns the most frequent tournament host countries in the dataset.
    Returns:
        pandas Series sorted by highest frequency
    """

    country_counts = df['country'].value_counts()

    if top_n:
        country_counts = country_counts.head(top_n)

    total_tournaments = len(df)
    percent = (country_counts.sum() / total_tournaments) * 100
    
    print("\nTop Countries by Tournament Frequency:")
    print(country_counts)
    print(f"These {top_n} countries are responsible for {percent:.2f}% of women's tournaments played from 2018 to 2022")

    return country_counts



#visualizing the top 5 countries
def plot_top5_countries(df):
    # Count how many matches each country hosted
    country_counts = df['country'].value_counts()

    # Select the top 5
    top5 = country_counts.head(5)

    # Pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(
        top5,
        labels=top5.index,
        autopct='%1.1f%%',
        startangle=140,
        wedgeprops={'edgecolor': 'black'}
    )

    plt.title("Top 5 Countries Hosting the Most Matches (2018–2021)")
    plt.tight_layout()
    plt.show()
