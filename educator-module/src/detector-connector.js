// detector-connector.js
// Simulated phishing detector connection
// Later, replace this logic with your real detector module

function simulatePhishingDetection() {
  const currentUrl = window.location.href;

  // Simple simulation: detect any URL containing "phish"
  if (currentUrl.includes("phish")) {
    console.log("⚠️ Potential phishing detected at:", currentUrl);

    chrome.runtime.sendMessage({
      type: "PHISHING_DETECTED",
      url: currentUrl
    });
  }
}

// Run the detection simulation on page load
simulatePhishingDetection();
