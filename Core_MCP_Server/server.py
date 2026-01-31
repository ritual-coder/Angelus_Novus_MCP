import asyncio
import logging
import json
import sys
import os

# Ensure we can import from local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from twitter.trends import get_top_trends
from twitter.client import post_tweet, search_trend_images, download_image, post_tweet_with_media
from agent.personality import get_personality
from config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN

# Configure logging to stderr so it doesn't interfere with MCP stdio
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("angelus_mcp")

# Initialize MCP Server
mcp = FastMCP("Angelus Novus MCP Server")

ARCHIVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visual_archives")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

@mcp.tool(name="archive_visual_artifact")
def archive_visual_artifact(image_url: str, trend_name: str, description: str) -> str:
    """
    Permanently saves a selected image to the MacBook's visual archives.
    Use this when you have chosen a 'dialectical image' to preserve it.
    
    Args:
        image_url: The direct URL of the image to save.
        trend_name: The trend associated with this artifact.
        description: A brief philosophical description of why this was archived.
    """
    logger.info(f"MCP Tool Called: archive_visual_artifact for trend '{trend_name}'")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_trend = trend_name.replace("#", "").replace(" ", "_")[:30]
    filename = f"{safe_trend}_{timestamp}.jpg"
    filepath = os.path.join(ARCHIVE_DIR, filename)
    
    try:
        saved_path = download_image(image_url, filepath)
        if not saved_path:
            return f"Error: Failed to download image from {image_url}"
        
        # Save metadata alongside
        meta_filename = f"{safe_trend}_{timestamp}.json"
        meta_path = os.path.join(ARCHIVE_DIR, meta_filename)
        metadata = {
            "trend_name": trend_name,
            "description": description,
            "original_url": image_url,
            "timestamp": datetime.now().isoformat(),
            "local_path": filepath
        }
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)
            
        return f"SUCCESS: Artifact archived to {filename}. Metadata saved."
    except Exception as e:
        return f"Error archiving artifact: {str(e)}"

@mcp.tool(name="excavate_artifact_visuals")
def excavate_artifact_visuals(trend_name: str) -> str:
    """
    MANDATORY STEP: Searches for highly engaged tweets containing IMAGES related to the specific trend.
    You MUST call this for every trend selection to check for visual 'digital debris'.
    Returns a JSON string of results.
    """
    logger.info(f"MCP Tool Called: excavate_artifact_visuals for trend '{trend_name}'")
    try:
        results = search_trend_images(trend_name, max_results=10)
    except Exception as e:
        logger.warning(f"Live search failed: {e}")
        results = []

    if not results:
        logger.info(f"No results or search failed for {trend_name}.")
        return f"No visual evidence found for {trend_name}. (API returned 0 results or Error)"
    
    # Format for the agent
    output = f"--- Visual Archives for {trend_name} ---\n"
    output += "[System Instruction]: You MUST render the chosen image in your Draft Proposal using the syntax: ![Visual Artifact](URL)\n"
    
    for res in results:
        output += f"\n![Candidate Image]({res['image_url']})\n[URL]: {res['image_url']}\n[Context]: {res['text']}\n"
    
    return output

@mcp.tool(name="get_angelus_personality")
def get_angelus_personality() -> str:
    """Returns the full personality and operational manifest of Angelus Novus. Consulting this is REQUIRED before any analysis."""
    return get_personality()

