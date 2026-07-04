const BACKEND = "http://localhost:8000";

let lastUrl = window.location.href;
let debounceTimer = null;
let expandedCategory = null;
let hoverCard = document.createElement("div");

hoverCard.id = "email-secure-hover";

hoverCard.style.cssText = `
position:fixed;
display:none;
z-index:999999;
width:270px;
padding:14px;
border-radius:16px;
background:rgba(22,27,34,.88);
backdrop-filter:blur(18px);
-webkit-backdrop-filter:blur(18px);
border:1px solid rgba(255,255,255,.08);
box-shadow:0 12px 35px rgba(0,0,0,.35);
color:#fff;
font-family:Google Sans,Arial,sans-serif;
font-size:13px;
line-height:1.5;
pointer-events:none;
transition:opacity .15s ease;
`;

document.body.appendChild(hoverCard);

/**
 * Extract Gmail rows
 */
function extractEmailRows() {

    const rows =
        document.querySelectorAll(
            "tr.zA"
        );

    return Array
        .from(rows)
        .map((row) => {

            const senderEl =
                row.querySelector(".yP") ||
                row.querySelector(".zF");

            const subjectEl =
                row.querySelector(".bog") ||
                row.querySelector(".bqe span");

            let sender = "";
            let subject = "";

            if (senderEl) {

                sender =
                    senderEl.getAttribute("email") ||
                    senderEl.getAttribute("title") ||
                    senderEl.textContent ||
                    "";
            }

            if (subjectEl) {
                subject =
                    subjectEl
                        .textContent
                        ?.trim() || "";
            }

            return {
                row,
                sender,
                subject
            };
        });
}

/**
 * FastAPI classifier
 */
async function classifyEmail(
    sender,
    subject,
    body
) {

    try {

        const response =
            await fetch(
                `${BACKEND}/classify`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            sender,
                            subject,
                            body
                        })
                }
            );

        if (
            !response.ok
        ) {
            return null;
        }

        return await response.json();

    } catch (error) {

        console.error(
            "[Email Secure] Classification failed:",
            error
        );

        return null;
    }
}

/**
 * Apply category badge + highlighting
 */
function applyHighlight(
    row,
    result,
    sender,
    subject
) {

    if (
        !result ||
        !result.primary
    ) {
        return;
    }

    const category =
        result.primary;

    row.style.borderLeft =
        `4px solid ${category.color}`;

    /*
     * High Risk Highlight
     */

    if (
        result.risk_label ===
        "CRITICAL"
    ) {

        row.style.background =
            "rgba(220,38,38,0.10)";

        row.style.border =
            "1px solid rgba(220,38,38,0.35)";
    }

    if (
        result.risk_label ===
        "HIGH"
    ) {

        row.style.background =
            "rgba(245,158,11,0.10)";

        row.style.border =
            "1px solid rgba(245,158,11,0.35)";
    }

    const subjectContainer =
        row.querySelector(".y6") ||
        row.querySelector(".bog");

    if (
        subjectContainer
    ) {

        const existingBadge =
            subjectContainer.querySelector(
                ".email-secure-badge"
            );

        if (
            !existingBadge
        ) {

            const badge =
                document.createElement(
                    "span"
                );

            badge.className =
                "email-secure-badge";

            const brand =
                result.brand || "Unknown";

            const intent =
                result.intent || category.name;

            badge.textContent =
                `${brand} [${intent}]`;

            badge.style.background =
                category.color;

            badge.style.color =
                category.text_color;

            badge.style.borderRadius =
                "999px";

            badge.style.padding =
                "2px 8px";

            badge.style.fontSize =
                "11px";

            badge.style.fontWeight =
                "600";

            badge.style.marginRight =
                "8px";

            badge.style.display =
                "inline-flex";

            badge.style.alignItems =
                "center";

            badge.style.gap =
                "4px";

            badge.style.whiteSpace =
                "nowrap";

            const dot =
                document.createElement(
                    "span"
                );

            dot.style.width =
                "6px";

            dot.style.height =
                "6px";

            dot.style.borderRadius =
                "50%";

            dot.style.background =
                category.text_color;

            badge.prepend(
                dot
            );

            subjectContainer.prepend(
                badge
            );
        }
    }

    /*
    * Save data for dashboard & hover
    */

    row._emailSecureData = result;

    row.addEventListener("mouseenter", showHoverCard);

    row.addEventListener("mousemove", moveHoverCard);

    row.addEventListener("mouseleave", hideHoverCard);
}

