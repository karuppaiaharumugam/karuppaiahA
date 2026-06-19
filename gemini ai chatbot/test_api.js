const fs = require('fs');
const API_KEY = "AIzaSyCir2cvTifsw2YcDeYhjpdwrkpPKmqBJCk";
const API_URL = "https://generativelanguage.googleapis.com/v1beta/models";

async function test() {
    try {
        const response = await fetch(`${API_URL}?key=${API_KEY}`);
        const data = await response.json();
        fs.writeFileSync('models.txt', data.models.map(m => m.name).join('\n'));
        console.log("Done");
    } catch (e) {
        console.error(e);
    }
}
test();
