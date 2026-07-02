const fontLink = document.createElement("link");
fontLink.rel = "stylesheet";
fontLink.href = "https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@700&display=swap";
document.head.appendChild(fontLink);

function getCurrentSlug() {
  const path = window.location.pathname;
  const parts = path.split("/").filter(Boolean);
  const slug = parts[parts.length - 1];
  return slug;
}

function loadRecommendations() {
  const url = chrome.runtime.getURL("recommendations.json");
  return fetch(url).then(response => response.json());
}

function renderRecommendations(matches) {
  if (!matches || matches.length === 0) {
    console.log("No recommendations for this article.");
    return;
  }

  const container = document.createElement("div");
  container.id = "sd-recommender-box";

  const heading = document.createElement("h3");
  heading.textContent = "You Might Also Like";
  container.appendChild(heading);

  const list = document.createElement("ul");
  matches.forEach(match => {
    const item = document.createElement("li");

    const link = document.createElement("a");
    link.href = match.link;
    link.className = "sd-rec-link";

    if (match.image_url) {
      const img = document.createElement("img");
      img.src = match.image_url;
      img.alt = match.title;
      link.appendChild(img);
    }

    const titleSpan = document.createElement("span");
    titleSpan.textContent = match.title;
    link.appendChild(titleSpan);

    item.appendChild(link);
    list.appendChild(item);
  });
  container.appendChild(list);

  const articleBody = document.querySelector("article");
  if (articleBody) {
    articleBody.appendChild(container);
  } else {
    console.log("Could not find article element to attach to.");
  }
}

const slug = getCurrentSlug();
loadRecommendations().then(data => {
  const matches = data[slug];
  renderRecommendations(matches);
});