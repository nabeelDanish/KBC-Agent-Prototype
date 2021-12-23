import './styles.css';
import { ChatBox } from 'react-chatbox-component';
import { useDispatch } from 'react-redux';
import React from 'react'
import { sendMessage } from '../../actions/message'
import { sender, agent } from './state';
import TypingIndictor from './TypingIndictor/TypingIndictor'
import { setTyping } from './TypingIndictor/setTyping';

const Chatbox = ({ messages, setMessages, setSpanSelected, setResponses }) => {
    // Dispatcher
    const dispatch = useDispatch();

    // Function to handle onSubmitMessage
    const onSubmitMessage = (message) => {
      setTyping();
      setMessages(messages => [...messages, {
        "text": message,
        "id": "0",
        "sender": sender
      }])
      dispatch(sendMessage({"message": message}, setMessages, setSpanSelected, setResponses))
    }

    // Building HTML
    return (
        <div>
            <ChatBox messages={messages} onSubmit={onSubmitMessage}/>
            <TypingIndictor />
        </div>
    );
}

export default Chatbox
