import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

continents_facts = {
    "Africa": {
        "population": 1549867579,
        "main_languages": ["Arabic", "French", "Swahili", "English", "Hausa", "Amharic", "Yoruba", "Oromo", "Igbo"],
        "interesting_facts": [
            "Africa is the second most populous continent and the most linguistically diverse, with over 2,000 languages spoken.",
            "It is home to the Sahara Desert, the largest hot desert in the world.",
            "Arabic has the most native speakers (over 213 million), while English is widely spoken across the continent."
        ]
        
    },
    "America": {
        "population": 1000000000,
        "main_languages": ["Spanish", "English", "Portuguese", "French", "Indigenous languages"],
        "interesting_facts": [
            "The Americas (North and South) are home to diverse ecosystems, including the Amazon Rainforest, the world's largest.",
            "Spanish is the most spoken language, with over 460 million speakers, followed by English and Portuguese (primarily in Brazil).",
            "The continent features the longest mountain range, the Andes, and ancient civilizations like the Maya and Inca."
        ]
    },
    "Asia": {
        "population": 4835320060,
        "main_languages": ["Mandarin Chinese", "Hindi", "English", "Bengali", "Arabic"],
        "interesting_facts": [
            "Asia is the most populous continent, housing over 60% of the world's population.",
            "Mandarin Chinese is the most spoken language globally, with over 1.3 billion speakers.",
            "It includes Mount Everest, the highest point on Earth, and ancient civilizations like those in China and India."
        ]
    },
    "Europe": {
        "population": 744398832,
        "main_languages": ["Russian", "German", "French", "English", "Italian", "Spanish", "Polish"],
        "interesting_facts": [
            "Europe has over 140 million Russian speakers, making it the most spoken language on the continent.",
            "It is known for its rich history, including ancient Greece and Rome, and has a high concentration of developed countries.",
            "The continent features diverse architecture, from the Eiffel Tower to the Colosseum, and is a hub for global cuisine."
        ]
    },
    "Oceania": {
        "population": 47000000,
        "main_languages": ["English", "French", "Indigenous languages (e.g., Maori, Hawaiian)"],
        "interesting_facts": [
            "Oceania includes Australia, New Zealand, and thousands of Pacific islands, with English as the most common language (30 million speakers).",
            "It is home to the Great Barrier Reef, the largest coral reef system in the world.",
            "The region has unique wildlife, such as kangaroos and kiwis, and over 1,200 indigenous languages."
        ]
    }
}