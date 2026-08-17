"""
Super Admin Console HTML Template & Asset Renderer for Cellular WKTK
Enhanced with high-performance responsive UI, interactive loading states,
Cancel/Submit dialogue controls, and dark cyberpunk styling.
"""

ADMIN_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cellular WKTK // Super Admin Console</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #080a0f;
            --bg-surface: #0f131c;
            --bg-card: #151a26;
            --bg-card-hover: #1c2233;
            --bg-input: #0b0e16;
            --border-subtle: #202738;
            --border-highlight: #2f3952;
            
            --gold: #f59e0b;
            --gold-light: #fbbf24;
            --gold-glow: rgba(245, 158, 11, 0.16);
            
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

        /* Top Progress Bar for API Requests */
        #topProgressBar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #f59e0b, #fbbf24, #10b981, #f59e0b);
            background-size: 300% 100%;
            animation: moveGradient 1.5s infinite linear;
            z-index: 99999;
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
        }

        #topProgressBar.active {
            opacity: 1;
        }

        @keyframes moveGradient {
            0% { background-position: 0% 0; }
            100% { background-position: 300% 0; }
        }

        /* Top Header */
        header {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border-subtle);
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(12px);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);
            flex-shrink: 0;
        }

        .brand-icon svg {
            width: 20px;
            height: 20px;
            fill: #000;
        }

        .brand-text h1 {
            font-size: 16px;
            font-weight: 800;
            letter-spacing: 0.04em;
            color: #fff;
            line-height: 1.2;
        }

        .brand-text p {
            font-size: 10px;
            color: var(--gold);
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .db-status {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            padding: 6px 12px;
            border-radius: var(--radius-md);
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--emerald);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--emerald);
            animation: pulseDot 2s infinite ease-in-out;
        }

        @keyframes pulseDot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.85); }
        }

        .btn-logout {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 7px 14px;
            border-radius: var(--radius-md);
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 6px;
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
            padding: 24px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 14px;
        }

        .stat-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 18px 20px;
            position: relative;
            overflow: hidden;
            transition: var(--transition);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .stat-card:hover {
            border-color: var(--border-highlight);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.35);
        }

        .stat-label {
            font-size: 11px;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }

        .stat-value {
            font-size: 30px;
            font-weight: 800;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.1;
        }

        .stat-sub {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 6px;
            font-weight: 500;
        }

        /* Skeleton shimmer for loading */
        .skeleton {
            background: linear-gradient(90deg, #151a26 25%, #222a3d 50%, #151a26 75%);
            background-size: 200% 100%;
            animation: skeletonShimmer 1.5s infinite;
            border-radius: 4px;
            display: inline-block;
        }

        .skeleton-text {
            height: 14px;
            width: 80%;
            margin: 4px 0;
        }

        .skeleton-value {
            height: 28px;
            width: 50%;
            margin: 4px 0;
            border-radius: 6px;
        }

        .skeleton-pill {
            height: 20px;
            width: 70px;
            border-radius: 20px;
        }

        @keyframes skeletonShimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* Tabs Navigation & Toolbar */
        .tab-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 12px;
            gap: 12px;
            flex-wrap: wrap;
        }

        .tab-group {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            padding: 9px 18px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }

        .tab-btn:hover {
            color: var(--text-primary);
            background: var(--bg-card);
        }

        .tab-btn.active {
            background: var(--bg-card);
            border-color: var(--gold);
            color: var(--gold-light);
            box-shadow: 0 0 14px var(--gold-glow);
        }

        .tab-btn .badge {
            background: rgba(255,255,255,0.08);
            color: inherit;
            padding: 2px 7px;
            border-radius: 10px;
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
        }

        .tab-actions {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        /* Buttons & Inputs */
        .btn-primary {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            border: none;
            padding: 9px 18px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.02em;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            white-space: nowrap;
        }

        .btn-primary:hover:not(:disabled) {
            filter: brightness(1.1);
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);
        }

        .btn-primary:active:not(:disabled) {
            transform: translateY(0);
        }

        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            filter: grayscale(0.5);
        }

        .btn-secondary {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
            padding: 9px 16px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            white-space: nowrap;
        }

        .btn-secondary:hover:not(:disabled) {
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
            color: #fff;
        }

        .btn-secondary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .search-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .search-wrapper svg {
            position: absolute;
            left: 12px;
            color: var(--text-muted);
            pointer-events: none;
            width: 14px;
            height: 14px;
        }

        .search-input {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 8px 14px 8px 34px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
            width: 240px;
            transition: var(--transition);
        }

        .search-input:focus {
            border-color: var(--gold);
            box-shadow: 0 0 0 2px var(--gold-glow);
        }

        /* Spinners */
        .spinner {
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid rgba(255, 255, 255, 0.25);
            border-radius: 50%;
            border-top-color: currentColor;
            animation: spin 0.6s linear infinite;
        }

        .spinner-primary {
            border-color: rgba(0, 0, 0, 0.25);
            border-top-color: #000;
        }

        .spinning {
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Content Panel & Tables */
        .content-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        }

        .panel-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }

        .panel-title {
            font-size: 15px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .table-responsive {
            overflow-x: auto;
            width: 100%;
            -webkit-overflow-scrolling: touch;
        }

        .table-responsive::-webkit-scrollbar {
            height: 8px;
        }

        .table-responsive::-webkit-scrollbar-track {
            background: var(--bg-surface);
        }

        .table-responsive::-webkit-scrollbar-thumb {
            background: var(--border-highlight);
            border-radius: 4px;
        }

        table {
            width: 100%;
            min-width: 780px;
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
            padding: 13px 18px;
            border-bottom: 1px solid var(--border-subtle);
            white-space: nowrap;
        }

        td {
            padding: 14px 18px;
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
            gap: 5px;
            padding: 4px 9px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .pill-approved { background: var(--emerald-bg); color: var(--emerald); border: 1px solid rgba(16, 185, 129, 0.2); }
        .pill-pending { background: var(--amber-bg); color: var(--amber); border: 1px solid rgba(249, 115, 22, 0.2); }
        .pill-admin { background: var(--gold-glow); color: var(--gold-light); border: 1px solid rgba(245, 158, 11, 0.3); }
        .pill-user { background: var(--bg-card); color: var(--text-secondary); border: 1px solid var(--border-subtle); }
        .pill-protected { background: var(--rose-bg); color: var(--rose); border: 1px solid rgba(239, 68, 68, 0.2); }
        .pill-public { background: var(--cyan-bg); color: var(--cyan); border: 1px solid rgba(6, 182, 212, 0.2); }
        .pill-channel { background: var(--bg-card); color: var(--gold-light); font-family: 'JetBrains Mono', monospace; margin: 2px; border: 1px solid var(--border-subtle); }

        /* Action Buttons in Tables */
        .action-group {
            display: flex;
            align-items: center;
            gap: 6px;
            justify-content: flex-end;
        }

        .btn-icon {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition);
            flex-shrink: 0;
        }

        .btn-icon:hover:not(:disabled) {
            border-color: var(--gold);
            color: var(--gold-light);
            background: var(--bg-card-hover);
            transform: translateY(-1px);
        }

        .btn-icon.danger:hover:not(:disabled) {
            border-color: var(--rose);
            color: var(--rose);
            background: var(--rose-bg);
        }

        .btn-icon.success:hover:not(:disabled) {
            border-color: var(--emerald);
            color: var(--emerald);
            background: var(--emerald-bg);
        }

        .btn-icon:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        /* Modal Overlay & Card */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 16px;
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
            box-shadow: 0 25px 60px rgba(0,0,0,0.85);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            max-height: 90vh;
            transform: scale(0.95);
            transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .modal-overlay.active .modal-card {
            transform: scale(1);
        }

        .modal-header {
            padding: 18px 22px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--bg-surface);
        }

        .modal-header h3 {
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .modal-body {
            padding: 22px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
            -webkit-overflow-scrolling: touch;
        }

        .modal-body::-webkit-scrollbar {
            width: 6px;
        }

        .modal-body::-webkit-scrollbar-thumb {
            background: var(--border-highlight);
            border-radius: 3px;
        }

        .modal-footer {
            padding: 16px 22px;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 12px;
            background: var(--bg-card);
        }

        .form-grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .form-group label {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .form-control {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 10px 14px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
            transition: var(--transition);
            width: 100%;
        }

        .form-control:focus {
            border-color: var(--gold);
            box-shadow: 0 0 0 2px var(--gold-glow);
        }

        .form-control:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .checkbox-card {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: var(--transition);
        }

        .checkbox-card:hover {
            border-color: var(--border-highlight);
            background: var(--bg-card-hover);
        }

        .checkbox-card input[type="checkbox"] {
            width: 17px;
            height: 17px;
            accent-color: var(--gold);
            cursor: pointer;
        }

        .checkbox-card label {
            font-size: 13px;
            color: var(--text-primary);
            cursor: pointer;
            font-weight: 500;
            user-select: none;
        }

        .channels-picker {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 10px;
            max-height: 160px;
            overflow-y: auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 8px;
        }

        .channel-check-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 6px 8px;
            border-radius: var(--radius-sm);
            background: var(--bg-card);
            border: 1px solid transparent;
            transition: var(--transition);
            user-select: none;
        }

        .channel-check-item:hover {
            color: #fff;
            background: var(--bg-card-hover);
            border-color: var(--border-subtle);
        }

        .channel-check-item input[type="checkbox"] {
            accent-color: var(--gold);
            cursor: pointer;
        }

        /* Toast Notifications */
        #toastContainer {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: calc(100vw - 40px);
            pointer-events: none;
        }

        .toast {
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            color: #fff;
            padding: 12px 18px;
            border-radius: var(--radius-md);
            font-size: 13px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.6);
            display: flex;
            align-items: center;
            gap: 10px;
            pointer-events: all;
            animation: slideToast 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            transition: all 0.25s ease;
        }

        .toast.success { border-color: var(--emerald); color: #fff; }
        .toast.success .toast-icon { color: var(--emerald); }
        .toast.error { border-color: var(--rose); color: #fff; }
        .toast.error .toast-icon { color: var(--rose); }
        .toast.info { border-color: var(--gold); color: #fff; }
        .toast.info .toast-icon { color: var(--gold); }

        @keyframes slideToast {
            from { transform: translateX(60px); opacity: 0; }
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
            padding: 32px 28px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            gap: 18px;
            text-align: center;
        }

        .login-card h2 {
            font-size: 20px;
            font-weight: 800;
            color: #fff;
            margin-top: 6px;
        }

        .login-card p {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .hidden { display: none !important; }

        /* Responsive Media Queries */
        @media (max-width: 1024px) {
            main { padding: 18px; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 768px) {
            header {
                padding: 10px 16px;
            }
            .brand-text h1 {
                font-size: 14px;
            }
            .brand-text p {
                font-size: 9px;
            }
            .db-status span {
                display: none;
            }
            .db-status {
                padding: 6px 8px;
            }
            .btn-logout span {
                display: none;
            }
            .btn-logout {
                padding: 7px 10px;
            }
            main {
                padding: 14px;
                gap: 16px;
            }
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }
            .stat-card {
                padding: 14px;
            }
            .stat-value {
                font-size: 24px;
            }
            .tab-bar {
                flex-direction: column;
                align-items: stretch;
            }
            .tab-group {
                width: 100%;
            }
            .tab-btn {
                flex: 1;
                justify-content: center;
                padding: 8px 12px;
                font-size: 12px;
            }
            .tab-actions {
                width: 100%;
                display: flex;
                gap: 8px;
            }
            .search-wrapper {
                flex: 1;
            }
            .search-input {
                width: 100%;
            }
            .panel-header {
                padding: 12px 14px;
            }
            .form-grid-2 {
                grid-template-columns: 1fr;
            }
            .modal-card {
                max-height: 92vh;
            }
            .modal-header, .modal-body, .modal-footer {
                padding: 14px 16px;
            }
        }

        @media (max-width: 480px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .tab-actions {
                flex-direction: column;
            }
            .tab-actions .btn-secondary,
            .tab-actions .btn-primary {
                width: 100%;
            }
            .modal-footer {
                flex-direction: column-reverse;
            }
            .modal-footer button {
                width: 100%;
            }
            #toastContainer {
                bottom: 12px;
                right: 12px;
                left: 12px;
                max-width: none;
            }
        }
    </style>
</head>
<body>

    <!-- Top API Progress Bar -->
    <div id="topProgressBar"></div>

    <!-- Auth Protection Overlay -->
    <div id="loginOverlay">
        <div class="login-card">
            <div style="display: flex; justify-content: center;">
                <div class="brand-icon" style="width: 50px; height: 50px;">
                    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
                </div>
            </div>
            <div>
                <h2>Super Admin Access</h2>
                <p>Authenticate with master admin credentials to access database and permission controls.</p>
            </div>
            <form id="adminLoginForm" onsubmit="handleAdminLogin(event)" style="display: flex; flex-direction: column; gap: 12px; text-align: left;">
                <div class="form-group">
                    <label>Admin Phone Number</label>
                    <input type="text" id="loginPhone" class="form-control" placeholder="017XXXXXXXX" required autofocus>
                </div>
                <div class="form-group">
                    <label>Admin Passcode</label>
                    <input type="password" id="loginPassword" class="form-control" placeholder="••••••••" required>
                </div>
                <button type="submit" id="btnLoginSubmit" class="btn-primary" style="justify-content: center; width: 100%; padding: 11px; margin-top: 6px;">
                    <span>Authenticate & Enter Console</span>
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
            <div class="db-status" title="PostgreSQL Database Online">
                <div class="status-dot"></div>
                <span>Neon PostgreSQL Online</span>
            </div>
            <button class="btn-logout" onclick="handleLogout()" title="Sign Out">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
                <span>Sign Out</span>
            </button>
        </div>
    </header>

    <!-- Main Content Body -->
    <main>
        <!-- Live System Metric Cards -->
        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-label">Total Users</div>
                <div class="stat-value" id="statTotalUsers">
                    <span class="skeleton skeleton-value"></span>
                </div>
                <div class="stat-sub" id="statUsersSub">Loading metrics...</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Channels & Groups</div>
                <div class="stat-value" id="statTotalChannels">
                    <span class="skeleton skeleton-value"></span>
                </div>
                <div class="stat-sub" id="statChannelsSub">Loading metrics...</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Pending Approval</div>
                <div class="stat-value" id="statPendingCount" style="color: var(--gold-light);">
                    <span class="skeleton skeleton-value"></span>
                </div>
                <div class="stat-sub">Action required</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Admins Registered</div>
                <div class="stat-value" id="statAdminCount" style="color: var(--cyan);">
                    <span class="skeleton skeleton-value"></span>
                </div>
                <div class="stat-sub">Master privilege accounts</div>
            </div>
        </div>

        <!-- Navigation Tabs & Actions Toolbar -->
        <div class="tab-bar">
            <div class="tab-group">
                <button class="tab-btn active" onclick="switchTab('users')" id="tabBtnUsers">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
                    <span>User Directory</span>
                    <span class="badge" id="tabUserCount">0</span>
                </button>
                <button class="tab-btn" onclick="switchTab('channels')" id="tabBtnChannels">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                    <span>Channels & Radios</span>
                    <span class="badge" id="tabChannelCount">0</span>
                </button>
            </div>

            <div class="tab-actions">
                <div class="search-wrapper">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                    <input type="text" id="searchInput" class="search-input" placeholder="Search by name, phone, id..." oninput="handleSearch()">
                </div>
                <button class="btn-secondary" id="btnRefresh" onclick="refreshData()" title="Reload Data">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" id="refreshIcon"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
                    <span>Refresh</span>
                </button>
                <button class="btn-primary" id="btnPrimaryAction" onclick="openCreateUserModal()">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                    <span>Add Agent</span>
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
                        <!-- Skeleton loading initial rows -->
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
                        <!-- Skeleton loading initial rows -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <!-- User / Agent Modal (Create & Edit) -->
    <div class="modal-overlay" id="userModal" onclick="handleBackdropClick(event, 'userModal')">
        <div class="modal-card">
            <div class="modal-header">
                <h3 id="userModalTitle">Add New Agent</h3>
                <button type="button" class="btn-icon" onclick="closeModal('userModal')" title="Close">✕</button>
            </div>
            <form id="userForm" onsubmit="handleUserFormSubmit(event)">
                <input type="hidden" id="userFormId">
                <div class="modal-body">
                    <div class="form-group">
                        <label>Legal Name / Callsign</label>
                        <input type="text" id="userFormLegalName" class="form-control" placeholder="e.g. Asad Mushad" required>
                    </div>
                    <div class="form-group">
                        <label>Phone Number (Login ID)</label>
                        <input type="text" id="userFormPhone" class="form-control" placeholder="e.g. 01712345678" required>
                    </div>
                    <div class="form-group">
                        <label id="userFormPasswordLabel">Passcode (Required)</label>
                        <input type="password" id="userFormPassword" class="form-control" placeholder="Enter secure passcode">
                    </div>
                    <div class="form-grid-2">
                        <div class="checkbox-card">
                            <input type="checkbox" id="userFormApproved">
                            <label for="userFormApproved">Approved for App</label>
                        </div>
                        <div class="checkbox-card">
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
                    <button type="button" class="btn-secondary" id="userCancelBtn" onclick="closeModal('userModal')">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        <span>Cancel</span>
                    </button>
                    <button type="submit" class="btn-primary" id="userSubmitBtn">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                        <span>Submit</span>
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Channel Modal (Create & Edit) -->
    <div class="modal-overlay" id="channelModal" onclick="handleBackdropClick(event, 'channelModal')">
        <div class="modal-card">
            <div class="modal-header">
                <h3 id="channelModalTitle">Create Channel</h3>
                <button type="button" class="btn-icon" onclick="closeModal('channelModal')" title="Close">✕</button>
            </div>
            <form id="channelForm" onsubmit="handleChannelFormSubmit(event)">
                <input type="hidden" id="channelFormId">
                <div class="modal-body">
                    <div class="form-group">
                        <label>Channel Name</label>
                        <input type="text" id="channelFormName" class="form-control" placeholder="e.g. Tactical Alpha" required>
                    </div>
                    <div class="form-grid-2">
                        <div class="checkbox-card">
                            <input type="checkbox" id="channelFormProtected" onchange="toggleChannelPasswordInput()">
                            <label for="channelFormProtected">Protected (PIN)</label>
                        </div>
                        <div class="checkbox-card">
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
                    <button type="button" class="btn-secondary" id="channelCancelBtn" onclick="closeModal('channelModal')">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        <span>Cancel</span>
                    </button>
                    <button type="submit" class="btn-primary" id="channelSubmitBtn">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                        <span>Submit</span>
                    </button>
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
        let isInitialLoading = true;
        let activeRequests = 0;

        // Initialize Console on page load
        window.addEventListener('DOMContentLoaded', () => {
            renderSkeletonTable('usersTableBody', 6);
            renderSkeletonTable('channelsTableBody', 6);

            // Close modals on Escape key
            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    closeModal('userModal');
                    closeModal('channelModal');
                }
            });

            if (adminToken) {
                document.getElementById('loginOverlay').classList.add('hidden');
                loadAllData();
            } else {
                document.getElementById('loginOverlay').classList.remove('hidden');
            }
        });

        // Top Progress Bar Controller
        function updateProgressBar(delta) {
            activeRequests += delta;
            const bar = document.getElementById('topProgressBar');
            if (bar) {
                if (activeRequests > 0) {
                    bar.classList.add('active');
                } else {
                    activeRequests = 0;
                    bar.classList.remove('active');
                }
            }
        }

        // Render Skeleton Table Rows
        function renderSkeletonTable(tbodyId, rowCount = 5) {
            const tbody = document.getElementById(tbodyId);
            if (!tbody) return;
            let rows = '';
            for (let i = 0; i < rowCount; i++) {
                rows += `
                    <tr>
                        <td><span class="skeleton" style="width: 30px; height: 16px;"></span></td>
                        <td><span class="skeleton" style="width: 130px; height: 16px;"></span></td>
                        <td><span class="skeleton" style="width: 100px; height: 16px;"></span></td>
                        <td><span class="skeleton skeleton-pill"></span></td>
                        <td><span class="skeleton skeleton-pill"></span></td>
                        <td><span class="skeleton skeleton-pill"></span></td>
                        <td><span class="skeleton" style="width: 70px; height: 14px;"></span></td>
                        <td>
                            <div class="action-group">
                                <span class="skeleton" style="width: 30px; height: 30px; border-radius: 6px;"></span>
                                <span class="skeleton" style="width: 30px; height: 30px; border-radius: 6px;"></span>
                                <span class="skeleton" style="width: 30px; height: 30px; border-radius: 6px;"></span>
                            </div>
                        </td>
                    </tr>
                `;
            }
            tbody.innerHTML = rows;
        }

        // API Call Helper with Auth Headers & Progress Bar
        async function api(path, options = {}) {
            options.headers = options.headers || {};
            if (adminToken) {
                options.headers['Authorization'] = 'Bearer ' + adminToken;
            }
            if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(options.body);
            }
            
            updateProgressBar(1);
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
            } finally {
                updateProgressBar(-1);
            }
        }

        // Authentication Handler with Submit Loading State
        async function handleAdminLogin(e) {
            e.preventDefault();
            const phone = document.getElementById('loginPhone').value.trim();
            const password = document.getElementById('loginPassword').value.trim();
            const submitBtn = document.getElementById('btnLoginSubmit');

            setButtonLoading(submitBtn, true, 'Authenticating...');

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
            } finally {
                setButtonLoading(submitBtn, false, 'Authenticate & Enter Console');
            }
        }

        function handleLogout() {
            adminToken = '';
            localStorage.removeItem('wktk_admin_token');
            document.getElementById('loginOverlay').classList.remove('hidden');
            showToast('Signed out successfully', 'info');
        }

        // Refresh Data helper with button animation
        async function refreshData() {
            const refreshBtn = document.getElementById('btnRefresh');
            const icon = document.getElementById('refreshIcon');
            if (icon) icon.classList.add('spinning');
            if (refreshBtn) refreshBtn.disabled = true;

            await loadAllData();

            setTimeout(() => {
                if (icon) icon.classList.remove('spinning');
                if (refreshBtn) refreshBtn.disabled = false;
            }, 400);
        }

        // Fetch & Reload all Data
        async function loadAllData() {
            if (isInitialLoading) {
                renderSkeletonTable('usersTableBody', 5);
                renderSkeletonTable('channelsTableBody', 5);
            }
            try {
                const [stats, users, channels] = await Promise.all([
                    api('/admin/stats'),
                    api('/admin/users'),
                    api('/admin/channels')
                ]);

                usersData = users || [];
                channelsData = channels || [];
                isInitialLoading = false;

                updateStatsCards(stats);
                renderUsersTable();
                renderChannelsTable();
                
                const userCountEl = document.getElementById('tabUserCount');
                if (userCountEl) userCountEl.innerText = usersData.length;
                const channelCountEl = document.getElementById('tabChannelCount');
                if (channelCountEl) channelCountEl.innerText = channelsData.length;
            } catch (err) {
                console.error('Failed to load dashboard data:', err);
            }
        }

        function updateStatsCards(stats) {
            const elTotalUsers = document.getElementById('statTotalUsers');
            if (elTotalUsers) elTotalUsers.innerText = stats.total_users || usersData.length;
            const elUsersSub = document.getElementById('statUsersSub');
            if (elUsersSub) elUsersSub.innerText = `${stats.approved_users || 0} Approved · ${stats.pending_users || 0} Pending`;
            const elTotalChannels = document.getElementById('statTotalChannels');
            if (elTotalChannels) elTotalChannels.innerText = stats.total_channels || channelsData.length;
            const elChannelsSub = document.getElementById('statChannelsSub');
            if (elChannelsSub) elChannelsSub.innerText = `${stats.protected_channels || 0} Protected · ${stats.public_channels || 0} Open`;
            const elPendingCount = document.getElementById('statPendingCount');
            if (elPendingCount) elPendingCount.innerText = stats.pending_users || 0;
            const elAdminCount = document.getElementById('statAdminCount');
            if (elAdminCount) elAdminCount.innerText = stats.admin_users || 0;
        }

        // Switch Tabs
        function switchTab(tab) {
            currentTab = tab;
            document.getElementById('tabBtnUsers').classList.toggle('active', tab === 'users');
            document.getElementById('tabBtnChannels').classList.toggle('active', tab === 'channels');
            document.getElementById('panelUsers').classList.toggle('hidden', tab !== 'users');
            document.getElementById('panelChannels').classList.toggle('hidden', tab !== 'channels');
            
            const btnPrimary = document.getElementById('btnPrimaryAction');
            if (btnPrimary) {
                if (tab === 'users') {
                    btnPrimary.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg> <span>Add Agent</span>';
                    btnPrimary.onclick = openCreateUserModal;
                } else {
                    btnPrimary.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg> <span>Create Channel</span>';
                    btnPrimary.onclick = openCreateChannelModal;
                }
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
            const searchInput = document.getElementById('searchInput');
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
            const statusFilter = document.getElementById('userFilterStatus').value;
            const tbody = document.getElementById('usersTableBody');
            if (!tbody) return;

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
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" style="opacity: 0.4;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                                <span>No matching agents found</span>
                            </div>
                        </td>
                    </tr>
                `;
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
                    ? userChannels.map(c => `<span class="pill pill-channel">${escapeHtml(c.name)}</span>`).join(' ')
                    : '<span style="color: var(--text-muted); font-size: 11px;">None</span>';

                const createdStr = u.created_at ? new Date(u.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) : '--';

                return `
                    <tr id="user-row-${u.id}">
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
                                    ? `<button class="btn-icon" id="btn-toggle-${u.id}" title="Revoke Approval" onclick="toggleUserApproval(${u.id}, false)">⏸️</button>`
                                    : `<button class="btn-icon success" id="btn-toggle-${u.id}" title="Approve Agent" onclick="toggleUserApproval(${u.id}, true)">✅</button>`}
                                <button class="btn-icon" title="Edit Agent" onclick="openEditUserModal(${u.id})">✏️</button>
                                <button class="btn-icon danger" id="btn-del-user-${u.id}" title="Delete Agent" onclick="deleteUser(${u.id}, '${escapeHtml(u.legal_name || u.phone)}')">🗑️</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // Render Channels Table
        function renderChannelsTable() {
            const searchInput = document.getElementById('searchInput');
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
            const typeFilter = document.getElementById('channelFilterType').value;
            const tbody = document.getElementById('channelsTableBody');
            if (!tbody) return;

            let filtered = channelsData.filter(c => {
                const matchQuery = (c.name || '').toLowerCase().includes(query) || String(c.id).includes(query);
                if (!matchQuery) return false;

                if (typeFilter === 'permanent') return !c.is_temporary;
                if (typeFilter === 'temporary') return c.is_temporary;
                if (typeFilter === 'protected') return c.is_protected;
                return true;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" style="opacity: 0.4;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                                <span>No matching channels found</span>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }

            tbody.innerHTML = filtered.map(c => {
                const memberCount = c.allowed_user_ids ? c.allowed_user_ids.split(',').filter(x => x.trim()).length : (c.name && c.name.toLowerCase() === 'global' ? 'All (Public)' : 0);
                const adminUser = usersData.find(u => String(u.id) === String(c.admin_id));
                const adminName = adminUser ? `${adminUser.legal_name} (${adminUser.phone})` : (c.admin_id ? `ID #${c.admin_id}` : 'System');
                const createdStr = c.created_at ? new Date(c.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) : '--';

                return `
                    <tr id="channel-row-${c.id}">
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
                                <button class="btn-icon danger" id="btn-del-channel-${c.id}" title="Delete Channel" onclick="deleteChannel(${c.id}, '${escapeHtml(c.name)}')">🗑️</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // Toggle User Approval with loading state
        async function toggleUserApproval(userId, approve) {
            const btn = document.getElementById(`btn-toggle-${userId}`);
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner" style="width:12px; height:12px;"></span>';
            }
            try {
                if (approve) {
                    await api(`/admin/approve-user/${userId}`, { method: 'PATCH' });
                    showToast('Agent approved successfully', 'success');
                } else {
                    await api(`/admin/users/${userId}`, {
                        method: 'PATCH',
                        body: { is_approved: false }
                    });
                    showToast('Agent approval revoked', 'info');
                }
                await loadAllData();
            } catch (err) {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = approve ? '✅' : '⏸️';
                }
            }
        }

        // Delete User with loading state
        async function deleteUser(userId, name) {
            if (!confirm(`Are you sure you want to permanently delete agent "${name}" (ID #${userId})?`)) return;
            const btn = document.getElementById(`btn-del-user-${userId}`);
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner" style="width:12px; height:12px;"></span>';
            }
            try {
                await api(`/admin/users/${userId}`, { method: 'DELETE' });
                showToast(`Agent "${name}" deleted`, 'success');
                await loadAllData();
            } catch (err) {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '🗑️';
                }
            }
        }

        // Delete Channel with loading state
        async function deleteChannel(channelId, name) {
            if (!confirm(`Are you sure you want to delete channel "${name}" (ID #${channelId})?`)) return;
            const btn = document.getElementById(`btn-del-channel-${channelId}`);
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner" style="width:12px; height:12px;"></span>';
            }
            try {
                await api(`/admin/channels/${channelId}`, { method: 'DELETE' });
                showToast(`Channel "${name}" deleted`, 'success');
                await loadAllData();
            } catch (err) {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '🗑️';
                }
            }
        }

        // User / Agent Modal (Create & Edit)
        function openCreateUserModal() {
            const modalTitle = document.getElementById('userModalTitle');
            if (modalTitle) {
                modalTitle.innerHTML = `
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                    <span>Add New Agent</span>
                `;
            }
            document.getElementById('userFormId').value = '';
            document.getElementById('userFormLegalName').value = '';
            document.getElementById('userFormPhone').value = '';
            document.getElementById('userFormPassword').value = '';
            document.getElementById('userFormPasswordLabel').innerText = 'Passcode (Required)';
            document.getElementById('userFormPassword').required = true;
            document.getElementById('userFormApproved').checked = true;
            document.getElementById('userFormAdmin').checked = false;

            setButtonLoading(document.getElementById('userSubmitBtn'), false, 'Submit');
            const cancelBtn = document.getElementById('userCancelBtn');
            if (cancelBtn) cancelBtn.disabled = false;

            renderUserChannelsPicker([]);
            openModal('userModal');
        }

        function openEditUserModal(userId) {
            const user = usersData.find(u => String(u.id) === String(userId));
            if (!user) {
                showToast('User data not found, reloading...', 'error');
                loadAllData();
                return;
            }

            const modalTitle = document.getElementById('userModalTitle');
            if (modalTitle) {
                modalTitle.innerHTML = `
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
                    <span>Edit Agent: ${escapeHtml(user.legal_name || 'Agent')} (#${user.id})</span>
                `;
            }
            document.getElementById('userFormId').value = user.id;
            document.getElementById('userFormLegalName').value = user.legal_name || '';
            document.getElementById('userFormPhone').value = user.phone || '';
            document.getElementById('userFormPassword').value = '';
            document.getElementById('userFormPasswordLabel').innerText = 'New Passcode (Leave blank to keep unchanged)';
            document.getElementById('userFormPassword').required = false;
            document.getElementById('userFormApproved').checked = !!user.is_approved;
            document.getElementById('userFormAdmin').checked = !!user.is_admin;

            setButtonLoading(document.getElementById('userSubmitBtn'), false, 'Submit');
            const cancelBtn = document.getElementById('userCancelBtn');
            if (cancelBtn) cancelBtn.disabled = false;

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
            if (!container) return;
            if (!channelsData || channelsData.length === 0) {
                container.innerHTML = '<span style="color: var(--text-muted); font-size: 12px;">No channels registered</span>';
                return;
            }
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

            const submitBtn = document.getElementById('userSubmitBtn');
            const cancelBtn = document.getElementById('userCancelBtn');

            const payload = {
                legal_name,
                phone,
                is_approved,
                is_admin,
                channel_ids: selectedChannels
            };
            if (password) payload.password = password;

            setButtonLoading(submitBtn, true, 'Submitting...');
            if (cancelBtn) cancelBtn.disabled = true;

            try {
                if (id) {
                    await api(`/admin/users/${id}`, { method: 'PATCH', body: payload });
                    showToast('Agent details updated successfully', 'success');
                } else {
                    if (!password) { 
                        showToast('Password is required for new agents', 'error'); 
                        return; 
                    }
                    payload.password = password;
                    await api('/admin/users', { method: 'POST', body: payload });
                    showToast('Agent created successfully', 'success');
                }
                closeModal('userModal');
                await loadAllData();
            } catch (err) {
                // Error toast handled in api()
            } finally {
                setButtonLoading(submitBtn, false, 'Submit');
                if (cancelBtn) cancelBtn.disabled = false;
            }
        }

        // Channel Modal (Create & Edit)
        function openCreateChannelModal() {
            const modalTitle = document.getElementById('channelModalTitle');
            if (modalTitle) {
                modalTitle.innerHTML = `
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                    <span>Create Channel</span>
                `;
            }
            document.getElementById('channelFormId').value = '';
            document.getElementById('channelFormName').value = '';
            document.getElementById('channelFormProtected').checked = false;
            document.getElementById('channelFormTemporary').checked = false;
            document.getElementById('channelFormPassword').value = '';
            toggleChannelPasswordInput();

            populateChannelAdminSelect(null);
            renderChannelUsersPicker([]);

            setButtonLoading(document.getElementById('channelSubmitBtn'), false, 'Submit');
            const cancelBtn = document.getElementById('channelCancelBtn');
            if (cancelBtn) cancelBtn.disabled = false;

            openModal('channelModal');
        }

        function openEditChannelModal(channelId) {
            const channel = channelsData.find(c => String(c.id) === String(channelId));
            if (!channel) {
                showToast('Channel data not found, reloading...', 'error');
                loadAllData();
                return;
            }

            const modalTitle = document.getElementById('channelModalTitle');
            if (modalTitle) {
                modalTitle.innerHTML = `
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
                    <span>Edit Channel: ${escapeHtml(channel.name)} (#${channel.id})</span>
                `;
            }
            document.getElementById('channelFormId').value = channel.id;
            document.getElementById('channelFormName').value = channel.name || '';
            document.getElementById('channelFormProtected').checked = !!channel.is_protected;
            document.getElementById('channelFormTemporary').checked = !!channel.is_temporary;
            document.getElementById('channelFormPassword').value = '';
            toggleChannelPasswordInput();

            populateChannelAdminSelect(channel.admin_id);
            
            const allowedIds = channel.allowed_user_ids ? channel.allowed_user_ids.split(',').map(s => s.trim()) : [];
            renderChannelUsersPicker(allowedIds);

            setButtonLoading(document.getElementById('channelSubmitBtn'), false, 'Submit');
            const cancelBtn = document.getElementById('channelCancelBtn');
            if (cancelBtn) cancelBtn.disabled = false;

            openModal('channelModal');
        }

        function toggleChannelPasswordInput() {
            const isProtected = document.getElementById('channelFormProtected').checked;
            document.getElementById('channelPasswordGroup').style.display = isProtected ? 'flex' : 'none';
        }

        function populateChannelAdminSelect(selectedAdminId) {
            const select = document.getElementById('channelFormAdminId');
            if (!select) return;
            select.innerHTML = '<option value="">No Specific Admin (System Channel)</option>' +
                usersData.map(u => `
                    <option value="${u.id}" ${String(u.id) === String(selectedAdminId) ? 'selected' : ''}>
                        ${escapeHtml(u.legal_name)} (${u.phone}) ${u.is_admin ? '★ Admin' : ''}
                    </option>
                `).join('');
        }

        function renderChannelUsersPicker(selectedAllowedIds) {
            const container = document.getElementById('channelFormUsersPicker');
            if (!container) return;
            if (!usersData || usersData.length === 0) {
                container.innerHTML = '<span style="color: var(--text-muted); font-size: 12px;">No agents found</span>';
                return;
            }
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

            const submitBtn = document.getElementById('channelSubmitBtn');
            const cancelBtn = document.getElementById('channelCancelBtn');

            const payload = {
                name,
                is_protected,
                is_temporary,
                admin_id,
                allowed_user_ids: selectedUserIds.join(',')
            };
            if (password) payload.password = password;

            setButtonLoading(submitBtn, true, 'Submitting...');
            if (cancelBtn) cancelBtn.disabled = true;

            try {
                if (id) {
                    await api(`/admin/channels/${id}`, { method: 'PATCH', body: payload });
                    showToast('Channel updated successfully', 'success');
                } else {
                    await api('/admin/channels', { method: 'POST', body: payload });
                    showToast('Channel created successfully', 'success');
                }
                closeModal('channelModal');
                await loadAllData();
            } catch (err) {
                // Error handled in api()
            } finally {
                setButtonLoading(submitBtn, false, 'Submit');
                if (cancelBtn) cancelBtn.disabled = false;
            }
        }

        // Modal Helpers
        function openModal(id) { 
            const el = document.getElementById(id);
            if (el) el.classList.add('active'); 
        }

        function closeModal(id) { 
            const el = document.getElementById(id);
            if (el) el.classList.remove('active'); 
        }

        function handleBackdropClick(e, modalId) {
            if (e.target && e.target.id === modalId) {
                closeModal(modalId);
            }
        }

        // Button Loading State Helper (Safely preserves structure)
        function setButtonLoading(btn, isLoading, text = 'Submit') {
            if (!btn) return;
            btn.disabled = isLoading;
            if (isLoading) {
                btn.innerHTML = `<span class="spinner spinner-primary"></span> <span>${escapeHtml(text)}</span>`;
            } else {
                btn.innerHTML = `
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                    <span>${escapeHtml(text)}</span>
                `;
            }
        }

        // Toast Feedback Helper
        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            if (!container) return;
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            
            let iconSvg = '<svg class="toast-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>';
            if (type === 'success') {
                iconSvg = '<svg class="toast-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>';
            } else if (type === 'error') {
                iconSvg = '<svg class="toast-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>';
            }

            toast.innerHTML = `
                ${iconSvg}
                <span style="flex: 1;">${escapeHtml(message)}</span>
                <span style="cursor: pointer; opacity: 0.6; font-size: 14px;" onclick="this.parentElement.remove()">✕</span>
            `;
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
