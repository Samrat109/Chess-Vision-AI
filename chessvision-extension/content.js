(() => {
  const url = window.location.href;

  const isChessCom = window.location.hostname === "www.chess.com";

  const isAnalysisPage =
    window.location.pathname.includes("/analysis") ||
    window.location.pathname.includes("/game/computer") ||
    window.location.pathname.includes("/game/live/");

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "CHECK_PAGE") {
      sendResponse({
        website: isChessCom ? "Chess.com" : "Other",
        url: url,
        analysisPage: isChessCom && isAnalysisPage
      });
    }
  });
})();
