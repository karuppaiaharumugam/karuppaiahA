const localtunnel = require('localtunnel');

// You can change 'gold-price-demo-app' to any unique name you prefer!
// Keep it unique so no one else uses it at the same time.
const CUSTOM_SUBDOMAIN = 'gold-price-app-live-2024';
const PORT = 5000; // Match this to your Flask (or Node) port!

(async () => {
  try {
    const tunnel = await localtunnel({ 
        port: PORT, 
        subdomain: CUSTOM_SUBDOMAIN 
    });

    console.log("\n=======================================================");
    console.log("🎉 YOUR STATIC HTTPS LINK IS READY 🎉");
    console.log(`👉 ${tunnel.url} 👈`);
    console.log("=======================================================\n");
    console.log("Note: The first time someone visits this link, they may see a 'Friendly Reminder' page from LocalTunnel. They just need to click 'Click to Continue' to see your app.");

    tunnel.on('close', () => {
      console.log('Static Tunnel Closed.');
    });
    
  } catch (err) {
      console.error("Error creating tunnel: ", err);
  }
})();
