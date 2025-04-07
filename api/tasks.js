const { MongoClient } = require('mongodb');
require('dotenv').config();

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

exports.handler = async function(event, context) {
  try {
    await client.connect();
    const database = client.db('task_manager');
    const collection = database.collection('tasks');

    switch (event.httpMethod) {
      case 'GET':
        const tasks = await collection.find({}).toArray();
        return {
          statusCode: 200,
          body: JSON.stringify(tasks)
        };

      case 'POST':
        const task = JSON.parse(event.body);
        await collection.insertOne(task);
        return {
          statusCode: 201,
          body: JSON.stringify(task)
        };

      default:
        return {
          statusCode: 405,
          body: 'Method not allowed'
        };
    }
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  } finally {
    await client.close();
  }
}
