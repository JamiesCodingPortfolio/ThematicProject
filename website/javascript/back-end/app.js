const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { MongoClient } = require('mongodb');
const fs = require('fs');

const app = express();
const port = 3000;
app.use(express.json());

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

    return servers;

  }

  catch (error){
    console.error('An error occured:', error)
  }
  finally{
    await dbclient.close();
  }
}

async function compareServerIDs(receivedData) {
  try {
    // Access the database and retrieve the list of servers

    // Used to access the database and retrieve a full list of servers the bot is present in

    const servers = await accessDB();

    const serverIDs = receivedData.serverIDs;

      // Filter the servers based on the received server IDs
    const matchingServers = servers.filter(server => {
      // Compare server IDs with the received server IDs array
      return serverIDs.includes(server.ServerID);

    });

    console.log('Matching servers:', matchingServers);

    const matchingServersIDs = matchingServers.map(server => server.ServerID);
      // Return the list of matching servers
      return matchingServersIDs;
      
  } catch (error) {
      console.error('An error occurred during comparison:', error);
      throw error;
  }
}

accessDB();

app.listen(port, '0.0.0.0', () => {
  console.log(`Server listening on port ${port}`);
});
// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../../public')))

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
});

app.post('/user-data', (req, res) => {

  const data = req.body;

  console.log('Recieved data:', data);

  compareServerIDs(data)
    .then(matchingServers => {
      res.json({
        message: 'Data received successfully',
        receivedData: data,
        matchingServers: matchingServers
      });
  })
  .catch(error => {
    console.error('An error occurered:', error)
  });

});

