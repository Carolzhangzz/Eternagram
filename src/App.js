import "./App.css";
import React, { useState } from "react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";
// import image01 from './image01.jpeg';
// import image02 from './image02.jpeg';
// import audio01 from './audio01.mp3';
// import audio02 from './audio02.mp3';
import axios from "axios";

let firstclick = false;

const App = () => {
  var findimg = "";
  //the status flag is used to identify the status of images
  var status = 1;
  // Constants
  const [userId, setUserId] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [response, setResponse] = useState("");
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
    };

    // new array of messages
    const newMessages = [...messages, newMessage]; // all the old messages, + the new messages

    // Update our messages state
    setMessages(newMessages);

    // Set a typing indicator (Ryno is typing...)
    setTyping(true);

    return;
    // Send the message to your API
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message: message }),
    };

    const apiResponse = await fetch(
      "https://ryno-v2-cedo4cgxka-de.a.run.app/chat",
      requestOptions
    );
    const data = await apiResponse.json();
    setResponse(data.response);

    // Display the response from the API
    const separatedMessages = splitSentences(data.response);

    const sendSeparatedMessages = async () => {
      for (const message of separatedMessages) {
        setTyping(true);

        // Show Ryno typing indicator between messages
        await new Promise((resolve) => setTimeout(resolve, 1000));
        //A function to match images in the database
        //Status is a mark, can prevent the picture from being repeated;
        if (status == 1) {
          //set up port mapping to my backend
          axios
            .get("https://46601y073r.imdo.co/picture/in?message=" + findimg)
            .then((res) => {
              if (res.data) {
                if (status == 1) {
                  //if it matches,and it was the first time to send
                  console.log("return value judgment：", res);
                  const newMessageWithChatGPT1 = {
                    message:
                      "<img width='250'  height='250' src='https://46601y073r.imdo.co/picture/getjpg1?message=" +
                      findimg +
                      "'/>",
                    sender: "ChatGPT",
                    direction: "ingoing",
                  };
                  setMessages((prevMessages) => [
                    ...prevMessages,
                    newMessageWithChatGPT1,
                  ]);
                  status = 0;
                }
              }
            });
        }

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

  // A function to handle send with user id
  const handleSenduserid = async (message) => {
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing",
    };

    // new array of messages
    const newMessages = [...messages, newMessage]; // all the old messages, + the new messages

    // Update our messages state
    setUserId(newMessages);

    // Set a typing indicator (Ryno is typing...)
    // TODO: It is recommended Ryno give a prologue when the user first click submmit button
    setTyping(true);

    // Send the message to your API
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message: message }),
    };

    const apiResponse = await fetch(
      "https://ryno-v2-cedo4cgxka-de.a.run.app/chat",
      requestOptions
    );
    const data = (await apiResponse.json()) || { response: {} };
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
    <div className="chatBox">
      <div className="headerBox">
        <div className="header">
          <div>
            <img src="/icons/profile picture.png" alt="" /> <div>Ryno</div>
          </div>
          <div>
            <img src="/icons/phoneandvideo.png" alt="" srcset="" />
          </div>
        </div>
      </div>
      <div style={{ width: "100%", height: "100%" }}>
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
              <img src="/icons/camera.png" />
            </div>
            <input
              id="input"
              type="text"
              placeholder="please input your id first"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <div className="rightIcon">
              <img src="/icons/microphone.png" />
              <img src="/icons/pic.png" />
              {/* <img src="/icons/smail.png" /> */}
              <input
                className=""
                id="button"
                type="submit"
                value="Send"
                onClick={(e) => {
                  e.preventDefault();
                  // handleSend(message);
                  findimg = message;
                  status = 1;
                  //Message is obtained from the input box,
                  //as a global variable, obtained in the sending method
                  handleSend(message);
                  removementionandsenduserid();
                }}
              />
            </div>
          </div>
        </form>
      </div>
      {/* <p>Response: {response}</p> */}
    </div>
  );

  function removementionandsenduserid() {
    // test

    return;
    let mention = document.getElementById("mention");
    let input = document.getElementById("input");
    if (!firstclick) {
      firstclick = true;
      // return
      // Remove the text from the page
      mention.remove();
      handleSenduserid(message);
    } else {
      handleSend(message);
    }
    input.value = "";
  }
};

export default App;

