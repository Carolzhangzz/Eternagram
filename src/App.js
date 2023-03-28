import './App.css';
import React, { useState } from 'react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';



const App = () => {
  const [typing, setTyping] = useState(false);
  const [messages, setMessages] = useState([
    {
      message: "Hello, I am ChatGPT! Please ask me anything.",
      sender: "ChatGPT",
      direction: "ingoing",
    },
    {
      message: "This is a testing message👌. <img src={logo} alt='Logo' />",
      sender: "ChatGPT",
      direction: "ingoing",
    },
  ]);

  //Added the API constants
  const [userId, setUserId] = useState('');
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');



  //Code for handling submit to API
  const handleSubmit = async (e) => {
    e.preventDefault();

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message: message }),
    };

    const apiResponse = await fetch('https://ryno-v2-cedo4cgxka-de.a.run.app/chat', requestOptions);
    const data = await apiResponse.json();
    setResponse(data.response);
  };





  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing",
    }

    // new array of messages
    const newMessages = [...messages, newMessage]; // all the old messages, + the new messages 

    //update our messages state
    setMessages(newMessages);

    //set a typing indicator (chatgpt is typing...)
    setTyping(true);
    //process message to chatGPT (send it over and see reponse)

    await processMessageToChatGPT(newMessages);

  }

  async function processMessageToChatGPT(chatMessages) {
    //chatMessages { sender: "user" or "ChatGPT", message: "The message content here"}
    //apiMessages {role: "user" or "assistant", content: "The message content here"}

    let apiMessages = chatMessages.map((messageObject) => {
      let role = "";
      if (messageObject.sender === "ChatGPT") {
        role = "assistant"
      } else {
        role = "user"
      }
      return { role: role, content: messageObject.message }
    });

    //role: "user" -> a message from the user, "assistant -> a response from chatGPT"
    // "system" -> generally one initial message defining HOW we want chatgpt to talk

    const systemMessage = {
      role: "system",
      content: "Explain all concepts like I am a narrator for a digital game."
    }

    const apiRequestBody = {
      "model": "gpt-3.5-turbo",
      "messages": [
        systemMessage,
        ...apiMessages // [message1, message2, message3]
      ]
    }

    const apiKey = "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";


    await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(apiRequestBody)
    }).then((data) => {
      return data.json();
    }).then((data) => {
      console.log(data.choices[0].message.content);
      setMessages(
        [...chatMessages, {
          message: data.choices[0].message.content,
          sender: "ChatGPT"
        }]
      );
      setTyping(false);
    })
  }



  return (
    <div>

      <div style={{ position: "relative", height: "600px", width: "500px" }}>
        <MainContainer>
          <ChatContainer>
            <MessageList typingIndicator={typing ? <TypingIndicator content="ChatGPT is typing" /> : null}>
              {messages.map((message, i) => {
                return <Message key={i} model={message} />
              })}
            </MessageList>
            <MessageInput placeholder='Type message here' onSend={handleSend} />
          </ChatContainer>
        </MainContainer>
      </div>


      <div>
        <form onSubmit={handleSubmit}>
          <label>
            User ID:
            <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
          </label>
          <br />
          <label>
            Message:
            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>
          <br />
          <input type="submit" value="Submit" />
        </form>
        <p>Response: {response}</p>
      </div>


    </div>
  );
};

export default App;