function showHoverCard(e) {

    const row = e.currentTarget;

    const result = row._emailSecureData;

    if (!result)
        return;

    const category = result.primary;

    const riskColor = {

        CRITICAL: "#ef4444",

        HIGH: "#f59e0b",

        SAFE: "#22c55e"

    }[result.risk_label] || "#9ca3af";

    const priorityColor = {

        CRITICAL: "#dc2626",

        WARNING: "#ea580c",

        VERY_HIGH: "#f59e0b",

        HIGH: "#16a34a",

        MEDIUM: "#2563eb",

        LOW: "#6b7280"

    }[category.priority] || "#6b7280";

    /*
     * Link Status
     */

    let linkStatus = "";

    if (
        result.url_results &&
        result.url_results.length > 0
    ) {

        const hasDangerous =
            result.url_results.some(
                url => !url.is_safe
            );

        if (hasDangerous) {

            linkStatus = `
            <div style="
                margin-top:16px;
                font-weight:700;
                color:#ef4444;
            ">
                🔴 Found Links
            </div>
            `;

        } else {

            linkStatus = `
            <div style="
                margin-top:16px;
                font-weight:700;
                color:#22c55e;
            ">
                🟢 Found Links
            </div>
            `;

        }

    }

    hoverCard.innerHTML = `

<div style="
font-size:18px;
font-weight:700;
margin-bottom:2px;
">
🏢 ${result.brand}
</div>

<div style="
font-size:13px;
color:#cbd5e1;
margin-bottom:14px;
">
${result.intent}
</div>

<div style="
display:flex;
justify-content:space-between;
margin:8px 0;
">
<span>🚨 Risk</span>

<span style="
color:${riskColor};
font-weight:700;
">
${result.risk_label}
</span>
</div>

<div style="
display:flex;
justify-content:space-between;
margin:8px 0;
">
<span>⭐ Priority</span>

<span style="
color:${priorityColor};
font-weight:700;
">
${category.priority}
</span>
</div>

<div style="
display:flex;
justify-content:space-between;
margin:8px 0;
">
<span>🏷 Category</span>

<span>
${category.name}
</span>
</div>

<div style="
margin-top:14px;
">

<div style="
display:flex;
justify-content:space-between;
margin-bottom:5px;
">

<span>📊 Match Score</span>

<span>${result.category_score}%</span>

</div>

<div style="
height:7px;
border-radius:999px;
background:#2d3748;
overflow:hidden;
">

<div style="
height:100%;
width:${result.category_score}%;
background:linear-gradient(
90deg,
#22c55e,
#3b82f6
);
">
</div>

</div>

</div>

${linkStatus}

`;

    hoverCard.style.display = "block";

    moveHoverCard(e);

}

function moveHoverCard(e){

    hoverCard.style.left =
        (e.clientX + 20) + "px";

    hoverCard.style.top =
        (e.clientY + 20) + "px";

}

function hideHoverCard(){

    hoverCard.style.display =
        "none";

}

/**
 * Process Inbox
 */
