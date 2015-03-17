<results>{
for $t in doc("hw3.teams.xml")//team-standing
order by $t/name 
return <team>
        <name>{data($t/name)}</name>
        <goalie_cnt>{
            count(doc("hw3.goalies.xml")//skaterData[team=$t/title])
        }</goalie_cnt>
    </team>
}</results>
