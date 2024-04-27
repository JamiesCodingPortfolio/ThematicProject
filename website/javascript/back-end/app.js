const express = require('express');
const bodyParser = require('body-parser');
const path = require('path')

const app = express();
const port = 3000;

app.listen(port, '0.0.0.0', () => {
  console.log(`Server listening on port ${port}`);
});
// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../../public')))
// Database (replace with your actual database interaction)
let database = {};

// Route to serve the form
app.get('/', (req, res) => {
  // Send HTML with a form containing an input and submit button
  const filePath = path.join(__dirname, '../../public/html/index.html')
  res.sendFile(filePath.toString());
});

// Route to handle form submission
app.post('/', (req, res) => {
  const name = req.body.name; // Access submitted data

  // Update database (replace with actual logic)
  database.name = name;

  // Respond to user with success message
  res.send(`Data updated! Name: ${name}`);
});