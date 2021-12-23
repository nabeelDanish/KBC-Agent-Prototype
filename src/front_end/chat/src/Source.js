import { Component } from "react";
import React from "react";

class Source extends Component {
    state = {
        selected_topic: ""
    }

    renderOptions(t, current_topic) {
        if (t === current_topic) {
            return ( <option value={t} selected="selected">{t}</option> )
        } else {
            return ( <option value={t}>{t}</option> );
        }
    }

    onSubmit(e) {
        e.preventDefault();
        this.props.onTopicSelected(this.state.selected_topic);
    }
    
    handleChange(e) {
        this.setState({selected_topic: e.target.value});
    }

    render() {
        // Fetching source
        const { source, topics, current_topic } = this.props;

        // Building HTML
        return (
            <div className="source-container">
                <form className="source-form" onSubmit={e => this.onSubmit(e)}>
                    <textarea className="source-text" value={source} readonly/>
                    <table>
                        <tr>
                            <td className="select-topic">
                                <label for="topics">Select a Topic </label>
                                <select name="topics" id="topics" onChange={(e) => this.handleChange(e)}>
                                    { topics.map(t => this.renderOptions(t, current_topic)) }
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <button className="submit-source-btn">Submit</button>
                            </td>
                        </tr>
                    </table>
                </form>
            </div>
        );
    }
}

export default Source
