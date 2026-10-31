"""
Script to generate the complete Grade-wise (Pre-K to Grade 5) A-to-Z phonics & sentence corpus.
Starting with simple, early-reader words (CVC, Dolch/Fry sight words, foundational phonics)
and graduating systematically through grades.
"""

import json
from pathlib import Path

# Grade definitions:
# Pre-K & Kindergarten: Simple 3-letter CVC words, basic animal/everyday concepts, phonics basics.
# Grade 1: Foundational phonics, basic blends, high-frequency sight vocabulary.
# Grade 2: Expanding vocabulary, simple compound/descriptive words, multi-syllable basics.
# Grade 3: Descriptive vocabulary, nature, school, and community concepts.
# Grade 4: Academic, literary, scientific, and sensory vocabulary.
# Grade 5: Advanced expressive vocabulary, nuance, abstract concepts.

GRADE_METADATA = [
    {"level": "Pre-K", "name": "Pre-Kindergarten", "age": "3-4", "focus": "Alphabet recognition, 3-letter CVC words, simple phonemes"},
    {"level": "Kindergarten", "name": "Kindergarten", "age": "5-6", "focus": "Early sight words, foundational phonics, short vowels"},
    {"level": "Grade 1", "name": "First Grade", "age": "6-7", "focus": "Consonant blends, long vowels, high-frequency words"},
    {"level": "Grade 2", "name": "Second Grade", "age": "7-8", "focus": "Multi-syllable words, basic compounds, expanded story vocabulary"},
    {"level": "Grade 3", "name": "Third Grade", "age": "8-9", "focus": "Descriptive adjectives, nature, community, and inquiry words"},
    {"level": "Grade 4", "name": "Fourth Grade", "age": "9-10", "focus": "Academic, scientific, and literary vocabulary"},
    {"level": "Grade 5", "name": "Fifth Grade", "age": "10-11", "focus": "Abstract thinking, nuanced expressions, advanced concepts"}
]

