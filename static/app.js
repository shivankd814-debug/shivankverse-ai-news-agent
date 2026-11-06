
const newsBox = document.getElementById("news");
const titleInput = document.getElementById("title");
const sourceInput = document.getElementById("source");
const notesInput = document.getElementById("notes");
const output = document.getElementById("output");
const statusBox = document.getElementById("status");

async function loadNews() {
  newsBox.textContent = "खबरें लोड हो रही हैं...";
  try {
    const response = await fetch("/api/news");
    const data = await response.json();
    newsBox.innerHTML = "";

    if (!data.items || data.items.length === 0) {
      newsBox.textContent = "अभी खबरें नहीं मिलीं। दोबारा कोशिश करें।";
      return;
    }

    data.items.forEach(item => {
      const card = document.createElement("div");
      card.className = "news-item";

      const heading = document.createElement("h3");
      heading.textContent = item.title;

      const detail = document.createElement("p");
      detail.textContent = item.category + " · " + (item.published || "Date unavailable");

      const link = document.createElement("a");
      link.href = item.link;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = "मूल खबर पढ़ें";

      const select = document.createElement("button");
      select.textContent = "यह खबर चुनें";
      select.onclick = () => {
        titleInput.value = item.title;
        sourceInput.value = item.link;
      };

      card.append(heading, detail, link, select);
      newsBox.appendChild(card);
    });

    document.getElementById("updated").textContent =
      "Updated: " + (data.updated || "");
  } catch (error) {
    newsBox.textContent = "खबरें लोड नहीं हुईं। Server जाँचें।";
  }
}

document.getElementById("refresh").addEventListener("click", loadNews);

document.getElementById("generate").addEventListener("click", async () => {
  statusBox.textContent = "ड्राफ्ट तैयार हो रहा है...";
  try {
    const response = await fetch("/api/draft", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: titleInput.value,
        source: sourceInput.value,
        notes: notesInput.value
      })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "ड्राफ्ट नहीं बना");

    output.value = data.html || "";
    statusBox.textContent = data.notice || "ड्राफ्ट तैयार है।";
  } catch (error) {
    statusBox.textContent = error.message;
  }
});

document.getElementById("export").addEventListener("click", async () => {
  statusBox.textContent = "HTML तैयार हो रहा है...";
  try {
    const response = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: titleInput.value,
        html: output.value
      })
    });

    if (!response.ok) throw new Error("Export नहीं हुआ");

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "shivankverse-article.html";
    a.click();
    URL.revokeObjectURL(url);
    statusBox.textContent = "HTML डाउनलोड शुरू हुआ।";
  } catch (error) {
    statusBox.textContent = error.message;
  }
});

loadNews();
