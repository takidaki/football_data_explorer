import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    file_path = "Streamlit Full Database.csv"  # Update if needed
    df = pd.read_csv(file_path, delimiter=";")
    
    # Convert odds columns from comma to dot format
    for col in ['Home Win', 'Draw', 'Away Win']:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    # Add First Half Goals Column
    df["First Half Goals"] = df["Home Goals FH"] + df["Away Goals FH"]
    # Determine the winner of each match
    df["Winner"] = np.where(df["Home Goals"] > df["Away Goals"], df["Home Team"], 
                    np.where(df["Home Goals"] < df["Away Goals"], df["Away Team"], "Draw"))
    return df



df = load_data()

# Streamlit App
st.title("⚽ Football Match Data Explorer")

# Tabs
tab1, tab2 = st.tabs(["Match Data", "League Stats"])

with tab1:
    # Sidebar Filters
    league = st.sidebar.selectbox("Select League", sorted(df['League'].unique()))
    season = st.sidebar.selectbox("Select Season", sorted(df['Season'].unique()))
    teams_in_league = df[df['League'] == league]['Home Team'].unique()
    home_team = st.sidebar.selectbox("Select Home Team", sorted(teams_in_league))
    away_team = st.sidebar.selectbox("Select Away Team", sorted(teams_in_league))

    # Filter Data
    filtered_df = df[
        (df['League'] == league) &
        (df['Season'] == season) &
        (df['Home Team'] == home_team) &
        (df['Away Team'] == away_team)
    ]

    h2h_df = df[((df['Home Team'] == home_team) & (df['Away Team'] == away_team)) | 
                ((df['Home Team'] == away_team) & (df['Away Team'] == home_team))]

    # Compute H2H Stats
    home_wins = ((h2h_df['Home Team'] == home_team) & (h2h_df['Home Goals'] > h2h_df['Away Goals'])).sum()
    draws = (h2h_df['Home Goals'] == h2h_df['Away Goals']).sum()
    away_wins = ((h2h_df['Away Team'] == away_team) & (h2h_df['Away Goals'] > h2h_df['Home Goals'])).sum()
    avg_first_half_goals = h2h_df['First Half Goals'].mean()
    avg_home_possession = h2h_df['Home Ball Poss'].mean()
    avg_away_possession = h2h_df['Away Ball Poss'].mean()
    avg_home_goals = h2h_df['Home Goals'].mean()
    avg_away_goals = h2h_df['Away Goals'].mean()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Head-to-Head Statistics")
        st.write(f"- Home Wins: {home_wins}")
        st.write(f"- Draws: {draws}")
        st.write(f"- Away Wins: {away_wins}")
        st.write(f"- Average {home_team} Goals: {avg_home_goals:.2f}")
        st.write(f"- Average {away_team} Goals: {avg_away_goals:.2f}")
        st.write(f"- Average First Half Goals: {avg_first_half_goals:.2f}")
    with col2:
        st.subheader("H2H Comparison")
        st.write(f"- Average Home Possession: {avg_home_possession:.2f}%")
        st.write(f"- Average Away Possession: {avg_away_possession:.2f}%")

    # Display all H2H matches in a structured format
    st.subheader("Head-to-Head Matches")
    
    for index, row in h2h_df.iterrows():
        # Determine the match format
        match_result = f"{row['Home Goals']}:{row['Away Goals']} ({row['Home Goals FH']}:{row['Away Goals FH']})"
        possession = f"{row['Home Ball Poss']}:{row['Away Ball Poss']}"
        
        # Format the output
        st.markdown(f"**{row['Home Team']} - {row['Away Team']} {match_result} {possession}**")
        st.markdown("---")  # Add a horizontal line for separation

    # Compute Team Stats
    home_team_stats = df[df['Home Team'] == home_team]
    away_team_stats = df[df['Away Team'] == away_team]
    
    col3, col4 = st.columns(2)

    with col3:
        st.subheader(f"{home_team} Stats (Home)")
        st.write(f"- Average Goals Scored: {home_team_stats['Home Goals'].mean():.2f}")
        st.write(f"- Average Goals Conceded: {home_team_stats['Away Goals'].mean():.2f}")
        st.write(f"- Average First Half Goals: {home_team_stats['Home Goals FH'].mean():.2f}")
        # Calculate Win, Draw, and Loss percentages using the "Winner" column
        total_matches = home_team_stats.shape[0]  # Total number of matches played by the home team
        
        wins = (home_team_stats["Winner"] == home_team).sum()
        draws = (home_team_stats["Winner"] == "Draw").sum()
        losses = (home_team_stats["Winner"] == away_team).sum()

        st.write(f"- Win %: {(wins / total_matches) * 100:.2f}%")
        st.write(f"- Draw %: {(draws / total_matches) * 100:.2f}%")
        st.write(f"- Loss %: {(losses / total_matches) * 100:.2f}%")
        st.write(f"- Home Goals Standard Deviation: {home_team_stats['Home Goals'].std():.2f}")
        st.write(f"- Home Goals Variance: {home_team_stats['Home Goals'].var():.2f}")
        
        # Add statistic for number of home matches played
        home_matches_played = home_team_stats.shape[0]  # Count of rows in home_team_stats
        st.write(f"- Home Matches Played: {home_matches_played}")

    with col4:
        st.subheader(f"{away_team} Stats (Away)")
        st.write(f"- Average Goals Scored: {away_team_stats['Away Goals'].mean():.2f}")
        st.write(f"- Average Goals Conceded: {away_team_stats['Home Goals'].mean():.2f}")
        st.write(f"- Average First Half Goals: {away_team_stats['Away Goals FH'].mean():.2f}")
        # Calculate Win, Draw, and Loss percentages using the "Winner" column
        total_matches = away_team_stats.shape[0]  # Total number of matches played by the away team
        
        wins = (away_team_stats["Winner"] == away_team).sum()
        draws = (away_team_stats["Winner"] == "Draw").sum()
        losses = (away_team_stats["Winner"] == home_team).sum()

        st.write(f"- Win %: {(wins / total_matches) * 100:.2f}%")
        st.write(f"- Draw %: {(draws / total_matches) * 100:.2f}%")
        st.write(f"- Loss %: {(away_team_stats['Away Goals'] < away_team_stats['Home Goals']).mean() * 100:.2f}%")
        st.write(f"- Away Goals Standard Deviation: {away_team_stats['Away Goals'].std():.2f}")
        st.write(f"- Away Goals Variance: {away_team_stats['Away Goals'].var():.2f}")
        
        away_matches_played = away_team_stats.shape[0]  # Count of rows in away_team_stats
        st.write(f"- Away Matches Played: {away_matches_played}")

