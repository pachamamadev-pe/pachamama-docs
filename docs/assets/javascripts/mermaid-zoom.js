(function () {
  const READY_ATTR = "data-zoom-ready";
  const BUTTON_CLASS = "mermaid-zoom-button";
  const MODAL_ID = "mermaid-zoom-modal";
  const MIN_SCALE = 0.35;
  const MAX_SCALE = 6;
  const ZOOM_STEP = 0.2;

  let modal;
  let titleElement;
  let stageElement;
  let canvasElement;
  let viewportElement;
  let closeButton;
  let zoomInButton;
  let zoomOutButton;
  let resetButton;
  let lastPointerX = 0;
  let lastPointerY = 0;
  let isDragging = false;
  let dragOriginX = 0;
  let dragOriginY = 0;

  const state = {
    scale: 1,
    x: 0,
    y: 0,
    activeSource: null,
  };

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function ensureModal() {
    if (modal) {
      return;
    }

    modal = document.createElement("div");
    modal.id = MODAL_ID;
    modal.className = "mermaid-zoom-modal";
    modal.innerHTML = [
      '<div class="mermaid-zoom-dialog" role="dialog" aria-modal="true" aria-label="Diagrama ampliado">',
      '  <div class="mermaid-zoom-toolbar">',
      '    <div class="mermaid-zoom-title">Diagrama Mermaid</div>',
      '    <div class="mermaid-zoom-actions">',
      '      <button type="button" data-action="zoom-out">-</button>',
      '      <button type="button" data-action="zoom-in">+</button>',
      '      <button type="button" data-action="reset">Reset</button>',
      '      <button type="button" data-action="close">Cerrar</button>',
      '    </div>',
      '  </div>',
      '  <div class="mermaid-zoom-stage">',
      '    <div class="mermaid-zoom-canvas">',
      '      <div class="mermaid-zoom-viewport"></div>',
      '    </div>',
      '  </div>',
      '  <div class="mermaid-zoom-hint">Rueda del mouse para zoom, arrastra para mover, ESC para cerrar.</div>',
      '</div>',
    ].join("");

    document.body.appendChild(modal);

    titleElement = modal.querySelector(".mermaid-zoom-title");
    stageElement = modal.querySelector(".mermaid-zoom-stage");
    canvasElement = modal.querySelector(".mermaid-zoom-canvas");
    viewportElement = modal.querySelector(".mermaid-zoom-viewport");
    closeButton = modal.querySelector('[data-action="close"]');
    zoomInButton = modal.querySelector('[data-action="zoom-in"]');
    zoomOutButton = modal.querySelector('[data-action="zoom-out"]');
    resetButton = modal.querySelector('[data-action="reset"]');

    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        closeModal();
      }
    });

    closeButton.addEventListener("click", closeModal);
    zoomInButton.addEventListener("click", function () {
      zoomBy(ZOOM_STEP);
    });
    zoomOutButton.addEventListener("click", function () {
      zoomBy(-ZOOM_STEP);
    });
    resetButton.addEventListener("click", resetView);

    stageElement.addEventListener("wheel", function (event) {
      event.preventDefault();
      const delta = event.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP;
      const rect = stageElement.getBoundingClientRect();
      lastPointerX = event.clientX - rect.left - rect.width / 2;
      lastPointerY = event.clientY - rect.top - rect.height / 2;
      zoomBy(delta);
    }, { passive: false });

    stageElement.addEventListener("pointerdown", function (event) {
      if (!viewportElement.firstElementChild) {
        return;
      }

      isDragging = true;
      dragOriginX = event.clientX - state.x;
      dragOriginY = event.clientY - state.y;
      stageElement.classList.add("is-dragging");
      stageElement.setPointerCapture(event.pointerId);
    });

    stageElement.addEventListener("pointermove", function (event) {
      if (!isDragging) {
        return;
      }
      state.x = event.clientX - dragOriginX;
      state.y = event.clientY - dragOriginY;
      applyTransform();
    });

    stageElement.addEventListener("pointerup", stopDragging);
    stageElement.addEventListener("pointercancel", stopDragging);

    document.addEventListener("keydown", function (event) {
      if (!modal || !modal.classList.contains("is-open")) {
        return;
      }

      if (event.key === "Escape") {
        closeModal();
      } else if (event.key === "+" || event.key === "=") {
        zoomBy(ZOOM_STEP);
      } else if (event.key === "-") {
        zoomBy(-ZOOM_STEP);
      } else if (event.key.toLowerCase() === "0") {
        resetView();
      }
    });
  }

  function stopDragging(event) {
    if (!isDragging) {
      return;
    }
    isDragging = false;
    stageElement.classList.remove("is-dragging");
    if (event && stageElement.hasPointerCapture(event.pointerId)) {
      stageElement.releasePointerCapture(event.pointerId);
    }
  }

  function applyTransform() {
    viewportElement.style.transform = `translate(${state.x}px, ${state.y}px) scale(${state.scale})`;
  }

  function resetView() {
    state.scale = 1;
    state.x = 0;
    state.y = 0;
    applyTransform();
  }

  function zoomBy(delta) {
    const previousScale = state.scale;
    const nextScale = clamp(Number((state.scale + delta).toFixed(2)), MIN_SCALE, MAX_SCALE);
    if (nextScale === previousScale) {
      return;
    }

    const ratio = nextScale / previousScale;
    state.x = state.x - lastPointerX * (ratio - 1);
    state.y = state.y - lastPointerY * (ratio - 1);
    state.scale = nextScale;
    applyTransform();
  }

  function deriveDiagramTitle(diagram) {
    const heading = diagram.closest("section")?.querySelector("h1, h2, h3, h4");
    if (heading && heading.textContent.trim()) {
      return heading.textContent.trim();
    }
    return "Diagrama Mermaid";
  }

  function openModal(sourceDiagram) {
    ensureModal();

    const sourceSvg = sourceDiagram.querySelector("svg");
    if (!sourceSvg) {
      return;
    }

    viewportElement.innerHTML = "";
    const clone = sourceSvg.cloneNode(true);
    clone.removeAttribute("width");
    clone.removeAttribute("height");
    clone.style.maxWidth = "none";
    clone.style.maxHeight = "none";
    viewportElement.appendChild(clone);

    titleElement.textContent = deriveDiagramTitle(sourceDiagram);
    state.activeSource = sourceDiagram;
    resetView();

    modal.classList.add("is-open");
    document.body.classList.add("mermaid-zoom-open");
  }

  function closeModal() {
    if (!modal) {
      return;
    }
    modal.classList.remove("is-open");
    document.body.classList.remove("mermaid-zoom-open");
    viewportElement.innerHTML = "";
    state.activeSource = null;
    stopDragging();
  }

  function enhanceDiagram(diagram) {
    if (!diagram || diagram.getAttribute(READY_ATTR) === "true") {
      return;
    }

    const svg = diagram.querySelector("svg");
    if (!svg) {
      return;
    }

    diagram.setAttribute(READY_ATTR, "true");

    const button = document.createElement("button");
    button.type = "button";
    button.className = BUTTON_CLASS;
    button.textContent = "Ampliar";
    button.setAttribute("aria-label", "Ampliar diagrama Mermaid");
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      openModal(diagram);
    });

    diagram.appendChild(button);
    diagram.addEventListener("click", function (event) {
      if (event.target.closest(`.${BUTTON_CLASS}`)) {
        return;
      }
      openModal(diagram);
    });
  }

  function scanDiagrams(root) {
    (root || document).querySelectorAll(".mermaid").forEach(enhanceDiagram);
  }

  function watchDiagrams() {
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          if (!(node instanceof HTMLElement)) {
            return;
          }
          if (node.matches?.(".mermaid") || node.querySelector?.(".mermaid")) {
            scanDiagrams(node);
          }
        });
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }

  function boot() {
    ensureModal();
    scanDiagrams(document);
    watchDiagrams();

    if (typeof document$ !== "undefined" && typeof document$.subscribe === "function") {
      document$.subscribe(function () {
        window.requestAnimationFrame(function () {
          scanDiagrams(document);
        });
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();