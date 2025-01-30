import openai
import os
from dotenv import load_dotenv
import lyricsgenius
import logging

load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))

logger = logging.getLogger(__name__)

def get_lyrics(artist: str, song: str):
    """Get lyrics for a song using Genius API"""
    try:
        logger.debug(f"Fetching lyrics for: {song} by {artist}")
        song = genius.search_song(song, artist)
        if song:
            logger.debug("Lyrics found successfully")
            return song.lyrics
        logger.warning("No lyrics found")
        return "Lyrics not found"
    except Exception as e:
        logger.error(f"Error fetching lyrics: {e}", exc_info=True)
        return "Lyrics not found"

def analyze_personality(songs_with_features):
    """Analyze personality based on song choices and lyrics"""
    try:
        logger.debug("Starting personality analysis")
        songs_description = []
        for song in songs_with_features:
            logger.debug(f"Processing song: {song['name']}")
            lyrics = get_lyrics(song['artist'], song['name'])
            
            description = (
                f"Song: {song['name']} by {song['artist']}\n"
                f"Lyrics:\n{lyrics}\n"
            )
            songs_description.append(description)
        
        logger.debug("Sending request to OpenAI")
        prompt = (
            "Here are 5 songs this person loves. Based on their music taste and the lyrics, "
            "make fun of them in a funny way. Be savage but make it funny! Write it like "
            "you're roasting your friend's terrible music taste. Keep it casual and use "
            "simple language, like you're texting a friend:\n\n" +
            "\n".join(songs_description)
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You're a funny friend who loves roasting people's music taste. "
                              "Be savage but hilarious. Use casual language, slang, and even emojis. "
                              "Make it sound like a friend making fun of another friend's spotify playlist. And at the end, summarize within 1-2 paragraphs about all the songs"
                },
                {"role": "user", "content": prompt}
            ]
        )
        logger.debug("Received response from OpenAI")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in analysis: {e}", exc_info=True)
        raise 