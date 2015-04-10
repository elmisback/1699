/* Using aggregation, show the list of teams that have no top goalies and no
 * top scorers, at any point of time (i.e., for all the statistics in the
 * database). Your final output should only have a list of team names (e.g.,
 * BUF).
 */

SELECT short_name
FROM (
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
) T
WHERE top_players = 0
