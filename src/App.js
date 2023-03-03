import './App.css';
import React, { useState } from 'react';
import axios from "axios";
import openai from 'openai';


import ChatBot from 'react-simple-chatbot';
import { Segment } from 'semantic-ui-react';
import { ThemeProvider } from "styled-components";






const step = [
  {
    id: '1',
    message: 'Hi, I can show you some pictures. What type of picture do you want to see?',
    trigger: 'type',
  },
  {
    id: 'type',
    options: [
      { value: 'nature', label: 'Nature', trigger: 'nature' },
      { value: 'animals', label: 'Animals', trigger: 'animals' },
    ],
  },
  {
    id: 'nature',
    message: 'Here is a picture of nature:',
    trigger: 'nature_image',
  },
  {
    id: 'nature_image',
    component: (
      <img
        src="https://picsum.photos/200/300"
        width={200}
        height={300}
      />
    ),
    asMessage: true,
    trigger: 'more_pictures',
  },
  {
    id: 'animals',
    message: 'Here is a picture of animals:',
    trigger: 'animals_image',
  },
  {
    id: 'animals_image',
    component: (
      <img
        src="https://placeimg.com/200/300/animals"
        width={200}
        height={300}
      />
    ),
    asMessage: true,
    trigger: 'more_pictures',
  },
  {
    id: 'more_pictures',
    message: 'Do you want to see more pictures?',
    trigger: 'more_pictures_options',
  },
  {
    id: 'more_pictures_options',
    options: [
      { value: 'yes', label: 'Yes', trigger: 'type' },
      { value: 'no', label: 'No', end: true },
    ],
  },
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
      model: "gpt-3.5-turbo",
      messages: [{ role: 'user', content: prompt }],
    };
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    };
    const url = 'https://api.openai.com/v1/chat/completions';

    try {
      const completion = await axios.post(url, data, { headers });
      console.log(completion.data);
      setMessage(completion.data.choices[0].message.content);
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
