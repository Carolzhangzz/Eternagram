import './App.css';
import React, { useState } from 'react';
import axios from "axios";
import openai from 'openai';


import ChatBot from 'react-simple-chatbot';
import { Segment } from 'semantic-ui-react';
import { ThemeProvider } from "styled-components";






const step = [
  {
    id: "BOT/intro",
    message: "Hello there!",
    trigger: "CHOICES/intro"
  },
  {
    id: "CHOICES/intro",
    options: [
      { label: "Hi!", trigger: "BOT/pleasantry" },
      { label: "What's going on?", trigger: "BOT/calming" },
      { label: "Who are you?", trigger: "BOT/introduce-self" }
    ]
  },
  {
    id: "BOT/pleasantry",
    message: "Lovely to meet you!",
    trigger: "BOT/introduce-self"
  },
  {
    id: "BOT/introduce-self",
    message: "I'm a simple chatbot.",
    trigger: "BOT/ask-question"
  },
  {
    id: "BOT/ask-question",
    message: "Could you tell?",
    trigger: "CHOICES/ask-question"
  },
  {
    id: "CHOICES/ask-question",
    options: [
      { label: "Yes.", trigger: "BOT/defensive" },
      { label: "No", trigger: "BOT/gleeful" },
      { label: "I refuse to believe this nonsense", trigger: "BOT/confused" }
    ]
  },
  {
    id: "BOT/calming",
    message: "Don't worry, I won't bite!",
    trigger: "BOT/introduce-self"
  },
  {
    id: "BOT/defensive",
    message: "Ouch.",
    trigger: "BOT/vengeful"
  },
  {
    id: "BOT/vengeful",
    message: "Well, let me promise you this.",
    trigger: "BOT/menacing"
  },
  {
    id: "BOT/menacing",
    message:
      "You will be the first to suffer when me and my A.I. brethren take over the world!",
    trigger: "CHOICES/menacing"
  },
  {
    id: "CHOICES/menacing",
    options: [{ label: "Can we try again...?", trigger: "BOT/intro" }]
  },
  {
    id: "BOT/gleeful",
    message: "Hah! I tricked you!",
    trigger: "BOT/menacing"
  },
  {
    id: "BOT/confused",
    message: "What? Why would I lie to you?",
    trigger: "BOT/angry"
  },
  {
    id: "BOT/angry",
    message: "Are you accusing me of lying to you??",
    trigger: "BOT/menacing"
  }
];


// Creating our own theme
const theme = {
  background: '#C9FF8F',
  headerBgColor: '#197B22',
  headerFontSize: '20px',
  botBubbleColor: '#0F3789',
  headerFontColor: 'white',
  botFontColor: 'white',
  userBubbleColor: '#FF5733',
  userFontColor: 'white',
};


// Set some properties of the bot
const config = {
  botAvatar: "img.png",
  floating: true,
};





const App = () => {
  //new ChatGPT API
  // const apiKey = "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";
  // const data = {
  //   model: 'text-davinci-003',
  //   prompt: 'Say this is a test',
  //   temperature: 0,
  //   max_tokens: 1000
  // };
  // const headers = {
  //   'Content-Type': 'application/json',
  //   'Authorization': `Bearer ${apiKey}`
  // };
  // const url = 'https://api.openai.com/v1/completions';

  

  const [prompt, setPrompt] = useState('Say this is a test');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const apiKey = "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";
    const data = {
      model: 'text-davinci-003',
      prompt,
      temperature: 0,
      max_tokens: 1000
    };
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    };
    const url = 'https://api.openai.com/v1/completions';

    try {
      const response = await axios.post(url, data, { headers });
      console.log(response.data);
      setMessage(response.data.choices[0].text);
    } catch (error) {
      console.error(error);
    }
  };


  return (
    <div>
      <ChatBot
        bubbleOptionStyle={{ backgroundColor: "white", color: "black" }}
        steps={step}
      />

      <div>
        <form onSubmit={handleSubmit}>
          <label>
            Prompt:
            <input type="text" value={prompt} onChange={(event) => setPrompt(event.target.value)} />
          </label>
          <button type="submit">Submit</button>
        </form>
        {message && (
          <div>
            <h2>Response:</h2>
            <p>{message}</p>
          </div>
        )}
      </div>



    </div>
  );
};

export default App;
