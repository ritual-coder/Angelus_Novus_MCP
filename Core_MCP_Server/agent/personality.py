import os

def get_personality():
    """Reads the Angelus Novus personality manifest from personality.md"""
    personality_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "personality.md")
    try:
        with open(personality_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error loading personality: {str(e)}"
