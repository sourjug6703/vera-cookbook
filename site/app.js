const state = {
  recipes: [],
  activeSection: "All recipes",
  query: "",
  savedOnly: false,
  sort: "source",
  visible: 9,
  openRecipeId: null,
  sourceOpen: false,
  saved: new Set(JSON.parse(localStorage.getItem("vera-cookbook-saved") || "[]"))
};

const sections = ["All recipes", "Meats & poultry", "Fish", "Sides & dumplings", "Soups", "Baking & sweets"];
const artFor = {
  "Meats & poultry": "assets/meats.webp",
  Fish: "assets/fish.webp",
  "Sides & dumplings": "assets/sides.webp",
  Soups: "assets/soups.webp",
  "Baking & sweets": "assets/sweets.webp"
};

const grid = document.querySelector("#recipe-grid");
const template = document.querySelector("#recipe-card-template");
const tabs = document.querySelector("#collection-tabs");
const search = document.querySelector("#recipe-search");
const summary = document.querySelector("#result-summary");
const loadMore = document.querySelector("#load-more");
const emptyState = document.querySelector("#empty-state");
const feature = document.querySelector("#featured-recipe");
const savedFilter = document.querySelector("#saved-filter");
const savedCount = document.querySelector("#saved-count");
const collectionView = document.querySelector("#collection-view");
const recipeReader = document.querySelector("#recipe-reader");
const clearSearch = document.querySelector("#clear-search");
let recipeTrigger = null;

function escapeHtml(value = "") {
  return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character]));
}

function deliverySourceSet(pngPath, format) {
  const stem = pngPath.split("/").pop().replace(/\.png$/i, "");
  return [480, 720, 1080]
    .map((width) => `assets/delivery/recipes/${format}/${stem}-${width}.${format} ${width}w`)
    .join(", ");
}

function deliveryImage(pngPath, format = "webp", width = 1080) {
  const stem = pngPath.split("/").pop().replace(/\.png$/i, "");
  return `assets/delivery/recipes/${format}/${stem}-${width}.${format}`;
}

function recipePicture(recipe, sizes, className = "") {
  const illustration = recipe.illustration?.image;
  if (!illustration) {
    return `<img class="${className}" src="${escapeHtml(artFor[recipe.section])}" alt="" decoding="async" />`;
  }
  return `<picture class="${className}">
    <source type="image/avif" srcset="${escapeHtml(deliverySourceSet(illustration, "avif"))}" sizes="${escapeHtml(sizes)}" />
    <source type="image/webp" srcset="${escapeHtml(deliverySourceSet(illustration, "webp"))}" sizes="${escapeHtml(sizes)}" />
    <img src="${escapeHtml(deliveryImage(illustration))}" alt="" loading="lazy" decoding="async" />
  </picture>`;
}

function sourceReaderWebp(pngPath) {
  return pngPath
    .replace("assets/source-viewer/", "assets/delivery/source-reader-webp/")
    .replace(/\.png$/i, ".webp");
}

function persistSaved() {
  localStorage.setItem("vera-cookbook-saved", JSON.stringify([...state.saved]));
  savedCount.textContent = state.saved.size;
  savedCount.classList.toggle("is-visible", state.saved.size > 0);
}

function recipeMatches(recipe) {
  const needle = state.query.trim().toLocaleLowerCase();
  const haystack = [recipe.title, recipe.titleEnglish, recipe.titleCzech, recipe.section, ...recipe.ingredients].filter(Boolean).join(" ").toLocaleLowerCase();
  return (state.activeSection === "All recipes" || recipe.section === state.activeSection) &&
    (!state.savedOnly || state.saved.has(recipe.id)) &&
    (!needle || haystack.includes(needle));
}

function filteredRecipes() {
  const matching = state.recipes.filter(recipeMatches);
  return state.sort === "title" ? matching.sort((a, b) => a.title.localeCompare(b.title)) : matching.sort((a, b) => a.sourceOrder - b.sourceOrder);
}

function createTabs() {
  tabs.replaceChildren(...sections.map((section) => {
    const button = document.createElement("button");
    button.className = "collection-tab";
    button.type = "button";
    button.dataset.section = section;
    button.setAttribute("aria-pressed", String(section === state.activeSection));
    const count = section === "All recipes" ? state.recipes.length : state.recipes.filter((recipe) => recipe.section === section).length;
    button.innerHTML = `<span>${escapeHtml(section)}</span><span class="tab-count">${count}</span>`;
    button.addEventListener("click", () => { state.activeSection = section; state.visible = 9; state.openRecipeId = null; state.sourceOpen = false; render(); });
    return button;
  }));
}

