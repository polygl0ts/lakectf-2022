import re
import random

import pgpy

ME = "epfl-ctf-bot@protonmail.com"

SECRET_KEY, _ = pgpy.PGPKey.from_file("secret.asc")

with open("wordlist.txt") as f:
    WORDS = re.compile("|".join(f.read().split()), re.I)


def respond(feedback):
    if feedback is None:
        response = rand_answer(
            {
                "Sorry, can you repeat?": 8,
                "Do you know how to crypto?": 4,
                "Sorry, I don't speak gibberish?": 4,
                "What did you mess up this time?": 2,
                "Vouz parlez franchoise?": 1,
                "BITTE WIEDERHOLEN?": 1,
            }
        )
    elif len(feedback) > 1000000:
        response = "TL;DR lol"
    elif WORDS.search(feedback):
        response = "> " + WORDS.sub("[REDACTED]", feedback).strip()
        response += "\n\n"
        response += rand_answer(
            {
                "Nice try!": 4,
                "Good meme lol": 4,
                "Another time maybe": 4,
                "Right back at ya!": 2,
                "I'm not getting baited!": 2,
            }
        )
    else:
        response = "> " + feedback.strip()
        response += "\n\n"
        response += rand_answer(
            {
                "Thank you for your feedback!": 8,
                "This will receive consideration!": 8,
                "We are very sorry to see you go": 4,
            }
        )
    response += "\n\n- FishNinja"
    return response


def rand_answer(distribution):
    return random.choices(list(distribution), distribution.values())[0]