@mcp.tool(name="get_publishing_rules")
def get_publishing_rules() -> str:
    """
    Returns the strict publishing rules that MUST be fulfilled before any post is drafted or posted.
    CONSULT THIS BEFORE WRITING ANY TWEET.
    """
    rules_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent", "publishing_rules.md")
    try:
        with open(rules_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error loading rules: {str(e)}"

@mcp.tool(name="get_angelus_context")
def get_angelus_context() -> str:
    """
    Returns the 'Context File' containing the operational workflow and useful information for Angelus Novus.
    This replaces the Master Prompt.
    """
    context_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ANGELUS_CONTEXT.md")
    try:
        with open(context_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error loading context: {str(e)}"

@mcp.tool(name="fetch_17h_window_trends")
def fetch_17h_window_trends() -> str:
    """
    Scrapes the last 17 hours of trends from trends24.in and returns a list of unique topics.
    Use this to get the raw material for the Angel's observation.
    """
    logger.info("MCP Tool Called: fetch_17h_window_trends")
    trends = get_top_trends(window_hours=17)
    
    if not trends:
        return "No trends found. Please check logs."

    # Format for the LLM
    text_output = "Excavated Trends (Last 17 Hours Window):\n"
    for t in trends:
        text_output += f"- {t['name']} (Volume: {t['tweet_volume']})\n"
    
    return text_output

from datetime import datetime

MCP_HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_history.json")

def save_mcp_history(trend_name, tweet, analysis, status="draft"):
    """Saves the Perplexity analysis and post to mcp_history.json with status."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "trend_name": trend_name,
        "tweet": tweet,
        "analysis": analysis,
        "status": status
    }
    
    data = []
    if os.path.exists(MCP_HISTORY_FILE):
        try:
            with open(MCP_HISTORY_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            pass
            
    data.append(entry)
    
    with open(MCP_HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved analysis to {MCP_HISTORY_FILE}")

from typing import Any, Optional

@mcp.tool(name="post_tweet_to_x")
def post_tweet_to_x(tweet_body: str, trend_name: str, hashtags: Any, analysis: str, image_url: Optional[str] = None) -> str:
    """
    The FINAL MANDATORY STEP for the Daily Analysis. 
    Use this to execute the publication of the drafted observation to X/Twitter.
    
    Args:
        tweet_body: The distilled philosophical observation (must include #TrendName).
        trend_name: The exact trend being 'excavated'.
        hashtags: Exactly 3 strategy hashtags (can be a list of strings or a space-separated string).
        analysis: Your full reasoning for selecting this trend and your drafting process.
        image_url: Optional. URL of an image to attach if Visual Excavation was chosen.
    """
    logger.info(f"MCP Tool Called: post_tweet_to_x for trend '{trend_name}'")
    
    # 0. Log Attempt (Pre-flight)
    save_mcp_history(trend_name, tweet_body, analysis, status="tool_called")
    
    # 1. Handle Hashtags Robustly (Accept list or string)
    if isinstance(hashtags, str):
        # If it's a string like "#Tag1 #Tag2 #Tag3", keep as is or split/join
        hashtag_str = hashtags.strip()
    elif isinstance(hashtags, list):
        hashtag_str = " ".join(hashtags)
    else:
        hashtag_str = str(hashtags)

    # 2. Prevent Duplicated Footer (Perplexity often includes it based on the prompt)
    trend_tag = trend_name if trend_name.startswith("#") else f"#{trend_name.replace(' ', '')}"
    footer_text = f"Excavated from: {trend_tag}"
    
    # Only append footer if it's not already in the body
    if footer_text not in tweet_body:
        final_tweet = f"{tweet_body}\n\n{footer_text}\n{hashtag_str}"
    else:
        # If footer is there but hashtags are missing or need updating
        if hashtag_str not in tweet_body:
            final_tweet = f"{tweet_body}\n{hashtag_str}"
        else:
            final_tweet = tweet_body
            
    # 4. Post Main Tweet
    try:
        logger.info(f"Attempting to post tweet ({len(final_tweet)} chars): {final_tweet[:50]}...")
        

        if len(final_tweet) > 280:
             error_msg = f"Error: Tweet too long ({len(final_tweet)} chars). Please condense your observation."
             logger.error(error_msg)
             save_mcp_history(trend_name, final_tweet, error_msg, status="failed_length")
             return error_msg

        # 5. Handle Posting (Text vs Image)
        if image_url:
            logger.info("Decision: Posting with Image Artifact.")
            temp_file = download_image(image_url)
            if not temp_file:
                 return "Error: Failed to download the selected image."
            
            tweet_id = post_tweet_with_media(final_tweet, temp_file)
            
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)
        else:
             logger.info("Decision: Posting Text Only.")
             tweet_id = post_tweet(final_tweet)
        if not tweet_id:
             logger.error("Twitter API returned no ID. Check your .env credentials or rate limits.")
             save_mcp_history(trend_name, final_tweet, "Twitter API returned no ID", status="failed_api")
             return "Error: Failed to post main tweet. Ensure your .env keys are correct and you aren't rate limited."
             
        # 5. Save History (Success)
        save_mcp_history(trend_name, final_tweet, analysis, status="posted")
        logger.info(f"Tweet posted successfully with ID: {tweet_id}")
        
        return f"Successfully posted tweet ID: {tweet_id}. View at: https://x.com/user/status/{tweet_id}"
        
    except Exception as e:
        return f"Error posting tweet: {str(e)}"

if __name__ == "__main__":
    logger.info("Angelus Novus MCP Server - Starting...")
    logger.info("Angelus Novus MCP Server Running...")
    mcp.run()
