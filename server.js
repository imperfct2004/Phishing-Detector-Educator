// server.js
import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();
app.use(cors());

// Proxy endpoint for Google Translate TTS
app.get("/tts", async (req, res) => {
  const { text, lang } = req.query;
  if (!text || !lang) return res.status(400).send("Missing text or lang");

  const googleTTS = `https://translate.google.com/translate_tts?ie=UTF-8&q=${encodeURIComponent(
    text
  )}&tl=${lang}&client=tw-ob`;

  try {
    const response = await fetch(googleTTS, {
      headers: { "User-Agent": "Mozilla/5.0" }
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const buffer = await response.arrayBuffer();
    res.setHeader("Content-Type", "audio/mpeg");
    res.send(Buffer.from(buffer));
  } catch (err) {
    console.error("TTS proxy error:", err);
    res.status(500).send("TTS request failed");
  }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => console.log(`✅ TTS Proxy running on http://localhost:${PORT}`));
