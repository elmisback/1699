<results>{
for $t in doc("hw3.teams.xml")//team-standing
let $c := ( count(doc("hw3.goalies.xml")//skaterData[team=$t/title])
            + count(doc("hw3.leading_scorers.xml")//skaterData[team=$t/title])) 
order by $c
return <team>
        <name>{data($t/title)}</name>
        <cnt>{$c}</cnt>
    </team>
}</results>
