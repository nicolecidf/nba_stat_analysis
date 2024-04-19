import pandas as pd
import plotly.express as px
import plotly.graph_objects as graph
pd.set_option('display.max_columns', None)

data = pd.read_excel('nba_player_data.xlsx')


# CORRELATING PLAYER STATS

# Removing the 'Rank' and 'Eficiency' column as it is not needed
data.drop(columns=['RANK', 'EFF'], inplace=True)

# Adding a Season Start columnn
data['Season Start Year'] = data['Year'].str[:4].astype(int)

# Changing New Orleans Hornets to New Orleans Pelicans as the name was changed in the 2013-14 season and replacing Regular Season name
data['TEAM'].replace(to_replace=['NOH'], value='NOP', inplace=True)
data['Season_Type'].replace('Regular%20Season', 'Regular_Season', inplace=True)

# Filtering between Regular Season and Playoffs Data
regular_season_df = data[data['Season_Type'] == 'Regular_Season']
playoffs_df = data[data['Season_Type'] == 'Playoffs']

# Creating a list for all columns that include Total sums
totals = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
          'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

# Grouping by player and player_id and year to get a per minute analysis
data_per_min = data.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[
    totals].sum().reset_index()

for col in data_per_min.columns[4:]:
    data_per_min[col] = data_per_min[col]/data_per_min['MIN']

# Ratios:
# Shooting percenttages
data_per_min['FG%'] = data_per_min['FGM']/data_per_min['FGA']
data_per_min['3PT%'] = data_per_min['FG3M']/data_per_min['FG3A']
data_per_min['FT%'] = data_per_min['FTM']/data_per_min['FTA']
# Percentage of attempts that where 3-pointers
data_per_min['FG3A%'] = data_per_min['FG3A']/data_per_min['FGA']
# average point per attempt, it is a measure of shooting efficiency
data_per_min['PTS/FGA'] = data_per_min['PTS']/data_per_min['FGA']
# percentage of field goal mix that come from behing the arch
data_per_min['FG3M/FGM'] = data_per_min['FG3M']/data_per_min['FGM']
# free through rate
data_per_min['FTA/FGA'] = data_per_min['FTA']/data_per_min['FGA']
# true shooting rate. Gives more weight to 3-pointers
data_per_min['TRU%'] = 0.5*data_per_min['PTS'] / \
    (data_per_min['FGA']+0.475*data_per_min['FTA'])
# turn over ratio
data_per_min['AST_TOV'] = data_per_min['AST']/data_per_min['TOV']

# excluding players that barely played so ratios are more accurate
data_per_min = data_per_min[data_per_min['MIN'] >= 50]
data_per_min.drop(columns='PLAYER_ID', inplace=True)
numeric_data = data_per_min.select_dtypes(include=['float64', 'int64'])

# plotting using a heat map
fig = px.imshow(numeric_data.corr(method='pearson'))
fig.show()


# DISTRIBUTION OF MINUTES PLAYED

# comparing playoffs and regular season, all in percentages as data sets are of different sizes
# you can change the def below to check for other distributions, like points distribution, for example.
def hist_data(df=regular_season_df, min_MIN=0, min_GP=0):
    return df.loc[(df['MIN'] >= min_MIN) & (df['GP'] >= min_GP), 'MIN'] / df.loc[(df['MIN'] >= min_MIN) & (df['GP'] >= min_GP), 'GP']


fig = graph.Figure()
fig.add_trace(graph.Histogram(
    x=hist_data(regular_season_df, 50, 5), histnorm='percent', name="Regular_Season", xbins={'start': 0, 'end': 46, 'size': 1}))
fig.add_trace(graph.Histogram(
    x=hist_data(playoffs_df, 5, 1), histnorm='percent', name="Playoffs", xbins={'start': 0, 'end': 46, 'size': 1}))

fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.5)
fig.show()

# finding the Mean of minutes played for the middle part of the distribution
mean_mins_played_regular_season = ((hist_data(regular_season_df, 5, 1) >= 12) & (
    hist_data(regular_season_df, 5, 1) <= 34)).mean()
mean_mins_played_playoffs = ((hist_data(playoffs_df, 5, 1) >= 12) & (
    hist_data(playoffs_df, 5, 1) <= 34)).mean()
print(f'Mean Minutes Played in the Regular Season: {
      mean_mins_played_regular_season}')
print(f'Mean Minutes Played in the Playoffs: {mean_mins_played_playoffs}')
