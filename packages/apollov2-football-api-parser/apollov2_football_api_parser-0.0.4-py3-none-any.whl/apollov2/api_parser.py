import requests
import pandas as pd
import concurrent.futures
from tqdm import tqdm
import math


class APIParser:
    def __init__(self, api_key, league_id):
        self.league_id = league_id
        self.api_key = api_key
        self.session = requests.Session()
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.season_list = [str(i)
                            for i in self.get_all_seasons()['year'].to_list()]
        self.figure_list = self.get_all_fixtures_info().fixture_id.to_list()
        self.country_list = self.get_all_countries().name.unique().tolist()

    def replace_period(self, df):
        df.columns = df.columns.str.replace('.', '_', regex=False)
        return(df)

    def get_response_df(self, url, querystring=None, iter_list=None):
        """ This is a general method to get single response"""
        if querystring is None and iter_list is None:
            response = requests.get(url, headers=self.headers)
        else:
            response = requests.get(
                url, headers=self.headers, params=querystring)

        response_dic = response.json()['response']
        df_response = pd.json_normalize(response_dic)
        return df_response

    def json_decomposer(self, df, left_cols, right_cols):
        frames = []
        data_range = range(len(df))

        # Conditionally display progress bar
        if right_cols not in ['transfers', 'career']:
            data_range = tqdm(data_range)

        for i in data_range:
            left = df.iloc[[i]][left_cols].reset_index(drop='index')
            # Check if it's not an empty list and it's a list of dictionaries
            if df[right_cols][i] and (isinstance(df[right_cols][i], list) and all(isinstance(x, dict) for x in df[right_cols][i])):
                right = pd.json_normalize(df[right_cols][i])
                for _ in range(len(right) - 1):
                    left = pd.concat([left, left.loc[[0]]], ignore_index=True)
                df_combined = pd.concat([left, right], axis=1)
                frames.append(df_combined)

        if frames:
            df_final = pd.concat(frames).reset_index(drop=True)
            df_final.columns = df_final.columns.str.replace(
                '.', '_', regex=False)
            return df_final
        else:
            print("No data to decompose")
            return None

    def get_all_countries(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/countries"
        response = requests.get(url, headers=self.headers)
        response_dic = response.json()['response']
        get_all_countries = pd.json_normalize(response_dic)
        return get_all_countries

    def get_all_venues(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/venues"
        frames = []
        for i in self.country_list:
            querystring = {"country": i}
            df_temp = self.get_response_df(url=url, querystring=querystring)
            frames.append(df_temp)
        df_all_venues = pd.concat(frames).reset_index(drop=True)
        return df_all_venues

    def get_all_seasons(self):
        """get all seasons for a league"""
        url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
        querystring = {"id": self.league_id}
        df_seasons = self.get_response_df(url=url, querystring=querystring)

        frames = []
        for _, row in df_seasons.iterrows():
            # Access the list of dictionaries in 'seasons' column
            list_of_season_dicts = row['seasons']
            # Convert the list of dictionaries to a DataFrame
            df_season = pd.json_normalize(list_of_season_dicts)
            # Copy other columns from the row to the new DataFrame
            for col in df_seasons.columns:
                if col != 'seasons':
                    df_season[col] = row[col]
            # Append the new DataFrame to the list
            frames.append(df_season)
        df_all_seasons = pd.concat(frames).reset_index(drop=True)
        df_all_seasons = self.replace_period(df_all_seasons)
        return df_all_seasons

    def get_all_teams(self):
        frames = []
        url = "https://api-football-v1.p.rapidapi.com/v3/teams"
        total_seasons = len(self.season_list)

        # Create a progress bar
        progress_bar = tqdm(total=total_seasons,
                            desc="Fetching teams", unit="season")

        for i in self.season_list:
            querystring = {"league": self.league_id, "season": i}
            df_temp = self.get_response_df(url=url, querystring=querystring)
            df_temp.insert(0, 'season', int(i))
            df_temp.insert(0, 'league_id', self.league_id)
            frames.append(df_temp)

            # Update the progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()

        df_teams_info = pd.concat(frames).reset_index(drop=True)
        df_teams_info = self.replace_period(df_teams_info)

        return df_teams_info

    def get_all_fixtures_info(self):
        frames = []
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        for i in self.season_list:
            querystring = {"league": self.league_id, "season": i}
            df_temp = self.get_response_df(url=url, querystring=querystring)
            df_temp.insert(0, 'season', int(i))
            df_temp.insert(0, 'league_id', self.league_id)
            frames.append(df_temp)

        df_fixtures_info = pd.concat(frames).reset_index(drop=True)
        df_fixtures_info = self.replace_period(df_fixtures_info)

        return df_fixtures_info

    def get_df_stats_raw(self):
        breakdown_list = ['-'.join(map(str, self.figure_list[i:i+20]))
                          for i in range(0, len(self.figure_list), 20)]
        df_stats = pd.DataFrame()

        def process_fixtures(fixtures):
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            querystring = {"ids": fixtures}
            response = self.session.get(
                url, headers=self.headers, params=querystring)
            response_dic = response.json()['response']
            df_temp = pd.json_normalize(response_dic)
            df_temp.columns = df_temp.columns.str.replace(
                '.', '_', regex=False)
            return df_temp[['fixture_id', 'fixture_date', 'events', 'lineups', 'statistics', 'players']]

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_fixtures, fixtures)
                       for fixtures in breakdown_list]

            # Create a progress bar
            progress_bar = tqdm(total=len(futures),
                                desc="Processing raw fixtures")

            for future in concurrent.futures.as_completed(futures):
                df_temp = future.result()
                df_stats = pd.concat([df_stats, df_temp], ignore_index=True)

                # Update the progress bar
                progress_bar.update(1)

        progress_bar.close()

        return df_stats

    def get_all_lineups_general_stats(self):
        df_stats = self.get_df_stats_raw()
        all_lineups_raw_stats = self.json_decomposer(
            df_stats, ['fixture_id', 'fixture_date'], 'lineups')
        all_lineups_general_stats = all_lineups_raw_stats[[
            i for i in all_lineups_raw_stats.columns if i not in ['startXI', 'substitutes']]]
        return all_lineups_general_stats

    def all_lineups_start_stats(self):
        lineups_frames = []
        df_stats = self.get_df_stats_raw()
        df_lineups = self.json_decomposer(
            df_stats, ['fixture_id', 'fixture_date'], 'lineups')
        lineups_frames.append(df_lineups)
        all_lineups_raw_stats = pd.concat(
            lineups_frames).reset_index(drop=True)
        l = ['fixture_id', 'fixture_date', 'formation', 'team_id', 'team_name']
        r = 'startXI'
        all_lineups_start_stats = self.json_decomposer(
            all_lineups_raw_stats, l, r)
        return all_lineups_start_stats

    def all_lineups_substitutes_stats(self):
        lineups_frames = []
        df_stats = self.get_df_stats_raw()
        df_lineups = self.json_decomposer(
            df_stats, ['fixture_id', 'fixture_date'], 'lineups')
        all_lineups_general_stats = self.get_all_lineups_general_stats()
        lineups_frames.append(df_lineups)
        all_lineups_raw_stats = pd.concat(
            lineups_frames).reset_index(drop=True)
        l = ['fixture_id', 'fixture_date', 'formation', 'team_id', 'team_name']
        r = 'substitutes'
        all_lineups_substitutes_stats = self.json_decomposer(
            all_lineups_raw_stats, l, r)
        return all_lineups_substitutes_stats

    def get_all_injuries(self):
        frames = []
        url = "https://api-football-v1.p.rapidapi.com/v3/injuries"
        total_seasons = len(self.season_list)

        # Create a progress bar
        progress_bar = tqdm(total=total_seasons,
                            desc="Fetching injuries", unit="season")

        for i in self.season_list:
            querystring = {"league": self.league_id, "season": i}

            # Send the request
            response = requests.get(
                url, headers=self.headers, params=querystring)
            df_temp = self.replace_period(
                pd.json_normalize(response.json()['response']))
            df_temp.insert(0, 'season', int(i))
            frames.append(df_temp)

            # Update the progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()

        df_injuries = pd.concat(frames).reset_index(drop=True)

        return df_injuries

    def get_all_transfers(self, players_list):
        ''' df_all_players = parser.get_all_players()
            players_list = df_all_players['id'].unique().tolist()'''
        frames = []
        # Create a progress bar
        progress_bar = tqdm(players_list, desc="Processing players")

        for player_id in progress_bar:
            url = "https://api-football-v1.p.rapidapi.com/v3/transfers"
            querystring = {"player": str(player_id)}

            # Send the request
            response = requests.get(
                url, headers=self.headers, params=querystring)
            response_dic = response.json()['response']
            df_temp = self.replace_period(pd.json_normalize(response_dic))
            df_temp1 = self.json_decomposer(
                df_temp, ['player_id', 'player_name'], 'transfers')
            if df_temp1 is not None:
                frames.append(df_temp1)

        progress_bar.close()

        # Concatenate all the frames
        if frames:
            df_transfers = pd.concat(frames).reset_index(drop=True)
        else:
            print("No data to concatenate")

        return df_transfers

    def get_all_players(self):
        def fetch_player_data(season, page_number):
            params = {"league": self.league_id,
                      "season": season, "page": str(page_number)}
            response = self.session.get(
                'https://api-football-v1.p.rapidapi.com/v3/players', params=params)
            return pd.DataFrame(response.json()['response']) if response.status_code == 200 else None

        self.session = requests.Session()
        self.session.headers.update({
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        })
        player_frames = []
        for season in self.season_list:
            params = {"league": self.league_id, "season": season, "page": "1"}
            total_pages = self.session.get(
                'https://api-football-v1.p.rapidapi.com/v3/players', params=params).json()['paging']['total']

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                fetch_job = [executor.submit(
                    fetch_player_data, season, i) for i in range(1, total_pages + 1)]
                data_frames = [f.result() for f in tqdm(concurrent.futures.as_completed(
                    fetch_job), total=total_pages, desc=f"Processing season {season}")]
                data_frames = [df for df in data_frames if df is not None]

            if data_frames:
                df_all_players = pd.concat(data_frames).reset_index(drop=True)
                frames = [pd.concat([pd.json_normalize(df_all_players['player'].iloc[i]), pd.json_normalize(
                    df_all_players['statistics'].iloc[i])], axis=1) for i in range(len(df_all_players))]
                df_all_players_xxxx = pd.concat(frames).reset_index(drop=True)
                df_all_players_xxxx.columns = df_all_players_xxxx.columns.str.replace(
                    '.', '_', regex=False)
                df_all_players_xxxx.insert(0, 'season', int(season))
                player_frames.append(df_all_players_xxxx)

        final_df = pd.concat(player_frames).reset_index(drop=True)

        # Drop rows with null 'id' values and convert 'id' column to string
        final_df = final_df.dropna(subset=['id'])
        final_df['id'] = final_df['id'].values.astype(int).astype(str)

        return final_df

    def get_all_sidelined(self, players_list):
        frames = []
        session = requests.Session()
        session.headers.update({
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        })

        for i in tqdm(players_list, desc="Processing players"):
            try:
                response = session.get(
                    "https://api-football-v1.p.rapidapi.com/v3/sidelined", params={"player": str(i)})
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(f"HTTP error occurred for player_id: {i} - {err}")
            else:
                response_dic = response.json()['response']
                df_temp = pd.json_normalize(response_dic)
                df_temp.insert(0, 'player_id', str(i))
                frames.append(df_temp)

        if frames:
            df_sidelined = pd.concat(frames).reset_index(drop=True)
        else:
            print("No data to concatenate")
        return df_sidelined

    def get_all_coaches(self, coach_list, max_workers=3):
        '''here is how to get coach_list:
           lineups = parser.get_all_lineups_general_stats()
           coach_list = [str(int(i)) for i in lineups.coach_id.unique().tolist() if not math.isnan(i)]
        '''
        def fetch_data(i):
            df_temp = self.get_response_df(
                url="https://api-football-v1.p.rapidapi.com/v3/coachs", querystring={"id": str(i)})
            df_temp1 = self.json_decomposer(
                df_temp, [i for i in df_temp.columns if i != 'career'], 'career')
            return df_temp1
        frames = []
        # Adjust max_workers as necessary
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            df_coach = {executor.submit(fetch_data, i): i for i in coach_list}
            for future in tqdm(concurrent.futures.as_completed(df_coach), total=len(coach_list), desc="Processing coaches"):
                df_temp = future.result()
                if df_temp is not None:
                    frames.append(df_temp)
        if frames:
            df_coaches = pd.concat(frames).reset_index(drop=True)
        else:
            print("No data to concatenate")

        columns_to_rename = {'team_id': 'career_team_id',
                             'team_name': 'career_team_name', 'team_logo': 'career_team_logo'}
        df_r = df_coaches.iloc[:, -3:].rename(columns=columns_to_rename)
        df_l = df_coaches.iloc[:, :-3]
        df_coaches = pd.concat([df_l, df_r], axis=1)
        df_coaches['career_team_id'] = df_coaches['career_team_id'].values.astype(
            int).astype(str)
        return df_coaches
