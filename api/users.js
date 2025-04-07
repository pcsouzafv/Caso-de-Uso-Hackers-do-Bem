const { MongoClient } = require('mongodb');
require('dotenv').config();

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

exports.handler = async function(event, context) {
  try {
    await client.connect();
    const database = client.db('task_manager');
    const collection = database.collection('users');

    switch (event.httpMethod) {
      case 'GET':
        const users = await collection.find({}).toArray();
        return {
          statusCode: 200,
          body: JSON.stringify(users)
        };

      case 'POST':
        const user = JSON.parse(event.body);
        await collection.insertOne(user);
        return {
          statusCode: 201,
          body: JSON.stringify(user)
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
