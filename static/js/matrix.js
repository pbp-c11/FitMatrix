const matrix = (() => {
  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const state = {
    searchEndpoint: null,
  };

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
      });
    });
  };

  const init = () => {
    initMobileNav();
    initOrb();
    initMatrixCoordinates();
    initAsyncSearch();
    initDismissibleToasts();
  };

  return { init };
})();

window.addEventListener("DOMContentLoaded", () => matrix.init());
