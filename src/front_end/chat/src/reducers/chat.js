import { initialState } from '../components/Chatbox/state';

const messageReducer = (messages = initialState, action) => {
    switch (action.type) {
        default:
            return messages;
    }
}

export default messageReducer;
