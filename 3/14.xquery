<results>{
for $t in doc("hw3.teams.xml")//team-standing/title/text()
let $r0 := min(doc("hw3.goalies.xml")//skaterData[team=$t]/rank)
let $r1 := min(doc("hw3.leading_scorers.xml")//skaterData[team=$t]/rank)
let $r := min(($r0, $r1))
for $n in (doc("hw3.goalies.xml")//skaterData[team=$t and rank=$r]/name/text(),
           doc("hw3.leading_scorers.xml")//skaterData[team=$t 
                                                     and rank=$r]/name/text())
order by $t
return <team>
        <title>{$t}</title>
        <name>{$n}</name>
        <rank>{$r}</rank>
    </team>
}</results>
