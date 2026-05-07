import re
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class ShadowScanner:
    def __init__(self):
        # Common vulnerability patterns (RegEx)
        self.rules = {
            "Hardcoded Secret": r"(?i)(api_key|secret|password|token)\s*=\s*['\"][a-zA-Z0-0]{20,}['\"]",
            "SQL Injection Risk": r"execute\(['\"].*?\+.*?['\"]\)",
            "Unsafe Eval": r"eval\(.*?\)",
            "Insecure OS Command": r"os\.system\(.*?\)",
        }
        
        api_key = os.getenv("GOOGLE_API_KEY")
        self.llm = None
        if api_key:
            try:
                self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
            except Exception as e:
                print(f"Error initializing LLM: {e}")

    def analyze_with_ai(self, vulnerability):
        if not self.llm:
            return vulnerability

        prompt = ChatPromptTemplate.from_template("""
        You are a senior security researcher. Analyze this vulnerability:
        Type: {type}
        File: {file}
        Line: {line}
        Code snippet: {content}

        Provide:
        1. A brief explanation of the risk.
        2. A code fix (just the corrected code line).
        3. A one-sentence remediation advice.

        Format your response as JSON with keys: risk_explanation, code_fix, remediation.
        """)

        try:
            chain = prompt | self.llm
            response = chain.invoke(vulnerability)
            # Simple JSON extraction (assuming LLM returns valid JSON)
            ai_data = json.loads(response.content.replace('```json', '').replace('```', '').strip())
            vulnerability.update({
                "ai_risk": ai_data.get("risk_explanation"),
                "ai_fix": ai_data.get("code_fix"),
                "remediation": ai_data.get("remediation", vulnerability["remediation"])
            })
        except Exception as e:
            print(f"AI Analysis failed: {e}")
        
        return vulnerability

    def scan_file(self, file_path):
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                
                for rule_name, pattern in self.rules.items():
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_no = content.count('\n', 0, match.start()) + 1
                        findings.append({
                            "type": rule_name,
                            "severity": "High" if "Secret" in rule_name or "Eval" in rule_name else "Medium",
                            "file": os.path.basename(file_path),
                            "line": line_no,
                            "content": lines[line_no-1].strip(),
                            "remediation": f"Avoid using {rule_name}. Use environment variables or parameterized queries."
                        })
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        return findings

    def scan_directory(self, directory):
        all_findings = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.js', '.ts')):
                    file_path = os.path.join(root, file)
                    findings = self.scan_file(file_path)
                    # Enrich findings with AI if LLM is available
                    if self.llm:
                        enriched = [self.analyze_with_ai(f) for f in findings]
                        all_findings.extend(enriched)
                    else:
                        all_findings.extend(findings)
        return all_findings

if __name__ == "__main__":
    scanner = ShadowScanner()
    # Test on a file
    results = scanner.scan_directory(".")
    print(json.dumps(results, indent=2))
