import './App.css';
import React, { useState } from 'react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
import image01 from './image01.jpeg';
import image02 from './image02.jpeg';
import audio01 from './audio01.mp3';
import audio02 from './audio02.mp3';



const App = () => {



  const [typing, setTyping] = useState(false);

  //Added the API constants
  const [userId, setUserId] = useState('');
  const [message, setmessage] = useState('');
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


    const newMessage = {
      message: data.response,
      sender: "user",
      direction: "ingoing",
    }

    // new array of messages
    const newMessages = [...messages, newMessage]; // all the old messages, + the new messages 

    //update our messages state
    setMessages(newMessages);


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



  let audio01 = new Audio("/audio01.mp3")
  let audio02 = new Audio("/audio02.mp3")

  const play_01 = () => {
    audio01.play()
  }

  const play_02 = () => {
    audio02.play()
  }



  const [messages, setMessages] = useState([
    {
      message: "Hello, I am ChatGPT! Please ask me anything.  ",
      sender: "ChatGPT",
      direction: "ingoing",
    },
    {
      message: "This is a testing message👌.",
      sender: "ChatGPT",
      direction: "ingoing",
    },
    {
      message: "Where can I find the Peak Source?",
      sender: "user124",
      direction: "outgoing",
    },
    {
      message: "Ah, the Peak Source! It's one of the most enigmatic and fascinating structures in our world. [Ryno's eyes light up with excitement] To find it, we must venture to the edge of the vast Urbis Desert, where the remnants of a once-thriving metropolis stand. The journey is challenging but well worth the effort. Before we set off, would you like to know more about the history of the Peak Source and its significance to our world, especially in relation to the climate crises that have shaped our lives? <audio controls autoplay muted><source src='audio01.mp3' type='audio/mpeg'></audio>", direction: "ingoing",
    },
    {
      message: " <img width='250' height='250' src='/static/media/image01.a5ba873debed7aa334de.jpeg' />   ",
      sender: "ChatGPT",
      direction: "ingoing",
    },
    {
      message: "What is Urbis Desert? How can I get to there?",
      sender: "user124",
      direction: "outgoing",
    },
    {
      message: "Ah, the Urbis Desert. [Ryno gazes into the distance, reminiscing] It was once a bustling urban center, full of life and technological advancements. However, due to the climate crises that ravaged our world, it transformed into a vast, barren wasteland. The desertification was a result of extreme temperatures, water scarcity, and the collapse of our once-sustainable infrastructure. To get there, we have a few options. We could travel by hovercraft, which is the fastest and most convenient way, but it requires access to a functional vehicle. Alternatively, we could embark on a thrilling journey on the back of a Sandstrider, a magnificent creature adapted to the harsh desert conditions. The journey would be slower, but it would allow us to witness the remnants of the world that once was, and the resilience of life that continues to persist despite the harsh climate. Which mode of transportation do you prefer? And do you have any questions about the Urbis Desert or the journey ahead?",
      sender: "ChatGPT",
      direction: "ingoing",
    },
    {
      message: " <img width='250' height='250' src='/static/media/image02.95e4945ef4f26e905f0a.jpeg' />   ",
      sender: "ChatGPT",
      direction: "ingoing",
    },
    {
      message: "What is hovercraft?",
      sender: "user124",
      direction: "outgoing",
    },
    // {
    //   message: "Response: Today, my meal consisted of nutrient-rich algae cakes and a revitalizing beverage made from purified water and electrolytes. [Ryno rubs his stomach in satisfaction] The algae cakes are a sustainable food source that has become essential in our world, as traditional agriculture has been heavily impacted by the climate crises. By cultivating algae, we can produce food with minimal water usage and a smaller environmental footprint. How about you? Have you had a chance to try some of the unique cuisine our world has to offer? If not, I'd be happy to introduce you to some interesting dishes that have emerged as a result of our changing climate and the need for more sustainable food sources.",
    //   sender: "ChatGPT",
    //   direction: "ingoing",
    // },
  ]);


  // const msg_style = {
  //   fontFamily: "monospace",
  //   background: "rgb(110, 72, 170)",
  //   color: "rgb(255, 255, 255)"
  // }

  // const Msg = (model) => {

  //   console.log(model)
  //   return (
  //     <div style = {msg_style}>
  //       Hello + {model}
  //     </div>
  //   )
  // }




  return (
    <div>

      <div style={{ position: "relative", height: "700px", width: "500px" }}>
        <MainContainer>
          <ChatContainer>
            <MessageList typingIndicator={typing ? <TypingIndicator content="ChatGPT is typing" /> : null}>
              {messages.map((message, i) => {
                return <Message key={i} model={message} />
                // return <Msg key={i} model={message} />

              })}
            </MessageList>
            <MessageInput placeholder='Type message here' onSend={console.log("onsend clicked")} />
          </ChatContainer>
        </MainContainer>
      </div>
      {/* 
      <button style={{
        position:'absolute',
        zIndex: 1,
        top: 645,
        lef: 600,
        height: 37,
        width: 37,
        borderRadius: 10,
        backgroundColor: '#add8e6',
        borderColor: '#add8e6',
        marginLeft: 457,
        marginRight: 50,
        marginTop: 20
      }}> > </button> */}


      <div>
        <form onSubmit={handleSubmit}> <br/> <br/> <br /><br /><br /><br /><br /><br /><br /><br /> <br /><br /><br /><br /><br /><br /><br /><br />
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
          }}  type="text" value={message} onChange={(e) => setmessage(e.target.value)} />
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
          }} type="submit" value=">" />
        </form>
        {/* <p>Response: {response}</p> */}

      </div>


    </div>
  );
};

export default App;