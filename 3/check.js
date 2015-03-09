var xpath = require('xpath'), 
    dom = require('xmldom').DOMParser,
    fs = require('fs');

var xml = fs.readFileSync('hw3.leading_scorers.xml', {encoding:'utf-8'});
var doc = new dom().parseFromString(xml)
var nodes = xpath.select("/players/skaterData[goals>20 and assists>30]/name/text()", doc).toString()
console.log(nodes);
/*
for (var i=0; i < nodes.length; i++) {
    console.log(nodes[i].firstChild.data);
}
*/
