// ChessVision AI
// Reads explicit FEN values from permitted Chess.com analysis/review pages.
// It does not monitor live rated games.

function isValidFenFormat(fen) {
    if (typeof fen !== "string") return false;

    const parts = fen.trim().split(/\s+/);

    if (parts.length !== 6) return false;

    const ranks = parts[0].split("/");

    if (ranks.length !== 8) return false;

    return /^[wb]$/.test(parts[1]) &&
        /^(?:-|K?Q?k?q?)$/.test(parts[2]) &&
        /^(?:-|[a-h][36])$/.test(parts[3]);
}

function findFenInPage() {
    const selectors = [
        "[data-fen]",
        "[fen]",
        "chess-board[fen]",
        "[data-position]"
    ];

    for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);

        for (const element of elements) {
            const fen =
                element.getAttribute("data-fen") ||
                element.getAttribute("fen") ||
                element.getAttribute("data-position");

            if (fen && isValidFenFormat(fen)) {
                return fen.trim();
            }
        }
    }

    return null;
}

chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (message.action === "GET_CHESS_POSITION") {
            const fen = findFenInPage();

            if (fen) {
                sendResponse({
                    success: true,
                    fen: fen,
                    page: location.href
                });
            } else {
                sendResponse({
                    success: false,
                    message:
                        "No explicit FEN found. We need to inspect the Chess.com analysis board structure."
                });
            }
        }

        return true;
    }
);