function cardFor(recipe) {
  const fragment = template.content.cloneNode(true);
  const image = fragment.querySelector(".card-image");
  const title = fragment.querySelector("h2");
  const meta = fragment.querySelector(".card-meta");
  const save = fragment.querySelector(".save-recipe");
  const open = (event) => openRecipe(recipe, event.currentTarget);
  image.dataset.openRecipeId = recipe.id;
  fragment.querySelector(".open-recipe").dataset.openRecipeId = recipe.id;
  image.innerHTML = recipePicture(recipe, "(max-width: 500px) 100vw, (max-width: 980px) 45vw, 22vw", "card-art");
  image.addEventListener("click", open);
  title.textContent = recipe.titleEnglish || recipe.title;
  if (recipe.titleCzech) {
    const czechName = document.createElement("span");
    czechName.className = "card-czech-name";
    czechName.textContent = recipe.titleCzech;
    title.append(czechName);
  }
  const order = fragment.querySelector(".card-order");
  const section = document.createElement("strong");
  const number = document.createElement("span");
  section.textContent = recipe.section;
  number.textContent = `Recipe ${String(recipe.sourceOrder).padStart(3, "0")}`;
  order.append(section, number);
  meta.textContent = recipe.yieldTime[0] || "Source-checked family recipe";
  fragment.querySelector(".open-recipe").addEventListener("click", open);
  save.setAttribute("aria-pressed", String(state.saved.has(recipe.id)));
  save.setAttribute("aria-label", `${state.saved.has(recipe.id) ? "Remove" : "Save"} ${recipe.title}`);
  save.addEventListener("click", () => toggleSaved(recipe.id));
  return fragment;
}

function renderFeature(recipe) {
  if (!recipe) {
    feature.innerHTML = `<div class="feature-empty"><p>No recipe is on the table for this view.</p><button class="feature-reset" type="button">Return to the collection</button></div>`;
    feature.querySelector(".feature-reset").addEventListener("click", () => {
      state.activeSection = "All recipes";
      state.query = "";
      state.savedOnly = false;
      search.value = "";
      render();
      search.focus();
    });
    return;
  }
  const ingredients = recipe.ingredients.slice(0, 5).map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  feature.innerHTML = `
    <div class="featured-visual">${recipePicture(recipe, "(max-width: 780px) 100vw, (max-width: 1120px) 220px, 330px", "featured-art")}</div>
    <div>
      <h2 class="featured-title">${escapeHtml(recipe.title)}</h2>
      <p class="feature-meta"><span>${escapeHtml(recipe.yieldTime[0] || "Source-checked recipe")}</span><span>${escapeHtml(recipe.section)}</span></p>
    </div>
    <div>
      <h3 class="ingredients-label">Ingredients preview</h3>
      <ul class="ingredient-preview">${ingredients || "<li>Ingredients are preserved in the full recipe.</li>"}</ul>
    </div>
    <div class="feature-actions"><button class="feature-open" type="button">View full recipe</button><button class="feature-save" type="button" aria-label="Save featured recipe"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-3.8L6 21V3Z"></path></svg></button></div>`;
  const featureOpen = feature.querySelector(".feature-open");
  featureOpen.dataset.openRecipeId = recipe.id;
  featureOpen.addEventListener("click", (event) => openRecipe(recipe, event.currentTarget));
  const saveButton = feature.querySelector(".feature-save");
  saveButton.setAttribute("aria-pressed", String(state.saved.has(recipe.id)));
  saveButton.addEventListener("click", () => toggleSaved(recipe.id));
}

function render() {
  createTabs();
  const matching = filteredRecipes();
  const display = matching.slice(0, state.visible);
  grid.replaceChildren(...display.map(cardFor));
  emptyState.hidden = matching.length !== 0;
  loadMore.hidden = matching.length <= display.length;
  const collectionLabel = state.savedOnly
    ? " in saved recipes"
    : state.activeSection === "All recipes" ? " in the collection" : ` in ${state.activeSection}`;
  summary.textContent = `${matching.length} ${matching.length === 1 ? "recipe" : "recipes"}${collectionLabel}`;
  if (!matching.length) {
    emptyState.querySelector("p").textContent = state.savedOnly && !state.saved.size
      ? "No saved recipes yet."
      : "No recipe matches this view yet.";
    clearSearch.textContent = state.savedOnly ? "Browse all recipes" : "Clear search";
  }
  renderFeature(matching[0] || null);
  savedFilter.setAttribute("aria-pressed", String(state.savedOnly));
  persistSaved();
  const openRecipe = state.recipes.find((recipe) => recipe.id === state.openRecipeId);
  if (openRecipe) {
    state.sourceOpen ? renderSource(openRecipe) : renderRecipe(openRecipe);
    collectionView.hidden = true;
    recipeReader.hidden = false;
  } else {
    state.openRecipeId = null;
    collectionView.hidden = false;
    recipeReader.hidden = true;
  }
}

