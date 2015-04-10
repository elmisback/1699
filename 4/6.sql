/* Show for every division and for every team in that division, the count of
 * how many players each team has that are top scorers in year 2015. Do not
 * worry about duplicate scorers, i.e., if the same person shows up in two top
 * scorer lists, downloaded at different dates, count it as 2.
 */

SELECT division_name, full_name, COUNT(sid) AS top_scorers
FROM Teams INNER JOIN Scorers
ON short_name = team
WHERE YEAR(date_downloaded)="2015"
GROUP BY team
ORDER BY division_name