with tab2:
    st.header("📊 League Statistics")
    selected_league = st.selectbox("Choose League", sorted(df['League'].unique()))
    league_df = df[df['League'] == selected_league]
    
    stats = {
        "Home Goals Avg": league_df['Home Goals'].mean(),
        "Away Goals Avg": league_df['Away Goals'].mean(),
        "Home Win %": (league_df['Home Goals'] > league_df['Away Goals']).mean() * 100,
        "Draw %": (league_df['Home Goals'] == league_df['Away Goals']).mean() * 100,
        "Away Win %": (league_df['Away Goals'] > league_df['Home Goals']).mean() * 100,
        "Home Ball Poss Avg": league_df['Home Ball Poss'].mean(),
        "Away Ball Poss Avg": league_df['Away Ball Poss'].mean(),
        "First Half Goals Avg": league_df['First Half Goals'].mean(),
        "Home Goals Avg FH": league_df['Home Goals FH'].mean(),
        "Away Goals Avg FH": league_df['Away Goals FH'].mean(),
        "Standard Deviation": league_df['Home Goals'].std(),
        "Variance": league_df['Home Goals'].var(),
    }

    # Function to format percentage difference with arrows and colors
    def format_percentage_difference(league_value, overall_value):
        difference = league_value - overall_value
        percentage_diff = (difference / overall_value) * 100 if overall_value != 0 else 0
        if difference > 0:
            arrow = "<span style='color: green;'>⬆</span>"  # Green up arrow
        elif difference < 0:
            arrow = "<span style='color: red;'>⬇</span>"  # Red down arrow
        else:
            arrow = "➡️"  # Neutral arrow
        return f"{percentage_diff:.2f}% {arrow}"

    # Display all stats and compare with the whole database
    st.subheader(f"**{selected_league} League vs. All Leagues**")
    col4, col5 = st.columns(2)
   
    st.markdown(f"- **{selected_league} Home Goals Avg:** {stats['Home Goals Avg']:.2f} vs **Overall Home Goals Avg:** {df['Home Goals'].mean():.2f} ({format_percentage_difference(stats['Home Goals Avg'], df['Home Goals'].mean())})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Away Goals Avg:** {stats['Away Goals Avg']:.2f} vs **Overall Away Goals Avg:** {df['Away Goals'].mean():.2f} ({format_percentage_difference(stats['Away Goals Avg'], df['Away Goals'].mean())})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Home Win %:** {stats['Home Win %']:.2f}% vs **Overall Home Win %:** {(df['Home Goals'] > df['Away Goals']).mean() * 100:.2f}% ({format_percentage_difference(stats['Home Win %'], (df['Home Goals'] > df['Away Goals']).mean() * 100)})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Draw %:** {stats['Draw %']:.2f}% vs **Overall Draw %:** {(df['Home Goals'] == df['Away Goals']).mean() * 100:.2f}% ({format_percentage_difference(stats['Draw %'], (df['Home Goals'] == df['Away Goals']).mean() * 100)})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Away Win %:** {stats['Away Win %']:.2f}% vs **Overall Away Win %:** {(df['Away Goals'] > df['Home Goals']).mean() * 100:.2f}% ({format_percentage_difference(stats['Away Win %'], (df['Away Goals'] > df['Home Goals']).mean() * 100)})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} First Half Goals Avg:** {stats['First Half Goals Avg']:.2f} vs **Overall First Half Goals Avg:** {df['First Half Goals'].mean():.2f} ({format_percentage_difference(stats['First Half Goals Avg'], df['First Half Goals'].mean())})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Home Goals Avg FH:** {stats['Home Goals Avg FH']:.2f} vs **Overall Home Goals Avg FH:** {df['Home Goals FH'].mean():.2f} ({format_percentage_difference(stats['Home Goals Avg FH'], df['Home Goals FH'].mean())})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Away Goals Avg FH:** {stats['Away Goals Avg FH']:.2f} vs **Overall Away Goals Avg FH:** {df['Away Goals FH'].mean():.2f} ({format_percentage_difference(stats['Away Goals Avg FH'], df['Away Goals FH'].mean())})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Standard Deviation:** {stats['Standard Deviation']:.2f} vs **Overall Standard Deviation:** {df['Home Goals'].std():.2f} ({format_percentage_difference(stats['Standard Deviation'], df['Home Goals'].std())})", unsafe_allow_html=True)
    st.markdown(f"- **{selected_league} Variance:** {stats['Variance']:.2f} vs **Overall Variance:** {df['Home Goals'].var():.2f} ({format_percentage_difference(stats['Variance'], df['Home Goals'].var())})", unsafe_allow_html=True)
        
    st.subheader("Correlation Table")
    correlation_table = league_df[['Home Goals', 'Away Goals', 'Home Goals FH', 'Away Goals FH', 'Home Ball Poss', 'Away Ball Poss']].corr()
    st.write(correlation_table)
