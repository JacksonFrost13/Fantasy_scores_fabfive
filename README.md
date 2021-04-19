# Fantasy_scores_fabfive
Multiple versions of same app. App helps to choose the best fantasy team for DotA2 in FabFive application. Created only for me to improve my coding skills, but if someone will find it - you're welcome to use.

*Hint.* All data parsed from datdota.com and opendota.com for my GSheet document.

v1 - manual input of players data: nicknames, avg. score per game (according to FabFive formula), price, role. Manual sorting in dicts, for ex., necessary to create dict, named by team, insert 5 players with nicknames as keys, all other data - value for key. Manual input for desired and unwanted players. Using pd for readable output. No control of correct input of names.

v2 - added automated input from Google Sheets (my personal copy-paste database, where I took score of players from for v1 manual input). Dicts are creating after parsing, naming dicts after value in additional column "Team".

v3 - added divided calculations for win games and lose games, so it has to be two separate pages in GSheet document - *%region% win* and *%region% lose*. Added manual input field for expected match score between two teams in format *%team1% %score1% - %score2% %team2%*, so insteam of sum of avg. points output contains sum of expected points, based on match score.

v4 - added UI design for all program, fully reformatted code. Added tournament grid, based on all teams in database for chosen region, which is also the manual input field for expected match score. Added 4 frames for including/excluding cores/supports for searching certain rosters in post-calculation table.


Q/A.
Q: Why I chose GSheet with manual input over API requests to opendota/datdota?
A: Players and team rosters are inconsistent, so I may get wrong data from API or data, which won't be useful, for ex., because of changing player role. 
