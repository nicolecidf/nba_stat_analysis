import numpy as np
import time
import pandas as pd
import requests
pd.set_option('display.max_columns', None)

# we define the headers from the api
headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive', 'Host': 'stats.nba.com', 'Origin': 'https://www.nba.com', 'Referer': 'https://www.nba.com/',
           'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'
           }

# we are defining our variable with the initial api url for the 2012 season
raw_api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2011-12&SeasonType=Regular%20Season&StatCategory=PTS'
r = requests.get(url=raw_api_url, headers=headers).json()
df_cols_short = r['resultSet']['headers']


# the dataframe columns and the data frame are devided below, including the variables for all they years we will be analyzing
df_cols = ['Year', 'Season_Type'] + df_cols_short


season_types = ['Regular%20Season', 'Playoffs']
years = ['2012-13', '2013-14', '2014-15', '2015-16', '2016-17',
         '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']

df = pd.DataFrame(columns=df_cols)

initial_run_time = time.time()


# the for loop that will get all the data and then save it in the data frame df
for y in years:
    for s in season_types:
        api_url = f'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=' + \
            y+'&SeasonType='+s+'&StatCategory=PTS'
        print(api_url)
        r = requests.get(url=api_url, headers=headers).json()
        df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=df_cols_short)
        df2 = pd.DataFrame({'Year': [y for i in range(len(df1))], 'Season_Type': [
                           s for i in range(len(df1))]})
        df3 = pd.concat([df2, df1], axis=1)
        df = pd.concat([df, df3], axis=0)
        print(f'Finished scraping data for the {y} {s}.')
        # adding a lag time to improve the data gathering process.
        lag = np.random.uniform(low=5, high=40)
        print(f'...waiting {round(lag, 1)} seconds')
        time.sleep(lag)
print(f'Process completed! Total run time: {
      round((time.time() - initial_run_time)/60, 2)}')

df.to_excel('nba_player_data.xlsx', index=False)
