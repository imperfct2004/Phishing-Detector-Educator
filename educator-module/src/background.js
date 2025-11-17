// background.js
// Listens for phishing detection messages and opens the Educator popup

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "PHISHING_DETECTED") {
    console.log("🚨 Phishing detected! Showing Educator Module...");
    showEducatorPopup(message.url);
  }
});

// Opens the Educator popup window
function showEducatorPopup(url) {
  chrome.windows.create({
    url: chrome.runtime.getURL("src/educator/index.html"),
    type: "popup",
    width: 400,
    height: 600
  });
}
