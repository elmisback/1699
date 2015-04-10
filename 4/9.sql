/* Without using aggregation, show the list of teams that have no top goalies
 * and no top scorers, at any point of time (i.e., for all the statistics in
 * the database). Your final output should only have a list of team names
 * (e.g., BUF).
 */

SELECT short_name
FROM Teams
WHERE short_name NOT IN (
  SELECT short_name
  FROM Teams JOIN Goalies
  ON short_name = team
)
AND short_name NOT IN (
  SELECT short_name
  FROM Teams JOIN Scorers
  ON short_name = team
)
