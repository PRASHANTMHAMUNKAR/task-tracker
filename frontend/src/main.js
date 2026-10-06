import { cleanTitle, isValidTitle } from "./utils.js";

const list = document.getElementById("list");
const form = document.getElementById("form");
const input = document.getElementById("title");
const errorEl = document.getElementById("error");

async function api(path, options) {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.status === 204 ? null : res.json();
}

function render(tasks) {
  list.replaceChildren();
  for (const task of tasks) {
    const li = document.createElement("li");
    if (task.done) li.className = "done";

    const span = document.createElement("span");
    span.textContent = task.title;
    span.addEventListener("click", () => act(() => api(`/tasks/${task.id}`, { method: "PATCH" })));

    const del = document.createElement("button");
    del.textContent = "Delete";
    del.addEventListener("click", () => act(() => api(`/tasks/${task.id}`, { method: "DELETE" })));

    li.append(span, del);
    list.append(li);
  }
}

async function load() {
  render(await api("/tasks"));
}

async function act(fn) {
  errorEl.textContent = "";
  try {
    await fn();
    await load();
  } catch (e) {
    errorEl.textContent = e.message;
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!isValidTitle(input.value)) {
    errorEl.textContent = "Title must be 1-100 characters";
    return;
  }
  const title = cleanTitle(input.value);
  input.value = "";
  act(() => api("/tasks", { method: "POST", body: JSON.stringify({ title }) }));
});

act(load);
