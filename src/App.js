import "./App.css";
import React, { useState } from "react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";
import axios from "axios";

const App = () => {
  const [userId, setUserId] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [firstClick, setFirstClick] = useState(true);
  const [typing, setTyping] = useState(false);

  // Define status and finimg in the component's state
  const [status, setStatus] = useState(1);
  const [findimg, setFindimg] = useState("");

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

  const handleSend = async (message) => {
    setMessage(""); 
    
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing",
    };

    if (firstClick) {
      setUserId(message);
      setFirstClick(false);
    } else {

      // new array of messages
      const newMessages = [...messages, newMessage];

      // Update our messages state
      setMessages(newMessages);

      // Set a typing indicator (Ryno is typing...)
      setTyping(true);

      try {
        // Send the message to the API
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: userId, message: message }),
        };

        const apiResponse = await fetch(
          // "https://ryno-v2-cedo4cgxka-de.a.run.app/message",
          "http://localhost:8000/message",
          requestOptions
        );

        if (!apiResponse.ok) {
          console.log(apiResponse.statusText);
          throw new Error(`HTTP error! status: ${apiResponse.status}`);
        }
          
        const data = await apiResponse.json();

        if (data && data.response) {
          // If single response, convert it to an array containing single element.
          let responses = Array.isArray(data.response) ? data.response : [data.response];

          // Apply splitSentences on each response and flatten the result.
          responses = responses.flatMap(response => splitSentences(response));

          // const separatedMessages = splitSentences(data.response);
          const sendSeparatedMessages = async () => {
            for (const message of responses) {
              setTyping(true);
              await new Promise((resolve) => setTimeout(resolve, 1000));
      
              // Call image api only when status is set to 1
              if (status === 1) {
                try {
                  const res = await axios.get(
                    "https://46601y073r.imdo.co/picture/in?message=" + findimg
                  );
      
                  // If we obtained data, add image messsage and set status to 0
                  if (res.data && status === 1) {
                    console.log("return value judgment：", res);
                    const newMessageWithChatGPT1 = {
                      message:
                        "<img width='250'  height='250' src='https://46601y073r.imdo.co/picture/getjpg1?message=" +
                        findimg +
                        "'/>",
                      sender: "ChatGPT",
                      direction: "incoming",
                    };
                    setMessages((prevMessages) => [
                      ...prevMessages,
                      newMessageWithChatGPT1,
                    ]);
                    setStatus(0);
                  }
              } catch (err) {
                console.error('Error Message:', err.message);
                console.error('Error Object:', err);
              }
            }
    
            const newMessageWithChatGPT = {
              message: message,
              sender: "ChatGPT",
              direction: "incoming",
            };
    
            setMessages((prevMessages) => [...prevMessages, newMessageWithChatGPT]);
            setTyping(false);
            }
          };
    
          await sendSeparatedMessages();
          setTyping(false);
        }
      } catch (err) {
        console.error('Error:', err);
      } 
    }
  };


  return (
    <div className="chatBox">
      <div className="headerBox">
        <div className="header">
          <div>
            <img src="/profile picture.png" alt="" /> <div>Ryno</div>
          </div>
          <div>
            <img src="/phoneandvideo.png" alt="" srcset="" />
          </div>
        </div>
      </div>
      <div style={{ width: "100%", height: "0%",flex:'1' }}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator={
                typing ? <TypingIndicator content="Ryno is typing..." /> : null
              }
            >
              {messages.map((message, i) => {
                return <Message key={i} model={message} />;
              })}
            </MessageList>

            {/* <MessageInput placeholder='Type a message here...' onSend={handleSend} /> */}
          </ChatContainer>
        </MainContainer>
      </div>
      <div>
        <form className="inputForm">
          {/* <p id="mention">
            {" "}
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
          </p> */}
          <div className="inputBox">
            <div className="leftIcon">
              <img src="/camera.png" />
            </div>
            <input
              id="input"
              type="text"
              placeholder={userId ? "Please input your message" : "Please input your id first"}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <div className="rightIcon">
              <img src="/microphone.png" />
              <img src="/pic.png" />
              {/* <img src="/icons/smail.png" /> */}
              <input
                className=""
                id="button"
                type="submit"
                value="Send"
                onClick={(e) => {
                  e.preventDefault();
                  setFindimg(message);
                  setStatus(1);
                  // Message is obtained from the input box,
                  //as a global variable, obtained in the sending method
                  handleSend(message);
                }}
              />
            </div>
          </div>
        </form>
      </div>
      {/* <p>Response: {response}</p> */}
    </div>
  );
};

export default App;