function toggleSaved(id) {
  state.saved.has(id) ? state.saved.delete(id) : state.saved.add(id);
  render();
}

function openRecipe(recipe, trigger) {
  recipeTrigger = trigger || recipeTrigger;
  state.openRecipeId = recipe.id;
  state.sourceOpen = false;
  render();
  recipeReader.scrollIntoView({ block: "start", behavior: "auto" });
  recipeReader.querySelector("#recipe-reader-title")?.focus({ preventScroll: true });
}

function renderRecipe(recipe) {
  const ingredientItems = recipe.ingredients.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>No ingredient list is printed for this source record.</li>";
  const instructionItems = recipe.instructions.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>No preparation text is printed for this source record.</li>";
  const notes = recipe.notes.length ? `<section><h3>Notes from the cookbook</h3><ul>${recipe.notes.map((note) => `<li>${escapeHtml(note)}</li>`).join("")}</ul></section>` : "";
  const isSaved = state.saved.has(recipe.id);
  const sourceAction = recipe.sourcePreview?.pages?.length
    ? '<button class="source-open" type="button">View source</button>'
    : "";
  const history = recipe.history
    ? `<aside class="history-nugget" aria-label="History and kitchen context">
        <p class="history-kicker">History &amp; kitchen context</p>
        <h3>${escapeHtml(recipe.history.label)}</h3>
        <p>${escapeHtml(recipe.history.note)}</p>
        <p class="history-scope">${escapeHtml(recipe.history.scope)}</p>
        <ul class="history-citations">${recipe.history.citations.map((citation) => `<li><a href="${escapeHtml(citation.url)}" target="_blank" rel="noopener">${escapeHtml(citation.title)}</a><span>${escapeHtml(citation.publisher)} · accessed ${escapeHtml(citation.accessedOn)}</span></li>`).join("")}</ul>
      </aside>`
    : "";
  const recipeTitle = `${escapeHtml(recipe.titleEnglish || recipe.title)}${recipe.titleCzech ? `<span class="reader-czech-name">${escapeHtml(recipe.titleCzech)}</span>` : ""}`;
  recipeReader.innerHTML = `
    <article class="reader-recipe">
      <div class="reader-topline">
        <button class="reader-back" type="button"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m14.5 5-7 7 7 7M8 12h9"></path></svg>Back to collection</button>
        <p>Recipe ${String(recipe.sourceOrder).padStart(3, "0")} · ${escapeHtml(recipe.section)}</p>
      </div>
      <div class="reader-art-field" aria-hidden="true">${recipePicture(recipe, "(max-width: 780px) calc(100vw - 2rem), 900px", "reader-art")}</div>
      <div class="reader-recipe-body">
        <h1 id="recipe-reader-title" tabindex="-1">${recipeTitle}</h1>
        <p class="reader-meta">${escapeHtml(recipe.yieldTime.join(" · ") || "Source-checked family recipe")} · Source page ${escapeHtml(recipe.sourcePages.join(", ") || "not labeled")}</p>
        ${history}
        <div class="reader-actions"><button class="reader-save" type="button" aria-pressed="${isSaved}" aria-label="${isSaved ? "Remove" : "Save"} ${escapeHtml(recipe.title)}">${isSaved ? "Saved for the table" : "Save for the table"}</button>${sourceAction}</div>
        <div class="reader-grid"><section><h2>Ingredients</h2><ul>${ingredientItems}</ul></section><section><h2>Preparation</h2><ol>${instructionItems}</ol>${notes}</section></div>
        <p class="source-stamp">Transcription is shown as preserved from the source-checked record. Recipe ID: ${escapeHtml(recipe.id)}.</p>
      </div>
    </article>`;
  recipeReader.querySelector(".reader-back").addEventListener("click", () => closeRecipe());
  const readerSave = recipeReader.querySelector(".reader-save");
  readerSave.addEventListener("click", () => {
    state.saved.has(recipe.id) ? state.saved.delete(recipe.id) : state.saved.add(recipe.id);
    render();
    const saved = state.saved.has(recipe.id);
    readerSave.setAttribute("aria-pressed", String(saved));
    readerSave.setAttribute("aria-label", `${saved ? "Remove" : "Save"} ${recipe.title}`);
    readerSave.textContent = saved ? "Saved for the table" : "Save for the table";
  });
  recipeReader.querySelector(".source-open")?.addEventListener("click", () => openSource(recipe));
}

