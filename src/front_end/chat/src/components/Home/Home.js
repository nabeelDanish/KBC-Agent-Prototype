import React, { useState, useEffect } from "react";
import { useDispatch } from 'react-redux'
import { Grid } from "@material-ui/core";
import Chatbox from "../Chatbox/Chatbox";
import TabContainer from "../Tabs/Tabs";
import { initialState } from "../Chatbox/state";
import { fetchSource, fetchTopics } from "../../actions/message";

const Home = () => {
    // Defining dispatcher
    const dispatch = useDispatch();

    // Messages
    const [messages, setMessages] = useState(initialState)

    // Responses
    const [responses, setResponses] = useState(["Response 1", "Response 2"])

    // Topic
    const [topic, setTopic] = useState('');
    const [topics, setTopics] = useState([]);
    const [spanSelected, setSpanSelected] = useState(/Fusce placerat consequat elementum./g)

    // Source
    const dummySource = `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec lacus in dolor porta dignissim vitae eget massa. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec pulvinar massa vitae metus elementum, a sagittis felis tempor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut vestibulum est ante, eget viverra nisl rutrum tempor. Cras vestibulum ac orci sed imperdiet. Donec cursus fringilla nibh, id pellentesque odio semper condimentum. Nullam id felis non augue ultrices luctus et imperdiet tellus. Pellentesque purus ex, maximus et feugiat ac, rhoncus non mauris. Curabitur porta purus id risus sollicitudin aliquam. Pellentesque at tincidunt velit. Sed fermentum eros in ultricies interdum. Donec vitae quam sed enim suscipit suscipit. Aliquam ligula elit, vehicula vitae nunc eu, varius accumsan ex. In sit amet eleifend massa.

    Aliquam id cursus dui, eget placerat arcu. Ut congue facilisis efficitur. Vestibulum semper ipsum quis erat facilisis, vitae tincidunt lorem accumsan. Vestibulum congue turpis risus, eu scelerisque lectus posuere quis. Quisque pulvinar, dui a facilisis rutrum, ante leo ultrices justo, vitae varius nisi magna ut quam. Etiam mattis odio quis tincidunt posuere. Praesent congue aliquet porta.
    
    In quis bibendum lectus. Sed consequat in risus ac suscipit. Proin rutrum quam in leo ultrices ultricies. Pellentesque varius, libero id lobortis vulputate, risus tortor rhoncus mi, eget rutrum nisl lacus nec metus. Mauris augue dolor, tincidunt nec ligula at, hendrerit rhoncus turpis. Morbi vel efficitur ipsum, in congue enim. Nam vestibulum nulla non magna ultricies accumsan. Donec ornare ex sit amet aliquet auctor. Mauris tortor sem, molestie eleifend dui eu, porttitor convallis massa. Donec placerat diam condimentum lacus elementum iaculis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Mauris sed tempus mi. Cras rutrum aliquet lobortis.
    
    Donec vulputate ac ipsum nec congue. Fusce placerat consequat elementum. Phasellus egestas enim in faucibus sollicitudin. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Cras in congue orci. Praesent nec turpis velit. Donec sollicitudin neque vel volutpat sollicitudin. Donec consequat mauris eu massa mollis dapibus. Phasellus maximus enim leo. Nam sit amet lacus non arcu auctor laoreet. Donec luctus rutrum metus nec tincidunt. Ut malesuada velit vitae ligula fermentum, eu volutpat nibh egestas. Donec tincidunt vel nisi at fermentum.
    
    Vivamus luctus justo quis leo cursus, dictum vestibulum massa commodo. Ut laoreet venenatis nibh, non elementum magna tincidunt eu. Etiam neque urna, ultrices vitae ante in, dignissim porttitor felis. Vestibulum aliquam nisi sit amet interdum fermentum. Proin vitae arcu eu tortor viverra ultrices semper ut massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum fringilla, velit nec iaculis ultrices, eros nunc feugiat nisi, sed aliquet urna dolor ac tellus.`
    
    const [source, setSource] = useState(dummySource);

    // Using Effect to load initial Data
    useEffect(() => {
        dispatch(fetchSource(setSource));
        dispatch(fetchTopics(setTopic, setTopics))
    }, []);

    // Building HTML
    return (
        <div className={"mainContainer"} >
            <Grid container spacing={2}>
                <Grid item xs={6}>
                    <Chatbox 
                        messages={messages} 
                        setMessages={setMessages} 
                        setSpanSelected={setSpanSelected}
                        setResponses={setResponses}/>
                </Grid>
                <Grid item xs={6}>
                    <TabContainer 
                        source={source} 
                        setSource={setSource} 
                        spanSelected={spanSelected}
                        topic={topic}
                        setTopic={setTopic}
                        topics={topics}
                        setTopics={setTopics}
                        setMessages={setMessages}
                        responses={responses}
                        />
                </Grid>
            </Grid>
        </div>
    );
}

export default Home;
