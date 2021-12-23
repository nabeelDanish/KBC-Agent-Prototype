import { Component } from "react";
import React from "react";

class Input extends Component {
    state = {
        text: ""
    }

    render() {
        return (
        <div>
            <form onSubmit={e => this.onSubmit(e)} className="input-form">
                <input
                    onChange={e => this.onChange(e)}
                    value={this.state.text}
                    type="text"
                    placeholder="Enter your message and press ENTER"
                    autoFocus="true">
                </input>
                <button className="button">Send</button>
            </form>
        </div>
        );
    }

    onChange(e) {
        this.setState({text: e.target.value});
    }

    onSubmit(e) {
        e.preventDefault();
        this.setState({text: ""})
        this.props.onSendMessage(this.state.text);
    }
}

export default Input;
