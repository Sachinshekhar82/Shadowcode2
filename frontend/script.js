const scanBtn = document.getElementById('scanBtn');
const findingsList = document.getElementById('findingsList');
const criticalCount = document.getElementById('criticalCount');
const mediumCount = document.getElementById('mediumCount');
const aiChat = document.getElementById('aiChat');
let currentScanId = null;

const mockVulnerabilities = [
    {
        type: "Hardcoded Secret",
        severity: "High",
        file: "buggy_app.js",
        line: 2,
        content: 'const API_KEY = "ak_test_51MzByuSJRpG7zZzZzZzZzZzZzZzZzZz";',
        remediation: "Move sensitive keys to environment variables (.env) and use a secrets manager in production."
    },
    {
        type: "SQL Injection Risk",
        severity: "Medium",
        file: "buggy_app.js",
        line: 6,
        content: 'const query = "SELECT * FROM users WHERE id = " + userId;',
        remediation: "Use parameterized queries or an ORM to prevent SQL injection attacks."
    },
    {
        type: "Unsafe Eval",
        severity: "High",
        file: "buggy_app.js",
        line: 11,
        content: 'eval(data);',
        remediation: "Avoid using eval(). Use JSON.parse() or other safer alternatives for processing dynamic data."
    }
];

scanBtn.addEventListener('click', async () => {
    // Reset UI
    findingsList.innerHTML = '<div class="finding-placeholder">Analyzing codebase...</div>';
    scanBtn.disabled = true;
    scanBtn.textContent = 'Scanning...';
    
    try {
        const response = await fetch('http://localhost:8001/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_path: "./demo_files" })
        });
        const data = await response.json();
        currentScanId = data.id;
        const vuls = data.vulnerabilities;
        
        findingsList.innerHTML = '';
        let criticals = 0;
        let mediums = 0;
        
        if (vuls.length === 0) {
            findingsList.innerHTML = '<div class="finding-placeholder">No vulnerabilities found. System is secure.</div>';
        }

        vuls.forEach((v, index) => {
            setTimeout(() => {
                const item = document.createElement('div');
                item.className = 'finding-item';
                item.innerHTML = `
                    <div class="finding-row">
                        <strong>${v.type}</strong>
                        <span class="severity-badge sev-${v.severity.toLowerCase()}">${v.severity}</span>
                    </div>
                    <div class="finding-row" style="font-size: 12px; color: #94a3b8;">
                        <span>File: ${v.file} | Line: ${v.line}</span>
                    </div>
                    <div class="finding-content">
                        <code>${v.content}</code>
                    </div>
                `;
                findingsList.appendChild(item);
                
                if(v.severity === 'High') criticals++;
                if(v.severity === 'Medium') mediums++;
                
                criticalCount.textContent = criticals;
                mediumCount.textContent = mediums;
                
                if(index === vuls.length - 1) {
                    showAiResponse(vuls);
                }
            }, index * 200);
        });
    } catch (error) {
        console.error("Scan failed:", error);
        findingsList.innerHTML = '<div class="finding-placeholder">Error connecting to ShadowCode API.</div>';
    } finally {
        scanBtn.disabled = false;
        scanBtn.textContent = 'Start New Audit';
    }
});

function showAiResponse(vuls) {
    const highCount = vuls.filter(v => v.severity === 'High').length;
    const medCount = vuls.filter(v => v.severity === 'Medium').length;
    
    aiChat.innerHTML = `
        <div class="ai-msg">
            <strong>ShadowCode AI:</strong> Audit complete. I've detected ${highCount} High and ${medCount} Medium risk vulnerabilities. 
            <br><br>
            <strong>Key Insight:</strong> Found hardcoded secrets and SQL injection entry points in <code>demo_files/</code>. 
            <br><br>
            I've prepared remediation fixes for the detected issues. Would you like to generate a Pull Request?
        </div>
        <button id="prBtn" class="primary-btn" style="padding: 8px 16px; font-size: 12px; margin-top: 10px;">Generate AI Fix & PR</button>
    `;

    document.getElementById('prBtn').addEventListener('click', async () => {
        const btn = document.getElementById('prBtn');
        btn.disabled = true;
        btn.textContent = 'Generating PR...';
        
        try {
            const response = await fetch(`http://localhost:8001/remediate/${currentScanId}`, {
                method: 'POST'
            });
            const result = await response.json();
            
            if (result.html_url) {
                aiChat.innerHTML += `
                    <div class="ai-msg user">Yes, generate fix.</div>
                    <div class="ai-msg">
                        <strong>ShadowCode AI:</strong> Pull Request Created Successfully! <br> 
                        🚀 <a href="${result.html_url}" target="_blank" style="color: #60a5fa;">View PR on GitHub</a>
                    </div>
                `;
            } else {
                aiChat.innerHTML += `<div class="ai-msg"><strong>Error:</strong> ${result.error || 'Failed to create PR'}</div>`;
            }
        } catch (error) {
            aiChat.innerHTML += `<div class="ai-msg"><strong>Error:</strong> Connection failed.</div>`;
        } finally {
            btn.style.display = 'none';
        }
    });
}
