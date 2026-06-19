const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*", // Adjust appropriately in production for security
        methods: ["GET", "POST"]
    }
});

// Seed Initial Data Base
const DATA_FILE = './data.json';
let marketData = {
    gold: 2025.50,
    silver: 24.15,
    timestamp: new Date().toISOString()
};

// Check if data file exists; if not, create it
if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(marketData));
} else {
    const raw = fs.readFileSync(DATA_FILE);
    marketData = JSON.parse(raw);
}

const updateData = (newData) => {
    marketData = { ...marketData, ...newData, timestamp: new Date().toISOString() };
    fs.writeFileSync(DATA_FILE, JSON.stringify(marketData, null, 2));
    
    // Broadcast updating prices instantly to all clients connected
    io.emit('price_update', marketData);
};

// --- API Endpoints ---

// GET /prices
app.get('/api/prices', (req, res) => {
    res.json(marketData);
});

// POST /update-price
app.post('/api/update-price', (req, res) => {
    const { gold, silver } = req.body;
    if (gold || silver) {
        updateData({ gold, silver });
        res.json({ success: true, message: "Price updated and broadcasted globally.", data: marketData });
    } else {
        res.status(400).json({ error: "Missing gold or silver in payload." });
    }
});

// GET /news
app.get('/api/news', (req, res) => {
    // Example Trusted Links Endpoint
    res.json({
        news: [
            { source: "World Gold Council", url: "https://www.gold.org", headline: "Gold Market Update" },
            { source: "Reserve Bank of India", url: "https://www.rbi.org.in", headline: "RBI Svereign Gold Bond Details" }
        ]
    });
});

io.on('connection', (socket) => {
    console.log('New client connected: ' + socket.id);
    
    // Send current prices instantly on link
    socket.emit('price_update', marketData);

    socket.on('disconnect', () => {
        console.log('Client disconnected: ' + socket.id);
    });
});

const PORT = 5000;
server.listen(PORT, () => {
    console.log(`Real-Time Data Backend listening on http://localhost:${PORT}`);
    console.log(`Socket.IO Endpoint active on port ${PORT}`);
});
