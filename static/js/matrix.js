<<<<<<< HEAD
// static/js/matrix.js
=======
>>>>>>> origin/kanayradeeva010
const matrix = (() => {
  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const state = {
    searchEndpoint: null,
  };

<<<<<<< HEAD
  const getCsrfToken = () => {
    const tokenField = qs("input[name='csrfmiddlewaretoken']");
    if (tokenField && tokenField.value) {
      return tokenField.value;
    }
    const cookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  };

  // ===============================
  // MOBILE NAVIGATION
  // ===============================
=======
>>>>>>> origin/kanayradeeva010
  const initMobileNav = () => {
    const toggle = qs("[data-mobile-toggle]");
    const menu = qs("[data-mobile-menu]");
    if (!toggle || !menu) return;
    toggle.addEventListener("click", () => {
      menu.toggleAttribute("data-open");
      if (menu.hasAttribute("data-open")) {
        menu.style.maxHeight = `${menu.scrollHeight}px`;
      } else {
        menu.style.maxHeight = "0px";
      }
    });
  };

<<<<<<< HEAD
  // ===============================
  // ASYNC SEARCH
  // ===============================
  const updateSearchResults = (html, count) => {
    const target = qs("[data-search-results]");
    const countLabel = qs("[data-search-count]");
    if (target) target.innerHTML = html;
    if (countLabel) countLabel.textContent = String(count);
=======
  const initOrb = () => {
    const orb = qs("[data-matrix-orb]");
    if (!orb) return;
    let raf = null;
    const update = (event) => {
      const { clientX, clientY } = event;
      orb.style.transform = `translate3d(${clientX - 110}px, ${clientY - 110}px, 0)`;
    };
    const schedule = (event) => {
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => update(event));
    };
    window.addEventListener("pointermove", schedule);
  };

  const initMatrixCoordinates = () => {
    const container = qs("[data-matrix-coords]");
    if (!container) return;
    const xNode = qs("[data-coord-x]", container);
    const yNode = qs("[data-coord-y]", container);
    if (!xNode || !yNode) return;

    let pending = false;
    let latest = null;

    const render = ({ clientX, clientY }) => {
      const width = Math.max(window.innerWidth, 1);
      const height = Math.max(window.innerHeight, 1);
      const x = Math.round((clientX / width) * 999);
      const y = Math.round((clientY / height) * 999);
      xNode.textContent = String(x).padStart(3, "0");
      yNode.textContent = String(y).padStart(3, "0");
    };

    const schedule = (event) => {
      latest = event;
      if (pending) return;
      pending = true;
      requestAnimationFrame(() => {
        if (latest) render(latest);
        pending = false;
      });
    };

    window.addEventListener("pointermove", schedule, { passive: true });
    render({ clientX: window.innerWidth * 0.5, clientY: window.innerHeight * 0.5 });
  };

  const updateSearchResults = (html, count) => {
    const target = qs("[data-search-results]");
    const countLabel = qs("[data-search-count]");
    if (target) {
      target.innerHTML = html;
    }
    if (countLabel) {
      countLabel.textContent = String(count);
    }
>>>>>>> origin/kanayradeeva010
  };

  const serializeForm = (form) =>
    new URLSearchParams(new FormData(form)).toString();

  const initAsyncSearch = () => {
    const form = qs("[data-async-search]");
    if (!form) return;
    state.searchEndpoint = form.getAttribute("action") || window.location.pathname;
    const submit = async () => {
      const queryString = serializeForm(form);
      const response = await fetch(`${state.searchEndpoint}?${queryString}`, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      if (!response.ok) return;
      const payload = await response.json();
      updateSearchResults(payload.html, payload.count);
      history.replaceState({}, "", `${state.searchEndpoint}?${queryString}`);
    };
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      submit().catch(() => {});
    });

    qsa("[data-filter-trigger]").forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.filterTarget;
        const value = button.dataset.filterValue || "";
        if (!target) return;
        const input = qs(`[name='${target}']`, form);
        if (!input) return;
        if (button.dataset.selected === "true") {
          button.dataset.selected = "false";
          input.value = "";
        } else {
          qsa(`[data-filter-trigger][data-filter-target='${target}']`, form).forEach((item) => {
            item.dataset.selected = "false";
          });
          button.dataset.selected = "true";
          input.value = value;
        }
        submit().catch(() => {});
      });
    });
  };

