import pygame, sys, os
import json
#Project Conversation computer name is CH1P: Conversational Haver ( for 1 Person / or 1st Prototype )
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
flags = pygame.SCALED | pygame.RESIZABLE #makes game resizeable and not blurry
screen = pygame.display.set_mode((WIDTH, HEIGHT),flags)
pygame.display.set_caption("Project Conversation [OvO]") #name of window
pygame.display.set_icon(pygame.image.load("icon.png")) #icon for window
font = pygame.font.SysFont(None, 32)
current_audio_scene = None


# makes text not go off screen--------------------------------------
def _wrap_text(font, text, max_width):
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        test = current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines

# Loads the story from a text file--------------------------------------
def load_story(filename):
    story = {}
    current_scene = None
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): 
                continue
            if line.startswith("[") and line.endswith("]"):
                current_scene = line[1:-1]
                story[current_scene] = {"text":"", "choices":[], "image":"default", "audio":""}
            elif "=" in line and current_scene:
                key, value = line.split("=", 1)
                if key == "text":
                    story[current_scene]["text"] = value
                elif key == "image":
                    story[current_scene]["image"] = value
                elif key == "audio":
                    story[current_scene]["audio"] = value
                elif key == "choices":
                    choices = [tuple(c.strip().split(":",1)) for c in value.split(",") if ":" in c]
                    story[current_scene]["choices"] = choices
    return story

story = load_story("story.txt")
current_scene = "TitleScreen"

        
# load images/audio from folder based on text file--------------------------------------
image_folder = "image"  # folder where images are stored
audio_folder = "audio"  # folder where audio files are stored

images = {}
for scene in story:   #loads image for each scene based on text file, if messed up load placeholder
    img_file = os.path.join(image_folder, story[scene]["image"]+".png")
    if os.path.exists(img_file):
        img = pygame.image.load(img_file)
        images[story[scene]["image"]] = pygame.transform.scale(img, (525, 400))
    else:
        # placeholder gray box if messup load image
        surf = pygame.Surface((525, 400))
        surf.fill((50,50,50))
        images[story[scene]["image"]] = surf


audios = {} 
for scene in story: #loads audio for each scene based on text file, if no file then load None
    audio_name = story[scene].get("audio", "")
    if audio_name:
        audio_file = os.path.join(audio_folder, audio_name)
        if os.path.exists(audio_file):
            try:
                audios[audio_name] = pygame.mixer.Sound(audio_file)
            except pygame.error:
                audios[audio_name] = None
        else:
            audios[audio_name] = None


def play_scene_audio(scene_name): #plays audio for each scene based on text file "audio=name.mp3"
    global current_audio_scene
    scene = story.get(scene_name)
    if not scene:
        return
    audio_name = scene.get("audio", "")
    if audio_name == "" or audio_name is None:
        pygame.mixer.stop()
        current_audio_scene = None
        return
    if current_audio_scene == scene_name:
        return
    sound = audios.get(audio_name)
    if sound:
        pygame.mixer.stop()
        sound.play(loops=0) #makes not loop
        current_audio_scene = scene_name
    else:
        pygame.mixer.stop()
        current_audio_scene = None


# loop that makes thing work--------------------------------------
running = True
while running:
    if current_scene == "exit":
        pygame.quit()
        sys.exit()
    
    screen.fill((130,86,61)) #background color
    pygame.draw.rect(screen, (0,0,0), (133,0,540,400)) #border for image
    scene = story[current_scene]

    #shows image if not messed up--------------------------------------
    screen.blit(images[scene["image"]], (140,0))

    # shows text--------------------------------------
    pygame.draw.rect(screen, (52,11,56), (0,400,WIDTH,200))
    pygame.draw.rect(screen, (255,255,255), (0,400,WIDTH,200),2)
    max_w = WIDTH - 40
    lines = _wrap_text(font, scene["text"], max_w)
    y = 420
    for line in lines:
        surf = font.render(line, True, (255,255,255))
        screen.blit(surf, (20, y))
        y += font.get_linesize()

    # shows choices--------------------------------------
    for i, choice in enumerate(scene["choices"]):
        choice_text = f"{i+1}. {choice[0]}"
        choice_surface = font.render(choice_text, True, (255,242,0))
        screen.blit(choice_surface, (20,510 + i*30))

    # the button press reader 9000--------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and len(scene["choices"]) >=1:
                current_scene = scene["choices"][0][1]
            elif event.key == pygame.K_2 and len(scene["choices"]) >=2:
                current_scene = scene["choices"][1][1]
            elif event.key == pygame.K_3 and len(scene["choices"]) >=3:
                current_scene = scene["choices"][2][1]

    play_scene_audio(current_scene)

    pygame.display.flip()

pygame.quit()
sys.exit()

#Music Player --NOT USED BUT HELPFUL STUFF LEARNED--------------------------------------
#pygame.mixer.init()
#pygame.mixer.music.load("BGM.mp3")

# Play the music in a loop
#pygame.mixer.music.play(-1)

#pygame.mixer.music.set_volume(0.02)