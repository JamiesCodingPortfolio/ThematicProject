const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { MongoClient } = require('mongodb');
const fs = require('fs');

const app = express();
const port = 3000;

async function accessDB(){

  const variablesFile = fs.readFileSync('../../../variables.txt', 'utf-8');

  const firstLine = variablesFile.split('\n')[0];

  const mongoURL = firstLine.slice(12);

  const dbclient = new MongoClient(mongoURL);

  try {
    
    await dbclient.connect();

    const db = dbclient.db('BoomBot');

    const collection = db.collection('servers');

    const servers = await collection.find().toArray();

    console.log('Servers', servers);

  }

  catch (error){
    console.error('An error occured:', error)
  }
  finally{
    await dbclient.close();
  }
}

accessDB();

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
app.get('/auth/discord', (req, res) => {
  const name = req.body.name; // Access submitted data
  const dashboardPath = path.join(__dirname, '../../public/html/bot-dashboard.html');
  return res.sendFile(dashboardPath);
  // Update database (replace with actual logic)
  //database.name = name;

  // Respond to user with success message
  //res.send(`Data updated! Name: ${name}`);
});

app.post('/user-data')