<<<<<<< HEAD
  // ===============================
  // TOAST HANDLER (auto-dismiss)
  // ===============================
  const initDismissibleToasts = () => {
    const toasts = qsa("[data-toast]");
    toasts.forEach((toast) => {
      const dismiss = qs("[data-toast-dismiss]", toast);
      if (dismiss) {
        dismiss.addEventListener("click", () => {
          toast.classList.add("matrix-toast--hiding");
          toast.addEventListener("transitionend", () => toast.remove(), { once: true });
        });
      }

      // Auto hide after 3s
      setTimeout(() => {
        toast.classList.add("matrix-toast--hiding");
        toast.addEventListener("transitionend", () => toast.remove(), { once: true });
      }, 3000);
    });
  };

  // ===============================
  // WISHLIST TOGGLE
  // ===============================
  const updateWishlistButton = (button, isActive) => {
    button.dataset.active = isActive ? "true" : "false";
    if (button.hasAttribute("aria-pressed")) {
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    }
    const activeLabel = button.dataset.labelActive;
    const inactiveLabel = button.dataset.labelInactive;
    if (activeLabel !== undefined && inactiveLabel !== undefined) {
      button.textContent = isActive ? activeLabel : inactiveLabel;
    }
    const activeClass = button.dataset.activeClass;
    if (activeClass) {
      button.classList.toggle(activeClass, isActive);
    }
  };

  const initWishlistToggles = () => {
    const buttons = qsa("[data-wishlist-toggle]");
    if (!buttons.length) return;
    const csrfToken = getCsrfToken();

    const handleToggle = async (button) => {
      if (!button.dataset.url || button.dataset.loading === "true") return;
      button.dataset.loading = "true";
      try {
        const response = await fetch(button.dataset.url, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
        });
        if (!response.ok) throw new Error("Wishlist toggle failed");
        const payload = await response.json();
        const isActive = payload.status === "added";
        updateWishlistButton(button, isActive);
        document.dispatchEvent(
          new CustomEvent("wishlist:toggled", {
            detail: { button, status: payload.status, added: isActive, payload },
          }),
        );
      } catch (error) {
        button.dataset.error = "true";
        setTimeout(() => button.removeAttribute("data-error"), 2000);
      } finally {
        button.dataset.loading = "false";
      }
    };

    buttons.forEach((button) => {
      updateWishlistButton(button, button.dataset.active === "true");
      button.addEventListener("click", (event) => {
        event.preventDefault();
        handleToggle(button).catch(() => {});
=======
  const initDismissibleToasts = () => {
    qsa("[data-toast-dismiss]").forEach((button) => {
      button.addEventListener("click", () => {
        const toast = button.closest("[data-toast]");
        if (!toast) return;
        toast.classList.add("matrix-toast--hiding");
        toast.addEventListener(
          "transitionend",
          () => toast.remove(),
          { once: true },
        );
>>>>>>> origin/kanayradeeva010
      });
    });
  };

<<<<<<< HEAD
  // ===============================
  // INIT
  // ===============================
  const init = () => {
    initMobileNav();
    initAsyncSearch();
    initDismissibleToasts();
    initWishlistToggles();
=======
  const init = () => {
    initMobileNav();
    initOrb();
    initMatrixCoordinates();
    initAsyncSearch();
    initDismissibleToasts();
>>>>>>> origin/kanayradeeva010
  };

  return { init };
})();

window.addEventListener("DOMContentLoaded", () => matrix.init());
<<<<<<< HEAD


=======
>>>>>>> origin/kanayradeeva010
