sort active_players.txt | uniq > active_players_cleaned.txt;
rm active_players.txt; mv active_players_cleaned.txt active_players.txt;