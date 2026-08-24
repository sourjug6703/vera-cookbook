const state = {
  recipes: [],
  activeSection: "All recipes",
  query: "",
  savedOnly: false,
  sort: "source",
  visible: 9,
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
const dialog = document.querySelector("#recipe-dialog");
const dialogContent = document.querySelector("#dialog-content");
const sourceDialog = document.querySelector("#source-dialog");
const sourceContent = document.querySelector("#source-content");
const clearSearch = document.querySelector("#clear-search");
let recipeTrigger = null;
let sourceTrigger = null;

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
    button.addEventListener("click", () => { state.activeSection = section; state.visible = 9; render(); });
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
  image.innerHTML = `${recipePicture(recipe, "(max-width: 470px) 100vw, (max-width: 780px) 50vw, (max-width: 1120px) 33vw, 340px", "card-art")}<span class="collection-study">${recipe.illustration ? "Recipe study" : "Collection study"} · ${escapeHtml(recipe.section)}</span>`;
  image.addEventListener("click", open);
  title.textContent = recipe.title;
  fragment.querySelector(".card-order").textContent = `Recipe ${String(recipe.sourceOrder).padStart(3, "0")} · ${recipe.section}`;
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
    <div class="feature-actions"><button class="feature-open" type="button">View full recipe</button><button class="feature-save" type="button" aria-label="Save featured recipe"></button></div>`;
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
}

function toggleSaved(id) {
  state.saved.has(id) ? state.saved.delete(id) : state.saved.add(id);
  render();
}

function openRecipe(recipe, trigger) {
  recipeTrigger = trigger || recipeTrigger;
  const ingredientItems = recipe.ingredients.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>No ingredient list is printed for this source record.</li>";
  const instructionItems = recipe.instructions.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>No preparation text is printed for this source record.</li>";
  const notes = recipe.notes.length ? `<section><h3>Notes from the cookbook</h3><ul>${recipe.notes.map((note) => `<li>${escapeHtml(note)}</li>`).join("")}</ul></section>` : "";
  const isSaved = state.saved.has(recipe.id);
  const sourceAction = recipe.sourcePreview?.pages?.length
    ? '<button class="source-open" type="button">View source</button>'
    : "";
  dialogContent.innerHTML = `
    <article class="dialog-recipe">
      <div class="dialog-art-field" aria-hidden="true">${recipePicture(recipe, "(max-width: 780px) calc(100vw - 2rem), 900px", "dialog-art")}</div>
      <div class="dialog-recipe-body">
        <p class="dialog-eyeline">Recipe ${String(recipe.sourceOrder).padStart(3, "0")} · ${escapeHtml(recipe.section)}</p>
        <h2 id="dialog-title">${escapeHtml(recipe.title)}</h2>
        <p class="dialog-meta">${escapeHtml(recipe.yieldTime.join(" · ") || "Source-checked family recipe")} · Source page ${escapeHtml(recipe.sourcePages.join(", ") || "not labeled")}</p>
        <div class="dialog-actions"><button class="dialog-save" type="button" aria-pressed="${isSaved}" aria-label="${isSaved ? "Remove" : "Save"} ${escapeHtml(recipe.title)}">${isSaved ? "Saved for the table" : "Save for the table"}</button>${sourceAction}</div>
        <div class="dialog-grid"><section><h3>Ingredients</h3><ul>${ingredientItems}</ul></section><section><h3>Preparation</h3><ol>${instructionItems}</ol>${notes}</section></div>
        <p class="source-stamp">Transcription is shown as preserved from the source-checked record. Recipe ID: ${escapeHtml(recipe.id)}.</p>
      </div>
    </article>`;
  const dialogSave = dialogContent.querySelector(".dialog-save");
  dialogSave.addEventListener("click", () => {
    state.saved.has(recipe.id) ? state.saved.delete(recipe.id) : state.saved.add(recipe.id);
    render();
    const saved = state.saved.has(recipe.id);
    dialogSave.setAttribute("aria-pressed", String(saved));
    dialogSave.setAttribute("aria-label", `${saved ? "Remove" : "Save"} ${recipe.title}`);
    dialogSave.textContent = saved ? "Saved for the table" : "Save for the table";
  });
  dialogContent.querySelector(".source-open")?.addEventListener("click", (event) => openSource(recipe, event.currentTarget));
  if (!dialog.open) dialog.showModal();
}

function openSource(recipe, trigger) {
  const pages = recipe.sourcePreview?.pages || [];
  if (!pages.length) return;

  sourceTrigger = trigger;
  sourceContent.innerHTML = `
    <article class="source-recipe">
      <p class="dialog-eyeline">${escapeHtml(recipe.sourcePreview.label)} · recipe source</p>
      <h2 id="source-dialog-title">${escapeHtml(recipe.title)}</h2>
      <p class="source-dialog-note">This grayscale, deskewed reading rendition is derived from the retained scan used for this source-checked recipe. The untouched original remains available from each page.</p>
      <div class="source-pages">${pages.map((page) => `
        <figure class="source-figure">
          <picture>
            <source type="image/webp" srcset="${escapeHtml(sourceReaderWebp(page.image))}" />
            <img src="${escapeHtml(page.image)}" alt="Scanned cookbook page for ${escapeHtml(recipe.title)}" loading="lazy" decoding="async" />
          </picture>
          <figcaption>PDF page ${escapeHtml(page.pdfPage)} · printed page ${escapeHtml(page.printedPage || "not labeled")} · <a href="${escapeHtml(page.originalImage)}" target="_blank" rel="noopener">Open original scan</a></figcaption>
        </figure>`).join("")}</div>
    </article>`;
  if (!sourceDialog.open) sourceDialog.showModal();
}

search.addEventListener("input", (event) => { state.query = event.target.value; state.visible = 9; render(); });
loadMore.addEventListener("click", () => { state.visible += 9; render(); });
clearSearch.addEventListener("click", () => { search.value = ""; state.query = ""; state.savedOnly = false; render(); search.focus(); });
savedFilter.addEventListener("click", () => { state.savedOnly = !state.savedOnly; state.visible = 9; render(); });
document.querySelector("#sort-control").addEventListener("click", () => { state.sort = state.sort === "source" ? "title" : "source"; document.querySelector("#sort-label").textContent = state.sort === "source" ? "Cookbook order" : "Title A–Z"; render(); });
document.querySelector("#dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
dialog.addEventListener("close", () => {
  if (recipeTrigger?.isConnected) {
    recipeTrigger.focus();
    return;
  }
  const recipeId = recipeTrigger?.dataset.openRecipeId;
  document.querySelector(`[data-open-recipe-id="${recipeId}"]`)?.focus();
});
document.querySelector("#source-close").addEventListener("click", () => sourceDialog.close());
sourceDialog.addEventListener("click", (event) => { if (event.target === sourceDialog) sourceDialog.close(); });
sourceDialog.addEventListener("close", () => sourceTrigger?.focus());

fetch("data/recipes.json")
  .then((response) => response.ok ? response.json() : Promise.reject(new Error("Could not load the recipe collection.")))
  .then((payload) => { state.recipes = payload.recipes; render(); })
  .catch(() => { summary.textContent = "The recipe collection could not be loaded."; emptyState.hidden = false; emptyState.querySelector("p").textContent = "Start the local reader through its project server, then try again."; });
