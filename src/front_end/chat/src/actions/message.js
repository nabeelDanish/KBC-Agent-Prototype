import * as api from '../api'
import { agent, initialState } from '../components/Chatbox/state'
import { hideTyping } from '../components/Chatbox/TypingIndictor/setTyping'
import { scrollToHighlight } from '../components/Source/scroll'

// Function
export const sendMessage = (message, setMessages, setSpanSelected, setResponses) => async () => {
    try {
        const data = await api.sendMessage(message)

        // Retrieving Data
        var result = data.data.response
        var responseList = result.split(".")

        // Adding Multiple messages based on the full stops
        // Each sentence is uttered as a separate text message
        var i
        for (i = 0; i < responseList.length; ++i) 
        {
            if (responseList[i].length > 5) 
            {
                setMessages(messages => [...messages, {
                    "text": responseList[i],
                    "id": "0",
                    "sender": agent
                }]);
            }
        }

        // Setting Span of text by Q/A
        // var span = [data.data.k_start_index, data.data.k_end_index]
        var span = data.data.knowledge_sent
        setSpanSelected(span)

        // Setting Candidate Responses
        var responses = data.data.candidates
        setResponses(responses)
        
        // Updating UI
        hideTyping();
        scrollToHighlight();
        
    } catch (error) {
        console.log(error)
    }
}

export const fetchSource = (setSource) => async () => {
    try {
        const data = await api.fetchSource()
        setSource(data.data.response)
    } catch (error) {
        console.log(error)
    }
}

export const fetchTopics = (setTopic, setTopics) => async () => {
    try {
        const data = await api.fetchTopics()
        setTopic(data.data.current_topic)
        setTopics(data.data.topics)
    } catch (error) {
        console.log(error)
    }
}

export const topicSelect = (topic, setSource, setMessages, setProgress) => async (dispatch) => {
    try {
        const data = await api.changeTopic({"topic": topic});
        if (data.status == 200) {
            dispatch(fetchSource(setSource))
            setMessages(initialState)
            setProgress("hidden")
        } else {
            throw Error
        }
    } catch (error) {
        console.log(error)
    }
}
