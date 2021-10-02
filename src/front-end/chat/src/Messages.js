import { Component } from "react";
import React from "react";

class Messages extends Component {
    
    renderMessage(message) {
        const { member, text } = message;
        const { currentMember } = this.props;
        const messageFromMe = member.id === currentMember.id;
        const className = messageFromMe ? "Messages-message currentMember" : "Messages-message";

        // HTML Building
        return (
            <li className={className}>
                <span 
                    className="avatar"
                    style={{backgroundColor: member.color}}/>
                <div className="Message-content">
                    <div className="username">
                        { member.username }
                    </div>
                    <div className="text">{ text }</div>
                </div>
            </li>
        );
    }

    // Main Rendering function
    render() {
        // The messages are passed and stored in 
        // this class as props for now
        const { messages } = this.props;
        
        // HTML Building
        return (
            <ul className="Messages-list">
                { messages.map(m => this.renderMessage(m)) }
            </ul>
        );
    }
}

export default Messages;
