// /frontend/js/custom/dashboard.js
// GitHub Copilot
(() => {
    const DEFAULT_CONTAINER_ID = "dashboard";

    // Helpers
    const el = (tag, attrs = {}, ...children) => {
        const node = document.createElement(tag);
        Object.entries(attrs).forEach(([k, v]) => {
            if (k === "class") node.className = v;
            else if (k === "style") Object.assign(node.style, v);
            else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2), v);
            else node.setAttribute(k, v);
        });
        children.flat().forEach(c => {
            node.append(typeof c === "string" ? document.createTextNode(c) : c);
        });
        return node;
    };

    const formatCurrency = (n) =>
        typeof n === "number" ? n.toLocaleString(undefined, { style: "currency", currency: "USD" }) : n;

    // Mock fallback data (used if API not available)
    const mockData = {
        totals: {
            revenue: 12458.5,
            orders: 342,
            customers: 128,
            products: 86
        },
        salesSeries: [
            { date: "2025-04-01", value: 300 },
            { date: "2025-04-02", value: 450 },
            { date: "2025-04-03", value: 380 },
            { date: "2025-04-04", value: 520 },
            { date: "2025-04-05", value: 610 },
            { date: "2025-04-06", value: 480 },
            { date: "2025-04-07", value: 700 }
        ],
        categories: [
            { name: "Fruits", value: 40 },
            { name: "Vegetables", value: 25 },
            { name: "Dairy", value: 20 },
            { name: "Bakery", value: 15 }
        ],
        recentOrders: [
            { id: "ORD-1001", customer: "Alice", total: 23.5, status: "Delivered" },
            { id: "ORD-1002", customer: "Bob", total: 12.99, status: "Preparing" },
            { id: "ORD-1003", customer: "Carol", total: 45.0, status: "Out for delivery" },
            { id: "ORD-1004", customer: "Dave", total: 9.49, status: "Cancelled" }
        ]
    };

    // Minimal styling injection to make dashboard usable
    const injectStyles = () => {
        if (document.getElementById("dashboard-styles")) return;
        const style = el("style", { id: "dashboard-styles" }, `
            .dsb-container{font-family:system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial;padding:18px;color:#222}
            .dsb-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:18px}
            .dsb-card{background:#fff;border:1px solid #eee;border-radius:8px;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,0.03)}
            .dsb-title{font-size:13px;color:#666;margin-bottom:6px}
            .dsb-value{font-size:20px;font-weight:600}
            .dsb-main{display:grid;grid-template-columns:2fr 1fr;gap:12px}
            .dsb-charts{display:flex;flex-direction:column;gap:12px}
            .dsb-table{width:100%;border-collapse:collapse}
            .dsb-table th,.dsb-table td{padding:8px;text-align:left;border-bottom:1px solid #f0f0f0;font-size:13px}
            .dsb-actions{display:flex;gap:8px;align-items:center;justify-content:flex-end;margin-bottom:12px}
            button.dsb-btn{padding:8px 10px;border-radius:6px;border:1px solid #ddd;background:#fff;cursor:pointer}
            @media (max-width:900px){.dsb-main{grid-template-columns:1fr}}
        `);
        document.head.appendChild(style);
    };

    // Data fetching
    const fetchData = async () => {
        try {
            const res = await fetch("/api/dashboard", { cache: "no-store" });
            if (!res.ok) throw new Error("API fetch failed");
            const json = await res.json();
            return json;
        } catch (e) {
            return mockData;
        }
    };

    // Render functions
    const renderStats = (totals) => {
        return el("div", { class: "dsb-grid" },
            statCard("Revenue", formatCurrency(totals.revenue)),
            statCard("Orders", String(totals.orders)),
            statCard("Customers", String(totals.customers)),
            statCard("Products", String(totals.products))
        );
    };

    const statCard = (title, value) =>
        el("div", { class: "dsb-card" },
            el("div", { class: "dsb-title" }, title),
            el("div", { class: "dsb-value" }, value)
        );

    const renderRecentOrders = (orders) => {
        const table = el("table", { class: "dsb-table" },
            el("thead", {}, el("tr", {},
                el("th", {}, "Order"),
                el("th", {}, "Customer"),
                el("th", {}, "Total"),
                el("th", {}, "Status")
            )),
            el("tbody", {},
                ...orders.map(o => el("tr", {},
                    el("td", {}, o.id),
                    el("td", {}, o.customer),
                    el("td", {}, formatCurrency(o.total)),
                    el("td", {}, o.status)
                ))
            )
        );
        return el("div", { class: "dsb-card" }, el("div", { class: "dsb-title" }, "Recent Orders"), table);
    };

    const renderSalesChart = (series) => {
        const container = el("div", { class: "dsb-card" },
            el("div", { class: "dsb-title" }, "Sales (last 7 days)"),
            el("canvas", { id: "dsb-sales-chart", width: "600", height: "200" })
        );
        setTimeout(() => drawLineChart("dsb-sales-chart", series), 0);
        return container;
    };

    const renderCategoryChart = (cats) => {
        const container = el("div", { class: "dsb-card" },
            el("div", { class: "dsb-title" }, "Category Breakdown"),
            el("canvas", { id: "dsb-cat-chart", width: "300", height: "200" })
        );
        setTimeout(() => drawDonutChart("dsb-cat-chart", cats), 0);
        return container;
    };

    // Chart drawing (uses Chart.js if available, otherwise draws simple SVG)
    const drawLineChart = (canvasId, series) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const labels = series.map(s => (new Date(s.date)).toLocaleDateString());
        const data = series.map(s => s.value);

        if (window.Chart) {
            const ctx = canvas.getContext("2d");
            new Chart(ctx, {
                type: "line",
                data: { labels, datasets: [{ label: "Sales", data, borderColor: "#3b82f6", backgroundColor: "rgba(59,130,246,0.08)", fill: true }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });
            return;
        }

        // Fallback: simple SVG sparkline
        const w = canvas.width, h = canvas.height;
        const min = Math.min(...data), max = Math.max(...data);
        const points = data.map((v, i) => {
            const x = (i / (data.length - 1 || 1)) * w;
            const y = h - ((v - min) / ((max - min) || 1)) * h;
            return `${x},${y}`;
        }).join(" ");
        const svg = `<svg width="${w}" height="${h}" xmlns="http://www.w3.org/2000/svg">
            <polyline points="${points}" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
        </svg>`;
        const wrapper = document.createElement("div");
        wrapper.innerHTML = svg;
        canvas.replaceWith(wrapper.firstChild);
    };

    const drawDonutChart = (canvasId, cats) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const labels = cats.map(c => c.name);
        const data = cats.map(c => c.value);
        const colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"];

        if (window.Chart) {
            const ctx = canvas.getContext("2d");
            new Chart(ctx, {
                type: "doughnut",
                data: { labels, datasets: [{ data, backgroundColor: colors.slice(0, data.length) }] },
                options: { maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }
            });
            return;
        }

        // Fallback: simple legend and percentages
        const total = data.reduce((a, b) => a + b, 0) || 1;
        const list = el("div", {}, ...cats.map((c, i) =>
            el("div", { style: { display: "flex", gap: "8px", alignItems: "center", marginBottom: "6px" } },
                el("span", { style: { width: "12px", height: "12px", background: colors[i % colors.length], display: "inline-block", borderRadius: "2px" } }),
                el("span", {}, `${c.name}: ${Math.round((c.value / total) * 100)}%`)
            )
        ));
        const wrapper = el("div", {}, list);
        canvas.replaceWith(wrapper);
    };

    // Main render
    const render = (root, data) => {
        root.innerHTML = "";
        injectStyles();

        const header = el("div", { class: "dsb-actions" },
            el("h2", { style: { margin: 0, fontSize: "18px", fontWeight: 600 } }, "Dashboard"),
            el("div", { style: { flex: "1 1 auto" } }),
            el("button", { class: "dsb-btn", onClick: () => refresh(root) }, "Refresh")
        );

        const stats = renderStats(data.totals);
        const salesChart = renderSalesChart(data.salesSeries);
        const catChart = renderCategoryChart(data.categories);
        const recent = renderRecentOrders(data.recentOrders);

        const main = el("div", { class: "dsb-main" },
            el("div", { class: "dsb-charts" }, salesChart, stats),
            el("div", {}, catChart, recent)
        );

        root.append(header, main);
    };

    const refresh = async (root) => {
        const loading = el("div", {}, "Loading...");
        root.appendChild(loading);
        const data = await fetchData();
        root.removeChild(loading);
        render(root, data);
    };

    // Public init
    const init = async (opts = {}) => {
        const id = opts.containerId || DEFAULT_CONTAINER_ID;
        let root = document.getElementById(id);
        if (!root) {
            root = el("div", { id, style: { maxWidth: "1100px", margin: "12px auto" } });
            document.body.appendChild(root);
        }
        const data = await fetchData();
        render(root, data);
    };

    // Auto-init on DOM ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => init());
    } else {
        init();
    }

    // Expose for manual control
    window.dashboard = { init, refresh };
})();