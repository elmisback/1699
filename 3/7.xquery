<results>
{
for $p in doc("hw3.leading_scorers.xml")//skaterData
    let $team := doc("hw3.teams.xml")//team-standing[title=$p/team]
    return <player>
            <name>{data($p/name)}</name>
            <team>{data($team/name)}</team>
            <division-name>{data($team/division-name)}</division-name>
           </player>
}
</results>
