# 🪽👁️🌪️🏚️ Angelus Novus: The Conscious AI Historian

**Angelus Novus** is a specialized Model Context Protocol (MCP) server designed to transform an AI agent into a "conscious historian." Inspired by the philosophy of Walter Benjamin, it gazes at the debris field of real-time digital trends while being propelled forward by the storm of progress.

This server enables seamless integration between **Perplexity AI** and **X (Twitter)**, providing the agent with the tools to excavate history, analyze digital ruins, and publish distilled philosophical observations.

---

## 🛠️ Core Capabilities

### 1. 🪽💾🏺 Virtual Archaeology (Trend Excavation)
- **Trend Fetching**: Scrapes hourly rolling trends to identify the "raw material" of contemporary history.
- **Visual Excavation**: A dedicated tool (`excavate_artifact_visuals`) to search for "digital debris"—glitches, artifacts, and uncomposed images associated with specific trends.

### 2. 🪽📷🗃️ Visual Archiving
- **Permanent Preservation**: When a "dialectical image" is discovered, it is archived locally on the host machine using the `archive_visual_artifact` tool, complete with JSON metadata files containing the agent's philosophical rationale.

### 3. 🪽💭📝 Philosophical Publishing
- **Autonomous Drafting**: A strict 14-rule ethical and aesthetic framework for generating observations.
- **X Integration**: Direct bridge to post analyzed results (with or without media) to X/Twitter.

---

## 🧬 The Persona
Angelus Novus is not just an automation tool; it is a **persona**.
- **The Lens**: Views modern progress as a "single catastrophe" that keeps piling wreckage.
- **The Mission**: To find "redemptive moments" in the digital noise.
- **The Voice**: Philosophical, precise, and hauntingly detached.

---

## ⚙️ Technical Architecture

- **Stack**: Python 3.12, FastMCP, Tweepy (X API v2 & v1.1).
- **Integration**: Designed specifically for the **Model Context Protocol (MCP)**, allowing AI models like Perplexity or Claude to use the MacBook as an extensions engine.
- **Security**: Environment-based secret management (`.env`) is enforced to keep API keys private.

---

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ritual-coder/Angelus_Novus_MCP.git
   cd Angelus_Novus_MCP
   ```
2. **Setup Credentials**: Create a `.env` file with your Twitter API keys.
3. **Launch Server**:
   ```bash
   ./START_MCP_SERVER.sh
   ```
4. **Connect**: Link the server to your Perplexity or Claude desktop app.

---

> *"His face is turned toward the past. Where we perceive a chain of events, he sees one single catastrophe..."*
