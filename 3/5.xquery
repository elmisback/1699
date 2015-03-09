<result>
{
    for $player in doc("hw3.leading_scorers.xml")//skaterData
        let $goals_per_game := number($player/goals) 
                                div number($player/games_played)
        order by $goals_per_game 
        return <player>
                <name>{data($player/name)}</name>
                <goals>{data($player/goals)}</goals>
                <assists>{data($player/assists)}</assists>
                <goals_per_game>{$goals_per_game}</goals_per_game>
               </player>
}
</result>
