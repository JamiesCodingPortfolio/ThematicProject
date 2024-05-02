const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { MongoClient } = require('mongodb');
const fs = require('fs');

const app = express();
const port = 3000;
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../../public')));

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

    //console.log('Servers', servers);

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

async function retrieveData(receivedData) {
  try {
    // Access the database and retrieve the list of servers

    // Used to access the database and retrieve a full list of servers the bot is present in

    const servers = await accessDB();

    const serverIDs = receivedData.serverIDs;

      // Filter the servers based on the received server IDs
    const serverInformation = servers.filter(server => {
      // Compare server IDs with the received server IDs array
      return serverIDs.includes(server.ServerID);
    });
    console.log("Relevant server info:", serverInformation)
    return serverInformation
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

app.post('/user-data-server', (req, res) => {

  const data = req.body;

  console.log('Recieved data:', data);

  retrieveData(data)
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

app.post('/server-data', (req, res) => {

  const { serverUniqID } = req.body; 

  console.log('Received server ID:', serverUniqID);

  const serverData = { 
    message: 'Server data retrieved successfully',
    serverUniqID,
  };

  const dashboardPath = 'http://localhost:3000/html/commands-dashboard.html';
  const response = {
    message: serverData.message,
    serverUniqID: serverData.serverUniqID,
    redirectUrl: dashboardPath // Set the redirect URL in the response
  };

  res.json(response);
});

app.post('/command-data', async (req, res) => {
  const { serverID, cmdName, cmdStatus } = req.body; // Extract data from the request body

  console.log('Received data:', { serverID, cmdName, cmdStatus });

  try {
      // Access the database
      const servers = await accessDB();

      // Find the server by ID
      const server = servers.find(s => s.ServerID === serverID);

      if (!server) {
          res.status(404).json({ error: 'Server not found' });
          return;
      }

      // Find the command in the server's DefaultCommands
      const command = server.Commands[cmdName];

      if (!command) {
          res.status(404).json({ error: 'Command not found' });
          return;
      }

      // Update the command's active status
      command.active = cmdStatus;

      const variablesFile = fs.readFileSync('../../../variables.txt', 'utf-8');

      const firstLine = variablesFile.split('\n')[0];

      const mongoURL = firstLine.slice(12);
      
      console.log('MongoDB connection string:', mongoURL);
      // Save the updated server data back to the database
      const dbclient = new MongoClient(mongoURL);
      await dbclient.connect();
      const db = dbclient.db('BoomBot');
      const collection = db.collection('servers');
      await collection.updateOne({ ServerID: serverID }, { $set: server });

      // Close the database connection
      await dbclient.close();

      // Send a success response
      res.json({ message: 'Command status updated successfully' });

  } catch (error) {
      console.error('An error occurred while updating command status:', error);
      res.status(500).json({ error: 'An error occurred while updating command status' });
  }
});
