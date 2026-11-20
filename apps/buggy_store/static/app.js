/**
 * NovaMart Storefront Application Logic
 * Contains real, reproducible defects for visual and network forensic recording.
 */

// Simulated global state
window.userAuthSession = null; // Deliberately null to trigger Bug 1

const products = [
  { id: 1, name: "AI Tensor Accelerator v4", price: 1299.00, tag: "Flagship GPU", img: "fa-microchip" },
  { id: 2, name: "Ultra-Low-Power Edge Node", price: 449.00, tag: "IoT Cluster", img: "fa-server" },
  { id: 3, name: "Quantum Crypto Token Key", price: 89.00, tag: "HSM Security", img: "fa-key" },
];

let cart = [
  { id: 1, name: "AI Tensor Accelerator v4", price: 1299.00, qty: 1 }
];

function logEvent(msg, type = "info") {
  const logBox = document.getElementById("event-log");
  if (!logBox) return;
  const time = new Date().toLocaleTimeString();
  const div = document.createElement("div");
  if (type === "error") {
    div.className = "text-red-400 font-bold";
    div.innerText = `[${time}] [ERROR] ${msg}`;
  } else if (type === "network") {
    div.className = "text-amber-400";
    div.innerText = `[${time}] [HTTP] ${msg}`;
  } else {
    div.className = "text-slate-400";
    div.innerText = `[${time}] [LOG] ${msg}`;
  }
  logBox.appendChild(div);
  logBox.scrollTop = logBox.scrollHeight;
}

function renderProducts() {
  const grid = document.getElementById("products-grid");
  if (!grid) return;
  grid.innerHTML = products.map(p => `
    <div class="rounded-xl border border-slate-800 bg-[#0f172a] p-5 hover:border-slate-700 transition space-y-4">
      <div class="flex items-center justify-between">
        <div class="w-10 h-10 rounded-lg bg-indigo-950/80 border border-indigo-800/80 flex items-center justify-center text-indigo-400">
          <i class="fa-solid ${p.img} text-lg"></i>
        </div>
        <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-900">${p.tag}</span>
      </div>
      <div>
        <h3 class="font-bold text-white text-base">${p.name}</h3>
        <p class="text-xs text-slate-400 mt-0.5">High efficiency silicon for production inference workloads.</p>
      </div>
      <div class="flex items-center justify-between pt-2 border-t border-slate-800">
        <span class="mono font-bold text-white text-base">$${p.price.toFixed(2)}</span>
        <button onclick="addToCart(${p.id})" class="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition flex items-center space-x-1.5">
          <i class="fa-solid fa-plus text-[10px]"></i>
          <span>Add Node</span>
        </button>
      </div>
    </div>
  `).join("");
}

function renderCart() {
  const container = document.getElementById("cart-items");
  if (!container) return;

  if (cart.length === 0) {
    container.innerHTML = `<div class="text-xs text-slate-500 text-center py-6">Your order payload is empty.</div>`;
    updatePricing();
    return;
  }

  container.innerHTML = cart.map(item => `
    <div class="flex items-center justify-between bg-[#0b0f19] p-3 rounded-xl border border-slate-800">
      <div class="flex-1 pr-2">
        <div class="text-xs font-bold text-white truncate">${item.name}</div>
        <div class="text-[11px] mono text-slate-400">$${item.price.toFixed(2)} / unit</div>
      </div>
      <div class="flex items-center space-x-2">
        <!-- BUG 3: No lower bound check on decrement allows negative quantities -->
        <button onclick="changeQty(${item.id}, -1)" class="w-6 h-6 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold flex items-center justify-center">-</button>
        <span class="mono text-xs font-bold text-white w-5 text-center">${item.qty}</span>
        <button onclick="changeQty(${item.id}, 1)" class="w-6 h-6 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold flex items-center justify-center">+</button>
      </div>
    </div>
  `).join("");

  updatePricing();
}

// BUG 3: Decrementing past zero creates negative totals and state desync
function changeQty(id, delta) {
  const item = cart.find(x => x.id === id);
  if (!item) return;

  // Notice: missing `if (item.qty + delta < 1) return;`
  item.qty += delta;

  logEvent(`Cart item #${id} quantity altered to ${item.qty}`);
  if (item.qty <= 0) {
    logEvent(`CRITICAL: Inventory state desynchronization! Negative quantity detected (${item.qty})`, "error");
  }
  renderCart();
}

