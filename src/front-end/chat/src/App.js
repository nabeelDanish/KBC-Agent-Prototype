import logo from './logo.svg';
import './App.css';
import Messages from './Messages.js'
import Input from "./Input.js"
import Header from "./Header"
import Source from "./Source"
import { Component } from 'react';
import { Container } from '@material-ui/core'

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
        text: "Hello! I am MUKALMA. I am an Intelligent Q/A Chatbot. Please Ask me Anything",
        member: {
          id: 1,
          color: "blue",
          username: "MUKALMA"
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
      username: "MUKALMA"
    },
    response: "",
    source: "LOL LMAO",
    topics: [
      "Multan", "Karachi"
    ],
    currentTopic: "",
  }

  componentDidMount() {
    this.fetchSource();
    this.fetchTopics();
  }

  // Main Render Function
  render() {
    return (
      <div class="container" className="App-container" onLoad={this.fetchSource}>
        <Header />
        <div class="container" className="outer-container">
            <div className="left-container">
              <div className="App">
                <Messages 
                  messages={ this.state.messages } 
                  currentMember={ this.state.member }/>
                <Input 
                  onSendMessage={this.onSendMessage}/>
              </div>
            </div>
            <div className="right-container">
              <Source 
                source={this.state.source} 
                topics={this.state.topics}
                current_topic={this.state.currentTopic}
                onTopicSelected={this.onTopicSelected}
                />
            </div>
        </div>
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

    fetch("http://127.0.0.1:5000/reply", requestOptions)
      .then(response => response.json())
      .then(data => this.setState({ response: data.response }, this.onResponseReceived))
      .catch((e) => {
        console.log(e);
      })
  }

  sendTopicRequest(e) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: e })
    };

    fetch("http://127.0.0.1:5000/topics/select", requestOptions)
      .then(response => response.json())
      .catch((e) => {
        console.log(e);
      })
  }

  onTopicSelected(t) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: t })
    };

    fetch("http://127.0.0.1:5000/topics/select", requestOptions)
      .then(window.location.reload(false))
      .catch((e) => {
        console.log(e);
      })
  }

  fetchSource() {
    fetch("http://127.0.0.1:5000/source")
      .then(response => response.json())
      .then(data => this.setState({ ...this.state, source: data.response }))
      .catch((e) => {
        console.log("FETCH FAILED!");
        console.log(e);
      })
  }

  fetchTopics() {
    fetch("http://127.0.0.1:5000/topics")
      .then(response => response.json())
      .then(data => {
        this.addTopicMessage(data.current_topic)
        this.setState({ ...this.state, topics: data.topics, currentTopic: data.current_topic })
      })
      .then()
      .catch((e) => {
        console.log("FETCH FAILED!");
        console.log(e);
      })
  }

  addTopicMessage(t) {
    const messages = this.state.messages
    messages.push({
      text: "I can chat about " + t,
      member: this.state.bot
    })
    this.setState({...this.state, messages: messages, response: ""})
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
