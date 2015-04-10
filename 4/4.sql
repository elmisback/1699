/* Show the name of the top scorer with the highest number of assists (and the
 * number of assists), for date downloaded = "2015-03-24". In case of ties, all
 * players should be returned.
 */

SELECT name, assists
FROM Scorers
WHERE date_downloaded='2015-03-24'
AND assists IN (
  SELECT MAX(assists) 
  FROM Scorers 
  WHERE date_downloaded='2015-03-24'
)
