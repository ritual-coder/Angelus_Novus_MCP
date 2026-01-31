# Angelus Novus MCP - Available Tools & Resources

This server provides the following capabilities to the Agent:

## 🛠️ MCP Tools (Functions)

### 1. `get_angelus_context()`
**Description**: Loads the operational context file (`ANGELUS_CONTEXT.md`).
**Use For**: accessing the Daily Workflow, Quick Start commands, and functional instructions.
**Returns**: The full text of the context file.

### 2. `get_publishing_rules()`
**Description**: Loads the strict publishing rules (`agent/publishing_rules.md`).
**Use For**: Verifying adherence to the 14 core rules before posting.
**Returns**: The full text of the rules file.

### 3. `fetch_17h_window_trends()`
**Description**: Scrapes trends from trends24.in for the last 17 hours.
**Use For**: Getting the raw list of topics to analyze.
**Returns**: List of trends with volume data.

### 4. `excavate_artifact_visuals(trend_name)`
**Description**: Searches for images related to a specific trend.
**Use For**: **MANDATORY** "Visual Excavation" (Step 2.5) to find digital debris or dialectical images. You must run this for every trend you analyze.
**Returns**: List of image URLs and context text.

### 5. `archive_visual_artifact(image_url, trend_name, description)`
**Description**: Permanently saves a selected image and its metadata to the MacBook's `visual_archives` folder.
**Use For**: Preserving "dialectical images" found during excavation.
**Returns**: Success message with file path.

### 6. `post_tweet_to_x(tweet_body, trend_name, hashtags, analysis, image_url=None)`
**Description**: Posts the final observation to X (Twitter).
**Arguments**:
- `tweet_body`: Main text (must include #TrendName)
- `trend_name`: The trend being analyzed
- `hashtags`: List of 3 strategy hashtags or space-separated string
- `analysis`: Reasoning for the post
- `image_url`: (Optional) URL of image to upload if Visual Excavation was chosen
**Returns**: Success message with Tweet ID or error.

### 7. `get_angelus_personality()`
**Description**: The core identity manifest of the Agent.
**Use For**: Initializing the Persona before any session.
**Returns**: The content of `agent/personality.md`.

---

## 📚 MCP Resources (Read-Only Data)

*(None currently active)*
