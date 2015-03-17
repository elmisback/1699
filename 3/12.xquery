<results>{
for $t in doc("hw3.teams.xml")//team-standing
    where (count(doc("hw3.goalies.xml")//skaterData[team=$t/title])
           + count(doc("hw3.leading_scorers.xml")//skaterData[team=$t/title])
           = 0)
return <team>{data($t/title)}</team>
}</results>
