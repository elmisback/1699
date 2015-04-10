/* Using a join, list the full names of all teams that have had scorers in the
 * top 30 list (at any point in time) who had more than 20 goals and more than
 * 30 assists.
 */

SELECT DISTINCT Teams.full_name 
FROM Teams 
INNER JOIN Scorers
ON Teams.short_name=Scorers.team
WHERE Scorers.goals>20
AND Scorers.assists>30;
