import streamlit as st
import pandas as pd
import os
import requests
import base64

def load_view():
    path = os.getcwd()
    st.write(
        """
        <style>
        .stApp {
            margin-top: -120px;
        }
        </style>
        """,unsafe_allow_html=True
    )

    # Define a dictionary of players and their corresponding teams
    pitchers = pd.read_csv(f"{path}/data/pitchers.csv", index_col=0)

    hitters = pd.read_csv(f"{path}/data/hitters.csv", index_col=0)

    # Get a list of unique team names
    unique_teams = sorted(list(pitchers.team_nickname.unique()))
    st.markdown(f"<h5 style='text-align:center'>MLB At Bat Predictor - Beat the Line</h5>", unsafe_allow_html=True)

    columns = st.columns(2)

    pitching_team = columns[0].selectbox("Select Pitching Team", unique_teams)


    # Get a list of players from the selected pitching team
    if pitching_team:
        pitching_team_players = pitchers[pitchers.team_nickname == pitching_team]["full_name"].sort_values()
    else:
        pitching_team_players = []


    # Dropdown to select the pitcher from the pitching team
    pitcher = columns[0].selectbox("Select Pitcher", pitching_team_players)


    # Dropdown to select the hitting team
    hitting_team = columns[1].selectbox("Select Hitting Team", unique_teams)


    # Get a list of players from the selected hitting team
    if hitting_team:
        hitting_team_players = hitters[hitters.team_nickname == hitting_team]["full_name"].sort_values()
    else:
        hitting_team_players = []


    # Dropdown to select the hitter from the hitting team
    hitter = columns[1].selectbox("Select Hitter", hitting_team_players)


    # Display the selected teams and players
    text_vs = f"{pitcher} ({pitchers[(pitchers.full_name == pitcher) & (pitchers.team_nickname == pitching_team)].primary_position.iloc[0]} / \
            {pitching_team}) VS {hitter} ({hitters[(hitters.full_name == hitter) & (hitters.team_nickname == hitting_team)].primary_position.iloc[0]} / \
            {hitting_team})"
    st.write(f"<div style='text-align:center'><strong><span style='font-size:16px'>{text_vs}</span></strong></div>", unsafe_allow_html=True)


    # Pitcher stats
    columns = st.columns(2)

    pitcher_stats = pitchers[(pitchers.full_name == pitcher) & (pitchers.team_nickname == pitching_team)]
    pitcher_stats = pitcher_stats[['pitcher_ab_count', 'pitcher_hand', 'pitcher_previous_stats_szn']]

    pitcher_stats['pitcher_ab_count'] = int(pitcher_stats['pitcher_ab_count'])

    pitcher_stats['pitcher_previous_stats_szn'] = round(pitcher_stats['pitcher_previous_stats_szn'],3)

    pitcher_stats = pitcher_stats.rename(columns={'pitcher_ab_count': '2023 Batters Faced',
                                'pitcher_hand': 'Pitching Hand',
                                'pitcher_previous_stats_szn': 'Season Opp OBP'
                                })

    pitcher_stats = pitcher_stats.assign(hack='').set_index('hack').T


    columns[0].dataframe(pitcher_stats, width=1000)


    # Hitter stats
    hitter_stats = hitters[(hitters.full_name == hitter) & (hitters.team_nickname == hitting_team)]

    hitter_stats = hitter_stats[['hitter_ab_count', 'hitter_hand', 'hitter_previous_stats_szn']]

    hitter_stats['hitter_ab_count'] = int(hitter_stats['hitter_ab_count'])

    hitter_stats['hitter_previous_stats_szn'] = round(hitter_stats['hitter_previous_stats_szn'],3)

    hitter_stats = hitter_stats.rename(columns={'hitter_ab_count': '2023 At Bats',
                                'hitter_hand': 'Batter Hand',
                                'hitter_previous_stats_szn': 'Season OBP'})



    hitter_stats = hitter_stats.assign(hack='').set_index('hack').T

    # columns[1].write(hitter_stats)
    columns[1].dataframe(hitter_stats, width=1000)

    # API
    params = {
        "pitcher_name": pitcher,
        "hitter_name": hitter
    }

    line = st.slider('Select the current odds. Assumes positive odds (e.g. +100 or better)', 100, 300, 100)


    implied_proba = 100 / (100 + line) * 100

    st.write(f"<div style='text-align:left'><span style='font-size:14px'>Implied betting probability: <b>{round(implied_proba,1)}%</b></span></div>", unsafe_allow_html=True)

    if st.button("Predict"):

        mbl_api_url = 'https://mlb1315-ovcniiq53a-ew.a.run.app/predict'  # Replace with your API endpoint

        try:
            response = requests.get(mbl_api_url, params=params)
            response.raise_for_status()  # Raise an exception if the request is not successful

            prediction = response.json()

            pred = prediction.get('prediction')  # Use .get() to avoid KeyError if 'prediction' is missing
            proba = prediction.get('probability') # Use .get() to avoid KeyError if 'probability' is missing

            if proba > implied_proba:
                text = (f"Winner is...the batter, <b>{hitter}</b>! With <b>{round(proba,2)}</b>% probability, the line odds are beat")
                st.write(f"<div style='text-align:center'><span style='font-size:26px'>{text}</span></div>", unsafe_allow_html=True)

            elif proba <= implied_proba:
                text = (f"Winner is...the pitcher, <b>{pitcher}</b>! With <b>{round(proba,2)}</b>% probability, <b>{hitter}</b> does not beat the line odds")
                st.write(f"<div style='text-align:center'><span style='font-size:26px'>{text}</span></div>", unsafe_allow_html=True)
            else:
                st.warning(f"Unexpected prediction value: {pred}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while making the API request: {str(e)}")
        except KeyError:
            st.error("The API response is missing the 'prediction' key.")
