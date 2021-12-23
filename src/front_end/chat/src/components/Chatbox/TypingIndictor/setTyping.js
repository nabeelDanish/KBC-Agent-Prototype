
export function setTyping () {
    const indicator = document.getElementById("indicator")
    indicator.style.visibility = "visible"

    var chatBubbles = document.getElementsByClassName("chat-bubble-row")
    var last = chatBubbles.length - 1
    var rect = chatBubbles[last].getBoundingClientRect()

    var topPos = rect.top + 220 <= 550 ? rect.top + 220 : 550
    
    indicator.style.top = topPos + "px";
    indicator.style.left = rect.left + 80 + "px";
}

export function hideTyping() {
    const indicator = document.getElementById("indicator")
    indicator.style.visibility = "hidden"
}
