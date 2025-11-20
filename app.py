"""
Hugging Face Spaces - PHISHNET AI Cybersecurity Suite
Gradio Interface for AI-Powered Phishing Detection
"""
import gradio as gr
import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

try:
    from backend.ai.detection_engine import PhishingDetectionEngine
    from backend.ai.threat_intelligence_platform import ThreatIntelligencePlatform
except ImportError:
    # Fallback for demo mode
    class PhishingDetectionEngine:
        async def analyze_email(self, *args, **kwargs):
            return {"verdict": "Demo Mode", "risk_score": 0.5}
    
    class ThreatIntelligencePlatform:
        async def check_url(self, url):
            return {"status": "Demo", "threat_level": "UNKNOWN"}

# Initialize AI engines
detection_engine = PhishingDetectionEngine()
threat_intel = ThreatIntelligencePlatform()

async def analyze_email_content(email_text, sender_email=""):
    """Analyze email content for phishing threats"""
    try:
        result = await detection_engine.analyze_email(
            sender=sender_email,
            subject="Email Analysis",
            body=email_text,
            headers={}
        )
        
        risk_score = result.get('risk_score', 0.5)
        verdict = result.get('verdict', 'SUSPICIOUS')
        
        # Format results
        risk_percentage = f"{risk_score * 100:.1f}%"
        threat_level = "🔴 HIGH RISK" if risk_score > 0.7 else "🟡 MEDIUM RISK" if risk_score > 0.4 else "🟢 LOW RISK"
        
        indicators = result.get('indicators', {})
        recommendations = result.get('recommendations', ['No specific recommendations'])
        
        output = f"""
# 🧠 PHISHNET Analysis Results

## Threat Assessment
- **Risk Score**: {risk_percentage}
- **Threat Level**: {threat_level}
- **Verdict**: {verdict}

## Detected Indicators
"""
        for key, value in indicators.items():
            output += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        
        output += "\n## 🛡️ Recommendations\n"
        for rec in recommendations:
            output += f"- {rec}\n"
        
        return output
        
    except Exception as e:
        return f"⚠️ Analysis Error: {str(e)}\n\nDemo mode active - full AI features require backend setup."

async def analyze_url(url):
    """Analyze URL for phishing threats"""
    try:
        result = await threat_intel.check_url(url)
        
        status = result.get('status', 'UNKNOWN')
        threat_level = result.get('threat_level', 'UNKNOWN')
        
        output = f"""
# 🔗 URL Analysis Results

## URL: {url}

- **Status**: {status}
- **Threat Level**: {threat_level}
- **Safe to Click**: {'❌ NO' if threat_level in ['HIGH', 'CRITICAL'] else '✅ YES' if threat_level == 'LOW' else '⚠️ CAUTION'}

## Details
"""
        details = result.get('details', {})
        for key, value in details.items():
            output += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        
        return output
        
    except Exception as e:
        return f"⚠️ Analysis Error: {str(e)}"

def sync_analyze_email(email_text, sender_email):
    """Synchronous wrapper for email analysis"""
    return asyncio.run(analyze_email_content(email_text, sender_email))

def sync_analyze_url(url):
    """Synchronous wrapper for URL analysis"""
    return asyncio.run(analyze_url(url))

# Create Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="🧠 PHISHNET - AI Phishing Detection") as demo:
    
    gr.Markdown("""
    # 🧠 PHISHNET - AI Cybersecurity Suite
    ## Detect, Analyze, and Neutralize Phishing Threats in Real-Time
    
    **Powered by Advanced AI & Machine Learning**
    
    ### Features:
    - 🔍 Real-time email content analysis
    - 🔗 Malicious URL detection
    - 🎯 Threat intelligence integration
    - 🛡️ Advanced phishing pattern recognition
    """)
    
    with gr.Tab("📧 Email Analysis"):
        gr.Markdown("### Analyze Email Content for Phishing Threats")
        
        with gr.Row():
            with gr.Column():
                email_input = gr.Textbox(
                    label="Email Content",
                    placeholder="Paste suspicious email content here...",
                    lines=10
                )
                sender_input = gr.Textbox(
                    label="Sender Email (Optional)",
                    placeholder="sender@example.com"
                )
                email_button = gr.Button("🔍 Analyze Email", variant="primary")
            
            with gr.Column():
                email_output = gr.Markdown(label="Analysis Results")
        
        email_button.click(
            fn=sync_analyze_email,
            inputs=[email_input, sender_input],
            outputs=email_output
        )
        
        gr.Examples(
            examples=[
                ["URGENT: Your account will be suspended! Click here immediately to verify your identity: http://fake-bank.com/verify", "noreply@suspicious-bank.com"],
                ["Congratulations! You've won $1,000,000! Claim your prize now by providing your bank details.", "winner@lottery-scam.net"],
            ],
            inputs=[email_input, sender_input],
            label="Sample Phishing Emails"
        )
    
    with gr.Tab("🔗 URL Analysis"):
        gr.Markdown("### Check URLs for Malicious Content")
        
        with gr.Row():
            with gr.Column():
                url_input = gr.Textbox(
                    label="URL to Analyze",
                    placeholder="https://example.com"
                )
                url_button = gr.Button("🔍 Analyze URL", variant="primary")
            
            with gr.Column():
                url_output = gr.Markdown(label="URL Analysis Results")
        
        url_button.click(
            fn=sync_analyze_url,
            inputs=url_input,
            outputs=url_output
        )
        
        gr.Examples(
            examples=[
                ["http://fake-paypal-login.com"],
                ["https://secure-bank-verify.net"],
                ["https://github.com"],
            ],
            inputs=url_input,
            label="Sample URLs"
        )
    
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## About PHISHNET
        
        PHISHNET is an advanced AI-powered cybersecurity suite designed to detect and neutralize phishing threats in real-time.
        
        ### Technology Stack:
        - **AI Models**: PyTorch, Transformers, BERT
        - **NLP**: Spacy, NLTK, Sentiment Analysis
        - **Threat Intelligence**: Real-time feed integration
        - **Backend**: FastAPI, Python 3.11
        - **Frontend**: Next.js, React, TypeScript
        
        ### Admin Credentials:
        - **Username**: Mubashar
        - **Password**: Mubashar9266
        
        ### GitHub Repository:
        - [PHISHNET on GitHub](https://github.com/khantayyaba0987-afk/Phishnet)
        
        ### Developed by: Muhammad Mubashar
        ### Version: 1.0.0
        """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