# Mapping letters with phonetic guides and grade-graduated words
RAW_ALPHABET = {
    "A": {
        "phonetic_hint": "/eɪ/ or /æ/",
        "description": "First letter of the alphabet",
        "grades": {
            "Pre-K": ("Ant", "noun", "A tiny ant crawls on the leaf."),
            "Kindergarten": ("Apple", "noun", "I bite into a sweet red apple."),
            "Grade 1": ("Acorn", "noun", "A squirrel hides an acorn under the tree."),
            "Grade 2": ("Anchor", "noun", "The heavy anchor keeps the boat in place."),
            "Grade 3": ("Astronaut", "noun", "The astronaut floats gently in outer space."),
            "Grade 4": ("Altitude", "noun", "The airplane reached a high altitude above the clouds."),
            "Grade 5": ("Abundance", "noun", "The garden produced an abundance of fresh vegetables.")
        }
    },
    "B": {
        "phonetic_hint": "/biː/",
        "description": "Second letter of the alphabet",
        "grades": {
            "Pre-K": ("Bat", "noun", "The brown bat flies at night."),
            "Kindergarten": ("Ball", "noun", "She rolls the bright red ball to me."),
            "Grade 1": ("Bird", "noun", "A little blue bird sings on the branch."),
            "Grade 2": ("Bridge", "noun", "We walked safely across the wooden bridge."),
            "Grade 3": ("Bicycle", "noun", "He rode his new bicycle around the park."),
            "Grade 4": ("Blizzard", "noun", "A winter blizzard covered the rooftops in snow."),
            "Grade 5": ("Benevolent", "adjective", "The benevolent queen helped everyone in the village.")
        }
    },
    "C": {
        "phonetic_hint": "/siː/",
        "description": "Third letter of the alphabet",
        "grades": {
            "Pre-K": ("Cat", "noun", "The soft cat purrs on my lap."),
            "Kindergarten": ("Cup", "noun", "I drink cold water from a blue cup."),
            "Grade 1": ("Cloud", "noun", "A fluffy white cloud drifts in the sky."),
            "Grade 2": ("Castle", "noun", "The king lived in a grand stone castle."),
            "Grade 3": ("Compass", "noun", "The compass needle pointed straight to the north."),
            "Grade 4": ("Curiosity", "noun", "Curiosity leads scientists to make new discoveries."),
            "Grade 5": ("Courageous", "adjective", "The courageous climber reached the mountain summit.")
        }
    },
    "D": {
        "phonetic_hint": "/diː/",
        "description": "Fourth letter of the alphabet",
        "grades": {
            "Pre-K": ("Dog", "noun", "The happy dog wags its tail."),
            "Kindergarten": ("Duck", "noun", "A yellow duck swims across the quiet pond."),
            "Grade 1": ("Drum", "noun", "He tapped a steady beat on the drum."),
            "Grade 2": ("Dragon", "noun", "The friendly green dragon flew through the clouds."),
            "Grade 3": ("Dolphin", "noun", "A playful dolphin leapt gracefully out of the ocean."),
            "Grade 4": ("Dormant", "adjective", "The dormant volcano has been peaceful for centuries."),
            "Grade 5": ("Diligent", "adjective", "The diligent student studied hard every single afternoon.")
        }
    },
    "E": {
        "phonetic_hint": "/iː/",
        "description": "Fifth letter of the alphabet",
        "grades": {
            "Pre-K": ("Egg", "noun", "A small bird hatches from the white egg."),
            "Kindergarten": ("Elf", "noun", "The busy elf made wooden toys."),
            "Grade 1": ("Eagle", "noun", "A majestic eagle soared high above the cliffs."),
            "Grade 2": ("Engine", "noun", "The train engine chugged along the iron tracks."),
            "Grade 3": ("Echo", "noun", "Our voices made a clear echo across the canyon."),
            "Grade 4": ("Ecosystem", "noun", "Every animal plays an important role in the forest ecosystem."),
            "Grade 5": ("Eloquent", "adjective", "Her eloquent speech inspired everyone in the auditorium.")
        }
    },
    "F": {
        "phonetic_hint": "/ɛf/",
        "description": "Sixth letter of the alphabet",
        "grades": {
            "Pre-K": ("Fox", "noun", "The red fox hid behind the tall bush."),
            "Kindergarten": ("Fish", "noun", "The little orange fish swims in clear water."),
            "Grade 1": ("Frog", "noun", "A green frog hopped into the lily pond."),
            "Grade 2": ("Feather", "noun", "A soft feather drifted slowly to the ground."),
            "Grade 3": ("Fossil", "noun", "The ancient fossil was preserved in solid rock."),
            "Grade 4": ("Fierce", "adjective", "A fierce wind rattled the tall pine trees."),
            "Grade 5": ("Flourish", "verb", "Wildflowers flourish during the warm spring months.")
        }
    },
    "G": {
        "phonetic_hint": "/dʒiː/",
        "description": "Seventh letter of the alphabet",
        "grades": {
            "Pre-K": ("Gum", "noun", "He blew a pink bubble with sweet gum."),
            "Kindergarten": ("Gift", "noun", "I wrapped a special gift with a red ribbon."),
            "Grade 1": ("Grass", "noun", "Green grass grew thick in the sunny meadow."),
            "Grade 2": ("Garden", "noun", "Bright red tulips bloomed across our front garden."),
            "Grade 3": ("Glacier", "noun", "The huge glacier melted slowly into the sea."),
            "Grade 4": ("Gravity", "noun", "Gravity keeps our feet firmly on the ground."),
            "Grade 5": ("Gratitude", "noun", "We expressed heartfelt gratitude for their generous support.")
        }
    },
    "H": {
        "phonetic_hint": "/eɪtʃ/",
        "description": "Eighth letter of the alphabet",
        "grades": {
            "Pre-K": ("Hat", "noun", "She wears a yellow hat in the sun."),
            "Kindergarten": ("Hen", "noun", "The mother hen pecked at seeds on the ground."),
            "Grade 1": ("Heart", "noun", "My heart beat fast after running up the hill."),
            "Grade 2": ("Helmet", "noun", "Always wear a sturdy helmet while riding your bike."),
            "Grade 3": ("Horizon", "noun", "The orange sun sank slowly below the distant horizon."),
            "Grade 4": ("Harmony", "noun", "The choir singers blended their voices in perfect harmony."),
            "Grade 5": ("Hesitant", "adjective", "He was hesitant at first, but soon joined the team.")
        }
    },
    "I": {
        "phonetic_hint": "/aɪ/",
        "description": "Ninth letter of the alphabet",
        "grades": {
            "Pre-K": ("Ice", "noun", "The ice is cold and slippery."),
            "Kindergarten": ("Ink", "noun", "The black ink made dark letters on the paper."),
            "Grade 1": ("Igloo", "noun", "The warm lamp glowed inside the snowy igloo."),
            "Grade 2": ("Island", "noun", "Palm trees lined the sandy shore of the island."),
            "Grade 3": ("Insect", "noun", "A tiny striped insect crawled across the green leaf."),
            "Grade 4": ("Illuminate", "verb", "Lanterns illuminate the garden walkway at night."),
            "Grade 5": ("Ingenious", "adjective", "She invented an ingenious device to clean ocean plastic.")
        }
    },
    "J": {
        "phonetic_hint": "/dʒeɪ/",
        "description": "Tenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Jam", "noun", "I spread sweet strawberry jam on toast."),
            "Kindergarten": ("Jug", "noun", "We poured cold milk from a tall jug."),
            "Grade 1": ("Jump", "verb", "The kids jump high over the skipping rope."),
            "Grade 2": ("Jacket", "noun", "Zip up your warm jacket before going outside."),
            "Grade 3": ("Jungle", "noun", "Many colorful birds live in the tropical jungle."),
            "Grade 4": ("Journey", "noun", "Their brave journey led them across desert sands."),
            "Grade 5": ("Judicious", "adjective", "A judicious judge listens carefully to all evidence.")
        }
    },
    "K": {
        "phonetic_hint": "/keɪ/",
        "description": "Eleventh letter of the alphabet",
        "grades": {
            "Pre-K": ("Kid", "noun", "A cheerful kid played in the sandbox."),
            "Kindergarten": ("Kite", "noun", "A bright diamond kite danced in the spring wind."),
            "Grade 1": ("King", "noun", "The wise king sat upon the golden throne."),
            "Grade 2": ("Kitten", "noun", "The fluffy kitten chased a ball of blue yarn."),
            "Grade 3": ("Kangaroo", "noun", "A mother kangaroo hopped through the open plains."),
            "Grade 4": ("Keen", "adjective", "Hawks have keen eyesight to spot prey from afar."),
            "Grade 5": ("Kinship", "noun", "The teammates felt a strong kinship after working together.")
        }
    },
    "L": {
        "phonetic_hint": "/ɛl/",
        "description": "Twelfth letter of the alphabet",
        "grades": {
            "Pre-K": ("Log", "noun", "A sleepy turtle rested on a wooden log."),
            "Kindergarten": ("Leg", "noun", "He kicked the soccer ball with his right leg."),
            "Grade 1": ("Leaf", "noun", "A golden autumn leaf fluttered down from the tree."),
            "Grade 2": ("Lantern", "noun", "We carried a bright lantern into the dark cave."),
            "Grade 3": ("Lighthouse", "noun", "The lighthouse beamed bright light across the stormy waves."),
            "Grade 4": ("Luminous", "adjective", "Fireflies created a luminous glow in the evening forest."),
            "Grade 5": ("Liberate", "verb", "Volunteers worked tirelessly to liberate trapped wildlife.")
        }
    },
    "M": {
        "phonetic_hint": "/ɛm/",
        "description": "Thirteenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Map", "noun", "We looked at the treasure map to find the trail."),
            "Kindergarten": ("Mug", "noun", "Dad held a warm mug of cocoa in both hands."),
            "Grade 1": ("Moon", "noun", "The full moon shone like silver in the night sky."),
            "Grade 2": ("Monkey", "noun", "A funny monkey swung between the leafy branches."),
            "Grade 3": ("Mountain", "noun", "Snow covered the sharp peaks of the tall mountain."),
            "Grade 4": ("Mirage", "noun", "A shimmering mirage appeared on the hot desert road."),
            "Grade 5": ("Meticulous", "adjective", "The artist was meticulous with every brushstroke.")
        }
    },
    "N": {
        "phonetic_hint": "/ɛn/",
        "description": "Fourteenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Net", "noun", "We caught tiny minnows with a small mesh net."),
            "Kindergarten": ("Nut", "noun", "The brown squirrel cracked open a tasty nut."),
            "Grade 1": ("Nest", "noun", "Three blue eggs rested safely inside the bird nest."),
            "Grade 2": ("Needle", "noun", "Grandma threaded the silver needle with green yarn."),
            "Grade 3": ("Nomad", "noun", "The nomad traveled across rolling desert dunes with camels."),
            "Grade 4": ("Nebula", "noun", "A colourful nebula glowed brightly in deep outer space."),
            "Grade 5": ("Navigate", "verb", "Ancient sailors used bright stars to navigate across the ocean.")
        }
    },
    "O": {
        "phonetic_hint": "/oʊ/",
        "description": "Fifteenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Owl", "noun", "A wise owl hooted softly from the tree."),
            "Kindergarten": ("Ox", "noun", "The strong ox pulled the wagon through the farm."),
            "Grade 1": ("Orange", "noun", "She peeled a sweet and juicy orange for snack time."),
            "Grade 2": ("Otter", "noun", "A playful river otter floated happily on its back."),
            "Grade 3": ("Ocean", "noun", "Gentle blue waves rolled across the vast ocean."),
            "Grade 4": ("Orbit", "noun", "The moon completes one full orbit around the earth every month."),
            "Grade 5": ("Optimistic", "adjective", "Despite the rainy forecast, she remained optimistic about our picnic.")
        }
    },
    "P": {
        "phonetic_hint": "/piː/",
        "description": "Sixteenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Pig", "noun", "The pink pig splashed in a muddy puddle."),
            "Kindergarten": ("Pan", "noun", "Mom baked sweet blueberry pancakes in a warm pan."),
            "Grade 1": ("Puppy", "noun", "The fluffy puppy bounced excitedly near the front door."),
            "Grade 2": ("Planet", "noun", "Earth is the third planet orbiting our warm sun."),
            "Grade 3": ("Penguin", "noun", "The penguin slid swiftly down the snowy ice hill."),
            "Grade 4": ("Pinnacle", "noun", "The climbers celebrated when they reached the pinnacle of the mountain."),
            "Grade 5": ("Persevere", "verb", "If you persevere through challenges, you will achieve your dreams.")
        }
    },
    "Q": {
        "phonetic_hint": "/kjuː/",
        "description": "Seventeenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Quack", "verb", "The baby ducks quack as they follow their mother."),
            "Kindergarten": ("Queen", "noun", "The queen wore a sparkling silver crown upon her head."),
            "Grade 1": ("Quilt", "noun", "A warm handmade quilt kept us cozy all winter."),
            "Grade 2": ("Quiver", "noun", "The archer pulled a wooden arrow from his leather quiver."),
            "Grade 3": ("Quarry", "noun", "Workers cut large blocks of marble from the stone quarry."),
            "Grade 4": ("Quasar", "noun", "A distant quasar emits tremendous amounts of cosmic energy."),
            "Grade 5": ("Quintessential", "adjective", "Freshly baked apple pie is the quintessential autumn dessert.")
        }
    },
    "R": {
        "phonetic_hint": "/ɑːr/",
        "description": "Eighteenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Rug", "noun", "We sat together on the soft woven rug."),
            "Kindergarten": ("Ring", "noun", "A shiny golden ring sparkled in the jewelry box."),
            "Grade 1": ("Rain", "noun", "Cool spring rain tapped softly against the window glass."),
            "Grade 2": ("Rocket", "noun", "The roaring rocket blasted off toward the stars."),
            "Grade 3": ("Rainbow", "noun", "A bright rainbow arched across the valley after the shower."),
            "Grade 4": ("Radiant", "adjective", "The bride wore a radiant smile as music filled the hall."),
            "Grade 5": ("Resilient", "adjective", "The resilient oak tree stood firm against the raging gale.")
        }
    },
    "S": {
        "phonetic_hint": "/ɛs/",
        "description": "Nineteenth letter of the alphabet",
        "grades": {
            "Pre-K": ("Sun", "noun", "The warm yellow sun shines bright in the sky."),
            "Kindergarten": ("Sock", "noun", "I pulled a warm wool sock onto my cold foot."),
            "Grade 1": ("Star", "noun", "A tiny silver star twinkled high above the mountains."),
            "Grade 2": ("Spider", "noun", "The garden spider spun an intricate circular web."),
            "Grade 3": ("Sunflower", "noun", "A cheerful sunflower turned to face the morning sun."),
            "Grade 4": ("Stalwart", "adjective", "The stalwart bridge held firm through floods and storms."),
            "Grade 5": ("Serendipity", "noun", "Finding my lost childhood photo inside an old book was pure serendipity.")
        }
    },
    "T": {
        "phonetic_hint": "/tiː/",
        "description": "Twentieth letter of the alphabet",
        "grades": {
            "Pre-K": ("Tub", "noun", "Warm water filled the bath tub with soapy bubbles."),
            "Kindergarten": ("Top", "noun", "He spun the wooden top and watched it whirl around."),
            "Grade 1": ("Tree", "noun", "Birds built cozy nests inside the tall pine tree."),
            "Grade 2": ("Tiger", "noun", "The striped tiger walked quietly through tall jungle grass."),
            "Grade 3": ("Telescope", "noun", "Through the telescope, craters on the moon appeared sharp and clear."),
            "Grade 4": ("Turbulence", "noun", "The aircraft experienced sudden turbulence over the mountains."),
            "Grade 5": ("Tranquil", "adjective", "The tranquil mountain lake reflected the snow-dusted peaks like glass.")
        }
    },
    "U": {
        "phonetic_hint": "/juː/",
        "description": "Twenty-first letter of the alphabet",
        "grades": {
            "Pre-K": ("Up", "adverb", "Look up at the fluffy clouds floating by!"),
            "Kindergarten": ("Urn", "noun", "A clay urn sat by the fountain in the courtyard."),
            "Grade 1": ("Under", "preposition", "The sleepy cat rested under the kitchen table."),
            "Grade 2": ("Umbrella", "noun", "She held a yellow umbrella to keep off the rain."),
            "Grade 3": ("Unicorn", "noun", "The mythical unicorn had a shimmering silver horn."),
            "Grade 4": ("Unravel", "verb", "Detectives began to unravel the clues of the mystery."),
            "Grade 5": ("Unanimous", "adjective", "The jury reached a unanimous verdict after careful review.")
        }
    },
    "V": {
        "phonetic_hint": "/viː/",
        "description": "Twenty-second letter of the alphabet",
        "grades": {
            "Pre-K": ("Van", "noun", "We rode to the beach inside a blue van."),
            "Kindergarten": ("Vest", "noun", "He wore a warm wool vest over his collared shirt."),
            "Grade 1": ("Vine", "noun", "Green ivy vine climbed up the sunny garden wall."),
            "Grade 2": ("Violin", "noun", "She played a gentle melody on her wooden violin."),
            "Grade 3": ("Volcano", "noun", "Smoke rose gently from the summit of the ancient volcano."),
            "Grade 4": ("Vibrant", "adjective", "Vibrant autumn leaves painted the hillsides in scarlet and gold."),
            "Grade 5": ("Vindicate", "verb", "New evidence surfaced in court to fully vindicate the scientist.")
        }
    },
    "W": {
        "phonetic_hint": "/ˈdʌbəl.juː/",
        "description": "Twenty-third letter of the alphabet",
        "grades": {
            "Pre-K": ("Web", "noun", "Morning dew drops sparkled on the spider web."),
            "Kindergarten": ("Wig", "noun", "The actor wore a curly white wig for the play."),
            "Grade 1": ("Wind", "noun", "A cool autumn wind rustled the leaves on the ground."),
            "Grade 2": ("Whale", "noun", "A giant blue whale breached the ocean surface."),
            "Grade 3": ("Waterfall", "noun", "Cool mist sprayed from the roaring mountain waterfall."),
            "Grade 4": ("Wilderness", "noun", "We hiked through the untamed wilderness for three days."),
            "Grade 5": ("Whimsical", "adjective", "The illustrator created a whimsical world filled with flying teapots.")
        }
    },
    "X": {
        "phonetic_hint": "/ɛks/",
        "description": "Twenty-fourth letter of the alphabet",
        "grades": {
            "Pre-K": ("Box", "noun", "A surprise gift waited inside the cardboard box."),
            "Kindergarten": ("Fox", "noun", "The quick brown fox jumped over the sleeping dog."),
            "Grade 1": ("X-ray", "noun", "The doctor looked at the x-ray of my broken wrist."),
            "Grade 2": ("Xylophone", "noun", "The child tapped cheerful notes on the wooden xylophone."),
            "Grade 3": ("Xenon", "noun", "Xenon gas glows with a bright blue light in special lamps."),
            "Grade 4": ("Xeriscape", "noun", "Our desert school planted a xeriscape garden that saves water."),
            "Grade 5": ("Xenolith", "noun", "The geologist studied a rare xenolith rock trapped inside ancient lava.")
        }
    },
    "Y": {
        "phonetic_hint": "/waɪ/",
        "description": "Twenty-fifth letter of the alphabet",
        "grades": {
            "Pre-K": ("Yak", "noun", "The shaggy yak grazed on cold mountain slopes."),
            "Kindergarten": ("Yam", "noun", "We baked a sweet orange yam for holiday dinner."),
            "Grade 1": ("Yarn", "noun", "She knit a warm scarf using soft blue yarn."),
            "Grade 2": ("Yellow", "adjective", "A yellow school bus stopped at the street corner."),
            "Grade 3": ("Yacht", "noun", "A sleek white yacht glided across the calm blue harbor."),
            "Grade 4": ("Yield", "verb", "Rich farmland can yield bountiful crops of wheat."),
            "Grade 5": ("Yearning", "noun", "After years abroad, he felt a deep yearning to return home.")
        }
    },
    "Z": {
        "phonetic_hint": "/zɛd/ or /ziː/",
        "description": "Twenty-sixth letter of the alphabet",
        "grades": {
            "Pre-K": ("Zip", "verb", "Zip up your warm winter coat before stepping outside!"),
            "Kindergarten": ("Zoo", "noun", "We visited tall giraffes and monkeys at the city zoo."),
            "Grade 1": ("Zebra", "noun", "The striped zebra trotted across the grassy savannah."),
            "Grade 2": ("Zigzag", "noun", "The hiking trail made a sharp zigzag up the steep hill."),
            "Grade 3": ("Zephyr", "noun", "A gentle zephyr cooled the afternoon heat along the shore."),
            "Grade 4": ("Zenith", "noun", "At noon, the blazing summer sun reached its daily zenith."),
            "Grade 5": ("Zealous", "adjective", "The zealous volunteers planted hundreds of trees in a single weekend.")
        }
    }
}

