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

import CustomPopup from "./components/customPopup/popup";
import axios from "axios";

const App = () => {
  const [userId, setUserId] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [firstClick, setFirstClick] = useState(true);
  const [typing, setTyping] = useState(false);
  const [isShowPopup, setIsShowPopup] = useState(true);

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
          "https://ryno-v2-cedo4cgxka-de.a.run.app/message",
          requestOptions
        );

        if (!apiResponse.ok) {
          console.log(apiResponse.statusText);
          throw new Error(`HTTP error! status: ${apiResponse.status}`);
        }

        const data = await apiResponse.json();

        if (data && data.response) {
          // If single response, convert it to an array containing single element
          let responses = Array.isArray(data.response) ? data.response : [data.response];

          // Apply split sentences on each response
          responses = responses.flatMap(response => splitSentences(response));

          const sendSeparatedMessages = async () => {
            for (const message of responses) {
              setTyping(true);
              await new Promise((resolve) => setTimeout(resolve, 1000));

              // Call image api only when status is set to 1
              if (status === 1) {
                try {
                  const res = await axios.get(
                    "https://2dde-115-208-95-142.jp.ngrok.io/picture/in?message=" + findimg
                  );

                  // If we obtained data, add image messsage and set status to 0
                  if (res.data && status === 1) {
                    console.log("return value judgment：", res);
                    const newMessageWithChatGPT1 = {
                      message:
                        "<img width='250'  height='250' src='https://2dde-115-208-95-142.jp.ngrok.io/picture/getjpg1?message=" +
                        findimg +
                        "'/>",
                      sender: "ChatGPT",
                      direction: "ingoing",
                    };
                    setMessages((prevMessages) => [
                      ...prevMessages,
                      newMessageWithChatGPT1,
                    ]);
                    setStatus(0);
                  }
                } catch (err) {
                  console.log(err);
                }
              }

              const newMessageWithChatGPT = {
                message: message,
                sender: "ChatGPT",
                direction: "ingoing",
              };

              setMessages((prevMessages) => [
                ...prevMessages,
                newMessageWithChatGPT,
              ]);
              setTyping(false);
            }
          };

          await sendSeparatedMessages();
          setTyping(false);
        }
      } catch (err) {
        console.error("Error:", err);
      }
    }
  };

  const [isShowPopupDisplayed, setIsShowPopupDisplayed] = useState(false);
  const closePopup = (value) => {
    setFindimg(value);
    setStatus(1);
    handleSend(value);

    setIsShowPopup(false);
    setIsShowPopupDisplayed(true);
    document.querySelector("#input").focus();
  };

  return (
    <div className="chatBox">
      {!isShowPopupDisplayed && (
        <CustomPopup isShow={isShowPopup} closeEvent={closePopup} />
      )}
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
      <div style={{ width: "100%", height: "0%", flex: "1" }}>
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
              placeholder={
                userId
                  ? "Please input your message"
                  : "Please input your id first"
              }
              value={message}
              onFocus={(e) => {
                if (!isShowPopupDisplayed) {
                  document.querySelector("#input").blur();
                  setIsShowPopup(true);
                }
              }}
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
                  if (message === "") return;
                  setFindimg(message);
                  setStatus(1);
                  handleSend(message);
                  document.querySelector("#input").focus();
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