async function processInbox() {

    const emails =
        extractEmailRows();

    for (
        const email
        of emails
    ) {

        const row =
            email.row;

        if (
            row.querySelector(
                ".email-secure-badge"
            )
        ) {
            continue;
        }
        
        const bodyText =
            row.innerText || "";

        const result =
            await classifyEmail(
                email.sender,
                email.subject,
                bodyText
            );

        if (
            result
        ) {

            applyHighlight(
                row,
                result,
                email.sender,
                email.subject
            );
        }
    }

    createDashboard();
    updateDashboard();
}

/**
 * Initial Load
 */

window.addEventListener(
    "load",
    async () => {

        setTimeout(
            async () => {

                await processInbox();

                scanOpenedEmail();

            },
            1500
        );

    }
);

/**
 * Gmail Observer
 */

const observer =
    new MutationObserver(
        () => {

            clearTimeout(
                debounceTimer
            );

            debounceTimer =
                setTimeout(
                    async () => {

                        const currentUrl =
                            window.location.href;

                        if (
                            currentUrl !==
                            lastUrl
                        ) {

                            lastUrl =
                                currentUrl;

                            console.log(
                                "[Email Secure] Gmail navigation detected"
                            );

                            await processInbox();
                            scanOpenedEmail();
                        }

                        await processInbox();
                        scanOpenedEmail();

                    },
                    800
                );
        }
    );

observer.observe(
    document.body,
    {
        childList: true,
        subtree: true
    }
);

console.log(
    "[Email Secure] Content script loaded"
);

function createDashboard() {

    if (
        document.getElementById(
            "email-secure-dashboard"
        )
    ) {
        return;
    }

    const panel =
        document.createElement("div");

    panel.id =
        "email-secure-dashboard";

    panel.style.marginTop =
        "10px";

    panel.style.marginLeft =
        "12px";

    panel.style.marginRight =
        "12px";

    panel.style.width =
        "calc(100% - 24px)";

    panel.style.background =
        "transparent";

    panel.style.color =
        "#202124";

    panel.style.padding =
        "4px";

    panel.style.maxHeight =
        "calc(100vh - 120px)";

    panel.style.overflowY =
        "auto";

    panel.style.overflowX =
        "hidden";
    
    panel.style.scrollbarWidth =
    "thin";

    panel.innerHTML = `
        <div
            id="email-secure-toggle"
            style="
                font-size:14px;
                font-weight:600;
                padding:8px 0;
                cursor:pointer;
                user-select:none;
            "
        >
            ▶ Email Secure
        </div>

        <div
            id="email-secure-content"
            style="
                display:none;
                margin-top:6px;
            "
        >

            <div
                id="email-secure-overview"
                style="
                    margin-bottom:12px;
                "
            ></div>

            <div
                style="
                    font-size:11px;
                    font-weight:700;
                    color:#5f6368;
                    letter-spacing:.6px;
                    margin-bottom:6px;
                "
            >
                📂 CATEGORIES
            </div>

            <div
                id="email-secure-categories"
            ></div>

        </div>
    `;

    const sidebar =
        document.querySelector(
            '[role="navigation"]'
        );

    if (sidebar) {

        sidebar.appendChild(
            panel
        );

    } else {

        document.body.appendChild(
            panel
        );
    }

    const toggle =
        document.getElementById(
            "email-secure-toggle"
        );

    const content =
        document.getElementById(
            "email-secure-content"
        );

    if (
        toggle &&
        content
    ) {

        toggle.addEventListener(
            "click",
            () => {

                const expanded =
                    content.style.display !==
                    "none";

                content.style.display =
                    expanded
                        ? "none"
                        : "block";

                toggle.textContent =
                    expanded
                        ? "▶ Email Secure"
                        : "▼ Email Secure";
            }
        );
    }
}

function card(
    title,
    value,
    color
){

    return `
<div
style="
background:#fff;
border:1px solid #e0e0e0;
border-left:4px solid ${color};
border-radius:10px;
padding:10px;
">

<div
style="
font-size:11px;
color:#5f6368;
">
${title}
</div>

<div
style="
font-size:20px;
font-weight:700;
margin-top:4px;
color:#202124;
">
${value}
</div>

</div>
`;

}

