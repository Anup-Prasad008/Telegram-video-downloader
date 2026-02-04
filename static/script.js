/* =====================================
   Telegram Video Downloader – UI Logic
   Author: You
   Level: Production / SaaS-grade
===================================== */

document.addEventListener("DOMContentLoaded", () => {
    const fetchForm = document.querySelector("form[action='/fetch']");
    const downloadForm = document.querySelector("form[action='/download']");
    const submitButtons = document.querySelectorAll("button");

    // Utility: disable all buttons
    const setLoadingState = (isLoading, message = "Processing...") => {
        submitButtons.forEach(btn => {
            btn.disabled = isLoading;
            btn.dataset.originalText ||= btn.textContent;
            btn.textContent = isLoading ? message : btn.dataset.originalText;
        });
    };

    // ================================
    // FETCH VIDEO HANDLER
    // ================================
    if (fetchForm) {
        fetchForm.addEventListener("submit", () => {
            setLoadingState(true, "Fetching...");
        });
    }

    // ================================
    // DOWNLOAD HANDLER
    // ================================
    if (downloadForm) {
        downloadForm.addEventListener("submit", () => {
            setLoadingState(true, "Downloading...");
        });
    }
});
