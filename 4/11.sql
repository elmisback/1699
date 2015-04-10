/* For the latest date downloaded, for teams who have at least two players in
 * the top 30 scorers list, show the name, team name (short name), and rank of
 * any player(s) they may have in the top 30 goalies list. If a team with two
 * top scorers does not have a top goalie, list the team name and no goalie
 * information (e.g., CBJ, NULL, NULL).  (Hint: use views to simplify the
 * query)
 */

CREATE OR REPLACE VIEW latest AS
SELECT GREATEST(MAX(Scorers.date_downloaded), MAX(Goalies.date_downloaded))
        AS latest_date
FROM Scorers, Goalies ;

CREATE OR REPLACE VIEW relevant_teams AS
SELECT Teams.short_name AS team
FROM latest, Teams JOIN Scorers
ON Teams.short_name = Scorers.team
WHERE Scorers.date_downloaded = latest.latest_date 
GROUP BY Teams.short_name
HAVING COUNT(sid) >= 2 ;

SELECT R.team, G.name, G.rank
FROM latest, relevant_teams R LEFT JOIN 
            (SELECT * FROM Goalies, latest
             WHERE Goalies.date_downloaded = latest.latest_date) G
ON R.team = G.team
