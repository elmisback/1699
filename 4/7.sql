/* Show for every team, the count of how many top goalies it has for date
 * downloaded = ’2015-03-24’.  Use the full name of each team (e.g., Anaheim),
 * instead of the short version (e.g., ANA), and sort the results
 * alphabetically, by team name.
 */

SELECT full_name, COUNT(gid) AS top_goalies
FROM Teams INNER JOIN Goalies
ON short_name = team
WHERE date_downloaded = "2015-03-24"
GROUP BY team
ORDER BY full_name
