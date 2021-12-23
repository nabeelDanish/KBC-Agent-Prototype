// Javascript function to focus on the text that was selected
// Using Tree Parsing
export function scrollToHighlight() {
    console.log("scrollToHighlight: Called!")
    const outerContainer = document.getElementsByClassName("notranslate public-DraftEditor-content")
    var innerContainer = outerContainer[0].childNodes;
    var innerDivs = innerContainer[0].childNodes;
    
    var divWithMark = null;
    var markIndex = -1

    var i = 0;
    for (i = 0; i < innerDivs.length; ++i) {
        var nodes = innerDivs[i].childNodes
        var nodes_inner = nodes[0].childNodes
        if (nodes_inner.length > 1) {
            markIndex = i
            break
        }
    }

    // Scrolling into view
    divWithMark = innerDivs[markIndex]
    console.log("divWithMatk: " + divWithMark)
    divWithMark?.scrollIntoView()
}