function updateDashboard() {

    const container =
        document.getElementById(
            "email-secure-categories"
        );

    if (!container) {
        return;
    }

    const overview =
        document.getElementById(
            "email-secure-overview"
        );

    const rows =
        document.querySelectorAll("tr.zA");

    const unread =
        document.querySelectorAll("tr.zE");

    let critical = 0;
    let high = 0;

    rows.forEach(row => {

        const data =
            row._emailSecureData;

        if (!data)
            return;

        if (
            data.risk_label ===
            "CRITICAL"
        ) {
            critical++;
        }

        if (
            data.risk_label ===
            "HIGH"
        ) {
            high++;
        }

    });

    overview.innerHTML = `
    <div
    style="
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
    ">

    ${card(
        "All Emails",
        rows.length,
        "#1a73e8"
    )}

    ${card(
        "Unread",
        unread.length,
        "#5f6368"
    )}

    ${card(
        "Critical",
        critical,
        "#d93025"
    )}

    ${card(
        "Importance",
        high,
        "#f9ab00"
    )}

    </div>
    `;

    const counts = {};
    const companies = {};

    document
        .querySelectorAll(
            "tr.zA"
        )
        .forEach(
            (row) => {

                const data =
                    row._emailSecureData;

                if (!data) {
                    return;
                }

                const name = data.primary.name;
                const brand = data.brand;
                const color = data.primary.color;

                if (
                    !counts[name]
                ) {

                    counts[name] = {
                        count: 0,
                        color
                    };
                }

                counts[name]
                    .count++;

                if (!companies[name]) {
                    companies[name] = {};
                }

                companies[name][brand] =
                    (companies[name][brand] || 0) + 1;
            }
        );

    container.innerHTML =
        "";

    /*
     * SHOW ALL BUTTON
     */

    const showAll =
        document.createElement(
            "div"
        );

    showAll.textContent =
        "Show All";

    showAll.style.display =
        "inline-flex";

    showAll.style.alignItems =
        "center";

    showAll.style.padding =
        "6px 10px";

    showAll.style.margin =
        "4px";

    showAll.style.borderRadius =
        "999px";

    showAll.style.background =
        "#5f6368";

    showAll.style.color =
        "#fff";

    showAll.style.fontSize =
        "12px";

    showAll.style.cursor =
        "pointer";

    showAll.addEventListener(
        "click",
        () => {

            document
                .querySelectorAll(
                    "tr.zA"
                )
                .forEach(
                    (row) => {

                        row.style.display =
                            "";
                    }
                );
        }
    );

    container.appendChild(
        showAll
    );

    /*
     * CATEGORY PILLS
     */

    Object.entries(
        counts
    )
    .sort(
        (a, b) =>
            b[1].count -
            a[1].count
    )
    .forEach(
        ([name, item]) => {

            const pill =
                document.createElement(
                    "div"
                );

            pill.style.display =
                "inline-flex";

            pill.style.alignItems =
                "center";

            pill.style.gap =
                "6px";

            pill.style.padding =
                "6px 10px";

            pill.style.margin =
                "4px";

            pill.style.borderRadius =
                "999px";

            pill.style.background =
                item.color;

            pill.style.color =
                "#fff";

            pill.style.fontSize =
                "12px";

            pill.style.cursor =
                "pointer";

            pill.innerHTML =
                `
                <span>●</span>
                <span>${name}</span>
                <strong>(${item.count})</strong>
                `;

            

            container.appendChild(
                pill
            );

            const companyBox =
                document.createElement("div");

            companyBox.style.marginLeft = "20px";
            companyBox.style.display =
                expandedCategory === name
                    ? "block"
                    : "none";

            Object.entries(
                companies[name] || {}
            ).forEach(([company, count]) => {

                const div =
                    document.createElement("div");

                div.textContent =
                    `${company} (${count})`;

                div.style.cursor = "pointer";
                div.style.padding = "3px 0";
                div.style.fontSize = "11px";

                div.onclick = () => {

                    document
                        .querySelectorAll("tr.zA")
                        .forEach(row => {

                            const d =
                                row._emailSecureData;

                            row.style.display =
                                d &&
                                d.primary.name === name &&
                                d.brand === company
                                    ? ""
                                    : "none";
                        });

                };

                companyBox.appendChild(div);

            });

            container.appendChild(companyBox);

            pill.onclick = () => {

                expandedCategory =
                    expandedCategory === name
                        ? null
                        : name;

                updateDashboard();

                document
                    .querySelectorAll("tr.zA")
                    .forEach(row => {

                        const d = row._emailSecureData;

                        if (!d) return;

                        row.style.display =
                            d.primary.name === name
                                ? ""
                                : "none";

                    });

            };
        }
    );
}