def build_corpus_data():
    corpus = []
    
    for letter, ldata in RAW_ALPHABET.items():
        letter_obj = {
            "letter": letter,
            "phonetic_hint": ldata["phonetic_hint"],
            "description": ldata["description"],
            "words": []
        }
        
        for g_level, (word, pos, sentence) in ldata["grades"].items():
            clean_word = word.lower().replace("-", "_").replace(" ", "_")
            word_id = f"word_{letter.lower()}_{clean_word}"
            sent_id = f"sent_{letter.lower()}_{clean_word}_1"
            
            # Form clean standard relative audio paths
            word_audio_path = f"audio/words/{letter.lower()}_{clean_word}.wav"
            sent_audio_path = f"audio/sentences/{letter.lower()}_{clean_word}_1.wav"
            
            word_obj = {
                "id": word_id,
                "word": word,
                "grade": g_level,
                "part_of_speech": pos,
                "audio_path": word_audio_path,
                "image_path": "",
                "sentences": [
                    {
                        "id": sent_id,
                        "sentence": sentence,
                        "audio_path": sent_audio_path
                    }
                ]
            }
            letter_obj["words"].append(word_obj)
            
        corpus.append(letter_obj)
    
    return corpus

if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    output_json = repo_root / "data" / "corpus.json"
    
    corpus_data = build_corpus_data()
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(corpus_data, f, indent=2, ensure_ascii=False)
        
    print(f"Generated grade-wise corpus at: {output_json}")
    total_words = sum(len(item["words"]) for item in corpus_data)
    total_sentences = sum(len(w["sentences"]) for item in corpus_data for w in item["words"])
    print(f"Total letters: {len(corpus_data)}, Words: {total_words}, Sentences: {total_sentences}")
