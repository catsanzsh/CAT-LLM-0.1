import os
import json
import logging
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
import datetime
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameType(Enum):
    FIGHTING = "fighting"
    RACING = "racing"
    PLATFORMER = "platformer"
    RPG = "rpg"
    PUZZLE = "puzzle"
    SHOOTER = "shooter"

class Platform(Enum):
    DESKTOP = "desktop"
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

@dataclass
class GameConfig:
    game_type: GameType
    details: Dict[str, Any]
    engine: str = "pygame"
    resolution: tuple = (800, 600)
    target_fps: int = 60

class GameGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the game generator with optional API key."""
        self.api_key = api_key
        self.initialized = False
        if self.api_key:
            self.initialized = self._init_gemini()

    def _init_gemini(self) -> bool:
        """Validate the API key by checking user details."""
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/userinfo"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            user_data = response.json()
            logger.info(f"Welcome, {user_data['name']}!")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            return False

    # The rest of the class remains unchanged
    # (Refer to the original script for methods like `_validate_config`, `_generate_code`, etc.)

# Example usage with login functionality
def main():
    print("Welcome to the Game Dev Assistant!")
    use_gemini = input("Would you like to log in with your Gemini API key? (y/n): ").strip().lower()
    if use_gemini == "y":
        api_key = input("Please enter your Gemini API key: ").strip()
        generator = GameGenerator(api_key=api_key)
        if generator.initialized:
            print("Login successful!")
        else:
            print("Login failed. Continuing without Gemini integration.")
            generator = GameGenerator()
    else:
        print("Continuing without Gemini integration.")
        generator = GameGenerator()

    # Example game creation
    fighting_config = GameConfig(
        game_type=GameType.FIGHTING,
        details={
            "characters": ["robot_warrior", "cyborg_ninja"],
            "environment": "futuristic_arena",
            "moves_per_character": 8,
            "special_effects": ["laser_trails", "electric_impacts"]
        },
        engine="pygame",
        resolution=(1280, 720),
        target_fps=60
    )

    try:
        fighting_game = generator.create_game(fighting_config)
        print("Game created successfully!")
    except Exception as e:
        print(f"Failed to create game: {e}")

if __name__ == "__main__":
    main()
