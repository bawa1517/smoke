const STORAGE_KEY = "taskwell-tasks";

const starterTasks = [
  { id: 1, text: "Map out the day", completed: false },
  { id: 2, text: "Drink a glass of water", completed: true },
  { id: 3, text: "Reply to one important message", completed: false }
];

let tasks = loadTasks();
let activeFilter = "all";

const taskForm = document.querySelector("#task-form");
const taskInput = document.querySelector("#task-input");
const taskList = document.querySelector("#task-list");
const emptyState = document.querySelector("#empty-state");

function loadTasks() {
  try {
    const savedTasks = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return Array.isArray(savedTasks) ? savedTasks : starterTasks;
  } catch {
    return starterTasks;
  }
}

function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

function render() {
  const visibleTasks = tasks.filter((task) => {
    if (activeFilter === "active") return !task.completed;
    if (activeFilter === "completed") return task.completed;
    return true;
  });

  taskList.innerHTML = visibleTasks.map((task, index) => `
    <article class="task-item ${task.completed ? "completed" : ""}" style="animation-delay: ${index * 35}ms">
      <button class="check-button" type="button" data-action="toggle" data-id="${task.id}" aria-label="Mark ${escapeHtml(task.text)} as ${task.completed ? "open" : "done"}"></button>
      <span class="task-text">${escapeHtml(task.text)}</span>
      <button class="delete-button" type="button" data-action="delete" data-id="${task.id}" aria-label="Delete ${escapeHtml(task.text)}">x</button>
    </article>
  `).join("");

  emptyState.hidden = visibleTasks.length > 0;
  emptyState.textContent = activeFilter === "completed" ? "Nothing completed yet." : "No tasks here. Add one above.";

  const completedCount = tasks.filter((task) => task.completed).length;
  const activeCount = tasks.length - completedCount;
  const progress = tasks.length ? Math.round((completedCount / tasks.length) * 100) : 0;
  document.querySelector("#all-count").textContent = tasks.length;
  document.querySelector("#active-count").textContent = activeCount;
  document.querySelector("#completed-count").textContent = completedCount;
  document.querySelector("#progress-value").textContent = `${progress}%`;
  document.querySelector("#progress-ring").style.background = `conic-gradient(var(--coral) ${progress * 3.6}deg, var(--line) 0deg)`;
  document.querySelector("#progress-ring").setAttribute("aria-label", `${progress} percent complete`);
  document.querySelector("#focus-title").textContent = progress === 100 ? "You did it." : progress > 0 ? "Keep the rhythm." : "A fresh start.";
  document.querySelector("#focus-copy").textContent = progress === 100 ? "Everything on your list is done for today." : `${activeCount} ${activeCount === 1 ? "thing" : "things"} waiting for your attention.`;
  document.querySelector("#streak-count").textContent = completedCount ? "1" : "0";
  document.querySelectorAll(".filter-button").forEach((button) => button.classList.toggle("active", button.dataset.filter === activeFilter));
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[character]);
}

taskForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = taskInput.value.trim();
  if (!text) return;
  tasks.unshift({ id: Date.now(), text, completed: false });
  saveTasks();
  taskInput.value = "";
  activeFilter = "all";
  render();
  taskInput.focus();
});

taskList.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  const taskId = Number(button.dataset.id);
  if (button.dataset.action === "toggle") {
    tasks = tasks.map((task) => task.id === taskId ? { ...task, completed: !task.completed } : task);
  } else if (button.dataset.action === "delete") {
    tasks = tasks.filter((task) => task.id !== taskId);
  }
  saveTasks();
  render();
});

document.querySelector(".filters").addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  activeFilter = button.dataset.filter;
  render();
});

document.querySelector("#clear-completed").addEventListener("click", () => {
  tasks = tasks.filter((task) => !task.completed);
  saveTasks();
  render();
});

document.querySelector("#current-date").textContent = new Intl.DateTimeFormat("en-US", {
  weekday: "long", month: "long", day: "numeric"
}).format(new Date());

render();