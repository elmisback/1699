/* Without using a join, list the full names of all teams that have had scorers
 * in the top 30 list (at any point in time) who had more than 20 goals and
 * more than 30 assists.
 */

SELECT DISTINCT Teams.full_name
FROM Teams, Scorers
WHERE Teams.short_name = Scorers.team
AND Scorers.goals > 20
AND Scorers.assists > 30;
