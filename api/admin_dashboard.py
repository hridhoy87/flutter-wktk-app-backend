"""
Super Admin Console HTML Template & Asset Renderer for Cellular WKTK
"""

ADMIN_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cellular WKTK // Super Admin Console</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #0a0c10;
            --bg-surface: #12151d;
            --bg-card: #181c26;
            --bg-card-hover: #1e2330;
            --bg-input: #0f1219;
            --border-subtle: #232838;
            --border-highlight: #333a4f;
            
            --gold: #f59e0b;
            --gold-light: #fbbf24;
            --gold-glow: rgba(245, 158, 11, 0.15);
            
            --emerald: #10b981;
            --emerald-bg: rgba(16, 185, 129, 0.12);
            --rose: #ef4444;
            --rose-bg: rgba(239, 68, 68, 0.12);
            --amber: #f97316;
            --amber-bg: rgba(249, 115, 22, 0.12);
            --cyan: #06b6d4;
            --cyan-bg: rgba(6, 182, 212, 0.12);
            
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
            --radius-xl: 20px;
            --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Top Header */
        header {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border-subtle);
            padding: 14px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
        }

        .brand-icon svg {
            width: 22px;
            height: 22px;
            fill: #000;
        }

        .brand-text h1 {
            font-size: 17px;
            font-weight: 700;
            letter-spacing: 0.05em;
            color: #fff;
        }

        .brand-text p {
            font-size: 11px;
            color: var(--gold);
            font-weight: 600;
            letter-spacing: 0.15em;
            text-transform: uppercase;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .db-status {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            padding: 6px 14px;
            border-radius: var(--radius-md);
            font-size: 12px;
            color: var(--text-secondary);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--emerald);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--emerald);
        }

        .btn-logout {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-logout:hover {
            background: var(--rose-bg);
            color: var(--rose);
            border-color: var(--rose);
        }

        /* Main Container */
        main {
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            padding: 28px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }

        .stat-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: var(--transition);
        }

        .stat-card:hover {
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }

        .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 32px;
            font-weight: 800;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            line-height: 1;
        }

        .stat-sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 8px;
        }

        .stat-badge {
            position: absolute;
            top: 18px;
            right: 18px;
            width: 32px;
            height: 32px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Tabs Navigation */
        .tab-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 12px;
            gap: 16px;
            flex-wrap: wrap;
        }

        .tab-group {
            display: flex;
            gap: 8px;
        }

        .tab-btn {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            padding: 10px 20px;
            border-radius: var(--radius-md);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn:hover {
            color: var(--text-primary);
            background: var(--bg-card);
        }

        .tab-btn.active {
            background: var(--bg-card);
            border-color: var(--gold);
            color: var(--gold-light);
            box-shadow: 0 0 12px var(--gold-glow);
        }

        .tab-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* Buttons & Inputs */
        .btn-primary {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.04em;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary:hover {
            filter: brightness(1.1);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
            padding: 10px 18px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-secondary:hover {
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
        }

        .search-input {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 9px 16px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
            width: 260px;
            transition: var(--transition);
        }

        .search-input:focus {
            border-color: var(--gold);
            box-shadow: 0 0 0 2px var(--gold-glow);
        }

        /* Tables & Content Panel */
        .content-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }

        .panel-header {
            padding: 18px 24px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }

        .panel-title {
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .table-responsive {
            overflow-x: auto;
            width: 100%;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }

        th {
            background: var(--bg-card);
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.08em;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border-subtle);
            white-space: nowrap;
        }

        td {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            vertical-align: middle;
        }

        tr:hover td {
            background-color: var(--bg-card-hover);
        }

        .col-id {
            font-family: 'JetBrains Mono', monospace;
            color: var(--gold-light);
            font-weight: 600;
            width: 50px;
        }

        .col-user {
            font-weight: 600;
            color: var(--text-primary);
        }

        .col-mono {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        }

        /* Badges & Pills */
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .pill-approved { background: var(--emerald-bg); color: var(--emerald); }
        .pill-pending { background: var(--amber-bg); color: var(--amber); }
        .pill-admin { background: var(--gold-glow); color: var(--gold-light); border: 1px solid rgba(245,158,11,0.3); }
        .pill-user { background: var(--bg-card); color: var(--text-secondary); }
        .pill-protected { background: var(--rose-bg); color: var(--rose); }
        .pill-public { background: var(--cyan-bg); color: var(--cyan); }
        .pill-channel { background: var(--bg-card); color: var(--gold-light); font-family: 'JetBrains Mono', monospace; margin: 2px; }

        /* Action Buttons in Tables */
        .action-group {
            display: flex;
            align-items: center;
            gap: 8px;
            justify-content: flex-end;
        }

        .btn-icon {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition);
        }

        .btn-icon:hover {
            border-color: var(--gold);
            color: var(--gold-light);
            background: var(--bg-card-hover);
        }

        .btn-icon.danger:hover {
            border-color: var(--rose);
            color: var(--rose);
            background: var(--rose-bg);
        }

        .btn-icon.success:hover {
            border-color: var(--emerald);
            color: var(--emerald);
            background: var(--emerald-bg);
        }

        /* Modal Overlay */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.82);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: var(--transition);
            padding: 20px;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: all;
        }

        .modal-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 580px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            max-height: 90vh;
        }

        .modal-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .modal-header h3 {
            font-size: 17px;
            font-weight: 700;
            color: #fff;
        }

        .modal-body {
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .modal-footer {
            padding: 18px 24px;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 12px;
            background: var(--bg-card);
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .form-group label {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .form-control {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 11px 14px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
            transition: var(--transition);
        }

        .form-control:focus {
            border-color: var(--gold);
            box-shadow: 0 0 0 2px var(--gold-glow);
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 0;
        }

        .checkbox-group input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: var(--gold);
            cursor: pointer;
        }

        .checkbox-group label {
            font-size: 14px;
            color: var(--text-primary);
            cursor: pointer;
        }

        .channels-picker {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 12px;
            max-height: 180px;
            overflow-y: auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 10px;
        }

        .channel-check-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 6px 8px;
            border-radius: var(--radius-sm);
            background: var(--bg-card);
        }

        .channel-check-item:hover {
            color: #fff;
            background: var(--bg-card-hover);
        }

        /* Toast Notifications */
        #toastContainer {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toast {
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            color: #fff;
            padding: 14px 20px;
            border-radius: var(--radius-md);
            font-size: 13px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .toast.success { border-color: var(--emerald); color: var(--emerald); }
        .toast.error { border-color: var(--rose); color: var(--rose); }

        @keyframes slideIn {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        /* Login Overlay */
        #loginOverlay {
            position: fixed;
            inset: 0;
            background: var(--bg-base);
            z-index: 5000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .login-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            border-radius: var(--radius-xl);
            padding: 36px;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
            gap: 20px;
            text-align: center;
        }

        .login-card h2 {
            font-size: 22px;
            font-weight: 800;
            color: #fff;
            margin-top: 10px;
        }

        .login-card p {
            font-size: 13px;
            color: var(--text-secondary);
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- Auth Protection Overlay -->
    <div id="loginOverlay">
        <div class="login-card">
            <div style="display: flex; justify-content: center;">
                <div class="brand-icon" style="width: 56px; height: 56px;">
                    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
                </div>
            </div>
            <div>
                <h2>Super Admin Access</h2>
                <p>Authenticate with master admin credentials to access database and permission controls.</p>
            </div>
            <form id="adminLoginForm" onsubmit="handleAdminLogin(event)" style="display: flex; flex-direction: column; gap: 14px; text-align: left;">
                <div class="form-group">
                    <label>Admin Phone Number</label>
                    <input type="text" id="loginPhone" class="form-control" placeholder="017XXXXXXXX" required autofocus>
                </div>
                <div class="form-group">
                    <label>Admin Passcode</label>
                    <input type="password" id="loginPassword" class="form-control" placeholder="••••••••" required>
                </div>
                <button type="submit" class="btn-primary" style="justify-content: center; width: 100%; padding: 12px; margin-top: 8px;">
                    Authenticate & Enter Console
                </button>
            </form>
        </div>
    </div>

    <!-- Top Navigation Header -->
    <header>
        <div class="brand">
            <div class="brand-icon">
                <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>
            </div>
            <div class="brand-text">
                <h1>CELLULAR WKTK</h1>
                <p>Super Admin Console</p>
            </div>
        </div>

        <div class="header-actions">
            <div class="db-status">
                <div class="status-dot"></div>
                <span>Neon PostgreSQL Online</span>
            </div>
            <button class="btn-logout" onclick="handleLogout()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
                Sign Out
            </button>
        </div>
    </header>

    <!-- Main Content Body -->
    <main>
        <!-- Live System Metric Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Users</div>
                <div class="stat-value" id="statTotalUsers">--</div>
                <div class="stat-sub" id="statUsersSub">-- Approved · -- Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Channels & Groups</div>
                <div class="stat-value" id="statTotalChannels">--</div>
                <div class="stat-sub" id="statChannelsSub">-- Protected · -- Open</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Pending Approval</div>
                <div class="stat-value" id="statPendingCount" style="color: var(--gold-light);">--</div>
                <div class="stat-sub">Action required</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Admins Registered</div>
                <div class="stat-value" id="statAdminCount" style="color: var(--cyan);">--</div>
                <div class="stat-sub">Master privilege accounts</div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="tab-bar">
            <div class="tab-group">
                <button class="tab-btn active" onclick="switchTab('users')" id="tabBtnUsers">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
                    User Management (<span id="tabUserCount">0</span>)
                </button>
                <button class="tab-btn" onclick="switchTab('channels')" id="tabBtnChannels">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                    Channel & Frequency Manager (<span id="tabChannelCount">0</span>)
                </button>
            </div>

            <div class="tab-actions">
                <input type="text" id="searchInput" class="search-input" placeholder="Search by name, phone, id..." oninput="handleSearch()">
                <button class="btn-secondary" onclick="loadAllData()" title="Reload Data">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
                    Refresh
                </button>
                <button class="btn-primary" id="btnPrimaryAction" onclick="openCreateModal()">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                    Add User
                </button>
            </div>
        </div>

        <!-- Users Table Panel -->
        <div class="content-panel" id="panelUsers">
            <div class="panel-header">
                <div class="panel-title">
                    <span>Registered Agent Directory</span>
                </div>
                <div style="display: flex; gap: 8px;">
                    <select id="userFilterStatus" class="form-control" style="padding: 6px 12px; font-size: 12px; width: 140px;" onchange="renderUsersTable()">
                        <option value="all">All Status</option>
                        <option value="pending">Pending Only</option>
                        <option value="approved">Approved Only</option>
                        <option value="admin">Admins Only</option>
                    </select>
                </div>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th class="col-id">ID</th>
                            <th>Agent Name</th>
                            <th>Phone Number</th>
                            <th>Subscribed Channels</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Created At</th>
                            <th style="text-align: right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="usersTableBody">
                        <tr><td colspan="8" style="text-align: center; padding: 40px;">Loading directory...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Channels Table Panel -->
        <div class="content-panel hidden" id="panelChannels">
            <div class="panel-header">
                <div class="panel-title">
                    <span>Radio Channels & Frequencies</span>
                </div>
                <div style="display: flex; gap: 8px;">
                    <select id="channelFilterType" class="form-control" style="padding: 6px 12px; font-size: 12px; width: 150px;" onchange="renderChannelsTable()">
                        <option value="all">All Channels</option>
                        <option value="permanent">Permanent Only</option>
                        <option value="temporary">Temporary Only</option>
                        <option value="protected">Protected Only</option>
                    </select>
                </div>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th class="col-id">ID</th>
                            <th>Channel Name</th>
                            <th>Type</th>
                            <th>Security</th>
                            <th>Channel Admin</th>
                            <th>Entitled Members</th>
                            <th>Created At</th>
                            <th style="text-align: right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="channelsTableBody">
                        <tr><td colspan="8" style="text-align: center; padding: 40px;">Loading channels...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <!-- User Modal (Create & Edit) -->
    <div class="modal-overlay" id="userModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3 id="userModalTitle">Add New Agent</h3>
                <button class="btn-icon" onclick="closeModal('userModal')">✕</button>
            </div>
            <form id="userForm" onsubmit="handleUserFormSubmit(event)">
                <input type="hidden" id="userFormId">
                <div class="modal-body">
                    <div class="form-group">
                        <label>Legal Name / Callsign</label>
                        <input type="text" id="userFormLegalName" class="form-control" placeholder="e.g. Asad Mushad" required>
                    </div>
                    <div class="form-group">
                        <label>Phone Number (Unique Login ID)</label>
                        <input type="text" id="userFormPhone" class="form-control" placeholder="e.g. 01712345678" required>
                    </div>
                    <div class="form-group">
                        <label id="userFormPasswordLabel">Passcode</label>
                        <input type="password" id="userFormPassword" class="form-control" placeholder="Leave empty to keep unchanged">
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div class="checkbox-group">
                            <input type="checkbox" id="userFormApproved">
                            <label for="userFormApproved">Approved for App</label>
                        </div>
                        <div class="checkbox-group">
                            <input type="checkbox" id="userFormAdmin">
                            <label for="userFormAdmin">Grant Admin Role</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Assign Channel Entitlements</label>
                        <div class="channels-picker" id="userFormChannelsPicker">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn-secondary" onclick="closeModal('userModal')">Cancel</button>
                    <button type="submit" class="btn-primary">Save Agent</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Channel Modal (Create & Edit) -->
    <div class="modal-overlay" id="channelModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3 id="channelModalTitle">Create Channel</h3>
                <button class="btn-icon" onclick="closeModal('channelModal')">✕</button>
            </div>
            <form id="channelForm" onsubmit="handleChannelFormSubmit(event)">
                <input type="hidden" id="channelFormId">
                <div class="modal-body">
                    <div class="form-group">
                        <label>Channel Name</label>
                        <input type="text" id="channelFormName" class="form-control" placeholder="e.g. Tactical Alpha" required>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div class="checkbox-group">
                            <input type="checkbox" id="channelFormProtected" onchange="toggleChannelPasswordInput()">
                            <label for="channelFormProtected">Protected (PIN Required)</label>
                        </div>
                        <div class="checkbox-group">
                            <input type="checkbox" id="channelFormTemporary">
                            <label for="channelFormTemporary">Temporary Channel</label>
                        </div>
                    </div>
                    <div class="form-group" id="channelPasswordGroup" style="display: none;">
                        <label>Channel Passcode / PIN</label>
                        <input type="password" id="channelFormPassword" class="form-control" placeholder="Enter channel passcode">
                    </div>
                    <div class="form-group">
                        <label>Channel Admin (Owner)</label>
                        <select id="channelFormAdminId" class="form-control">
                            <option value="">No Specific Admin (System Channel)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Entitled Members (Allowed Users)</label>
                        <div class="channels-picker" id="channelFormUsersPicker" style="max-height: 150px;">
                            <!-- Populated dynamically with users -->
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn-secondary" onclick="closeModal('channelModal')">Cancel</button>
                    <button type="submit" class="btn-primary">Save Channel</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Toast Feedback Container -->
    <div id="toastContainer"></div>

    <script>
        let currentTab = 'users';
        let usersData = [];
        let channelsData = [];
        let adminToken = localStorage.getItem('wktk_admin_token') || '';

        // Initialize Console on page load
        window.addEventListener('DOMContentLoaded', () => {
            if (adminToken) {
                document.getElementById('loginOverlay').classList.add('hidden');
                loadAllData();
            } else {
                document.getElementById('loginOverlay').classList.remove('hidden');
            }
        });

        // API Call Helper with Auth Headers
        async function api(path, options = {}) {
            options.headers = options.headers || {};
            if (adminToken) {
                options.headers['Authorization'] = 'Bearer ' + adminToken;
            }
            if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(options.body);
            }
            
            try {
                const res = await fetch(path, options);
                if (res.status === 401 || res.status === 403) {
                    showToast('Admin session expired or unauthorized', 'error');
                    handleLogout();
                    throw new Error('Unauthorized');
                }
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || data.message || 'API request failed');
                }
                return data;
            } catch (err) {
                console.error('API Error:', err);
                showToast(err.message, 'error');
                throw err;
            }
        }

        // Authentication Handler
        async function handleAdminLogin(e) {
            e.preventDefault();
            const phone = document.getElementById('loginPhone').value.trim();
            const password = document.getElementById('loginPassword').value.trim();

            try {
                const res = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone, password })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Incorrect admin phone or passcode');

                // Verify user is actually admin
                const userRes = await fetch('/home', {
                    headers: { 'Authorization': 'Bearer ' + data.access_token }
                });
                const userData = await userRes.json();
                if (!userData.is_admin) {
                    throw new Error('Access denied: Account is not an administrator');
                }

                adminToken = data.access_token;
                localStorage.setItem('wktk_admin_token', adminToken);
                document.getElementById('loginOverlay').classList.add('hidden');
                showToast('Welcome to Super Admin Console', 'success');
                loadAllData();
            } catch (err) {
                showToast(err.message, 'error');
            }
        }

        function handleLogout() {
            adminToken = '';
            localStorage.removeItem('wktk_admin_token');
            document.getElementById('loginOverlay').classList.remove('hidden');
        }

        // Fetch & Reload all Data
        async function loadAllData() {
            try {
                const [stats, users, channels] = await Promise.all([
                    api('/admin/stats'),
                    api('/admin/users'),
                    api('/admin/channels')
                ]);

                usersData = users || [];
                channelsData = channels || [];

                updateStatsCards(stats);
                renderUsersTable();
                renderChannelsTable();
                document.getElementById('tabUserCount').innerText = usersData.length;
                document.getElementById('tabChannelCount').innerText = channelsData.length;
            } catch (err) {}
        }

        function updateStatsCards(stats) {
            document.getElementById('statTotalUsers').innerText = stats.total_users || usersData.length;
            document.getElementById('statUsersSub').innerText = `${stats.approved_users || 0} Approved · ${stats.pending_users || 0} Pending`;
            document.getElementById('statTotalChannels').innerText = stats.total_channels || channelsData.length;
            document.getElementById('statChannelsSub').innerText = `${stats.protected_channels || 0} Protected · ${stats.public_channels || 0} Open`;
            document.getElementById('statPendingCount').innerText = stats.pending_users || 0;
            document.getElementById('statAdminCount').innerText = stats.admin_users || 0;
        }

        // Switch Tabs
        function switchTab(tab) {
            currentTab = tab;
            document.getElementById('tabBtnUsers').classList.toggle('active', tab === 'users');
            document.getElementById('tabBtnChannels').classList.toggle('active', tab === 'channels');
            document.getElementById('panelUsers').classList.toggle('hidden', tab !== 'users');
            document.getElementById('panelChannels').classList.toggle('hidden', tab !== 'channels');
            
            const btnPrimary = document.getElementById('btnPrimaryAction');
            if (tab === 'users') {
                btnPrimary.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg> Add User';
                btnPrimary.onclick = openCreateUserModal;
            } else {
                btnPrimary.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg> Create Channel';
                btnPrimary.onclick = openCreateChannelModal;
            }
            handleSearch();
        }

        // Search Filter
        function handleSearch() {
            if (currentTab === 'users') renderUsersTable();
            else renderChannelsTable();
        }

        // Render Users Table
        function renderUsersTable() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const statusFilter = document.getElementById('userFilterStatus').value;
            const tbody = document.getElementById('usersTableBody');

            let filtered = usersData.filter(u => {
                const matchQuery = (u.legal_name || '').toLowerCase().includes(query) ||
                                   (u.phone || '').includes(query) ||
                                   String(u.id).includes(query);
                if (!matchQuery) return false;

                if (statusFilter === 'pending') return !u.is_approved;
                if (statusFilter === 'approved') return u.is_approved;
                if (statusFilter === 'admin') return u.is_admin;
                return true;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 40px; color: var(--text-muted);">No matching users found</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.map(u => {
                // Find which channels this user is entitled to
                const userChannels = channelsData.filter(c => {
                    if (c.allowed_user_ids) {
                        const allowed = c.allowed_user_ids.split(',').map(s => s.trim());
                        return allowed.includes(String(u.id)) || allowed.includes(u.phone) || c.admin_id === u.id;
                    }
                    return !c.is_protected && !c.is_temporary && (c.name || '').toLowerCase() === 'global';
                });

                const channelPills = userChannels.length > 0 
                    ? userChannels.map(c => `<span class="pill pill-channel">${c.name}</span>`).join(' ')
                    : '<span style="color: var(--text-muted); font-size: 11px;">None</span>';

                const createdStr = u.created_at ? new Date(u.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) : '--';

                return `
                    <tr>
                        <td class="col-id">#${u.id}</td>
                        <td class="col-user">${escapeHtml(u.legal_name || 'Agent')}</td>
                        <td class="col-mono">${escapeHtml(u.phone)}</td>
                        <td>${channelPills}</td>
                        <td>
                            ${u.is_admin ? '<span class="pill pill-admin">Admin 👑</span>' : '<span class="pill pill-user">User</span>'}
                        </td>
                        <td>
                            ${u.is_approved 
                                ? '<span class="pill pill-approved">● Approved</span>' 
                                : '<span class="pill pill-pending">● Pending</span>'}
                        </td>
                        <td style="font-size: 12px; color: var(--text-muted);">${createdStr}</td>
                        <td>
                            <div class="action-group">
                                ${u.is_approved
                                    ? `<button class="btn-icon" title="Revoke Approval" onclick="toggleUserApproval(${u.id}, false)">⏸️</button>`
                                    : `<button class="btn-icon success" title="Approve Agent" onclick="toggleUserApproval(${u.id}, true)">✅</button>`}
                                <button class="btn-icon" title="Edit Agent" onclick="openEditUserModal(${u.id})">✏️</button>
                                <button class="btn-icon danger" title="Delete User" onclick="deleteUser(${u.id}, '${escapeHtml(u.legal_name || u.phone)}')">🗑️</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // Render Channels Table
        function renderChannelsTable() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const typeFilter = document.getElementById('channelFilterType').value;
            const tbody = document.getElementById('channelsTableBody');

            let filtered = channelsData.filter(c => {
                const matchQuery = (c.name || '').toLowerCase().includes(query) || String(c.id).includes(query);
                if (!matchQuery) return false;

                if (typeFilter === 'permanent') return !c.is_temporary;
                if (typeFilter === 'temporary') return c.is_temporary;
                if (typeFilter === 'protected') return c.is_protected;
                return true;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 40px; color: var(--text-muted);">No matching channels found</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.map(c => {
                const memberCount = c.allowed_user_ids ? c.allowed_user_ids.split(',').filter(x => x.trim()).length : (c.name && c.name.toLowerCase() === 'global' ? 'All (Public)' : 0);
                const adminUser = usersData.find(u => u.id === c.admin_id);
                const adminName = adminUser ? `${adminUser.legal_name} (${adminUser.phone})` : (c.admin_id ? `ID #${c.admin_id}` : 'System');
                const createdStr = c.created_at ? new Date(c.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : '--';

                return `
                    <tr>
                        <td class="col-id">#${c.id}</td>
                        <td class="col-user" style="color: var(--gold-light); font-weight: 700;">${escapeHtml(c.name)}</td>
                        <td>
                            ${c.is_temporary ? '<span class="pill pill-pending">Temporary</span>' : '<span class="pill pill-user">Permanent</span>'}
                        </td>
                        <td>
                            ${c.is_protected ? '<span class="pill pill-protected">🔒 PIN Protected</span>' : '<span class="pill pill-public">🌐 Open</span>'}
                        </td>
                        <td style="font-size: 12px;">${escapeHtml(adminName)}</td>
                        <td><span class="pill pill-channel">${memberCount} Members</span></td>
                        <td style="font-size: 12px; color: var(--text-muted);">${createdStr}</td>
                        <td>
                            <div class="action-group">
                                <button class="btn-icon" title="Edit Channel" onclick="openEditChannelModal(${c.id})">✏️</button>
                                <button class="btn-icon danger" title="Delete Channel" onclick="deleteChannel(${c.id}, '${escapeHtml(c.name)}')">🗑️</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // Toggle User Approval
        async function toggleUserApproval(userId, approve) {
            try {
                if (approve) {
                    await api(`/admin/approve-user/${userId}`, { method: 'PATCH' });
                    showToast('User approved successfully', 'success');
                } else {
                    await api(`/admin/users/${userId}`, {
                        method: 'PATCH',
                        body: { is_approved: false }
                    });
                    showToast('User approval revoked', 'success');
                }
                loadAllData();
            } catch (err) {}
        }

        // Delete User
        async function deleteUser(userId, name) {
            if (!confirm(`Are you sure you want to permanently delete user "${name}" (ID #${userId})?`)) return;
            try {
                await api(`/admin/users/${userId}`, { method: 'DELETE' });
                showToast(`User "${name}" deleted`, 'success');
                loadAllData();
            } catch (err) {}
        }

        // Delete Channel
        async function deleteChannel(channelId, name) {
            if (!confirm(`Are you sure you want to delete channel "${name}" (ID #${channelId})?`)) return;
            try {
                await api(`/admin/channels/${channelId}`, { method: 'DELETE' });
                showToast(`Channel "${name}" deleted`, 'success');
                loadAllData();
            } catch (err) {}
        }

        // User Create / Edit Modal
        function openCreateUserModal() {
            document.getElementById('userModalTitle').innerText = 'Add New Agent';
            document.getElementById('userFormId').value = '';
            document.getElementById('userFormLegalName').value = '';
            document.getElementById('userFormPhone').value = '';
            document.getElementById('userFormPassword').value = '';
            document.getElementById('userFormPasswordLabel').innerText = 'Passcode (Required)';
            document.getElementById('userFormPassword').required = true;
            document.getElementById('userFormApproved').checked = true;
            document.getElementById('userFormAdmin').checked = false;

            renderUserChannelsPicker([]);
            openModal('userModal');
        }

        function openEditUserModal(userId) {
            const user = usersData.find(u => u.id === userId);
            if (!user) return;

            document.getElementById('userModalTitle').innerText = `Edit Agent (#${user.id})`;
            document.getElementById('userFormId').value = user.id;
            document.getElementById('userFormLegalName').value = user.legal_name || '';
            document.getElementById('userFormPhone').value = user.phone || '';
            document.getElementById('userFormPassword').value = '';
            document.getElementById('userFormPasswordLabel').innerText = 'New Passcode (Leave empty to keep current)';
            document.getElementById('userFormPassword').required = false;
            document.getElementById('userFormApproved').checked = user.is_approved;
            document.getElementById('userFormAdmin').checked = user.is_admin;

            // Find user's current channel IDs
            const userChannelIds = channelsData.filter(c => {
                if (c.allowed_user_ids) {
                    const allowed = c.allowed_user_ids.split(',').map(s => s.trim());
                    return allowed.includes(String(user.id)) || allowed.includes(user.phone) || c.admin_id === user.id;
                }
                return false;
            }).map(c => c.id);

            renderUserChannelsPicker(userChannelIds);
            openModal('userModal');
        }

        function renderUserChannelsPicker(selectedIds) {
            const container = document.getElementById('userFormChannelsPicker');
            container.innerHTML = channelsData.map(c => `
                <label class="channel-check-item">
                    <input type="checkbox" name="userChannels" value="${c.id}" ${selectedIds.includes(c.id) ? 'checked' : ''}>
                    <span>${escapeHtml(c.name)}</span>
                </label>
            `).join('');
        }

        async function handleUserFormSubmit(e) {
            e.preventDefault();
            const id = document.getElementById('userFormId').value;
            const legal_name = document.getElementById('userFormLegalName').value.trim();
            const phone = document.getElementById('userFormPhone').value.trim();
            const password = document.getElementById('userFormPassword').value.trim();
            const is_approved = document.getElementById('userFormApproved').checked;
            const is_admin = document.getElementById('userFormAdmin').checked;

            const selectedChannels = Array.from(document.querySelectorAll('input[name="userChannels"]:checked'))
                                          .map(cb => parseInt(cb.value));

            const payload = {
                legal_name,
                phone,
                is_approved,
                is_admin,
                channel_ids: selectedChannels
            };
            if (password) payload.password = password;

            try {
                if (id) {
                    await api(`/admin/users/${id}`, { method: 'PATCH', body: payload });
                    showToast('Agent updated successfully', 'success');
                } else {
                    if (!password) { showToast('Password is required for new users', 'error'); return; }
                    payload.password = password;
                    await api('/admin/users', { method: 'POST', body: payload });
                    showToast('Agent created successfully', 'success');
                }
                closeModal('userModal');
                loadAllData();
            } catch (err) {}
        }

        // Channel Create / Edit Modal
        function openCreateChannelModal() {
            document.getElementById('channelModalTitle').innerText = 'Create Channel';
            document.getElementById('channelFormId').value = '';
            document.getElementById('channelFormName').value = '';
            document.getElementById('channelFormProtected').checked = false;
            document.getElementById('channelFormTemporary').checked = false;
            document.getElementById('channelFormPassword').value = '';
            toggleChannelPasswordInput();

            populateChannelAdminSelect(null);
            renderChannelUsersPicker([]);
            openModal('channelModal');
        }

        function openEditChannelModal(channelId) {
            const channel = channelsData.find(c => c.id === channelId);
            if (!channel) return;

            document.getElementById('channelModalTitle').innerText = `Edit Channel (#${channel.id})`;
            document.getElementById('channelFormId').value = channel.id;
            document.getElementById('channelFormName').value = channel.name || '';
            document.getElementById('channelFormProtected').checked = channel.is_protected;
            document.getElementById('channelFormTemporary').checked = channel.is_temporary;
            document.getElementById('channelFormPassword').value = '';
            toggleChannelPasswordInput();

            populateChannelAdminSelect(channel.admin_id);
            
            const allowedIds = channel.allowed_user_ids ? channel.allowed_user_ids.split(',').map(s => s.trim()) : [];
            renderChannelUsersPicker(allowedIds);
            openModal('channelModal');
        }

        function toggleChannelPasswordInput() {
            const isProtected = document.getElementById('channelFormProtected').checked;
            document.getElementById('channelPasswordGroup').style.display = isProtected ? 'flex' : 'none';
        }

        function populateChannelAdminSelect(selectedAdminId) {
            const select = document.getElementById('channelFormAdminId');
            select.innerHTML = '<option value="">No Specific Admin (System Channel)</option>' +
                usersData.map(u => `
                    <option value="${u.id}" ${u.id === selectedAdminId ? 'selected' : ''}>
                        ${escapeHtml(u.legal_name)} (${u.phone}) ${u.is_admin ? '★ Admin' : ''}
                    </option>
                `).join('');
        }

        function renderChannelUsersPicker(selectedAllowedIds) {
            const container = document.getElementById('channelFormUsersPicker');
            container.innerHTML = usersData.map(u => {
                const isChecked = selectedAllowedIds.includes(String(u.id)) || selectedAllowedIds.includes(u.phone);
                return `
                    <label class="channel-check-item">
                        <input type="checkbox" name="channelUsers" value="${u.id}" ${isChecked ? 'checked' : ''}>
                        <span>${escapeHtml(u.legal_name)} (${u.phone})</span>
                    </label>
                `;
            }).join('');
        }

        async function handleChannelFormSubmit(e) {
            e.preventDefault();
            const id = document.getElementById('channelFormId').value;
            const name = document.getElementById('channelFormName').value.trim();
            const is_protected = document.getElementById('channelFormProtected').checked;
            const is_temporary = document.getElementById('channelFormTemporary').checked;
            const password = document.getElementById('channelFormPassword').value.trim();
            const admin_id_val = document.getElementById('channelFormAdminId').value;
            const admin_id = admin_id_val ? parseInt(admin_id_val) : null;

            const selectedUserIds = Array.from(document.querySelectorAll('input[name="channelUsers"]:checked'))
                                         .map(cb => cb.value);

            const payload = {
                name,
                is_protected,
                is_temporary,
                admin_id,
                allowed_user_ids: selectedUserIds.join(',')
            };
            if (password) payload.password = password;

            try {
                if (id) {
                    await api(`/admin/channels/${id}`, { method: 'PATCH', body: payload });
                    showToast('Channel updated successfully', 'success');
                } else {
                    await api('/admin/channels', { method: 'POST', body: payload });
                    showToast('Channel created successfully', 'success');
                }
                closeModal('channelModal');
                loadAllData();
            } catch (err) {}
        }

        // Modal Helpers
        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }

        // Toast Feedback Helper
        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.innerText = message;
            container.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        function escapeHtml(str) {
            if (!str) return '';
            return String(str).replace(/[&<>"']/g, m => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
            })[m]);
        }
    </script>
</body>
</html>
"""