function scanOpenedEmail() {

    const emailBody =

        document.querySelector(".a3s");

    if (!emailBody)
        return;

    console.log(
        "[Email Secure] Opened email detected."
    );

    highlightLinks(
        emailBody
    );

}

async function checkUrl(url) {

    try {

        const response =
            await fetch(
                `${BACKEND}/check-url`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                        "application/json"

                    },

                    body: JSON.stringify({

                        url

                    })

                }
            );

        return await response.json();

    }

    catch (e) {

        console.error(e);

        return null;

    }

}

async function highlightLinks(
    emailBody
) {

    const links =
        emailBody.querySelectorAll("a");

    console.log(
        `[Email Secure] Found ${links.length} links.`
    );

    for (const link of links) {

        const href =
            link.href;

        if (!href)
            continue;

        const result =
            await checkUrl(href);

        link._emailSecureUrlResult = result;

        link._originalHref = href;

        console.log(result);

        if (!result)
            continue;

        if (result.is_safe) {

            link.style.background =
                "#dcfce7";

            link.style.color =
                "#15803d";

            link.style.border =
                "2px solid #22c55e";

            link.style.borderRadius =
                "6px";

            link.style.padding =
                "2px 4px";

        }

        else {

            link.style.background =
                "#fee2e2";

            link.style.color =
                "#b91c1c";

            link.style.border =
                "2px solid #ef4444";

            link.style.borderRadius =
                "6px";

            link.style.padding =
                "2px 4px";

        }

        link.addEventListener(
            "mouseenter",
            showLinkHover
        );

        link.addEventListener(
            "mousemove",
            moveHoverCard
        );

        link.addEventListener(
            "mouseleave",
            hideLinkHover
        );

    }

}

function showLinkHover(e) {

    const link =
        e.currentTarget;

    const result =
        link._emailSecureUrlResult;

    if (!result)
        return;

    let html = "";

    if (result.is_safe) {

        html = `
        <div style="
        font-size:16px;
        font-weight:700;
        color:#22c55e;
        margin-bottom:10px;
        ">
        🟢 Safe Link
        </div>

        <div style="
        font-size:12px;
        color:#9ca3af;
        ">
        Actual URL
        </div>

        <div style="
        word-break:break-word;
        margin-top:4px;
        ">
        ${link.href}
        </div>
        `;

    } else {

        html = `
        <div style="
        font-size:16px;
        font-weight:700;
        color:#ef4444;
        margin-bottom:10px;
        ">
        🔴 Dangerous Link
        </div>

        <div style="
        font-size:12px;
        color:#9ca3af;
        ">
        Mail Fake URL
        </div>

        <div style="
        color:#ef4444;
        word-break:break-word;
        margin-top:4px;
        ">
        ${link.href}
        </div>
        `;

    }

    hoverCard.innerHTML = html;

    hoverCard.style.display =
        "block";

    moveHoverCard(e);

}

function hideLinkHover() {

    hoverCard.style.display =
        "none";

}