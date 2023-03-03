const express = require('express');
const cors = require('cors');
const openai = require('openai');
// const openai = require('@openai/api');


const app = express();

app.use(cors());
app.use(express.json());

const OPENAI_API_KEY = "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";

console.log(OPENAI_API_KEY);


const generateText = async (prompt) => {
  console.log('Prompt:', prompt);


  const completions = await openai.completions.create({
    engine: 'davinci',
    prompt: prompt,
    max_tokens: 1024,
    n: 1,
    stop: '\n',
    temperature: 0.7,
  }, {
    headers: {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
  });

  console.log('Completions:', completions);


  return completions.choices[0].text.trim();
};

app.get('/', (req, res) => {
  // res.send('Server is running!');

  console.log("Server is running!");
});

app.post('/api/generate-text', async (req, res) => {
  const { prompt } = req.body;

  try {
    const text = await generateText(prompt);
    res.send(text);
  } catch (err) {
    console.error(err);
    res.status(500).send('Error generating text');
  }
});

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});