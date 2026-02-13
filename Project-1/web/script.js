function loadTodos() {
    const saved = localStorage.getItem("todos");
    return saved ? JSON.parse(saved) : [];
}

function saveTodos(todos) {
    localStorage.setItem("todos", JSON.stringify(todos));
}

function renderTodos() {
    const list = document.getElementById("todo-list");
    list.innerHTML = "";
    const todos = loadTodos();
    todos.forEach((todo, idx) => {
        const li = document.createElement("li");
        li.textContent = todo;
        const delBtn = document.createElement("button");
        delBtn.textContent = "Delete";
        delBtn.className = "delete-btn";
        delBtn.onclick = function() { deleteTodo(idx); };
        li.appendChild(delBtn);
        list.appendChild(li);
    });
}

function addTodo() {
    const input = document.getElementById("todo-input");
    const todoText = input.value.trim();
    if (!todoText) return;
    const todos = loadTodos();
    todos.push(todoText);
    saveTodos(todos);
    renderTodos();
    input.value = "";
}

function deleteTodo(idx) {
    const todos = loadTodos();
    todos.splice(idx, 1);
    saveTodos(todos);
    renderTodos();
}

document.getElementById("todo-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        addTodo();
    }
});

document.addEventListener("DOMContentLoaded", renderTodos);
