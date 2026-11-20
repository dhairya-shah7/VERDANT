# NovaMart Cloud Store — Standalone Defect Testbed

This web application is **100% independent** from VERDANT. Nothing from this site is hardcoded into VERDANT's database, templates, or logic. It provides real, live, reproducible bugs for genuine multimodal screen recording and automated forensic analysis.

---

## How to Start the App

In a separate terminal:
```powershell
python apps/buggy_store/server.py
```
Open your browser at: **`http://localhost:5050`**

---

## 3 Live Reproducible Bugs to Screen-Record

### 🔴 Bug 1: Silent UI Freeze & Race Condition on Checkout (Frontend JS Crash)
* **What to do:**
  1. Open the page (`http://localhost:5050`). You have 1 item already in the cart.
  2. Open your browser Developer Tools (`F12` $\rightarrow$ Console tab).
  3. Click the blue **"Complete Purchase"** button.
* **What happens (Visual & Console):**
  - The button turns into a spinning state *"Authorizing Transaction..."* and gets disabled.
  - A fatal JavaScript error fires in DevTools Console:
    `Uncaught TypeError: Cannot read properties of null (reading 'token') at processCheckout (app.js:142)`
  - The button remains permanently stuck in a disabled spinning state. The checkout never finishes.
* **What VERDANT catches:**
  - **Visual:** Freeze at button transition with zero DOM repaint.
  - **Console:** `TypeError: Cannot read properties of null (reading 'token')`.
  - **Root Cause:** Missing null check on `window.userAuthSession` before accessing `token.id`.

---

### 🔴 Bug 2: HTTP 500 Backend Crash on Promotional Code (API Failure)
* **What to do:**
  1. In the **Promotional Code** box, type: `SAVE50`
  2. Click **"Apply"**.
* **What happens (Visual & Network):**
  - A red error banner appears on screen: `Backend Crash: ZeroDivisionError: float division by zero`.
  - The live telemetry box shows `[HTTP 500 Internal Server Error]`.
  - DevTools Network tab shows a failed `POST /api/coupon` returning HTTP 500.
* **What VERDANT catches:**
  - **Network:** HTTP `500` status on `/api/coupon`.
  - **Trace:** `ZeroDivisionError: float division by zero in pricing_engine.py:42`.

---

### 🔴 Bug 3: State Desynchronization & Negative Quantity Calculation
* **What to do:**
  1. On the cart item, click the **`-`** button twice.
* **What happens:**
  - Quantity decrements from `1` $\rightarrow$ `0` $\rightarrow$ `-1`.
  - The item subtotal drops to `-$1,299.00`, and the Total Amount turns red with a negative balance (`-$1,402.92`).
* **What VERDANT catches:**
  - **DOM & Visual:** Cart state desync with invalid negative quantities.
