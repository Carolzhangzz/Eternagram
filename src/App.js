import './App.css';
import React, { useState } from 'react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
import image01 from './image01.jpeg';
import image02 from './image02.jpeg';
import audio01 from './audio01.mp3';
import audio02 from './audio02.mp3';



const App = () => {
  // Constants
  const [userId, setUserId] = useState('');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [response, setResponse] = useState('');
  const [typing, setTyping] = useState(false);

  // A function to split sentences to shorter messages
  function splitSentences(responseText) {
    const parts = responseText.split(/(\[.*?\])/g);
    const messages = [];
    let currentMessage = "";
  
    for (const part of parts) {
      if (part.startsWith("[")) {
        if (currentMessage.trim()) {
          messages.push(currentMessage.trim());
          currentMessage = "";
        }
        currentMessage += part;
      } else {
        currentMessage += part;
      }
    }
  
    if (currentMessage.trim()) {
      messages.push(currentMessage.trim());
    }
  
    return messages;
  }

  // A function to handle send
  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing",
    }

    // new array of messages
    const newMessages = [...messages, newMessage]; // all the old messages, + the new messages 

    // Update our messages state
    setMessages(newMessages);

    // Set a typing indicator (Ryno is typing...)
    setTyping(true);

    // Send the message to your API
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message: message }),
    };

    const apiResponse = await fetch('https://ryno-v2-cedo4cgxka-de.a.run.app/chat', requestOptions);
    const data = await apiResponse.json();
    setResponse(data.response);

    // Display the response from the API
    const separatedMessages = splitSentences(data.response);

    const sendSeparatedMessages = async () => {
      for (const message of separatedMessages) {
        setTyping(true);

        // Show Ryno typing indicator between messages
        await new Promise((resolve) => setTimeout(resolve, 1000)); 

        const newMessageWithChatGPT = {
          message: message,
          sender: "ChatGPT",
          direction: "ingoing",
        };

        setMessages((prevMessages) => [...prevMessages, newMessageWithChatGPT]);
        setTyping(false);
      }
    };

    await sendSeparatedMessages();

    // hide the typing indicator after receiving the response
    setTyping(false);

    // Clear the input field
    setMessage("");
  };

  return (
    <div>

      <div style={{ position: "relative", height: "700px", width: "500px" }}>
        <MainContainer>
          <ChatContainer>
            <MessageList typingIndicator={typing ? <TypingIndicator content="Ryno is typing..." /> : null}>
              {messages.map((message, i) => {
                return <Message key={i} model={message} />

              })}
            </MessageList>
            <MessageInput placeholder='Type a message here...' onSend={handleSend} />
          </ChatContainer>
        </MainContainer>
      </div>

      <div>
        <form> <br></br>
          <label>
            User ID:
            <input  
          
          type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
          </label>
          <br />
          <label>

            <input style={{
            position: 'absolute',
            zIndex: 1,
            top: 635,
            lef: 0,
            height: 32,
            width: 400,
            borderRadius: 10,
            backgroundColor: '#e8f4f8',
            borderColor: '#e8f4f8',
            marginLeft: 45,
            marginRight: 50,
            marginTop: 20
          }}  type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>
         
          <input style={{
            position: 'absolute',
            zIndex: 1,
            top: 635,
            lef: 600,
            height: 37,
            width: 37,
            borderRadius: 10,
            backgroundColor: '#add8e6',
            borderColor: '#add8e6',
            marginLeft: 457,
            marginRight: 50,
            marginTop: 20
          }} 
          type="submit" 
          value=">"
          onClick={(e) => {
            e.preventDefault();
            handleSend(message);
          }} />
        </form>
        {/* <p>Response: {response}</p> */}

      </div>


    </div>
  );
};

export default App;