function addToCart(id) {
  const existing = cart.find(x => x.id === id);
  if (existing) {
    existing.qty += 1;
  } else {
    const prod = products.find(x => x.id === id);
    if (prod) cart.push({ ...prod, qty: 1 });
  }
  logEvent(`Item #${id} added to active cart`);
  renderCart();
}

function updatePricing() {
  const subtotal = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
  const tax = subtotal * 0.08;
  const total = subtotal + tax;

  const subtotalEl = document.getElementById("summary-subtotal");
  const taxEl = document.getElementById("summary-tax");
  const totalEl = document.getElementById("summary-total");

  if (subtotalEl) subtotalEl.innerText = `$${subtotal.toFixed(2)}`;
  if (taxEl) taxEl.innerText = `$${tax.toFixed(2)}`;
  if (totalEl) {
    totalEl.innerText = `$${total.toFixed(2)}`;
    if (total < 0) {
      totalEl.className = "mono text-red-400 text-lg font-bold";
    } else {
      totalEl.className = "mono text-emerald-400 text-lg font-bold";
    }
  }

  const badge = document.getElementById("cart-badge");
  if (badge) badge.innerText = cart.reduce((acc, x) => acc + x.qty, 0);
}

// BUG 2: Server 500 Internal Server Error when code is 'SAVE50'
async function applyCoupon() {
  const input = document.getElementById("coupon-input");
  const btn = document.getElementById("coupon-btn");
  const msg = document.getElementById("coupon-msg");
  const banner = document.getElementById("error-banner");
  const code = (input ? input.value : "").trim();

  if (!code) return;

  btn.innerText = "Checking...";
  btn.disabled = true;
  logEvent(`POST /api/coupon -> payload: {"code": "${code}"}`, "network");

  try {
    const res = await fetch("/api/coupon", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code })
    });

    const data = await res.json();

    if (!res.ok) {
      // 500 error triggered
      logEvent(`HTTP ${res.status} Internal Server Error on /api/coupon: ${data.message || data.exception}`, "error");
      msg.className = "text-[11px] font-bold text-red-400";
      msg.innerText = `HTTP ${res.status}: ${data.exception || "Internal Server Error"}`;
      msg.classList.remove("hidden");

      if (banner) {
        document.getElementById("error-title").innerText = `Backend Crash: ${data.exception || "HTTP 500"}`;
        document.getElementById("error-desc").innerText = `${data.message || "pricing_engine.py:42 ZeroDivisionError"}\nEndpoint: POST /api/coupon (HTTP 500)`;
        banner.classList.remove("hidden");
      }
    } else {
      msg.className = "text-[11px] font-bold text-emerald-400";
      msg.innerText = `Discount applied: -10%`;
      msg.classList.remove("hidden");
      logEvent(`Coupon ${code} validated successfully.`);
    }
  } catch (err) {
    logEvent(`Network failure during coupon verification: ${err.message}`, "error");
  } finally {
    btn.innerText = "Apply";
    btn.disabled = false;
  }
}

// BUG 1: Silent UI Freeze & Race Condition on Checkout
function processCheckout() {
  const btn = document.getElementById("checkout-btn");
  const spinner = document.getElementById("checkout-spinner");
  const btnText = document.getElementById("checkout-btn-text");
  const btnIcon = document.getElementById("checkout-btn-icon");

  logEvent("User initiated 'Complete Purchase' action", "info");

  // 1. Put UI into pending/loading state
  btn.disabled = true;
  btn.classList.add("opacity-80", "cursor-not-allowed");
  spinner.classList.remove("hidden");
  btnText.innerText = "Authorizing Transaction...";
  btnIcon.classList.add("hidden");

  logEvent("Button disabled. Contacting Payment Session Gateway...", "network");

  // 2. Uncaught TypeError: Cannot read properties of null (reading 'token')
  // Deliberate defect: accesses property on uninitialized session object without validation
  setTimeout(() => {
    logEvent("Resolving user auth session token...", "info");
    
    // THIS LINE CRASHES UNCAUGHT IN THE BROWSER CONSOLE:
    const sessionToken = window.userAuthSession.token.id;

    // Execution stops here. The spinner keeps spinning forever,
    // the button remains permanently disabled, and the user is locked out!
    fetch("/api/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: sessionToken, cart: cart })
    });
  }, 600);
}

// Initialization
window.onload = () => {
  renderProducts();
  renderCart();
};
