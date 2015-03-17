for $p in ('D','L','R','C')
    let $c := count(doc("hw3.leading_scorers.xml")//skaterData[position=$p])
    return <position>
            <posname>{$p}</posname>
            <numplayers>{$c}</numplayers>
        </position>
