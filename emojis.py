# Emoji cache

from typing import Final

halloween_emojis: Final[str] = ['💀','🦇','🎃','🍬','🍫','🍭','🪄','🦴','👻','🕸️']
halloween_scores: Final[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def get_emojis() -> str:
    current_emojis: Final[str] = halloween_emojis
    return current_emojis

def get_emoji_scores() -> int:
    current_scores: Final[int] = halloween_scores
    return current_scores