function closeRecipe() {
  const recipeId = state.openRecipeId;
  state.openRecipeId = null;
  state.sourceOpen = false;
  render();
  const selector = `[data-open-recipe-id="${recipeId}"]`;
  const nextTrigger = recipeTrigger?.isConnected ? recipeTrigger : document.querySelector(selector);
  nextTrigger?.focus({ preventScroll: true });
}

function openSource(recipe) {
  const pages = recipe.sourcePreview?.pages || [];
  if (!pages.length) return;

  state.sourceOpen = true;
  render();
  recipeReader.scrollIntoView({ block: "start", behavior: "auto" });
  recipeReader.querySelector("#source-reader-title")?.focus({ preventScroll: true });
}

function renderSource(recipe) {
  const pages = recipe.sourcePreview?.pages || [];
  recipeReader.innerHTML = `
    <article class="source-reader">
      <div class="reader-topline">
        <button class="reader-back source-back" type="button"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m14.5 5-7 7 7 7M8 12h9"></path></svg>Back to recipe</button>
        <p>Recipe ${String(recipe.sourceOrder).padStart(3, "0")} · source pages</p>
      </div>
      <div class="source-reader-body">
        <h1 id="source-reader-title" tabindex="-1">Source pages for ${escapeHtml(recipe.titleEnglish || recipe.title)}</h1>
        <p class="source-reader-note">This grayscale, deskewed reading rendition is derived from the retained scan used for this source-checked recipe. The untouched original remains available from each page.</p>
      <div class="source-pages">${pages.map((page) => `
        <figure class="source-figure">
          <picture>
            <source type="image/webp" srcset="${escapeHtml(sourceReaderWebp(page.image))}" />
            <img src="${escapeHtml(page.image)}" alt="Scanned cookbook page for ${escapeHtml(recipe.title)}" loading="lazy" decoding="async" />
          </picture>
          <figcaption>PDF page ${escapeHtml(page.pdfPage)} · printed page ${escapeHtml(page.printedPage || "not labeled")} · <a href="${escapeHtml(page.originalImage)}" target="_blank" rel="noopener">Open original scan</a></figcaption>
        </figure>`).join("")}</div>
      </div>
    </article>`;
  recipeReader.querySelector(".source-back").addEventListener("click", closeSource);
}

function closeSource() {
  state.sourceOpen = false;
  render();
  recipeReader.scrollIntoView({ block: "start", behavior: "auto" });
  recipeReader.querySelector("#recipe-reader-title")?.focus({ preventScroll: true });
}

search.addEventListener("input", (event) => { state.query = event.target.value; state.visible = 9; state.openRecipeId = null; state.sourceOpen = false; render(); });
loadMore.addEventListener("click", () => { state.visible += 9; render(); });
clearSearch.addEventListener("click", () => { search.value = ""; state.query = ""; state.savedOnly = false; state.openRecipeId = null; state.sourceOpen = false; render(); search.focus(); });
savedFilter.addEventListener("click", () => { state.savedOnly = !state.savedOnly; state.visible = 9; state.openRecipeId = null; state.sourceOpen = false; render(); });
document.querySelector("#sort-control").addEventListener("click", () => { state.sort = state.sort === "source" ? "title" : "source"; document.querySelector("#sort-label").textContent = state.sort === "source" ? "Cookbook order" : "Title A–Z"; render(); });
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && state.sourceOpen) {
    event.preventDefault();
    closeSource();
  } else if (event.key === "Escape" && state.openRecipeId) {
    event.preventDefault();
    closeRecipe();
  }
});

fetch("data/recipes.json")
  .then((response) => response.ok ? response.json() : Promise.reject(new Error("Could not load the recipe collection.")))
  .then((payload) => { state.recipes = payload.recipes; render(); })
  .catch(() => { summary.textContent = "The recipe collection could not be loaded."; emptyState.hidden = false; emptyState.querySelector("p").textContent = "Start the local reader through its project server, then try again."; });
