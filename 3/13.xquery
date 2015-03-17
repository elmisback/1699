<results>{
for $t in doc("hw3.teams.xml")//team-standing/title[
    not(.=doc("hw3.goalies.xml")//skaterData/team) 
    and not(.=doc("hw3.leading_scorers.xml")//skaterData/team)]
return <team>{data($t)}</team>
}</results>
