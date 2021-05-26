import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_daily_lineups():
    lineup_url = 'https://rotogrinders.com/lineups/nba?site=draftkings'
    soup_summaries = BeautifulSoup(urlopen(lineup_url), 'lxml')
    date = soup_summaries.find('li', class_='date-content').get_text().strip('th') + ' ' + str(datetime.now().year)
    date = datetime.strptime(date, '%A, %B %d %Y').strftime('%Y%m%d')
    games = soup_summaries.find_all('ul', class_='lst lineup')
    lineup_cards = games[0].find_all('li', {'data-role': 'lineup-card'})
    lineup_list = []
    for lc in lineup_cards:
        lineup_dict = {'Name': [],
                       'Pos': [],
                       'Salary': [],
                       'Starter': [],
                       'Home': []}

        away_team = lc.find('div', class_='blk away-team')
        away_players = away_team.find_all('li', class_='player')

        for count, player in enumerate(away_players):
            name = player.find('span', class_='pname').get_text().strip('\n')
            position = player.find('span', class_='position').get_text().strip().strip('\n')
            salary = player.find('span', class_='salary').get_text().strip().strip('\n').strip('$')
            if salary != '':
                salary = float(salary.strip('K')) * 1000
            else:
                salary = 0
            starter = 0
            if count < 5:
                starter = 1
            home = 0

            lineup_dict['Name'].append(name)
            lineup_dict['Pos'].append(position)
            lineup_dict['Salary'].append(salary)
            lineup_dict['Starter'].append(starter)
            lineup_dict['Home'].append(home)

        home_team = lc.find('div', class_='blk home-team')
        home_players = home_team.find_all('li', class_='player')

        for count, player in enumerate(home_players):
            name = player.find('span', class_='pname').get_text().strip('\n')
            position = player.find('span', class_='position').get_text().strip().strip('\n')
            salary = player.find('span', class_='salary').get_text().strip().strip('\n').strip('$')
            if salary != '':
                salary = float(salary.strip('K')) * 1000
            else:
                salary = 0
            starter = 0
            if count < 5:
                starter = 1
            home = 1

            lineup_dict['Name'].append(name)
            lineup_dict['Pos'].append(position)
            lineup_dict['Salary'].append(salary)
            lineup_dict['Starter'].append(starter)
            lineup_dict['Home'].append(home)

        df_lineup = pd.DataFrame.from_dict(lineup_dict)
        lineup_list.append(df_lineup)

    all_lineups = pd.concat(lineup_list)
    # add Date
    all_lineups['Date'] = date

    return all_lineups

if __name__ == "__main__":
    daily_lineups = get_daily_lineups()