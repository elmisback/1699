<results> {
for $d in distinct-values(doc("hw3.teams.xml")//division-name)
    return <division> {attribute name {$d}} {
        for $t in doc("hw3.teams.xml")//team-standing[division-name=$d]
        let $c := count(doc("hw3.leading_scorers.xml")//skaterData[team=$t/title])
        return <team>{attribute count {$c}} {data($t/name)}</team>
    }</division>
}</results>
