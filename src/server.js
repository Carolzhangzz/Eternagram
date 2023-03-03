const express = require('express');
const cors = require('cors');
const openai = require('openai');

const app = express();

app.use(express.json());
app.use(cors());

const port = process.env.PORT || 5000;

app.post('/api/generate-text', async (req, res) => {
  const inputText = req.body.inputText;

  try {
    const result = await openai.Completion.create({
      engine: 'davinci',
      prompt: `Generate a text based on the following prompt: ${inputText}`,
      max_tokens: 100,
      n: 1,
      stop: '\n',
    });
    const generatedText = result.choices[0].text;
    res.json({ generatedText });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

app.listen(port, () => console.log(`Server running on port ${port}`));