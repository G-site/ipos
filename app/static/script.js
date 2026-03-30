const popupLayer = document.getElementById("popup-layer");
const popupCard = document.getElementById("popup-card");
const popupBody = document.getElementById("popup-body");
const popupClose = document.getElementById("popup-close");

function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function renderPopup(type, value) {
    if (type === "image") {
        return `<img src="${escapeHtml(value)}" alt="Ілюстрація до навчального матеріалу">`;
    }

    if (type === "youtube") {
        return `<iframe src="${escapeHtml(value)}" title="Відео матеріал" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
    }

    return `<p>${escapeHtml(value)}</p>`;
}

function positionPopup(trigger) {
    const rect = trigger.getBoundingClientRect();
    const cardWidth = popupCard.offsetWidth;
    const gap = 12;
    let left = rect.left;
    let top = rect.bottom + gap;

    if (left + cardWidth > window.innerWidth - 12) {
        left = window.innerWidth - cardWidth - 12;
    }

    if (top + popupCard.offsetHeight > window.innerHeight - 12) {
        top = rect.top - popupCard.offsetHeight - gap;
    }

    if (top < 12) {
        top = 12;
    }

    popupCard.style.left = `${Math.max(12, left)}px`;
    popupCard.style.top = `${top}px`;
}

function closePopup() {
    popupLayer.hidden = true;
    popupBody.innerHTML = "";
    popupCard.style.left = "";
    popupCard.style.top = "";
}

function openPopup(trigger) {
    popupBody.innerHTML = renderPopup(
        trigger.dataset.popupType || "comment",
        trigger.dataset.popupValue || "",
    );

    popupLayer.hidden = false;
    positionPopup(trigger);
}

document.querySelectorAll(".inline-popup-trigger").forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
        event.stopPropagation();

        const isSameTarget =
            !popupLayer.hidden &&
            popupBody.dataset.currentValue === (trigger.dataset.popupValue || "");

        popupBody.dataset.currentValue = trigger.dataset.popupValue || "";

        if (isSameTarget) {
            closePopup();
            return;
        }

        openPopup(trigger);
    });
});

popupClose?.addEventListener("click", closePopup);

document.addEventListener("click", (event) => {
    if (popupLayer.hidden) {
        return;
    }

    if (popupCard.contains(event.target)) {
        return;
    }

    closePopup();
});

window.addEventListener("scroll", () => {
    if (!popupLayer.hidden) {
        closePopup();
    }
}, { passive: true });

window.addEventListener("resize", () => {
    if (!popupLayer.hidden) {
        closePopup();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !popupLayer.hidden) {
        closePopup();
    }
});
