import logo from './logo.svg';
import './App.css';
import Messages from './Messages.js'
import Input from "./Input.js"
import { Component } from 'react';

class App extends Component {
  randomName() {
    const adjectives = ["autumn", "hidden", "bitter", "misty", "silent", "empty", "dry", "dark", "summer", "icy", "delicate", "quiet", "white", "cool", "spring", "winter", "patient", "twilight", "dawn", "crimson", "wispy", "weathered", "blue", "billowing", "broken", "cold", "damp", "falling", "frosty", "green", "long", "late", "lingering", "bold", "little", "morning", "muddy", "old", "red", "rough", "still", "small", "sparkling", "throbbing", "shy", "wandering", "withered", "wild", "black", "young", "holy", "solitary", "fragrant", "aged", "snowy", "proud", "floral", "restless", "divine", "polished", "ancient", "purple", "lively", "nameless"];
    const nouns = ["waterfall", "river", "breeze", "moon", "rain", "wind", "sea", "morning", "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn", "glitter", "forest", "hill", "cloud", "meadow", "sun", "glade", "bird", "brook", "butterfly", "bush", "dew", "dust", "field", "fire", "flower", "firefly", "feather", "grass", "haze", "mountain", "night", "pond", "darkness", "snowflake", "silence", "sound", "sky", "shape", "surf", "thunder", "violet", "water", "wildflower", "wave", "water", "resonance", "sun", "wood", "dream", "cherry", "tree", "fog", "frost", "voice", "paper", "frog", "smoke", "star"];
    const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
    const noun = nouns[Math.floor(Math.random() * nouns.length)];
    return adjective + noun;
  }
  
  randomColor() {
    return '#' + Math.floor(Math.random() * 0xFFFFFF).toString(16);
  }

  // Setting the State of the App
  state = {
    messages: [
      {
        text: "Hello! I am DANISH. I am an Intelligent Q/A Chatbot. Please Ask me Anything",
        member: {
          id: 1,
          color: "blue",
          username: "DANISH"
        }
      }
    ],
    member: {
      id: 0,
      username: this.randomName(),
      color: this.randomColor()
    },
    bot: {
      id: 1,
      color: "blue",
      username: "DANISH"
    },
    response: ""
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h1>DANISH</h1> 
          <ul className="Members">
            <li>Nabeel Danish 18I-0579</li>
            <li>Farjad Ilyas 18I-0436</li>
            <li>Saad Saqlain 18I-0694</li>
          </ul>
        </div>
        <Messages 
          messages={ this.state.messages } 
          currentMember={ this.state.member }/>
        <Input 
          onSendMessage={this.onSendMessage}/>
      </div>
    );
  }

  onSendMessage = (message) => {
    const messages = this.state.messages
    messages.push({
      text: message,
      member: this.state.member
    })
    this.setState({messages: messages})
    this.sendRequest(message)
  }

  sendRequest(e) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: e })
    };

    fetch("https://4f5f-206-84-140-151.ngrok.io/reply", requestOptions)
      .then(response => response.json())
      .then(data => this.setState({ response: data.response }, this.onResponseReceived))
  }

  onResponseReceived() {
    const messages = this.state.messages
    messages.push({
      text: this.state.response,
      member: this.state.bot
    })
    this.setState({messages: messages, response: ""})
  }
}

export default App;
