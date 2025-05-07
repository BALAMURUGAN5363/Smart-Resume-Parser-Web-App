const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 5000; // Choose an appropriate port

// Middleware
app.use(cors());
app.use(bodyParser.json());

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/extractedTextDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// Check DB connection
mongoose.connection.once('open', () => {
    console.log('Connected to MongoDB');
});

// Define a schema for the extracted text
const extractedTextSchema = new mongoose.Schema({
    filename: String,
    text: String,
});

const ExtractedText = mongoose.model('ExtractedText', extractedTextSchema);

// POST endpoint to save extracted text to MongoDB
app.post('/save-text', async (req, res) => {
    const { filename, text } = req.body;

    const newText = new ExtractedText({
        filename,
        text,
    });

    try {
        await newText.save();
        res.status(200).json({ message: 'Text saved successfully!' });
    } catch (err) {
        res.status(500).json({ message: 'Error saving text', error: err });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
