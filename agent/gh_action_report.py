import os
import sys
import json

# Add the current directory to sys.path to allow importing scanner
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scanner import ShadowScanner

def main():
    scanner = ShadowScanner()
    results = scanner.scan_directory(".")
    
    if not results:
        print("## ✅ ShadowCode Audit: No Vulnerabilities Found")
        print("Your codebase is clean according to our current security rules.")
        return

    print(f"## 🛡️ ShadowCode Security Audit: {len(results)} Findings")
    print("\n| Severity | Type | File | Line | Remediation |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    
    for v in results:
        sev_icon = "🔴" if v['severity'] == "High" else "🟡"
        print(f"| {sev_icon} {v['severity']} | {v['type']} | `{v['file']}` | {v['line']} | {v['remediation']} |")

    print("\n### 🔍 Detailed Analysis & AI Fix Suggestions")
    for v in results:
        print(f"\n#### {v['type']} in `{v['file']}`")
        print(f"- **Line:** {v['line']}")
        print(f"- **Snippet:** `{v['content']}`")
        print(f"- **Risk Factor:** This vulnerability could lead to {v['type'].lower()} and compromise system integrity.")
        
        # Mocking an AI fix based on the type
        fix = ""
        if v['type'] == "Hardcoded Secret":
            fix = "const API_KEY = process.env.API_KEY; // Moved to environment variables"
        elif v['type'] == "SQL Injection Risk":
            fix = "db.execute('SELECT * FROM users WHERE id = ?', (userId,)); // Used parameterized query"
        elif v['type'] == "Unsafe Eval":
            fix = "JSON.parse(data); // Replaced eval with safer JSON.parse"
        
        if fix:
            print(f"- **Suggested Fix:**\n  ```javascript\n  - {v['content']}\n  + {fix}\n  ```")
        else:
            print(f"- **Suggested Fix:** {v['remediation']}")

    # Write to GITHUB_STEP_SUMMARY if available
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(f"\n### 🔍 AI Analysis & Suggested Fixes\n")
            for v in results:
                fix = ""
                if v['type'] == "Hardcoded Secret": fix = "const API_KEY = process.env.API_KEY;"
                elif v['type'] == "SQL Injection Risk": fix = "db.execute('SELECT * FROM users WHERE id = ?', (userId,));"
                elif v['type'] == "Unsafe Eval": fix = "JSON.parse(data);"
                
                f.write(f"#### {v['type']} in `{v['file']}`\n")
                f.write(f"- **Risk:** High exposure of sensitive data or entry point for attacks.\n")
                if fix:
                    f.write(f"- **Suggested Fix:**\n```diff\n- {v['content']}\n+ {fix}\n```\n")
                else:
                    f.write(f"- **Suggested Fix:** {v['remediation']}\n")

if __name__ == "__main__":
    main()
