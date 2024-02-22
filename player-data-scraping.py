from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

all_teams = []

url = 'https://fbref.com/en/comps/12/La-Liga-Stats'

response = requests.get(url)  # http get request to url to retrieve web contents

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        table = soup.find_all('table', class_='stats_table')[0] # first table with links/stats of entire league

        # extracts links to specific team info
        links = table.find_all('a')
        links = [l.get("href") for l in links]
        links = [l for l in links if "/squads" in l]
        
        team_urls = [f"https://fbref.com{l}" for l in links]  # complete url for each team's stats page

        for team_url in team_urls:
            print(f"Processing team URL: {team_url}")

            team_name = team_url.split("/")[-1].replace("-Stars", "")  # extracts team name
            data = requests.get(team_url).text  # html get request to team's detailed stats page            
            soup = BeautifulSoup(data, "lxml")
            
            stats = soup.find_all("table", class_="stats_table")[0]  # find table with team stats

            if stats and hasattr(stats, 'columns') and stats.columns:
                stats.columns = stats.columns.droplevel()

            # read html table to pd df
            team_data = pd.read_html(str(stats))[0]
            team_data["Team"] = team_name
            all_teams.append(team_data)
            
            time.sleep(5)  # prevents overloading server

        # prevents issues if no data is scraped and concats teams data to single df
        if all_teams:
            stat_df = pd.concat(all_teams, ignore_index=True)
            stat_df.to_csv("stat.csv", index=False, encoding='utf-8')
            print('Data retrieval and CSV export successful')
            import pandas as pd

    except Exception as e:
        print('Error:', e)
else:
    print('Failed to retrieve the webpage. Status Code:', response.status_code)
