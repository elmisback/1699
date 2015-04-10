/* Show for every team, how many top goalies and top scorers each team has
 * combined for date downloaded = ’2015-03-24’. The output should be the name
 * of the short name of the team (e.g., ANA) followed by the total count of
 * goalies and scorers. The results should be ordered by the total number of
 * top goalies and top scorers (in descending order). If a team has no top
 * goalies and no top scorers, then a 0 should be shown as the count.
 */

SELECT G.short_name AS short_name, (top_goalies + top_scorers) AS top_players
FROM (
  SELECT short_name, COUNT(gid) AS top_goalies
  FROM Teams LEFT JOIN Goalies
  ON short_name = team
  AND date_downloaded = "2015-03-24"
  GROUP BY short_name) G
INNER JOIN (
  SELECT short_name, COUNT(sid) AS top_scorers 
  FROM Teams LEFT JOIN Scorers
  ON short_name = team
  AND date_downloaded = "2015-03-24"
  GROUP BY short_name) S
ON G.short_name = S.short_name 
ORDER BY top_players DESC
