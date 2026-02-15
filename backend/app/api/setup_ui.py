from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["setup-ui"])


SETUP_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Restaurant POS Setup</title>
  <style>
    :root {
      --bg: #f7f8fb;
      --card: #ffffff;
      --text: #141726;
      --muted: #5d6478;
      --accent: #0d6efd;
      --border: #e4e7ef;
      --error: #b42318;
      --ok: #067647;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      background: linear-gradient(135deg, #eef2ff, #f8fafc);
      color: var(--text);
      min-height: 100vh;
      padding: 28px;
    }
    .container {
      max-width: 880px;
      margin: 0 auto;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 10px 24px rgba(20, 23, 38, 0.08);
    }
    h1 {
      margin: 0 0 8px;
      font-size: 28px;
    }
    .sub {
      color: var(--muted);
      margin-bottom: 22px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }
    .full { grid-column: span 2; }
    label {
      display: block;
      font-weight: 600;
      margin-bottom: 6px;
    }
    input, select {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 14px;
      background: #fff;
    }
    .box {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      background: #fcfdff;
    }
    .plugins {
      max-height: 220px;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px;
      background: #fff;
    }
    .plugin {
      padding: 8px;
      border-bottom: 1px solid #f0f2f7;
      display: flex;
      align-items: flex-start;
      gap: 10px;
    }
    .plugin:last-child { border-bottom: none; }
    .plugin small { color: var(--muted); display: block; }
    button {
      border: none;
      border-radius: 10px;
      padding: 12px 16px;
      background: var(--accent);
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    button[disabled] { opacity: 0.65; cursor: not-allowed; }
    .status {
      margin-top: 14px;
      border-radius: 10px;
      padding: 10px 12px;
      display: none;
      white-space: pre-wrap;
    }
    .status.error { display: block; background: #fef3f2; color: var(--error); border: 1px solid #fecdca; }
    .status.ok { display: block; background: #ecfdf3; color: var(--ok); border: 1px solid #abefc6; }
    @media (max-width: 720px) {
      .grid { grid-template-columns: 1fr; }
      .full { grid-column: span 1; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Initial Setup Wizard</h1>
    <p class="sub">Configure database, create first tenant/admin, activate plugins, and run migrations.</p>

    <div id="alreadySetup" class="status ok" style="display:none"></div>

    <form id="setupForm" class="grid">
      <div class="box full">
        <h3>Database</h3>
        <div class="grid">
          <div>
            <label for="dbKind">Database Type</label>
            <select id="dbKind" name="dbKind">
              <option value="sqlite">SQLite</option>
              <option value="postgres">PostgreSQL URL</option>
            </select>
          </div>
          <div id="sqliteBlock">
            <label for="sqlitePath">SQLite File Path</label>
            <input id="sqlitePath" name="sqlitePath" value="data.db" />
          </div>
          <div id="postgresBlock" style="display:none" class="full">
            <label for="postgresUrl">PostgreSQL URL</label>
            <input id="postgresUrl" name="postgresUrl" placeholder="postgresql://user:pass@localhost:5432/restaurant_pos" />
          </div>
        </div>
      </div>

      <div class="box">
        <h3>Admin</h3>
        <label for="adminName">Full Name</label>
        <input id="adminName" required />
        <label for="adminUser">Username</label>
        <input id="adminUser" required />
        <label for="adminPass">Password</label>
        <input id="adminPass" type="password" required />
      </div>

      <div class="box">
        <h3>Tenant</h3>
        <label for="tenantName">Tenant Name</label>
        <input id="tenantName" required />
        <label for="tenantSlug">Tenant Slug</label>
        <input id="tenantSlug" required />
        <label for="currency">Currency</label>
        <input id="currency" value="USD" />
        <label for="locale">Locale</label>
        <input id="locale" value="en" />
      </div>

      <div class="box full">
        <h3>Plugins</h3>
        <div id="plugins" class="plugins"></div>
      </div>

      <div class="full" style="display:flex; gap:10px; align-items:center;">
        <button id="submitBtn" type="submit">Initialize Instance</button>
      </div>
    </form>

    <div id="status" class="status"></div>
  </div>

  <script>
    const statusBox = document.getElementById("status");
    const setupForm = document.getElementById("setupForm");
    const pluginsEl = document.getElementById("plugins");
    const submitBtn = document.getElementById("submitBtn");

    const dbKind = document.getElementById("dbKind");
    const sqliteBlock = document.getElementById("sqliteBlock");
    const postgresBlock = document.getElementById("postgresBlock");

    function setStatus(message, kind) {
      statusBox.className = "status " + kind;
      statusBox.textContent = message;
    }

    dbKind.addEventListener("change", () => {
      const kind = dbKind.value;
      sqliteBlock.style.display = kind === "sqlite" ? "block" : "none";
      postgresBlock.style.display = kind === "postgres" ? "block" : "none";
    });

    async function loadStatus() {
      const res = await fetch("/api/setup/status");
      if (!res.ok) return;
      const data = await res.json();
      if (data.is_setup) {
        const box = document.getElementById("alreadySetup");
        box.style.display = "block";
        box.textContent = "This instance is already initialized.";
      }
    }

    async function loadPlugins() {
      pluginsEl.innerHTML = "Loading plugins...";
      const res = await fetch("/api/setup/plugins");
      if (!res.ok) {
        pluginsEl.innerHTML = "Failed to load plugins.";
        return;
      }
      const plugins = await res.json();
      if (!Array.isArray(plugins) || !plugins.length) {
        pluginsEl.innerHTML = "No plugins found.";
        return;
      }

      pluginsEl.innerHTML = "";
      for (const plugin of plugins) {
        const row = document.createElement("label");
        row.className = "plugin";
        row.innerHTML = `
          <input type="checkbox" value="${plugin.key}" />
          <div>
            <strong>${plugin.name}</strong> <small>${plugin.key} v${plugin.version}</small>
            <small>${plugin.description || ""}</small>
          </div>
        `;
        pluginsEl.appendChild(row);
      }
    }

    function selectedPlugins() {
      return Array.from(pluginsEl.querySelectorAll("input[type=checkbox]:checked")).map((n) => n.value);
    }

    setupForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      submitBtn.disabled = true;
      setStatus("Running core/plugin migrations and creating initial tenant...", "ok");

      const payload = {
        db: {
          kind: dbKind.value,
          sqlite_path: document.getElementById("sqlitePath").value,
          postgres_url: document.getElementById("postgresUrl").value
        },
        setup: {
          tenant_name: document.getElementById("tenantName").value,
          tenant_slug: document.getElementById("tenantSlug").value,
          currency: document.getElementById("currency").value,
          locale: document.getElementById("locale").value,
          admin_username: document.getElementById("adminUser").value,
          admin_password: document.getElementById("adminPass").value,
          admin_name: document.getElementById("adminName").value,
          enabled_plugins: selectedPlugins()
        }
      };

      try {
        const res = await fetch("/api/setup/bootstrap", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) {
          setStatus("Setup failed: " + JSON.stringify(data.detail || data), "error");
          submitBtn.disabled = false;
          return;
        }

        const restartHint = data.restart_required
          ? "\\nRestart backend to apply DATABASE_URL from .env."
          : "";
        setStatus("Setup completed. Tenant ID: " + data.tenant_id + "\\nConfig written: " + data.config_path + restartHint, "ok");
      } catch (error) {
        setStatus("Setup failed: " + error, "error");
        submitBtn.disabled = false;
      }
    });

    loadStatus().catch(() => {});
    loadPlugins().catch(() => {});
  </script>
</body>
</html>
"""


@router.get("/setup", response_class=HTMLResponse, include_in_schema=False)
async def setup_ui() -> HTMLResponse:
    return HTMLResponse(content=SETUP_HTML)
