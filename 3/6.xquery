(: Highest number of assists :)
let $m := max(doc("hw3.leading_scorers.xml")//skaterData/assists)
for $p in doc("hw3.leading_scorers.xml")//skaterData
    where $p/assists = $m
        return <player>
                <name>{data($p/name)}</name>
                <assists>{data($p/assists)}</assists>
               </player> 
