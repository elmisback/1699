/* Show the full names of all the top scorers, along with the full name of
 * their team, and the name of the division they play in, for all of 2015. Show
 * the name of a top scorer only once, unless they changed teams. In other
 * words, show only unique combinations of scorer name, team name, division
 * name. 
 */

SELECT DISTINCT Scorers.name, Teams.full_name, Teams.division_name
FROM Scorers INNER JOIN Teams
ON Teams.short_name=Scorers.team
WHERE YEAR(Scorers.date_downloaded)="2015"
