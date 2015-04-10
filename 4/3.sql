/* Show all top scorers’ names, goals, assists, and average number of goals per
 * game, sorted by average number of goals per game, for date downloaded =
 * ’2015-03-24’.
 */

SELECT name, goals, assists, (goals/games_played AS avgGPG)
FROM Scorers
WHERE date_downloaded = '2015-03-24'
ORDER BY avgGPG;
