cat > popup.js <<'EOF'
const BASE_URL = "http://127.0.0.1:8001";
const API_URL = `${BASE_URL}/api/positions/predict/`;

const $ = (id) => document.getElementById(id);

$("analyze").addEventListener("click", analyzePosition);
$("reviewGame").addEventListener("click", loadSavedGame);

$("openDashboard").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/` });
});

async function apiRequest(url, options = {}) {
  let response;

  try {
    response = await fetch(url, {
      ...options,
      signal: AbortSignal.timeout(15000)
    });
  } catch {
    throw new Error(
      "Cannot connect to Django. Start your server on port 8001 and try again."
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok || data.success === false) {
    throw new Error(data.message || data.detail || `Request failed (${response.status}).`);
  }

  return data;
}

async function checkServer() {
  const dot = $("serverDot");
  const label = $("serverStatus");

  try {
    await fetch(`${BASE_URL}/`, {
      signal: AbortSignal.timeout(3000)
    });

    dot.className = "dot online";
    label.textContent = "Django server connected";
  } catch {
    dot.className = "dot offline";
    label.textContent = "Django server offline";
  }
}

function showMessage(message) {
  $("status").textContent = message;
}

async function analyzePosition() {
  const button = $("analyze");
  const results = $("results");

  button.disabled = true;
  results.replaceChildren();
  showMessage("Analyzing with Stockfish...");

  const fen = $("fen").value.trim();

  try {
    const data = await apiRequest(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fen ? { fen } : {})
    });

    const candidates = data.candidates || data.best_moves || [];

    if (candidates.length === 0) {
      showMessage("No candidate moves were returned.");
      return;
    }

    candidates.forEach((candidate, index) => {
      const card = document.createElement("article");
      card.className = "move";

      const title = document.createElement("strong");
      title.textContent =
        `${index + 1}. ${candidate.san || candidate.uci || "Unknown move"}`;

      const evaluation = document.createElement("p");
      const score = candidate.evaluation?.centipawns;
      const mate = candidate.evaluation?.mate_in;

      if (mate !== null && mate !== undefined) {
        evaluation.textContent = `Mate in ${mate}`;
      } else if (score !== null && score !== undefined) {
        evaluation.textContent =
          `Evaluation: ${(score / 100).toFixed(2)} pawns`;
      } else {
        evaluation.textContent = "Evaluation unavailable";
      }

      card.append(title, evaluation);

      if (candidate.principal_variation) {
        const line = document.createElement("p");
        line.textContent = `Line: ${candidate.principal_variation}`;
        card.appendChild(line);
      }

      results.appendChild(card);
    });

    showMessage(`Analysis complete · ${candidates.length} candidate moves`);
  } catch (error) {
    showMessage(error.message);
  } finally {
    button.disabled = false;
  }
}

async function loadSavedGame() {
  const button = $("reviewGame");
  const results = $("gameResults");
  const gameId = Number($("gameId").value);

  results.replaceChildren();

  if (!Number.isInteger(gameId) || gameId < 1) {
    showMessage("Enter a valid saved game ID.");
    return;
  }

  button.disabled = true;
  showMessage("Loading saved game...");

  try {
    const data = await apiRequest(
      `${BASE_URL}/api/positions/games/${gameId}/`
    );

    const game = data.game;

    if (!game) {
      throw new Error("The API did not return saved-game details.");
    }

    const summary = document.createElement("article");
    summary.className = "move";

    const heading = document.createElement("strong");
    heading.textContent = `Game #${game.id}`;

    const details = document.createElement("p");
    details.textContent =
      `${game.white_player || "White"} vs ${game.black_player || "Black"}`;

    const result = document.createElement("p");
    result.textContent = `Result: ${game.result || "Not recorded"}`;

    const moveCount = document.createElement("p");
    moveCount.textContent = `Recorded moves: ${(game.moves || []).length}`;

    summary.append(heading, details, result, moveCount);
    results.appendChild(summary);

    const moves = document.createElement("p");
    moves.className = "muted";
    moves.textContent = (game.moves || [])
      .map((move) => `${move.move_number}. ${move.san}`)
      .join(" · ") || "No moves recorded.";

    results.appendChild(moves);

    const openButton = document.createElement("button");
    openButton.className = "secondary";
    openButton.textContent = "Open Dashboard to Continue Review";
    openButton.addEventListener("click", () => {
      chrome.tabs.create({ url: `${BASE_URL}/` });
    });
    results.appendChild(openButton);

    showMessage("Saved game loaded successfully.");
  } catch (error) {
    showMessage(error.message);
  } finally {
    button.disabled = false;
  }
}

checkServer();
EOF