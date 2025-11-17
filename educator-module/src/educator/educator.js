// src/educator/educator.js
document.addEventListener("DOMContentLoaded", async () => {
  const languageSelect = document.getElementById("language");
  const playAudioBtn = document.getElementById("play-audio");
  const contentSection = document.getElementById("content-section");
  const titleEl = document.getElementById("title");
  const descEl = document.getElementById("description");

  // default language
  let currentLang = "en";

  // Default fallback content in case JSON fails
  const defaultData = {
    title: "⚠️ Phishing Alert!",
    description: "This website may try to steal your personal information.",
    section1: { title: "What is Phishing?", content: "Phishing is an attempt to trick you into revealing sensitive data." },
    section2: { title: "How to Identify Fake Websites?", content: "Check the URL carefully and avoid unknown links." }
  };

  // try to load saved language from storage (if available)
  try {
    const stored = await new Promise(resolve => chrome.storage?.local?.get?.(["userLang"], resolve) || resolve({ userLang: undefined }));
    if (stored && stored.userLang) currentLang = stored.userLang;
    languageSelect.value = currentLang;
  } catch (e) {
    // ignore storage errors
    console.warn("Could not read stored language:", e);
  }

  // initial load
  await loadLanguage(currentLang);

  // language change handler
  languageSelect.addEventListener("change", async () => {
    currentLang = languageSelect.value;
    try { await new Promise(r => chrome.storage?.local?.set?.({ userLang: currentLang }, r)); } catch (e) { /* ignore */ }
    await loadLanguage(currentLang);
  });

  // audio play button
  playAudioBtn.addEventListener("click", () => {
    const textToSpeak = `${titleEl.innerText}\n${descEl.innerText}\n${contentSection.innerText}`;
    const msg = new SpeechSynthesisUtterance(textToSpeak);
    msg.lang = getSpeechLangCode(currentLang);
    try {
      speechSynthesis.cancel(); // stop existing
      speechSynthesis.speak(msg);
    } catch (e) {
      console.error("TTS failed:", e);
    }
  });

  // robust loader with fallback
  async function loadLanguage(lang) {
    const path = `../translations/${lang}.json`;
    let data = null;

    try {
      const resp = await fetch(path);
      if (!resp.ok) {
        console.warn(`Translation fetch failed (${resp.status}) for ${path}. Falling back to English.`);
        throw new Error(`HTTP ${resp.status}`);
      }

      // try to parse, guard against empty body
      const text = await resp.text();
      if (!text || text.trim().length === 0) {
        throw new Error("Empty translation file");
      }

      try {
        data = JSON.parse(text);
      } catch (parseErr) {
        console.warn("Translation JSON parse error:", parseErr);
        throw parseErr;
      }

    } catch (err) {
      // If we failed to load chosen language, try English as fallback
      if (lang !== "en") {
        console.warn(`Falling back to English due to error loading ${lang}:`, err);
        try {
          const resp2 = await fetch("../translations/en.json");
          const text2 = await resp2.text();
          data = text2 && text2.trim().length ? JSON.parse(text2) : null;
        } catch (e) {
          console.error("Failed to load fallback English translation:", e);
          data = null;
        }
      } else {
        data = null;
      }
    }

    // final fallback to defaultData
    if (!data) {
      console.warn("Using hardcoded defaultData for UI text.");
      data = defaultData;
    }

    // render UI safely (guard each property)
    titleEl.innerText = data.title || defaultData.title;
    descEl.innerText = data.description || defaultData.description;

    const s1 = data.section1 || defaultData.section1;
    const s2 = data.section2 || defaultData.section2;

    contentSection.innerHTML = `
      <h3>${s1.title || ""}</h3>
      <p>${s1.content || ""}</p>
      <h3>${s2.title || ""}</h3>
      <p>${s2.content || ""}</p>
    `;

    console.log(`Loaded language: ${lang}`);
  }

  function getSpeechLangCode(lang) {
    switch (lang) {
      case "kn": return "kn-IN";
      case "hi": return "hi-IN";
      case "ta": return "ta-IN";
      case "te": return "te-IN";
      default: return "en-US";
    }
  }
});
