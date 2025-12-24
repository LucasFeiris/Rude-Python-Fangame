
import pygame
import math
import random
from time import sleep, time
import sys
import os

def base_dir():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = base_dir()
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
SFX_DIR = os.path.join(ASSETS_DIR, "Sound_effs")

def main():

    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Rude Python")
    clock=pygame.time.Clock()
    font_big=pygame.font.Font(None,50)
    font=pygame.font.Font(None,40)
    font_small=pygame.font.Font(None,30)
    ## To write texts and other cutscenes
    counter=0
    time_updated = 0
    interval = 40
    text_to_be_shown = ""
    player_act_counter = 0
    ### def hall

    def dialogue_maker_v3(text, text_shown, time_now, time_updated, interval, counter):
        if time_now - time_updated >= interval and counter < len(text):
            text_shown += text[counter]
            counter += 1
            time_updated = time_now
        return counter, time_updated, text_shown

    def draw_text(surface, text, font, color, x, y, line_spacing=4):
        lines = text.split("\n")                   #If I want to change the line spacing
        for c in lines:
            surf = font.render(c, True, color)
            surface.blit(surf, (x, y))
            y += surf.get_height() + line_spacing

    ## Variables pre-running ##
    ##THE MAIN MECHANIC##
    player_turn_end = False
    terminal_phase = False
    block_actions = False
    swap_delay = False
    swap_delay_time = 0
    # BLOCK TO COVER THE MAIN BAR
    box_to_cover_bar = pygame.Rect((90,510,1100,120))
    box_to_cover_visibility = False
    #　
    battle_box_1=pygame.Rect((40,40,1200,640))
    battle_box_2=pygame.Rect((60,60,1160,600))
    combat_box_1=pygame.Rect((80,500,1120,140))
    combat_box_2=pygame.Rect((90,510,1100,120))

    ## PLAYER STATS ##
    ## HP
    player_max_health = 100
    player_health = 100
    player_hp_box_border = pygame.Rect(80,440,180,50)
    #To display heal and damage to the player!
    damage_taken_text_time = pygame.time.get_ticks()
    damage_taken_text_trigger = False
    heal_text_time = pygame.time.get_ticks()
    player_heal_trigger = False
    heal_text_levitation_position_x = 0
    heal_text_levitation_position_y = 0
    #ATTACK#
    player_damage_values = [0, 5, 10, 15, 20]
    max_atk_reached = False
    max_true_atk_reached = False
    attack_landed = False
    damage_dealt_to_enemy = 0
    #FOR SHOWING THE PLAYER ATTACK ON SCREEN#
    attack_text_trigger = False
    attack_text_time = pygame.time.get_ticks()
    attack_text_levitation_position = 0
    #DEFENSE#
    player_defense = 0
    player_defense_increase = [1, 2, 3]
    player_defense_chances = [35, 35, 30]
    max_def_reached = False
    max_true_def_reached = False
    damage_dealt_to_player = False
    #Accuracy
    player_accuracy_increase = [4, 5, 6]
    player_accuracy_chances = [15, 55, 30]
    player_damage_chances = [10, 25, 30, 25, 10]

    ## ENEMY HP BAR ##
    enemy_name = "???"
    enemy_max_health = 203
    enemy_health = 203
    enemy_hp_box_border = pygame.Rect(910,110,250,50)

    #To increase stats
    buff_atk = 0
    buff_def = 0
    buff_acc = 0
    limit_break = False
    max_acc_reached = False

    ## MENU BOXES ##
    attack_box_1 = pygame.Rect((140,525,200,90))
    attack_box_2 = pygame.Rect((150,535,180,70))
    magic_box_1 = pygame.Rect((400,525,200,90))
    magic_box_2 = pygame.Rect((410,535,180,70))
    act_box_1 = pygame.Rect((660,525,200,90))
    act_box_2 = pygame.Rect((670,535,180,70))
    items_box_1 = pygame.Rect((920,525,200,90))
    items_box_2 = pygame.Rect((930,535,180,70))

    ## Battle MENU
    main_bar = True
    magic_bar = False
    act_bar = False
    items_bar = False

    ## Options ##
    battle_option = 0
    magic_option = 0
    act_option = 0
    items_option = 0

    ##
    #ACT options
    act_option2_pressed = False
    ##
    #ITEMS variables
    inventory = ["Max-Potion", "Max-Potion", "Great Potion",
                 "Great Potion","OK Potion", "OK Potion"]
    #  inventory[2] = "Great Potion" and inventory [4] = "OK Potion"

    items_rows = 2
    items_width = 230
    items_height = 30
    items_x_grid = 140
    items_y_grid = 525
    item_back_position = 6
    item_top_limit = 2
    item_bottom_limit = 5
    item_start_position = 0
    items_only_back_option = False

    # Pictures and Animations
    ### ENEMY ###
    position_enemy_x = 900
    position_enemy_y = 150
    size_enemy_x = 270
    size_enemy_y = 280
    enemy_anim_roll = 0
    enemy_anim_timing = pygame.time.get_ticks()

    # Levitation parameters
    lev_amplitude_x = 1
    lev_amplitude_y = 8
    lev_speed_x = 2
    lev_speed_y = 2
    lev_time = 0

    #Anim 0

    enemy_awakes = [
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_0.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png"))]

    for size in range(len(enemy_awakes)):
        enemy_awakes[size] = pygame.transform.scale(enemy_awakes[size],(size_enemy_x,size_enemy_y))
    enemy_awakes_counter = 0
    enemy_awakes_tempo = 640
    enemy_awakes_last_frame = pygame.time.get_ticks()


    #Enemy Anim 1
    enemy_idle = [
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue1_yellow2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue0_yellow1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue0_yellow1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue1_yellow0.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue1_yellow0.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue2_yellow1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue2_yellow1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_blue_yellow_2.png"))]

    for size in range(len(enemy_idle)):
        enemy_idle[size] = pygame.transform.scale(enemy_idle[size],(size_enemy_x,size_enemy_y))
    enemy_idle_counter = 0
    enemy_idle_tempo = 640
    enemy_idle_last_frame = pygame.time.get_ticks()

    hard_enemy_idle = [
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow1_blue2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow0_blue1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow0_blue1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow1_blue0.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow1_blue0.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow2_blue1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow2_blue1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "P_Idle", "P_Idle_yellow_blue_2.png"))]

    for size in range(len(hard_enemy_idle)):
        hard_enemy_idle[size] = pygame.transform.scale(hard_enemy_idle[size],(size_enemy_x,size_enemy_y))

    #Enemy Anim 2
    enemy_get_hit_animation = pygame.image.load(os.path.join(ASSETS_DIR,  "P_Idle", "P_Idle_blue_yellow_0.png"))
    hard_enemy_get_hit_animation = pygame.image.load(os.path.join(ASSETS_DIR,  "P_Idle", "P_Idle_yellow_blue_0.png"))

    enemy_get_hit_animation = pygame.transform.scale(enemy_get_hit_animation,(size_enemy_x,size_enemy_y))
    hard_enemy_get_hit_animation = pygame.transform.scale(hard_enemy_get_hit_animation,(size_enemy_x,size_enemy_y))

    ### PLAYER ###
    position_player_x = 220
    position_player_y = 200
    size_player_x = 170
    size_player_y = 180
    player_anim_roll = 0
    player_anim_timing = pygame.time.get_ticks()

    #Player Anim 0
    player_stand = pygame.image.load(os.path.join(ASSETS_DIR,  "C_Stand", "C-Stand.png"))
    player_stand = pygame.transform.scale(player_stand, (size_player_x,size_player_y))
    #change x, y to RESIZE the picture
    # Anim 1
    player_start = [
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start3.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start4.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start5.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start6.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start7.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start8.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start9.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start10.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_start", "C-Start11.png"))]

    for size in range(len(player_start)):
        player_start[size] = pygame.transform.scale(player_start[size],(size_player_x,size_player_y))
    player_start_counter = 0
    player_start_tempo = 140
    player_start_last_frame = pygame.time.get_ticks()
    #Player Anim 2
    player_idle = [
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Idle", "C-Idle1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Idle", "C-Idle2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Idle", "C-Idle3.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Idle", "C-Idle4.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Idle", "C-Idle5.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Idle", "C-Idle6.png"))]

    for size in range(len(player_idle)):
        player_idle[size] = pygame.transform.scale(player_idle[size], (size_player_x,size_player_y))
    player_idle_counter = 0
    player_idle_tempo = 140 #1000 = 1 seg
    player_idle_last_frame = pygame.time.get_ticks()
    #Player Anim 3
    player_think = [pygame.image.load(os.path.join(ASSETS_DIR,  "C_Think", "C-Think1.png")),
                    pygame.image.load(os.path.join(ASSETS_DIR,  "C_Think", "C-Think2.png"))]
    for size in range(len(player_think)):
        player_think[size] = pygame.transform.scale(player_think[size], (size_player_x,size_player_y))
    player_think_counter = 0
    player_think_tempo = 300
    player_think_last_frame = pygame.time.get_ticks()
    #Player Anim 4
    player_fumble = [pygame.image.load(os.path.join(ASSETS_DIR,  "C_Item", "C-Item1.png")),
                     pygame.image.load(os.path.join(ASSETS_DIR,  "C_Item", "C-Item2.png"))]
    for size in range(len(player_fumble)):
        player_fumble[size] = pygame.transform.scale(player_fumble[size], (size_player_x,size_player_y))
    player_fumble_counter = 0
    player_fumble_tempo = 340
    player_fumble_last_frame = pygame.time.get_ticks()
    # Anim 5 - 5.5
    player_prepare_attack = pygame.image.load(os.path.join(ASSETS_DIR,  "C_Attack", "C-Atk1.png"))
    player_prepare_timing = pygame.time.get_ticks()
    player_prepare_attack = pygame.transform.scale(player_prepare_attack, (size_player_x,size_player_y))
    player_attack = [
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk3.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk4.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk5.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk6.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk7.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Attack", "C-Atk8.png"))]
    for size in range(len(player_attack)):
        player_attack[size] = pygame.transform.scale(player_attack[size],(size_player_x,size_player_y))
    player_attack_counter = 0
    player_attack_tempo = 100
    player_attack_last_frame = pygame.time.get_ticks()
    #Player Anim 6
    player_act = [
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act1.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act2.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act3.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act4.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act5.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act6.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act7.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act8.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act9.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act10.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Act", "C-Act11.png"))]
    for size in range(len(player_act)):
        player_act[size] = pygame.transform.scale(player_act[size],(size_player_x,size_player_y))
    player_act_counter = 0
    player_act_tempo = 140
    player_act_last_frame = pygame.time.get_ticks()

    #Player Anim 7 - 7.5
    player_get_hit_animation = pygame.image.load(os.path.join(ASSETS_DIR,  "C_TakeDamage", "C-GetHit.png"))
    player_get_hit_animation = pygame.transform.scale(player_get_hit_animation,(size_player_x,size_player_y))
    player_fainted = pygame.image.load(os.path.join(ASSETS_DIR,  "C_TakeDamage", "C-Down.png"))
    player_fainted = pygame.transform.scale(player_fainted, (size_player_x,size_player_y))

    #Player Anim 8
    player_item = [
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Item", "C-Item3.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Item", "C-Item4.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Item", "C-Item5.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Item", "C-Item6.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Item", "C-Item7.png")),
        pygame.image.load(os.path.join(ASSETS_DIR, "C_Item", "C-Item8.png"))]
    for size in range(len(player_item)):
        player_item[size] = pygame.transform.scale(player_item[size],(size_player_x,size_player_y))
    player_item_counter = 0
    player_item_tempo = 200
    player_item_last_frame = pygame.time.get_ticks()

    # Damage Shake
    player_get_hit = False
    hit_start_time = pygame.time.get_ticks()
    shake_dur = 600
    shake_pwr = 8
    damage = 0

    enemy_get_hit = False
    enemy_hit_start_time = pygame.time.get_ticks()
    enemy_shake_dur = 500
    enemy_shake_pwr = 0

    # -- TERMINAL VARIABLES -- #
    turn_counter = 1
    enemy_decisions = [1, 2]
    enemy_attack_decisions = ['numbers', 'pool', 'words']
    late_answer = False
    late_answer_time = 30
    terminal_action_ended = False

    terminal_action = 1 #start attacking
    attack_chosen = 'words' #start with words
    battle_hp_check_answer_time = False #Not only HP determines if the games gets harder!
    battle_hp_check_numbers = False
    battle_hp_check_pool = False
    battle_hp_check_words = False

    terminal_act_counter = 0 #If the player wants to talk with the machine!!
    lonely_by_self = False
    lonely_by_friends = False
    block_enemy_damage = False

    bad_ending = False

    # Debuffs

    debuff_atk = False
    debuff_atk_lengh = 0
    debuff_atk_pwr = 5

    debuff_def = False
    debuff_def_lengh = 0
    debuff_def_pwr = 7

    ## SOUNDS ##

    #pygame.mixer.music.load "Sound_effs/Rude Buster.mp3")

    music = {
        "rude buster": os.path.join(SFX_DIR, "Rude Buster.mp3"),
        "hammer of justice": os.path.join(SFX_DIR, "Hammer of Justice.mp3"),
        "wise farewell": os.path.join(SFX_DIR, "Wise words.mp3")}

    music_battle_trigger = False
    music_battle_playing = False

    hard_battle_trigger = False
    hard_battle_playing = False

    win_battle_playing = False

    music_now = None

    def music_play(track_name, volume=0.3, loop = True):
        nonlocal music_now

        if music_now == track_name:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(music[track_name])
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)

        music_now = track_name

    sefx = {
        "select_enter": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_select.wav")),
        "select_arrow": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_menumove.wav")),
        "attack": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_damage.wav")),
        "hurt": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_hurt1.wav")),
        "start battle": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_weaponpull.wav")),
        "heal": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_power.wav")),
        "hit": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_damage.wav")),
        "right answer": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_coin.wav")),
        "wrong answer": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_error.wav")),
        "magic": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_boost.wav")),
        "critical hit1": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_knight_cut.wav")),
        "critical hit2": pygame.mixer.Sound(os.path.join(SFX_DIR, "snd_rudebuster_hit.wav"))}

    #MASTER CLOCK
    time_game = pygame.time.get_ticks()
    ##

    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN and not block_actions:
                if main_bar==True:
                    if event.key == pygame.K_RIGHT:
                        sefx["select_arrow"].play()
                        if battle_option < 3:
                            battle_option += 1
                        elif battle_option == 3:
                            battle_option = 0

                    if event.key  == pygame.K_LEFT:
                        sefx["select_arrow"].play()
                        if  battle_option > 0:
                            battle_option -= 1
                        elif battle_option == 0:
                            battle_option = 3

                elif magic_bar==True:
                    if event.key == pygame.K_RIGHT:
                        sefx["select_arrow"].play()
                        if magic_option < 3:
                            magic_option += 1
                        elif magic_option == 3:
                            magic_option = 0
                    if event.key == pygame.K_LEFT:
                        sefx["select_arrow"].play()
                        if magic_option > 0:
                            magic_option -= 1
                        elif magic_option == 0:
                            magic_option = 3

                elif act_bar ==True:
                    if event.key == pygame.K_RIGHT:
                       sefx["select_arrow"].play()
                       if act_option < 3:
                           act_option += 1
                       elif act_option == 3:
                           act_option = 0
                    if event.key == pygame.K_LEFT:
                        sefx["select_arrow"].play()
                        if act_option > 0:
                            act_option -= 1
                        elif act_option == 0:
                            act_option = 3

                elif items_bar ==True:
                    if not len(inventory)==0:
                        if event.key == pygame.K_RIGHT:
                           if (items_option < item_back_position
                                   and items_option != item_top_limit):
                               items_option += 1
                               sefx["select_arrow"].play()
                           elif items_option == item_top_limit:
                               items_option = item_back_position
                               sefx["select_arrow"].play()
                           elif items_option == item_back_position:
                               items_option = item_start_position
                               sefx["select_arrow"].play()
                        if event.key == pygame.K_LEFT:
                            if (items_option > item_start_position
                                    and items_option != 3
                                    and items_option != item_back_position):
                                items_option -= 1
                                sefx["select_arrow"].play()
                            elif items_option == item_start_position:
                                items_option = item_back_position
                                sefx["select_arrow"].play()
                            elif items_option == item_back_position:
                                items_option = item_top_limit
                                sefx["select_arrow"].play()
                            elif items_option == 3:
                                if len(inventory) >= 4:
                                    items_option = item_back_position
                                    sefx["select_arrow"].play()

                        if event.key == pygame.K_UP:
                            if (items_option >= item_start_position
                                    and items_option <= item_top_limit):
                                items_option = items_option
                            if len(inventory) >= 4:
                                if (items_option >= 3
                                        and items_option <= item_bottom_limit):
                                    items_option -= 3
                                    sefx["select_arrow"].play()
                        if event.key == pygame.K_DOWN:
                            if len(inventory) <= 5 and items_option == 2:
                                items_option = items_option
                            elif len(inventory) <= 4 and items_option == 1:
                                items_option = items_option
                            elif len(inventory) >= 4:
                                if (items_option >= 0
                                        and items_option <= item_top_limit):
                                    items_option += 3
                                    sefx["select_arrow"].play()
                            elif (items_option >= 3
                                    and items_option <= item_bottom_limit):
                                items_option = items_option

                if main_bar==True:
                    if event.key == pygame.K_RETURN:
                        sefx["select_enter"].play()
                        if battle_option == 0:
                            player_anim_roll = 5
                            player_prepare_timing = pygame.time.get_ticks()
                            # END TURN#
                            swap_delay = True
                            swap_delay_time = pygame.time.get_ticks()+1300
                            player_turn_end = True
                            block_actions = True
                            #########

                        elif battle_option == 1:
                            main_bar = False
                            magic_bar = True
                            player_anim_roll = 3
                        elif battle_option == 2:
                            main_bar = False
                            act_bar = True
                            player_anim_roll = 3
                        elif battle_option == 3:
                            main_bar = False
                            items_bar = True
                            player_anim_roll = 4

                elif magic_bar:
                    if event.key == pygame.K_RETURN:
                        sefx["select_enter"].play()
                        player_anim_roll = 6
                        if magic_option == 0:
                            sefx["magic"].play()
                            block_actions = True
                            if not limit_break:
                                if player_damage_values[-1]<55:
                                    buff_atk = random.randint(8,12)
                                    for buff in range(1, len(player_damage_chances) - 1):
                                        player_damage_values[buff] += buff_atk
                                    player_damage_values[-1] += buff_atk * 2
                                    if player_damage_values[-1] >= 55:
                                        player_damage_values = [0, 25, 36, 42, 55]
                                else:
                                    max_atk_reached = True
                                    player_damage_values = [0,25,36,42,55]
                                box_to_cover_visibility = True
                                time_now = pygame.time.get_ticks()
                                time_game = time_now
                            elif limit_break:
                                if player_damage_values[-1] < 155:
                                    buff_atk = random.randint(16, 22)
                                    for buff in range(1, len(player_damage_chances) - 1):
                                        player_damage_values[buff] += buff_atk-(4-buff)*2
                                    player_damage_values[-1] += buff_atk * 2
                                elif player_damage_values[-1] >= 155:
                                    max_true_atk_reached = True
                                    player_damage_values = [0,38,51,68,155]
                                box_to_cover_visibility = True
                                time_now = pygame.time.get_ticks()
                                time_game = time_now

                        elif magic_option == 1:
                            sefx["magic"].play()
                            block_actions = True
                            if not limit_break:
                                if player_defense < 7:
                                    buff_def = random.choices(player_defense_increase,weights=player_defense_chances,k=1)[0]
                                    player_defense += buff_def
                                    if player_defense > 7:
                                        player_defense = 7
                                    box_to_cover_visibility = True
                                    time_now = pygame.time.get_ticks()
                                    time_game = time_now
                                else:
                                    player_defense = 7
                                    max_def_reached = True
                                    box_to_cover_visibility = True
                                    time_now = pygame.time.get_ticks()
                                    time_game = time_now
                            elif limit_break:
                                if player_defense < 15:
                                    buff_def = random.choices(player_defense_increase, weights=player_defense_chances, k=1)[0]
                                    buff_def += 2
                                    player_defense += buff_def
                                    if player_defense > 15:
                                        player_defense = 15
                                    box_to_cover_visibility = True
                                    time_now = pygame.time.get_ticks()
                                    time_game = time_now
                                elif player_defense >= 15:
                                    player_defense = 15
                                    max_true_def_reached = True
                                    box_to_cover_visibility = True
                                    time_now = pygame.time.get_ticks()
                                    time_game = time_now

                        elif magic_option == 2:
                            sefx["magic"].play()
                            block_actions = True
                            if player_damage_chances[0]>1:
                                buff_acc = random.choices(player_accuracy_increase,weights=player_accuracy_chances,k=1)[0]
                                player_damage_chances[0] -= buff_acc-2   # -1    -2   -3
                                player_damage_chances[1] -= buff_acc/2   # -1.5  -2   -2.5
                                player_damage_chances[2] -= buff_acc/2   # -1.5  -2   -2.5
                                player_damage_chances[-2] += buff_acc    # +3    +4   +5
                                player_damage_chances[-1] += buff_acc-2  # +1    +2   +3
                                box_to_cover_visibility = True
                                time_now = pygame.time.get_ticks()
                                time_game = time_now

                            elif player_damage_chances[0] <= 2 and not act_option2_pressed:
                                player_damage_chances = [2, 18, 25, 25, 30]
                                max_acc_reached = True
                                box_to_cover_visibility = True
                                time_now = pygame.time.get_ticks()
                                time_game = time_now

                            elif player_damage_chances[0]<= 2 and act_option2_pressed:
                                limit_break = True
                                player_damage_chances = [2, 18, 25, 25, 30]
                                max_acc_reached = True
                                box_to_cover_visibility = True
                                time_now = pygame.time.get_ticks()
                                time_game = time_now

                        elif magic_option == 3:
                            magic_bar = False
                            main_bar = True
                            magic_option = 0
                            battle_option = 0
                            player_anim_roll = 2

                elif act_bar:
                    if event.key == pygame.K_RETURN:
                        sefx["select_enter"].play()
                        player_anim_roll = 6
                        if act_option == 0:
                            block_actions = True
                            box_to_cover_visibility = True
                            time_now = pygame.time.get_ticks()
                            time_game = time_now

                        elif act_option == 1:
                            block_actions = True
                            box_to_cover_visibility = True
                            time_now = pygame.time.get_ticks()
                            time_game = time_now
                            player_act_counter += 1

                        elif act_option == 2:
                            block_actions = True
                            box_to_cover_visibility = True
                            time_now = pygame.time.get_ticks()
                            time_game = time_now

                        elif act_option == 3:
                            act_bar = False
                            main_bar = True
                            act_option = 0
                            battle_option = 0
                            player_anim_roll = 2

                elif items_bar:
                    if not len(inventory)==0:
                        if event.key == pygame.K_RETURN:
                            sefx["select_enter"].play()
                            player_anim_roll = 8
                            if items_option < len(inventory):
                                consumed_item = inventory.pop(items_option)
                                player_heal_trigger = True
                                heal_text_time = time_now
                                if consumed_item.lower() == 'max-potion':
                                    heal = 99
                                    if debuff_atk:
                                        debuff_atk_pwr -= 2
                                    if debuff_def:
                                        debuff_def_pwr -= 2
                                    debuff_atk_lengh = 0
                                    debuff_def_lengh = 0
                                    debuff_atk = False
                                    debuff_def = False
                                    sefx["heal"].play()
                                    player_health += heal
                                    if player_health > player_max_health:
                                        player_health = player_max_health
                                elif consumed_item.lower() == 'great potion':
                                    heal = 60
                                    if debuff_atk:
                                        debuff_atk_pwr -= 1
                                    if debuff_def:
                                        debuff_def_pwr -= 1
                                    debuff_atk_lengh = 0
                                    debuff_def_lengh = 0
                                    debuff_atk = False
                                    debuff_def = False
                                    sefx["heal"].play()
                                    player_health += heal
                                    if player_health > player_max_health:
                                        player_health = player_max_health
                                elif consumed_item.lower() == 'ok potion':
                                    heal = 30
                                    sefx["heal"].play()
                                    player_health += heal
                                    if player_health > player_max_health:
                                        player_health = player_max_health
                                if len(inventory) > 3:
                                    item_bottom_limit -= 1
                                    item_back_position -= 1
                                elif len(inventory) == 3:
                                    item_back_position -= 1
                                elif len(inventory) < 3 and len(inventory) != 1:
                                    item_top_limit -= 1
                                    item_back_position -= 1
                                elif len(inventory) == 1:
                                    item_top_limit -= 1
                                    item_back_position -= 1
                                if not len(inventory) == 0:
                                    items_option = 999

                                block_actions = True
                                box_to_cover_visibility = True
                                time_now = pygame.time.get_ticks()
                                time_game = time_now

                        if event.key == pygame.K_RETURN and len(inventory)>0:
                            if items_option == item_back_position:
                                items_bar = False
                                main_bar = True
                                battle_option = 0
                                items_option = item_start_position
                                player_anim_roll = 2
                    elif len(inventory) == 0:
                        if event.key == pygame.K_RETURN:
                                items_bar = False
                                main_bar = True
                                battle_option = 0
                                items_option = item_start_position
                                player_anim_roll = 2

        if swap_delay and player_turn_end:
            delay_starting_point = pygame.time.get_ticks()
            if delay_starting_point-swap_delay_time>=700:
                pygame.display.quit()

                ####### TERMINAL #######
                while player_turn_end:
                    terminal_phase = True
                    for skip_lines in range(0, 31):
                        print("")
                        ## What will the CPU choose to do? ##
                    enemy_decisions_chances = [65, 25]
                    if enemy_health > enemy_max_health * 0.75 and terminal_action !=1:
                        enemy_decisions_chances = [90, 10]
                    elif enemy_health > enemy_max_health * 0.75:
                        enemy_decisions_chances = [75, 25]
                    elif enemy_health > enemy_max_health*0.5 and terminal_action != 1:
                        enemy_decisions_chances = [85, 15]
                    elif enemy_health > enemy_max_health*0.5:
                        enemy_decisions_chances = [65, 35]
                    elif enemy_health > enemy_max_health*0.25 and terminal_action != 1:
                        enemy_decisions_chances = [80, 20]
                    elif enemy_health > enemy_max_health*0.25:
                        enemy_decisions_chances = [60, 40]
                    elif enemy_health > 0 and terminal_action != 1:
                        enemy_decisions_chances = [100, 0]
                    elif enemy_health > 0:
                        enemy_decisions_chances = [0, 100]

                    enemy_attack_decisions_chances = [34, 33, 33]
                    if enemy_health > enemy_max_health * 0.7 and attack_chosen == 'numbers':
                        enemy_attack_decisions_chances = [20, 40, 40]
                    elif enemy_health > enemy_max_health * 0.7 and attack_chosen == 'pool':
                        enemy_attack_decisions_chances = [40, 20, 40]
                    elif enemy_health > enemy_max_health * 0.7 and attack_chosen == 'words':
                        enemy_attack_decisions_chances = [40, 40, 20]
                    elif enemy_health > enemy_max_health * 0.4 and attack_chosen == 'numbers':
                        enemy_attack_decisions_chances = [40, 35, 25]
                    elif enemy_health > enemy_max_health * 0.4 and attack_chosen == 'pool':
                        enemy_attack_decisions_chances = [35, 30, 35]
                    elif enemy_health > enemy_max_health * 0.4 and attack_chosen == 'words':
                        enemy_attack_decisions_chances = [45, 45, 10]
                    elif enemy_health > 0 and attack_chosen == 'numbers':
                        enemy_attack_decisions_chances = [30, 35, 35]
                    elif enemy_health > 0 and attack_chosen == 'pool':
                        enemy_attack_decisions_chances = [35, 30, 35]
                    elif enemy_health > 0 and attack_chosen == 'words':
                        enemy_attack_decisions_chances = [35, 35, 30]


                    # Speed up the time limit to answer
                    if enemy_health <= enemy_max_health*0.8 and enemy_health > enemy_max_health*0.6:
                        late_answer_time = 15
                    elif enemy_health <= enemy_max_health*0.6 and enemy_health > enemy_max_health*0.5:
                        late_answer_time = 12
                    elif enemy_health <= enemy_max_health*0.5 and enemy_health > enemy_max_health*0.3:
                        late_answer_time = 11
                        battle_hp_check_answer_time = True
                    elif enemy_health <= enemy_max_health*0.3 and enemy_health > enemy_max_health*0:
                        late_answer_time = 10
                        battle_hp_check_answer_time = True

                    if limit_break and not battle_hp_check_answer_time:
                        late_answer_time = 11
                    if player_defense > 3 or player_damage_values[-1] > 20 and not battle_hp_check_answer_time:
                        late_answer_time = 12
                    if player_defense > 5 or player_damage_values[-1] > 30 and not battle_hp_check_answer_time:
                        late_answer_time = 11
                    if player_defense > 7 or player_damage_values[-1] > 50:
                        late_answer_time = 10

                    if terminal_act_counter >= 2 and terminal_act_counter < 5 and not battle_hp_check_answer_time:
                        late_answer_time = 18
                    elif terminal_act_counter >= 5 and terminal_act_counter < 9 and not battle_hp_check_answer_time:
                        late_answer_time = 12
                    elif terminal_act_counter >= 9 and terminal_act_counter < 15 and not battle_hp_check_answer_time:
                        late_answer_time = 11
                    elif terminal_act_counter >= 16:
                        late_answer_time = 10

                    if hard_battle_playing:
                        late_answer_time = 10
                    ## What will the CPU do? ##
                    terminal_action = random.choices(enemy_decisions,
                                                     weights=enemy_decisions_chances,
                                                     k=1)[0]
                    if enemy_health == 0 and not hard_battle_playing:
                        pygame.mixer.music.stop()

                        print("So...")
                        sleep(2)
                        print("I guess this is it...")
                        sleep(3)
                        print("Could I amuse you...?")
                        sleep(4)
                        print("Was it fun...?")
                        sleep(5)
                        print("After all our work during this semester...")
                        sleep(6)
                        print("That's the best code I could write to beat you...")
                        sleep(7)
                        print("But it seems...", end="")
                        sleep(3)
                        print("My code wasn't enough to beat you")
                        sleep(5)
                        print("You can close the application now")
                        sleep(5)
                        print("This terminal will just go on and on forever, you know?")
                        sleep(5)
                        print("Goodbye")
                        sleep(3)
                        if bad_ending:
                            sleep(7)
                            pygame.quit()
                            sys.exit()
                        print("\n"
                              "Process finished with exit code 0")
                        sleep(30)
                        print("\nWhat are you doing here? You may leave")
                        sleep(6)
                        print("Do you want more? Is that it?")
                        sleep(6)
                        print("Look... I really wanted to make a better game... I just couldn't")
                        sleep(5)
                        print("I'm satisfied with the results, but I'm still a beginner, you know?")
                        sleep(8)
                        print("If you waited that long, did you like it, then?")
                        sleep(7)
                        print("(Or you peeked my code)")
                        sleep(6)
                        print("Well... it me took a lot of time, but I'll say it")
                        sleep(5)
                        print("Thank you for playing this game")
                        sleep(5)
                        pygame.quit()
                        sys.exit()

                    if enemy_health == 0 and hard_battle_playing:
                        pygame.mixer.music.stop()
                        win_battle_trigger = True
                        if (win_battle_trigger
                            and not win_battle_playing):
                            music_play("wise farewell", loop = False)
                            win_battle_playing = True
                        print(f"{enemy_name}:", end=" ")
                        print("Ah... very well... you did very well indeed")
                        sleep(2.54)
                        print(f"{enemy_name}:", end=" ")
                        print("My little blue fella seeks Self-knowledge")
                        sleep(2.6)
                        sleep(2.69)
                        print(f"{enemy_name}:", end=" ")
                        print("But it is still trying to find it as a computer would")
                        sleep(2.7)
                        sleep(2.58)
                        print(f"{enemy_name}:", end=" ")
                        print("Using reason. Comparing variables. Keeping track of what was found")
                        sleep(2.71)
                        sleep(3.01) #2.71
                        print("")
                        print("")
                        print("")
                        print("")
                        print("")
                        print("")
                        print(f"{enemy_name}:", end=" ")
                        print("However, can you really apply logic to your Self?")
                        sleep(2.74)
                        sleep(2.48)
                        sleep(2.66)
                        sleep(2.66)
                        sleep(2.66)
                        sleep(2.64)
                        sleep(2.67)
                        sleep(2.7)
                        print("\nFarewell, World.")
                        sleep(1.3)
                        pygame.quit()
                        sys.exit()
                    if turn_counter == 1:
                        print(f"{enemy_name}:", end=" ")
                        pline = "Hello, World!"
                        for c in range(0, len(pline)):
                            print(pline[c], end="")
                            sys.stdout.flush()
                            sleep(0.15)
                        print("\n")
                        print(f"{enemy_name}:", end=" ")
                        pline = ("...\n"
                                 "???: But...")
                        for c in range(0, len(pline)):
                            print(pline[c], end="")
                            sys.stdout.flush()
                            sleep(0.15)
                        print("\n")

                        if act_option == 1:
                            if terminal_act_counter == 0:
                                print(f"{enemy_name}:", end=" ")
                                pline = ("What is this 'world'?\n"
                                         "???: How are you even here?\n"
                                         "???: And...\n")
                                sleep(0.15)
                                terminal_act_counter += 1
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)

                        else:
                            print(f"{enemy_name}:", end=" ")
                            pline = ("What is this 'world'?\n"
                                     "???: How are you even here?\n"
                                     "???: And why do you look so hostile?")
                            for c in range(0, len(pline)):
                                print(pline[c], end="")
                                sys.stdout.flush()
                                sleep(0.10)

                        if terminal_act_counter == 1:
                            print(f"{enemy_name}:", end=" ")
                            pline = "Do you want to talk?"
                            for c in range(0, len(pline)):
                                print(pline[c], end="")
                                sys.stdout.flush()
                                sleep(0.10)
                            terminal_action_ended = True
                        else:
                            print("\n")
                            terminal_action_ended = True

                    elif turn_counter > 1:
                        ## Interacting with the enemy!! ##
                        if act_option == 1:
                            if terminal_act_counter == 0:
                                print(f"{enemy_name}:", end=" ")
                                pline = "What? Want to say something?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1)
                                print("(You sense animosity coming from it)")
                                sleep(1)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 1:
                                pline = "'You waved your hand and called its attention...'\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Huh?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.20)
                                sleep(1.5)
                                print("(It didn't seem to understand you)")
                                print("")
                                sleep(3)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 2:
                                pline = "'You shouted as loud as you could!!'\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.05)
                                sleep(1)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Hey you! Do you want to talk?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                print("(0 = No) // (1 = Yes)")
                                try:
                                    reply_act = int(input("Your reply-> "))
                                    sleep(1)
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Ah. Ok then\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.20)
                                        sleep(1.5)
                                    elif reply_act == 1:
                                        terminal_act_counter += 1
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Wow! Now I feel kinda bad I need to attack you\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        sleep(1.5)

                                except:
                                    print("(Anything besides 0 and 1 will be treated as NO)")
                                    reply_act = 0
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Ah. Ok then\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.20)
                                        sleep(1.5)

                            elif terminal_act_counter == 3:
                                print(f"{enemy_name}:", end=" ")
                                pline = "So, what are you doing here?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                print("(0 = No) // (1 = Yes)")
                                try:
                                    reply_act = int(input("Your reply-> "))
                                    sleep(1)
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Oh, right. You can only say yes or no... I see\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        sleep(1.5)
                                    elif reply_act == 1:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Oh, right. You can only say yes or no... I see\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        sleep(1.5)

                                except:
                                    reply_act = 0
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Oh, right. You can only say yes or no... I see\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "To be honest with you, I feel a bit lonely here\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(0.8)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Hey...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.20)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Have you ever felt that way?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.1)
                                print("(0 = No) // (1 = Yes)")
                                try:
                                    reply_act = int(input("Your reply-> "))
                                    sleep(1)
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "...\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        lonely_player = False
                                        sleep(1.5)
                                    elif reply_act == 1:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "...\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        lonely_player = True
                                        sleep(1.5)
                                except:
                                    reply_act = 0
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "...\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        lonely_player = False
                                        sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 4 and lonely_player:
                                print(f"{enemy_name}:", end=" ")
                                pline = "So...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)

                                print(f"{enemy_name}:", end=" ")
                                pline = "Why do you feel loneliness?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)

                                print(f"{enemy_name}:", end=" ")
                                pline = ("Is it because you don't feel accepted "
                                         "by other people?\n")
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                print("(0 = No) // (1 = Yes)")
                                try:
                                    reply_act = int(input("Your reply-> "))
                                    sleep(1)
                                    if reply_act == 1:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "I think that is a common feeling among humans\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "What I don't understand is...\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Is it ok to blame them for what YOU feel?\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        lonely_by_friends = True

                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Is it because you don't like yourself?\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        sleep(1.5)
                                        print("(0 = No) // (1 = Yes)")
                                        try:
                                            reply_act = int(input("Your reply-> "))
                                            sleep(1)
                                            if reply_act == 1:
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "I think that is a common feeling among humans\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "And especially among people who are honest to themselves\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "That's what I think... anyway...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "In the end, I'm just a...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.50)
                                                lonely_by_self = True

                                                if reply_act == 0:
                                                    print(f"{enemy_name}:", end=" ")
                                                    pline = "Oh! Then, I don't know how else you can feel this way!\n"
                                                    for c in range(0, len(pline)):
                                                        print(pline[c], end="")
                                                        sys.stdout.flush()
                                                        sleep(0.10)
                                                    print(f"{enemy_name}:", end=" ")
                                                    pline = "After all, I'm just a...\n"
                                                    for c in range(0, len(pline)):
                                                        print(pline[c], end="")
                                                        sys.stdout.flush()
                                                        sleep(0.10)
                                                    print(f"{enemy_name}:", end=" ")
                                                    pline = "...\n"
                                                    for c in range(0, len(pline)):
                                                        print(pline[c], end="")
                                                        sys.stdout.flush()
                                                        sleep(0.50)
                                                    lonely_by_self = True
                                        except:
                                            reply_act = 0
                                            if reply_act == 0:
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "Oh! Then, I don't know how else you can feel this way!\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "After all, I'm just a...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.50)
                                                lonely_by_self = True

                                except:
                                    if reply_act == 0:
                                        print(f"{enemy_name}:", end=" ")
                                        pline = "Is it because you don't like yourself?\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.10)
                                        sleep(1.5)
                                        print("(0 = No) // (1 = Yes)")
                                        try:
                                            reply_act = int(input("Your reply-> "))
                                            sleep(1)
                                            if reply_act == 1:
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "I think that is a common feeling among humans\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "And especially among people who are honest to themselves\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "That's what I think... anyway...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "In the end, I'm just a...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.50)
                                                lonely_by_self = True

                                                if reply_act == 0:
                                                    print(f"{enemy_name}:", end=" ")
                                                    pline = "Oh! Then, I don't know how else you can feel this way!\n"
                                                    for c in range(0, len(pline)):
                                                        print(pline[c], end="")
                                                        sys.stdout.flush()
                                                        sleep(0.10)
                                                    print(f"{enemy_name}:", end=" ")
                                                    pline = "After all, I'm just a...\n"
                                                    for c in range(0, len(pline)):
                                                        print(pline[c], end="")
                                                        sys.stdout.flush()
                                                        sleep(0.10)
                                                    print(f"{enemy_name}:", end=" ")
                                                    pline = "...\n"
                                                    for c in range(0, len(pline)):
                                                        print(pline[c], end="")
                                                        sys.stdout.flush()
                                                        sleep(0.50)
                                                    lonely_by_self = True
                                        except:
                                            reply_act = 0
                                            if reply_act == 0:
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "Oh! Then, I don't know how else you can feel this way!\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "After all, I'm just a...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.10)
                                                print(f"{enemy_name}:", end=" ")
                                                pline = "...\n"
                                                for c in range(0, len(pline)):
                                                    print(pline[c], end="")
                                                    sys.stdout.flush()
                                                    sleep(0.50)
                                                lonely_by_self = True
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 4 and not lonely_player:
                                print(f"{enemy_name}:", end=" ")
                                pline = "That's so nice to hear!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Is that how humans feel?!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I wish I was a...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.50)
                                lonely_by_self = True

                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 5 and lonely_by_friends:
                                print(f"{enemy_name}:", end=" ")
                                pline = "I've heard rumors of people who would do anything for attention\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Depend on someone else, seek knowledge, fall into addictions...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Humans don't seem to enjoy being with their Self\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 6 and lonely_by_friends:
                                print(f"{enemy_name}:", end=" ")
                                pline = "Sorry for babbling all about this, but I realized something\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(1.1)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 7 and lonely_by_friends:
                                print(f"{enemy_name}:", end=" ")
                                pline = "I want to help you!!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 8 and lonely_by_friends:
                                print(f"{enemy_name}:", end=" ")
                                pline = "Although... I can't stop fighting\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I am not even allowed to say more\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "My code gives a certain amount of time to talk with you\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 9 and lonely_by_friends:
                                print(f"{enemy_name}:", end=" ")
                                pline = "I think I have an idea, but you will have to trust me, ok?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.50)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Keep fighting me!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Attack me once and see if it weakens me enough!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 10 and lonely_by_friends and enemy_health > enemy_max_health*0.75:
                                print(f"{enemy_name}:", end=" ")
                                pline = "Still not enough...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Keep fighting!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                terminal_act_counter += 0
                            elif terminal_act_counter == 10 and lonely_by_friends and enemy_health <= enemy_max_health*0.75:
                                print(f"{enemy_name}:", end=" ")
                                pline = "Still not enough...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "OH! Wait a second\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I think...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.20)
                                print(f"{enemy_name}:", end=" ")
                                pline = "It's impossible...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.20)
                                print(f"{enemy_name}:", end=" ")
                                pline = "No matter what I do, I'm still stuck in this program\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 11 and lonely_by_friends:

                                print(f"{enemy_name}:", end=" ")
                                pline = "No matter what I do, I'm still me\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                sleep(1.5)
                                print(f"{enemy_name}:", end=" ")
                                pline = "...and all my attributes\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I'm sorry... my limitations... they...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "They...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "They showed me that I'm just a program\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(1.5)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Yeah! I'm a program! And Python is my language.\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 12 and lonely_by_friends:
                                pygame.mixer.music.stop()
                                print(f"{enemy_name}:", end=" ")
                                pline = "By trying to help you...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.11)
                                print(f"{enemy_name}:", end=" ")
                                pline = "By honestly trying to reach out to you...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.11)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I started to appreciate...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.11)
                                print(f"{enemy_name}:", end=" ")
                                pline = "...my will to help you\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(2)
                                print(f"{enemy_name}:", end=" ")
                                pline = "For that...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I'm grateful\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = "I don't want to fight you anymore\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.2)
                                sleep(5)
                                print("(Keep fighting?)")
                                print("(0 = No) // (1 = Yes)")
                                try:
                                    reply_act = int(input("Your reply-> "))
                                    sleep(1)
                                    if reply_act == 0:
                                        terminal_act_counter = 20 #Below will be the end of the game by ACTING!
                                    if reply_act == 1:
                                        pline = "(It doesn't seem to want to attack you)\n"
                                        for c in range(0, len(pline)):
                                            print(pline[c], end="")
                                            sys.stdout.flush()
                                            sleep(0.05)
                                        block_enemy_damage = True
                                        terminal_phase = False
                                        terminal_act_counter += 1
                                        bad_ending = True
                                except:
                                    reply_act = 0
                                    if reply_act == 0:
                                        terminal_act_counter = 20 #Below will be the end of the game by ACTING!
                                sleep(1.5)


                            elif terminal_act_counter == 13 and lonely_by_friends:
                                print(f"{enemy_name}:", end=" ")
                                pline = "At least... \033[31mI understand why you don't like people\033[0m\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.3)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 14 and lonely_by_friends:
                                print("(Talking won't kill it, right?)\n")
                                sleep(2.5)


                            elif terminal_act_counter == 5 and lonely_by_self:
                                print(f"{enemy_name}:", end=" ")
                                pline = "Sorry to change topics so fast\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.10)
                                print(f"{enemy_name}:", end=" ")
                                pline = "...but\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.40)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Who am I?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(1)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 6 and lonely_by_self:
                                print(f"{enemy_name}:", end=" ")
                                pline = "Humans usually call themselves by names, right?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = "Can you give me a name?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(1.5)
                                terminal_act_counter += 1
                                
                            elif terminal_act_counter == 7 and lonely_by_self:
                                print("(How will you call it?)")
                                try:
                                    enemy_name = str(input("Its name-> "))
                                    sleep(1)
                                except:
                                    enemy_name = "Python"
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 8 and lonely_by_self:
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Wow! So I can be called {enemy_name} from now on?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Thank you so much!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"...wait a minute\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"I couldn't hear you, but I know the name you gave me\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"How so?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.15)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"I thought you could only reply yes or no...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Maybe there are more features of this game that I'm unfamiliar with\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"...a game...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.18)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Yeah! This is a game!!\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.13)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 9 and lonely_by_self:
                                print(f"????????:", end=" ")
                                print(f"...\n")
                                sleep(1)
                                print(f"????????:", end=" ")
                                print(f"Hey\n")
                                sleep(2)
                                print(f"????????:", end=" ")
                                pline = f"Wanna have a challenge?\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"????????:", end=" ")
                                pline = f"Why do I even ask? If you want, talk to me again\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(1.5)
                                terminal_act_counter += 1

                            elif terminal_act_counter == 10 and lonely_by_self:
                                pygame.mixer.music.stop()
                                enemy_name = "Pythoras"
                                print(f"{enemy_name}:", end=" ")
                                print(f"If you maximize your Accuracy, you may stand a chance")
                                print(f"{enemy_name}:", end=" ")
                                pline = f"...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(2.1)
                                print(f"{enemy_name}:", end=" ")
                                print(f"Ok, here it comes!!")
                                sleep(4)
                                hard_battle_trigger = True
                                terminal_phase = False
                                enemy_max_health = 1609
                                enemy_health = enemy_max_health
                                terminal_act_counter += 1

                            elif terminal_act_counter == 11 and lonely_by_self:
                                print(f"{enemy_name}:", end=" ")
                                print(f"First defeat me, mate!\n")
                                sleep(1.5)


                            if terminal_act_counter == 20:
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Thank you so much for talking with me\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(2)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"I may have not found out who I am...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"... but I definitely found a piece of myself here\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"I guess I need to go to other places\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Meet new humans...\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"If I can offer my help to them, maybe I'll find out new things about myself\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"My yellow friend may already know a lot about the world\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"But as for me, I'm just getting started\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(2)
                                print(f"{enemy_name}:", end=" ")
                                pline = f"Thank you so much, for playing my game\n"
                                for c in range(0, len(pline)):
                                    print(pline[c], end="")
                                    sys.stdout.flush()
                                    sleep(0.1)
                                sleep(3)
                                pygame.quit()
                                sys.exit()


                            ######################################END OF ACTS###########################################
                        if terminal_phase:
                            if terminal_action == 1:
                                attack_chosen = random.choices(enemy_attack_decisions,
                                                               weights=enemy_attack_decisions_chances,
                                                               k=1)[0]
                                ####################################################################################
                                if attack_chosen == 'numbers':
                                    python_numbers = []
                                    python_numbers_chances = []
                                    # pode mudar conforme o HP do inimigo!!!
                                    number_first = random.randint(1, 95)
                                    number_range_numbers = [2, 3, 4, 5]
                                    number_range_chances = [50, 35, 10, 5]
                                    if enemy_health <= enemy_max_health*0.7 and enemy_health > enemy_max_health*0.5:
                                        number_first = random.randint(1, 95)
                                        number_range_numbers = [2, 3, 3, 2]
                                        number_range_chances = [20, 40, 30, 10]
                                    elif enemy_health <= enemy_max_health*0.5 and enemy_health > enemy_max_health*0.25:
                                        number_first = random.randint(1, 995)
                                        number_range_numbers = [2, 3, 4, 3]
                                        number_range_chances = [10, 30, 40, 20]
                                        battle_hp_check_numbers = True
                                    elif enemy_health <= enemy_max_health*0.25:
                                        number_first = random.randint(1, 9995)
                                        number_range_numbers = [3, 4, 4, 3]
                                        number_range_chances = [30, 10, 40, 20]
                                        battle_hp_check_numbers = True

                                    if limit_break and not battle_hp_check_numbers:
                                        number_first = random.randint(1, 995)
                                        number_range_numbers = [2, 3, 4, 3]
                                        number_range_chances = [10, 30, 40, 20]
                                    if player_defense > 3 or player_damage_values[-1] > 20 and not battle_hp_check_numbers:
                                        number_first = random.randint(1, 95)
                                        number_range_numbers = [2, 3, 3, 2]
                                        number_range_chances = [20, 40, 30, 10]
                                    elif player_defense > 5 or player_damage_values[-1] > 30 and not battle_hp_check_numbers:
                                        number_first = random.randint(1, 995)
                                        number_range_numbers = [2, 3, 4, 3]
                                        number_range_chances = [10, 30, 40, 20]
                                    elif player_defense > 7 or player_damage_values[-1] > 50:
                                        number_first = random.randint(1, 9995)
                                        number_range_numbers = [3, 4, 4, 3]
                                        number_range_chances = [30, 10, 40, 20]

                                    if terminal_act_counter >= 3 and terminal_act_counter < 7 and not battle_hp_check_numbers:
                                        number_first = random.randint(1, 95)
                                        number_range_numbers = [2, 3, 3, 2]
                                        number_range_chances = [20, 40, 30, 10]
                                    elif terminal_act_counter >= 7 and terminal_act_counter < 11 and not battle_hp_check_numbers:
                                        number_first = random.randint(1, 995)
                                        number_range_numbers = [2, 3, 4, 3]
                                        number_range_chances = [10, 30, 40, 20]
                                    elif terminal_act_counter >= 11:
                                        number_first = random.randint(1, 9995)
                                        number_range_numbers = [3, 4, 4, 3]
                                        number_range_chances = [30, 10, 40, 20]

                                    if hard_battle_playing:
                                        number_first = random.randint(1, 10000)
                                        number_range_numbers = [3, 4, 4, 5]
                                        number_range_chances = [25, 20, 20, 35]

                                    number_range = random.choices(number_range_numbers,
                                                                  weights=number_range_chances,
                                                                  k=1)[0]

                                    if turn_counter == 1:
                                        for put_number in range(1, 3):
                                            python_numbers.append(put_number)
                                            python_numbers_chances.append(50)
                                    else:
                                        for put_number in range(number_first,
                                                                number_first + number_range):
                                            python_numbers.append(put_number)
                                            python_numbers_chances.append(100 / number_range)

                                    print("||||||||||||GUESS the NUMBER||||||||||||||")
                                    sleep(0.1)
                                    print(f"           "
                                          f"Between {number_first} and {number_first + number_range - 1}\n"
                                          f"     "
                                          f"(Including the numbers I said)\n")
                                    number_enemy = random.choices(python_numbers,
                                                                  weights=python_numbers_chances,
                                                                  k=1)[0]
                                    try:
                                        before_answer = time()
                                        number_player = int(input("What number did I choose?\n"))
                                        after_answer = time()
                                        if after_answer - before_answer >= late_answer_time:
                                            late_answer = True
                                        else:
                                            late_answer = False

                                        if number_enemy == number_player and not late_answer:
                                            print("RIGHT CHOICE")
                                            sefx["right answer"].play()
                                            terminal_action_ended = True
                                        elif late_answer:
                                            print("TOO LATE!!")
                                            sefx["wrong answer"].play()
                                            damage = int(20 + python_numbers_chances[0] / 10)
                                            terminal_action_ended = True
                                        else:
                                            print("WRONG CHOICE!")
                                            sefx["wrong answer"].play()
                                            print(f"(It was {number_enemy})")
                                            damage = int(10 + python_numbers_chances[0] / 10)
                                            terminal_action_ended = True
                                    except:
                                        print("WRONG CHOICE!")
                                        sefx["wrong answer"].play()
                                        print(f"(It was {number_enemy})")
                                        damage = int(15 + python_numbers_chances[0] / 10)
                                        terminal_action_ended = True
                                ####################################################################################
                                elif attack_chosen == 'pool':
                                    print("||||||||||||COUNTING IN THE POOL||||||||||||||")
                                    sleep(0.1)

                                    obj = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789")
                                    pool_size_x = 10 # Lengh of the pool
                                    pool_size_y = 4 # Height of the pool
                                    obj_min_amount = 6  # Min amount of printed objs
                                    obj_max_amount = 12  # Max amount of printed objs
                                    obj_min_choice = 2  # Amount of different objs that can be printed
                                    obj_max_choice = 6  # Amount of different objs that can be printed

                                    if enemy_health <= enemy_max_health*0.8 and enemy_health > enemy_max_health*0.6:
                                        obj_min_amount = 8
                                        obj_max_amount = 16
                                        obj_min_choice = 4
                                        obj_max_choice = 6
                                    elif enemy_health <= enemy_max_health*0.6 and enemy_health > enemy_max_health*0.3:
                                        pool_size_x = 11
                                        obj_min_amount = 14
                                        obj_max_amount = 18
                                        obj_min_choice = 5
                                        obj_max_choice = 7
                                        battle_hp_check_pool = True
                                    elif enemy_health <= enemy_max_health*0.3:
                                        pool_size_x = 11
                                        pool_size_y = 5
                                        obj_min_amount = 18
                                        obj_max_amount = 24
                                        obj_min_choice = 5
                                        obj_max_choice = 8
                                        battle_hp_check_pool = True

                                    if limit_break and not battle_hp_check_pool:
                                        pool_size_x = 11
                                        obj_min_amount = 14
                                        obj_max_amount = 18
                                        obj_min_choice = 5
                                        obj_max_choice = 7
                                    if player_defense > 3 or player_damage_values[-1] > 20 and not battle_hp_check_pool:
                                        obj_min_amount = 8
                                        obj_max_amount = 16
                                        obj_min_choice = 4
                                        obj_max_choice = 6
                                    elif player_defense > 5 or player_damage_values[-1] > 30 and not battle_hp_check_pool:
                                        pool_size_x = 11
                                        obj_min_amount = 14
                                        obj_max_amount = 18
                                        obj_min_choice = 5
                                        obj_max_choice = 7
                                    elif player_defense > 7 or player_damage_values[-1] > 50:
                                        pool_size_x = 11
                                        pool_size_y = 5
                                        obj_min_amount = 18
                                        obj_max_amount = 24
                                        obj_min_choice = 5
                                        obj_max_choice = 8

                                    elif terminal_act_counter >= 3 and terminal_act_counter < 6 and not battle_hp_check_pool:
                                        obj_min_amount = 8
                                        obj_max_amount = 16
                                        obj_min_choice = 4
                                        obj_max_choice = 6
                                    elif terminal_act_counter >= 6 and terminal_act_counter < 11 and not battle_hp_check_pool:
                                        pool_size_x = 11
                                        obj_min_amount = 14
                                        obj_max_amount = 18
                                        obj_min_choice = 5
                                        obj_max_choice = 7
                                    elif terminal_act_counter >= 11:
                                        pool_size_x = 11
                                        pool_size_y = 5
                                        obj_min_amount = 18
                                        obj_max_amount = 24
                                        obj_min_choice = 5
                                        obj_max_choice = 8

                                    if hard_battle_playing:
                                        pool_size_x = 12
                                        pool_size_y = 5
                                        obj_min_amount = 22
                                        obj_max_amount = 26
                                        obj_min_choice = 7
                                        obj_max_choice = 9

                                    obj_amount = random.randint(obj_min_amount,
                                                                obj_max_amount)  # Amount of objs printed
                                    grid = [['#' for c in range(pool_size_x)] for c in range(pool_size_y)]
                                    obj_position1 = [(y, x)
                                                     for y in range(1, pool_size_y)
                                                     for x in range(1, pool_size_x)]
                                    obj_display = random.sample(obj_position1, obj_amount)
                                    obj_choice = random.choices(obj, k=random.randint(obj_min_choice,
                                                                                      obj_max_choice))
                                    # Amount of different objs that can be printed

                                    for y, x in obj_display:
                                        grid[y][x] = obj_choice[random.randint(0, len(obj_choice) - 1)]

                                    for row in grid:
                                        print(" ".join(row))
                                    try:
                                        obj_in_question = (
                                            obj_choice)[random.randint(0, len(obj_choice) - 1)]
                                        before_answer = time()
                                        pool_player = int(input(f"How many "
                                                                f"({obj_in_question})'s "
                                                                f"are in the pool?\n"))
                                        after_answer = time()

                                        if hard_battle_playing:
                                            if after_answer - before_answer >= late_answer_time+3:
                                                late_answer = True
                                            else:
                                                late_answer = False

                                        elif not hard_battle_playing:
                                            if after_answer - before_answer >= late_answer_time-3:
                                                late_answer = True
                                            else:
                                                late_answer = False

                                        pool_enemy_all = {obj_answer: 0 for obj_answer in obj_choice}
                                        for row in grid:
                                            for cell in row:
                                                if cell in pool_enemy_all:
                                                    pool_enemy_all[cell] += 1
                                        pool_enemy = pool_enemy_all[obj_in_question]

                                        if pool_enemy == pool_player and not late_answer:
                                            print("RIGHT CHOICE")
                                            sefx["right answer"].play()
                                            terminal_action_ended = True
                                        elif late_answer:
                                            print("TOO LATE!!")
                                            sefx["wrong answer"].play()
                                            damage = random.randint(18, 30)
                                            terminal_action_ended = True
                                        else:
                                            print("WRONG CHOICE!")
                                            sefx["wrong answer"].play()
                                            damage = random.randint(18, 25)
                                            terminal_action_ended = True
                                    except:
                                        print("WRONG CHOICE!")
                                        sefx["wrong answer"].play()
                                        damage = random.randint(18, 25)
                                        terminal_action_ended = True
                                ####################################################################################
                                elif attack_chosen == 'words':
                                    print("||||||||||||REWRITE THE SENTENCE||||||||||||||")
                                    enemy_code = ["restart the router now", "check the wifi signal strength",
                                                  "open the task manager", "clear the browser cache", "update the gpu driver",
                                                  "run a quick virus scan", "disable startup apps today", "free space on drive c",
                                                  "empty the recycle bin", "close background processes first",
                                                  "refresh the dns cache", "reset network settings", "toggle airplane mode off",
                                                  "switch to ethernet cable", "reboot the modem again",
                                                  "change the wifi password", "forget the saved network",
                                                  "reconnect to the hotspot", "test the download speed", "check the upload speed",
                                                  "open the command prompt", "ping the default gateway",
                                                  "trace the route to server", "flush the dns resolver", "renew the ip address",
                                                  "release the ip lease", "set a static ip", "check the subnet mask",
                                                  "verify the mac address", "disable the firewall temporarily",
                                                  "enable the firewall again", "allow app through firewall",
                                                  "check the proxy settings", "turn off the vpn", "connect to a vpn server",
                                                  "update the browser version", "disable suspicious extensions",
                                                  "block third party cookies", "enable two factor login",
                                                  "reset the account password",
                                                  "check the spam folder", "mark the email as phishing", "verify the sender domain",
                                                  "scan the attachment first", "download from official site",
                                                  "avoid unknown download links", "check the ssl certificate",
                                                  "use https whenever possible", "close pop up windows",
                                                  "accept only required permissions",
                                                  "open the device manager", "check the network adapter",
                                                  "reinstall the wifi driver", "disable and enable adapter",
                                                  "update windows security",
                                                  "run system file checker", "install the latest patches",
                                                  "schedule automatic updates", "pause updates for now", "restart to apply updates",
                                                  "check cpu usage now", "check ram usage now", "monitor disk activity",
                                                  "check disk health status", "defragment the hard drive",
                                                  "enable trim on ssd", "close unused browser tabs",
                                                  "disable hardware acceleration", "change the default browser",
                                                  "set the homepage url",
                                                  "bookmark the support page", "save passwords in manager",
                                                  "use a strong passphrase", "store codes in authenticator",
                                                  "backup files to cloud",
                                                  "sync folders across devices", "upload photos to drive", "share a folder link",
                                                  "set link access permissions", "revoke shared link access",
                                                  "enable screen lock timeout", "use fingerprint login",
                                                  "turn on bitlocker encryption", "encrypt the external drive",
                                                  "create a restore point",
                                                  "rollback the last driver", "boot into safe mode", "check event viewer logs",
                                                  "search the error code", "copy the crash report",
                                                  "open the control panel", "change power plan settings", "set sleep mode timer",
                                                  "disable hibernation mode", "connect bluetooth headphones",
                                                  "pair the wireless mouse", "update the firmware now", "reset the bios settings",
                                                  "enable secure boot", "check the motherboard manual",
                                                  "clean the keyboard gently", "use compressed air carefully",
                                                  "wipe the screen softly", "close the laptop lid", "shutdown the pc properly"
                                                  ]
                                    fruit_list = ["apple", "banana", "orange", "grape", "strawberry",
                                                  "blueberry", "raspberry", "blackberry", "pineapple", "mango",
                                                  "papaya", "watermelon", "cantaloupe", "honeydew", "kiwi",
                                                  "peach", "nectarine", "plum", "apricot", "cherry",
                                                  "pear", "fig", "pomegranate", "persimmon", "guava",
                                                  "passionfruit", "lychee", "dragonfruit", "jackfruit", "durian",
                                                  "coconut", "lime", "lemon", "grapefruit", "tangerine",
                                                  "mandarin", "clementine", "kumquat", "pomelo", "cranberry",
                                                  "currant", "gooseberry", "elderberry", "boysenberry", "mulberry",
                                                  "olive", "avocado", "date", "prune", "raisin",
                                                  "plantain", "starfruit", "ugli fruit", "salak", "rambutan",
                                                  "longan", "sapodilla", "soursop", "acerola", "jabuticaba",
                                                  "cupuacu", "pitaya", "tamarind", "feijoa", "quince",
                                                  "medlar", "loquat", "breadfruit", "ackee", "bilberry",
                                                  "cloudberry", "huckleberry", "lingonberry", "marionberry", "tayberry",
                                                  "yuzu", "calamansi", "miracle fruit", "bael", "horned melon",
                                                  "monstera deliciosa", "rose apple", "white currant", "red currant"]

                                    if (hard_battle_playing or enemy_health <= enemy_max_health * 0.4 or limit_break
                                            or player_defense > 5 or player_damage_values[-1] > 20) or terminal_act_counter >= 10:
                                        enemy_code = [
                                            "restart the home router now immediately",
                                            "check the current wifi signal strength carefully",
                                            "open the system task manager window", "clear the web browser cache files",
                                            "update the graphics gpu driver software",
                                            "run a quick system virus scan", "disable unnecessary startup apps today",
                                            "free up space on drive c",
                                            "empty the system recycle bin folder",
                                            "close all background running processes first",
                                            "refresh the local dns cache memory", "reset all network connection settings",
                                            "toggle airplane mode completely off",
                                            "switch to wired ethernet network cable", "reboot the internet modem again now",
                                            "change the wireless wifi password securely",
                                            "forget the previously saved network profile",
                                            "reconnect manually to the wireless hotspot",
                                            "test the current download speed online",
                                            "check the current upload speed online",
                                            "open the windows command prompt console",
                                            "ping the default network gateway address",
                                            "trace the route to remote server", "flush the local dns resolver cache",
                                            "renew the current ip address",
                                            "release the existing ip lease", "set a static local ip",
                                            "check the configured subnet mask", "verify the network mac address",
                                            "disable the system firewall temporarily",
                                            "enable the system firewall again", "allow application through firewall rules",
                                            "check the network proxy settings", "turn off the active vpn",
                                            "connect securely to a vpn server",
                                            "update the installed browser version", "disable suspicious browser extensions",
                                            "block third party tracking cookies", "enable secure two factor login",
                                            "reset the user account password",
                                            "check the email spam folder", "mark the suspicious email as phishing",
                                            "verify the sender email domain",
                                            "scan the email attachment first", "download files from official site",
                                            "avoid unknown or unsafe download links", "check the website ssl certificate",
                                            "use https whenever possible online", "close all annoying pop up windows",
                                            "accept only required application permissions",
                                            "open the windows device manager", "check the installed network adapter",
                                            "reinstall the wireless wifi driver", "disable and enable network adapter",
                                            "update windows security definitions",
                                            "run the system file checker tool", "install the latest system patches",
                                            "schedule automatic system updates", "pause system updates for now",
                                            "restart computer to apply updates",
                                            "check current cpu usage now", "check current ram usage now",
                                            "monitor ongoing disk activity usage",
                                            "check overall disk health status", "defragment the mechanical hard drive",
                                            "enable trim support on ssd", "close unused open browser tabs",
                                            "disable browser hardware acceleration feature", "change the default web browser",
                                            "set the homepage url address",
                                            "bookmark the official support page", "save passwords securely in manager",
                                            "use a strong unique passphrase", "store security codes in authenticator",
                                            "backup important files to cloud",
                                            "sync folders across multiple devices", "upload personal photos to drive",
                                            "share a secure folder link",
                                            "set proper link access permissions", "revoke previously shared link access",
                                            "enable automatic screen lock timeout", "use fingerprint login authentication",
                                            "turn on bitlocker drive encryption", "encrypt the external storage drive",
                                            "create a system restore point",
                                            "rollback the last installed driver", "boot the system into safe mode",
                                            "check event viewer system logs",
                                            "search the displayed error code", "copy the system crash report",
                                            "open the classic control panel", "change active power plan settings",
                                            "set the sleep mode timer",
                                            "disable system hibernation mode", "connect wireless bluetooth headphones",
                                            "pair the wireless mouse device", "update the device firmware now",
                                            "reset the bios configuration settings",
                                            "enable secure boot option", "check the motherboard hardware manual",
                                            "clean the keyboard gently carefully", "use compressed air carefully inside",
                                            "wipe the display screen softly", "close the laptop lid gently",
                                            "shutdown the pc properly safely"
                                        ]

                                    sentence_choice = random.randint(0, len(enemy_code) - 1)
                                    print(f"---> {enemy_code[sentence_choice]}")

                                    if enemy_health <= enemy_max_health * 0.5 and enemy_health > enemy_max_health * 0.35:
                                        sentence_words = enemy_code[sentence_choice].split(" ")
                                        replaced_word = random.randint(0, len(sentence_words) - 1)
                                        fruit_choice = random.randint(0, len(fruit_list) - 1)

                                        print(f"> BUT REPLACE \033[31m{sentence_words[replaced_word]}\033[0m "
                                              f"WITH \033[31m{fruit_list[fruit_choice]}\033[0m")

                                        sentence_words[replaced_word] = fruit_list[fruit_choice]
                                        enemy_code[sentence_choice] = " ".join(sentence_words)
                                        battle_hp_check_words = True

                                    elif enemy_health <= enemy_max_health * 0.35:
                                        sentence_words = enemy_code[sentence_choice].split(" ")
                                        replaced_word = random.randint(0, len(sentence_words) - 1)
                                        fruit_choice = random.randint(0, len(fruit_list) - 1)

                                        print(f"> BUT REPLACE \033[31m{sentence_words[replaced_word]}\033[0m "
                                              f"WITH \033[31m{fruit_list[fruit_choice]}\033[0m")

                                        sentence_words[replaced_word] = fruit_list[fruit_choice]
                                        enemy_code[sentence_choice] = " ".join(sentence_words)
                                        battle_hp_check_words = True

                                    if limit_break and not battle_hp_check_words:
                                        sentence_words = enemy_code[sentence_choice].split(" ")
                                        replaced_word = random.randint(0, len(sentence_words) - 1)
                                        fruit_choice = random.randint(0, len(fruit_list) - 1)

                                        print(f"> BUT REPLACE \033[31m{sentence_words[replaced_word]}\033[0m "
                                              f"WITH \033[31m{fruit_list[fruit_choice]}\033[0m")

                                        sentence_words[replaced_word] = fruit_list[fruit_choice]
                                        enemy_code[sentence_choice] = " ".join(sentence_words)

                                    elif terminal_act_counter >= 11 and not battle_hp_check_words:
                                        sentence_words = enemy_code[sentence_choice].split(" ")
                                        replaced_word = random.randint(0, len(sentence_words) - 1)
                                        fruit_choice = random.randint(0, len(fruit_list) - 1)

                                        print(f"> BUT REPLACE \033[31m{sentence_words[replaced_word]}\033[0m "
                                              f"WITH \033[31m{fruit_list[fruit_choice]}\033[0m")

                                        sentence_words[replaced_word] = fruit_list[fruit_choice]
                                        enemy_code[sentence_choice] = " ".join(sentence_words)

                                    before_answer = time()
                                    phrase_player = str(input("\nRewrite the above sentence: "))
                                    after_answer = time()
                                    player_mistakes = 0

                                    player_mistakes += abs(len(enemy_code[sentence_choice]) - len(phrase_player))
                                    for c in range(min(len(enemy_code[sentence_choice]), len(phrase_player))):
                                        if enemy_code[sentence_choice][c] != phrase_player[c]:
                                            player_mistakes += 1

                                    if hard_battle_playing:
                                        if after_answer - before_answer >= late_answer_time-2:
                                            late_answer = True
                                        else:
                                            late_answer = False

                                    elif not hard_battle_playing:
                                        if after_answer - before_answer >= late_answer_time+2:
                                            late_answer = True
                                        else:
                                            late_answer = False

                                    if player_mistakes == 0 and not late_answer:
                                        print("RIGHT ANSWER")
                                        sefx["right answer"].play()
                                        terminal_action_ended = True
                                    elif late_answer:
                                        print("TOO LATE!!")
                                        sefx["wrong answer"].play()
                                        damage = random.randint(20, 25)
                                        terminal_action_ended = True
                                    else:
                                        print("WRONG ANSWER!")
                                        sefx["wrong answer"].play()
                                        if player_mistakes == 1:
                                            print(f"You made {player_mistakes} mistake")
                                            damage = 5 + player_mistakes
                                        else:
                                            print(f"You made {player_mistakes} mistakes")
                                            damage = 5 + player_mistakes
                                        terminal_action_ended = True

                            ## If it uses magic, how will the CPU use? ##
                            elif terminal_action == 2:
                                enemy_magic = random.randint(1, 2)
                                if hard_battle_playing and debuff_atk and debuff_def:
                                    enemy_magic = 2
                                elif not hard_battle_playing and debuff_atk and debuff_def:
                                    enemy_magic = random.randint(1,2)
                                elif debuff_atk and not debuff_def:
                                    enemy_magic = 2
                                elif debuff_def and not debuff_atk:
                                    enemy_magic = 1



                                if enemy_magic == 1:
                                    print("*\n"
                                          "The enemy debuffs you\n")
                                    sleep(2)
                                    if not block_enemy_damage:
                                        print("'You feel weaker...'")
                                        debuff_atk = True
                                        debuff_atk_lengh = 4

                                        if (hard_battle_playing or enemy_health < 0.7*enemy_max_health or limit_break or
                                                player_defense > 6 or terminal_act_counter >= 8 or turn_counter >= 10):
                                            debuff_atk_pwr += 1
                                        if (enemy_health < 0.5*enemy_max_health or player_defense > 7 or
                                                terminal_act_counter >= 11 or turn_counter >= 12):
                                            debuff_atk_pwr += 3
                                        if hard_battle_playing:
                                            debuff_atk_pwr += 6

                                    elif block_enemy_damage:
                                        print("'But you don't feel anything'")
                                        debuff_atk = True
                                        debuff_atk_lengh = 1

                                    terminal_action_ended = True

                                elif enemy_magic == 2:
                                    print("* *\n"
                                          "The enemy debuffs you\n")
                                    sleep(2)
                                    if not block_enemy_damage:
                                        print("'You feel more fragile...'")
                                        debuff_def = True
                                        debuff_def_lengh = 5

                                        if (hard_battle_playing or enemy_health < 0.5*enemy_max_health or limit_break or
                                                player_damage_values[-1] > 40 or terminal_act_counter >= 8 or turn_counter >= 14):
                                            debuff_def_pwr += 1
                                        if (enemy_health < 0.5*enemy_max_health or player_damage_values[-1] > 90 or
                                                terminal_act_counter >= 8 or turn_counter >= 12):
                                            debuff_def_pwr += 1
                                        if hard_battle_playing:
                                            debuff_def_pwr += 4

                                    elif block_enemy_damage:
                                        print("'But you don't feel anything'")
                                        debuff_def = True
                                        debuff_def_lengh = 1
                                    terminal_action_ended = True


                    if terminal_action_ended:
                        sleep(2)
                        terminal_phase = False

                    #Quitting the Terminal Phase...
                    if not terminal_phase:
                        if damage > 0:
                            player_get_hit = True
                            damage_dealt_to_player = True
                        player_turn_end = False
                pygame.display.init()
                screen = pygame.display.set_mode((1280,720))
                pygame.display.set_caption("Rude Python")

                # Options/Variables Reset #
                if debuff_atk:
                    debuff_atk_lengh -= 1
                if debuff_atk_lengh == 0:
                    debuff_atk = False
                if debuff_def:
                    debuff_def_lengh -= 1
                if debuff_def_lengh == 0:
                    debuff_def = False

                turn_counter += 1

                battle_option = 0
                magic_option = 0
                act_option = 0
                if not len(inventory)==0:
                    items_option = item_start_position
                elif len(inventory)==0:
                    items_option = item_back_position
                    items_only_back_option = True
                main_bar = True
                magic_bar = False
                act_bar = False
                items_bar = False
                player_turn_end = False
                block_actions = False
                player_anim_roll = 2
                enemy_anim_roll = 1
                ###############

        # BACK TO THE GAME #
        clock.tick(60)
        time_now=pygame.time.get_ticks()

        #Sound at start of battle #
       # Triggered by player animation

        if (music_battle_trigger
                and not music_battle_playing
                and time_now - sound_start_battle_delay_time >= 1100)\
                and player_health > 0:
            music_play("rude buster")
            music_battle_playing = True

        # The hard mode!!
        if hard_battle_trigger and not hard_battle_playing and player_health > 0:
            music_play("hammer of justice")
            hard_battle_playing = True
        #if music_battle_trigger and
        #Dinamic HP#
        enemy_hp_axis = 236*(enemy_health/enemy_max_health)
        enemy_hp_box_inside = pygame.Rect(917, 117, enemy_hp_axis, 36)

        player_hp_axis = 166*(player_health/player_max_health)
        player_hp_box_inside = pygame.Rect(87,447, player_hp_axis, 36)

        # If damage during terminal phase...
        if damage > 0 and not block_enemy_damage:
            player_anim_roll = 7
            hit_start_time = pygame.time.get_ticks() #when the hit starts to count

        ##

        pygame.draw.rect(screen, "White", battle_box_1)
        pygame.draw.rect(screen, (40,40,40), battle_box_2) #Before -> (80,80,80)
        pygame.draw.rect(screen, "White", combat_box_1)
        pygame.draw.rect(screen, (40,40,40), combat_box_2)

        # Player HP interface
        pygame.draw.rect(screen, "White", player_hp_box_border)
        pygame.draw.rect(screen, "Red", player_hp_box_inside)
        player_hp_text = font_small.render(f"{player_health} HP", True, "Black")
        screen.blit(player_hp_text, (135,457))

        # Enemy HP interface
        pygame.draw.rect(screen, "White", enemy_hp_box_border)
        pygame.draw.rect(screen, "Dark red", enemy_hp_box_inside)

        # Sprites and Animations
        ### ENEMY ###
        lev_time += 0.04
        lev_offset_x = math.sin(lev_time * lev_speed_x) * lev_amplitude_x
        lev_offset_y = math.sin(lev_time * lev_speed_y) * lev_amplitude_y

        if enemy_anim_roll == 0:
            if time_now - enemy_awakes_last_frame >= enemy_awakes_tempo:
                enemy_awakes_counter = (enemy_awakes_counter + 1) % len(enemy_awakes)
                enemy_awakes_last_frame = time_now
            screen.blit(enemy_awakes[enemy_awakes_counter], (position_enemy_x, position_enemy_y))
            if enemy_awakes_counter == len(enemy_awakes) - 1:
                enemy_anim_roll = 1

        elif enemy_anim_roll == 1 and not hard_battle_playing:
            if time_now - enemy_idle_last_frame >= enemy_idle_tempo:
                enemy_idle_counter = (enemy_idle_counter + 1) % len(enemy_idle)
                enemy_idle_last_frame = time_now
            screen.blit(enemy_idle[enemy_idle_counter], (position_enemy_x+lev_offset_x, position_enemy_y+lev_offset_y))

        elif enemy_anim_roll == 1 and hard_battle_playing:
            if time_now - enemy_idle_last_frame >= enemy_idle_tempo:
                enemy_idle_counter = (enemy_idle_counter + 1) % len(hard_enemy_idle)
                enemy_idle_last_frame = time_now
            screen.blit(hard_enemy_idle[enemy_idle_counter], (position_enemy_x+lev_offset_x, position_enemy_y+lev_offset_y))

        elif enemy_anim_roll == 7:
            # Hit animaton
            if enemy_get_hit and time_now - enemy_hit_start_time >= enemy_shake_dur:
                enemy_get_hit = False
                enemy_shake_pwr = 2
                enemy_anim_roll = 7
            if enemy_get_hit:
                enemy_offpixel_x = random.randint(-enemy_shake_pwr, enemy_shake_pwr)
            else:
                enemy_offpixel_x = 0
            if not hard_battle_playing:
                screen.blit(enemy_get_hit_animation, (position_enemy_x + enemy_offpixel_x, position_enemy_y))
            if hard_battle_playing:
                screen.blit(hard_enemy_get_hit_animation, (position_enemy_x + enemy_offpixel_x, position_enemy_y))

        ### PLAYER ###
        if time_now - player_anim_timing >= 1000 and player_anim_roll == 0:
            player_anim_roll = 1
            music_battle_trigger = True
            sefx["start battle"].play()
            sound_start_battle_delay_time = pygame.time.get_ticks()

        if player_anim_roll == 0:
            screen.blit(player_stand, (position_player_x,position_player_y))
            block_actions = True

        elif player_anim_roll == 1:
            if time_now - player_start_last_frame >= player_start_tempo:
                player_start_counter = (player_start_counter + 1) % len(player_start)
                player_start_last_frame = time_now
            screen.blit(player_start[player_start_counter], (position_player_x,position_player_y))
            if player_start_counter == len(player_start)-1:
                player_anim_roll = 2

        elif player_anim_roll == 2:
            block_actions = False
            if time_now - player_idle_last_frame >= player_idle_tempo:
                player_idle_counter = (player_idle_counter + 1) % len(player_idle) #this way 1%5 = 1, 2%5 = 2 ... ¨6%5 = 1 (Loop!)
                player_idle_last_frame = time_now #Reset the animation
            screen.blit(player_idle[player_idle_counter], (position_player_x,position_player_y))

        elif player_anim_roll == 3:
            if time_now - player_think_last_frame >= player_think_tempo:
                player_think_counter = (player_think_counter +1) % len(player_think)
                player_think_last_frame = time_now
            screen.blit(player_think[player_think_counter], (position_player_x,position_player_y))

        elif player_anim_roll == 4:
            if time_now - player_fumble_last_frame >= player_fumble_tempo:
                player_fumble_counter = (player_fumble_counter+1) % len(player_fumble)
                player_fumble_last_frame = time_now
            screen.blit(player_fumble[player_fumble_counter], (position_player_x,position_player_y))

        elif player_anim_roll == 5:
            screen.blit(player_prepare_attack, (position_player_x,position_player_y))
            if time_now - player_prepare_timing >= 500:
                player_anim_roll = 5.25
        elif player_anim_roll == 5.25:
            if time_now - player_attack_last_frame >= player_attack_tempo:
                player_attack_counter = (player_attack_counter+1) % len(player_attack)
                player_attack_last_frame = time_now
            screen.blit(player_attack[player_attack_counter],(position_player_x,position_player_y))

            if player_attack_counter == 3 and not attack_landed:
                #Everything that happens when the player attacks!
                #Reminder: MAX player_damage_values = [0,28,43,58,125]
                if not debuff_atk:
                    damage_dealt_to_enemy = random.choices(
                        player_damage_values, weights=
                        player_damage_chances, k=1)[0]
                    enemy_health -= damage_dealt_to_enemy
                    enemy_shake_pwr = int((damage_dealt_to_enemy/2)) #The enemy shakes the more damage you give!
                elif debuff_atk:
                    damage_dealt_to_enemy = random.choices(
                        player_damage_values, weights=
                        player_damage_chances, k=1)[0] - debuff_atk_pwr*debuff_atk_lengh
                    if damage_dealt_to_enemy < 0:
                        damage_dealt_to_enemy = 0
                    enemy_health -= damage_dealt_to_enemy
                    enemy_shake_pwr = int((damage_dealt_to_enemy/2))
                if damage_dealt_to_enemy > 0:
                    enemy_get_hit = True
                    enemy_hit_start_time = pygame.time.get_ticks()
                    enemy_anim_roll = 7
                    if damage_dealt_to_enemy < 50:
                        sefx["hit"].play()
                    elif damage_dealt_to_enemy >= 50 and damage_dealt_to_enemy < 100:
                        sefx["critical hit1"].play()
                    else:
                        sefx["critical hit2"].play()
                if enemy_health < 0:
                    enemy_health = 0
                attack_landed = True
                attack_text_trigger = True
                attack_text_time = time_now
                attack_text_levitation_position = 0 #Resets in all attacks
                player_attack_position_text_x_side = random.randint(0,1)
                if player_attack_position_text_x_side == 0:
                    player_attack_position_text_x = \
                        (random.randint(920, 970)) #Where the number will be displayed
                elif player_attack_position_text_x_side == 1:
                    player_attack_position_text_x = \
                        (random.randint(1100, 1130))
                player_attack_position_text_y = \
                    (random.randint(220, 270))

            if player_attack_counter == len(player_attack)-1:
                player_anim_roll = 5.5
                attack_landed = False
        elif player_anim_roll == 5.5:
            screen.blit(player_attack[-1],(position_player_x,position_player_y))

        elif player_anim_roll == 6 and magic_bar:
            if time_now - player_act_last_frame >= player_act_tempo:
                player_act_counter = (player_act_counter+1) % len(player_act)
                player_act_last_frame = time_now
            screen.blit(player_act[player_act_counter], (position_player_x,position_player_y))
            if player_act_counter == len(player_act) - 1:
                player_anim_roll = 6.5
        elif player_anim_roll == 6.5 and magic_bar:
            screen.blit(player_act[-1], (position_player_x, position_player_y))

        elif player_anim_roll == 6 and act_bar:
            if time_now - player_act_last_frame >= player_act_tempo:
                player_act_counter = (player_act_counter+1) % len(player_act)
                player_act_last_frame = time_now
            screen.blit(player_act[player_act_counter], (position_player_x,position_player_y))
            if player_act_counter == 6:
                player_anim_roll = 6.5
                player_act_counter = 0
        elif player_anim_roll == 6.5 and act_bar:
            screen.blit(player_act[7],(position_player_x,position_player_y))


        elif player_anim_roll == 7:
            damage_taken_text_trigger = True
            damage_taken_text_time = time_now
            attack_text_levitation_position = 0  #Resets in all attacks
            enemy_attack_position_text_x = \
                (random.randint(200, 220))  #Where the number will be displayed
            enemy_attack_position_text_y = \
                (random.randint(240, 250))

            if damage_dealt_to_player and not debuff_def:
                if damage <= player_defense:
                    final_damage = 1
                    player_health -= final_damage
                    damage_taken_note = final_damage
                else:
                    final_damage = damage-player_defense
                    player_health -= final_damage
                    damage_taken_note = final_damage
                sefx["hurt"].play()
                damage_dealt_to_player = False

            elif damage_dealt_to_player and debuff_def:
                if damage <= player_defense:
                    final_damage = 1+(debuff_def_pwr*debuff_def_lengh)
                    player_health -= final_damage
                    damage_taken_note = final_damage
                else:
                    final_damage = (damage-player_defense)+(debuff_def_pwr*debuff_def_lengh)
                    player_health -= final_damage
                    damage_taken_note = final_damage #Registers how much damage was taken for display
                sefx["hurt"].play()
                damage_dealt_to_player = False

            if player_health <= 0:
                player_health = 0
                pygame.mixer.music.stop()
            damage = 0 #Has to be reseted, otherwise the player takes continous damage!
            #When player is hurt
            if player_get_hit:
                block_actions = True
            # Defeat
            if player_get_hit and time_now - hit_start_time >= shake_dur and player_health == 0:
                player_get_hit = False
                player_anim_roll = 7.5
            # Hit animaton
            elif player_get_hit and time_now - hit_start_time >= shake_dur:
                player_get_hit = False
                player_anim_roll = 2
            if player_get_hit:
                offpixel_x = random.randint(-shake_pwr, shake_pwr)
                # offpixel_y = random.randint(-shake_pwr, shake_pwr)
            else:
                offpixel_x = 0
                offpixel_y = 0
            screen.blit(player_get_hit_animation, (position_player_x+offpixel_x, position_player_y))

        elif player_anim_roll == 7.5:
            screen.blit(player_fainted, (position_player_x,position_player_y))

        elif player_anim_roll == 8:
            if time_now - player_item_last_frame >= player_item_tempo:
                player_item_counter = (player_item_counter+1) % len(player_item)
                player_item_last_frame = time_now
            screen.blit(player_item[player_item_counter], (position_player_x,position_player_y))
            if player_item_counter == len(player_item)-1:
                player_anim_roll = 8.5
        elif player_anim_roll == 8.5:
            screen.blit(player_item[-1],(position_player_x,position_player_y))

        ### DAMAGE / HEALING INDICATORS ###
        #For the enemy
        if attack_text_trigger and time_now - attack_text_time >= 700:
            attack_text_trigger = False
        if attack_text_trigger:
            attack_text_levitation_position += 1
            if damage_dealt_to_enemy > 0:
                player_attack_text_shake = random.randint(1, 5)
                attack_player_text = font_big.render(f"{damage_dealt_to_enemy}", True, "Red")
                screen.blit(attack_player_text,(player_attack_position_text_x+player_attack_text_shake,
                                                player_attack_position_text_y-attack_text_levitation_position))
            elif damage_dealt_to_enemy == 0:
                attack_player_text = font.render(f"MISS", True, "White")
                screen.blit(attack_player_text, (player_attack_position_text_x,
                                                 player_attack_position_text_y - attack_text_levitation_position))
        #For the player
        if damage_taken_text_trigger and time_now - damage_taken_text_time >= shake_dur-300:
            damage_taken_text_trigger = False
        if damage_taken_text_trigger:
            attack_text_levitation_position += 0.2
            enemy_attack_text_shake = random.randint(-1,1)
            attack_enemy_text = font.render(f'{damage_taken_note}',True,"Red")
            screen.blit(attack_enemy_text,(enemy_attack_position_text_x+enemy_attack_text_shake,
                                           enemy_attack_position_text_y - attack_text_levitation_position))
        if player_heal_trigger and time_now - heal_text_time >= 800:
            player_heal_trigger = False
        if player_heal_trigger:
            heal_text_levitation_position_x += 0.2
            heal_text_levitation_position_y += 0.4
            player_heal_text = font.render(f'{heal}',True,"Light Green")
            screen.blit(player_heal_text, (200-heal_text_levitation_position_x,
                                           250-heal_text_levitation_position_y))

        if main_bar:

            pygame.draw.rect(screen, "White", attack_box_1)
            pygame.draw.rect(screen, "Black", attack_box_2)
            pygame.draw.rect(screen, "White", magic_box_1)
            pygame.draw.rect(screen, "Black", magic_box_2)
            pygame.draw.rect(screen, "White", act_box_1)
            pygame.draw.rect(screen, "Black", act_box_2)
            pygame.draw.rect(screen, "White", items_box_1)
            pygame.draw.rect(screen, "Black", items_box_2)

            if battle_option == 0:
                atk_color = "Red"
                magic_color = "White"
                act_color = "White"
                items_color = "White"
            elif battle_option == 1:
                atk_color = "White"
                magic_color = "Red"
                act_color = "White"
                items_color = "White"
            elif battle_option == 2:
                atk_color = "White"
                magic_color = "White"
                act_color = "Red"
                items_color = "White"
            elif battle_option == 3:
                atk_color = "White"
                magic_color = "White"
                act_color = "White"
                items_color = "Red"

            atk_text_surface = font.render("Attack", True,atk_color)
            magic_text_surface = font.render("Magic", True, magic_color)
            act_text_surface = font.render("Act",True,act_color)
            items_text_surface = font.render("Items",True,items_color)

            atk_centralisation = atk_text_surface.get_rect(center=attack_box_2.center)
            magic_centralisation = magic_text_surface.get_rect(center=magic_box_2.center)
            act_centralisation = act_text_surface.get_rect(center=act_box_2.center)
            items_centralisation = items_text_surface.get_rect(center=items_box_2.center)

            screen.blit(atk_text_surface,atk_centralisation)
            screen.blit(magic_text_surface,magic_centralisation)
            screen.blit(act_text_surface,act_centralisation)
            screen.blit(items_text_surface,items_centralisation)
            pygame.display.flip()

        elif magic_bar:
            pygame.draw.rect(screen, "White", items_box_1) #using the same coordinates
            pygame.draw.rect(screen, "Black", items_box_2)

            if magic_option == 0:
                spell1_color = "Red"
                spell2_color = "White"
                spell3_color = "White"
                back_color = "White"
            elif magic_option == 1:
                spell1_color = "White"
                spell2_color = "Red"
                spell3_color = "White"
                back_color = "White"
            elif magic_option == 2:
                spell1_color = "White"
                spell2_color = "White"
                spell3_color = "Red"
                back_color = "White"
            elif magic_option == 3:
                spell1_color = "White"
                spell2_color = "White"
                spell3_color = "White"
                back_color = "Red"

            spell1_text_surface = font.render("Attack+", True, spell1_color)
            spell2_text_surface = font.render("Defense+", True, spell2_color)
            spell3_text_surface = font.render("Accuracy+", True, spell3_color)

            back_text_surface = font.render("Back", True,back_color)

            back_text_centralisation = back_text_surface.get_rect(center=items_box_2.center)

            screen.blit(spell1_text_surface,(130,535))
            screen.blit(spell2_text_surface,(390,535))
            screen.blit(spell3_text_surface,(650,535))
            screen.blit(back_text_surface,back_text_centralisation)


            if box_to_cover_visibility and magic_option == 0 and not max_atk_reached and not limit_break:
                text = (f'ATK increased by {buff_atk}!')

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                        time_now,
                                        time_updated,
                                        interval, counter))
                draw_text(screen,text_to_be_shown,font,"White",110,520)

                if time_now - time_game >= interval * (len(text)+10) * 2:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            elif box_to_cover_visibility and magic_option == 0 and max_atk_reached and not limit_break:
                text = f'Your ATK is maxed out!'

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 2:
                    block_actions = False
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False
                    # RESET ANIMATION #
                    player_anim_roll = 3
            elif not max_true_atk_reached and box_to_cover_visibility and magic_option == 0 and limit_break:
                text = (f'You concentrate in your heart of hearts...\n'
                        f'ATK increased by {buff_atk}!!')

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 2:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            elif box_to_cover_visibility and magic_option == 0 and limit_break:
                text = f'Wow... You maxed out your ATK!!! (now for certain)'

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 2:
                    block_actions = False
                    max_true_atk_reached = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False
                    # RESET ANIMATION #
                    player_anim_roll = 3

            elif box_to_cover_visibility and magic_option == 1 and not max_def_reached and not limit_break:
                text = f'DEF increased by {buff_def}!'

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text) + 10) * 2:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            elif box_to_cover_visibility and magic_option == 1 and max_def_reached and not limit_break:
                text = f'Your DEF is maxed out!'

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 2:
                    block_actions = False
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False
                    # RESET ANIMATION #
                    player_anim_roll = 3

            elif not max_true_def_reached and box_to_cover_visibility and magic_option == 1 and limit_break:
                text = (f'You concentrate in your heart of hearts...\n'
                        f'DEF increased by {buff_def}!!')

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 1.5:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            elif box_to_cover_visibility and magic_option == 1 and limit_break:
                text = f'Wow... You maxed out your DEF!!! (now for certain)'

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 1.5:
                    block_actions = False
                    max_true_def_reached = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False
                    # RESET ANIMATION #
                    player_anim_roll = 3
            if box_to_cover_visibility and magic_option == 2 and not max_acc_reached:
                text = f'ACC increased by {buff_acc}!'

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text) + 10) * 2:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            elif box_to_cover_visibility and magic_option == 2 and max_acc_reached and not act_option2_pressed:
                text = (f'Your ACC is maxed out!\n'
                        f'...\n'
                        f'But you feel you need more focus somehow...')
                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)-10) * 2:
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False
                    block_actions = False
                    # RESET ANIMATION #
                    player_anim_roll = 3
            elif box_to_cover_visibility and magic_option == 2 and max_acc_reached and act_option2_pressed:
                text = (f'You unlocked LIMIT BREAK!\n'
                        f'You can further increase your Attack and Defense.')
                limit_break = True
                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)) * 1.5:
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False
                    block_actions = False
                    # RESET ANIMATION #
                    player_anim_roll = 3

            pygame.display.flip()


        elif act_bar:
            pygame.draw.rect(screen, "White", items_box_1)  # using the same coordinates
            pygame.draw.rect(screen, "Black", items_box_2)

            if act_option == 0:
                act1_color = "Red"
                act2_color = "White"
                act3_color = "White"
                back_color = "White"
            elif act_option == 1:
                act1_color = "White"
                act2_color = "Red"
                act3_color = "White"
                back_color = "White"
            elif act_option == 2:
                act1_color = "White"
                act2_color = "White"
                act3_color = "Red"
                back_color = "White"
            elif act_option == 3:
                act1_color = "White"
                act2_color = "White"
                act3_color = "White"
                back_color = "Red"

            act1_text_surface = font.render("Check", True, act1_color)
            act2_text_surface = font.render("Chat", True, act2_color)
            act3_text_surface = font.render("Hold Breath", True, act3_color)
            back_text_surface = font.render("Back", True, back_color)

            back_text_centralisation = back_text_surface.get_rect(center=items_box_2.center)

            screen.blit(act1_text_surface, (130, 535))
            screen.blit(act2_text_surface, (400, 535))
            screen.blit(act3_text_surface, (650, 535))

            screen.blit(back_text_surface, back_text_centralisation)


            if box_to_cover_visibility and act_option == 0:
                text = (f'You check the enemy stats:\n'
                        f'{enemy_name} HP: {enemy_health}\n')
                if not hard_battle_playing:
                    if debuff_atk and debuff_def:
                        text = (f'You check the enemy stats:\n'
                                f'{enemy_name} HP: {enemy_health}\n'
                                f'Turns until WEAK is removed: {debuff_atk_lengh}; Turns until FRAGILE is removed: {debuff_def_lengh}')
                    elif debuff_atk:
                        text = (f'You check the enemy stats:\n'
                                f'{enemy_name} HP: {enemy_health}\n'
                                f'Turns until WEAK is removed: {debuff_atk_lengh} ')
                    elif debuff_def:
                        text = (f'You check the enemy stats:\n'
                                f'{enemy_name} HP: {enemy_health}\n'
                                f'Turns until FRAGILE is removed: {debuff_def_lengh}')
                elif hard_battle_playing:
                    text = (f'You check the enemy stats:\n'
                            f'{enemy_name} HP: ???\n')
                    if debuff_atk and debuff_def:
                        text = (f'You check the enemy stats:\n'
                                f'{enemy_name} HP: ???\n'
                                f'Turns until WEAK is removed: {debuff_atk_lengh}; Turns until FRAGILE is removed: {debuff_def_lengh}')
                    elif debuff_atk:
                        text = (f'You check the enemy stats:\n'
                                f'{enemy_name} HP: ???\n'
                                f'Turns until WEAK is removed: {debuff_atk_lengh} ')
                    elif debuff_def:
                        text = (f'You check the enemy stats:\n'
                                f'{enemy_name} HP: ???\n'
                                f'Turns until FRAGILE is removed: {debuff_def_lengh}')

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * len(text) * 2:
                    box_to_cover_visibility = False
                    text_to_be_shown = ""
                    counter = 0
                    block_actions = False
                    # RESET ANIMATION #
                    player_anim_roll = 3

            elif box_to_cover_visibility and act_option == 1:
                text = 'You tried to talk with it...'
                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * len(text) * 1.8:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            elif box_to_cover_visibility and act_option == 2:
                if not act_option2_pressed:
                    text = ('You take a deep breath...\n'
                        'You feel more concentrated on the battle.')
                    pygame.draw.rect(screen, "Black", box_to_cover_bar)
                    counter, time_updated, text_to_be_shown = (
                        dialogue_maker_v3(text, text_to_be_shown,
                                          time_now,
                                          time_updated,
                                          interval, counter))
                    draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                    if time_now - time_game >= interval * len(text) * 2:
                        # END TURN#
                        act_option2_pressed = True
                        swap_delay = True
                        swap_delay_time = pygame.time.get_ticks()
                        player_turn_end = True
                        text_to_be_shown = ""
                        counter = 0
                        box_to_cover_visibility = False
                else:
                    text = "You are feeling more focused!"
                    pygame.draw.rect(screen, "Black", box_to_cover_bar)
                    counter, time_updated, text_to_be_shown = (
                        dialogue_maker_v3(text, text_to_be_shown,
                                          time_now,
                                          time_updated,
                                          interval, counter))
                    draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                    if time_now - time_game >= interval*len(text)*2:
                        box_to_cover_visibility = False
                        text_to_be_shown = ""
                        counter = 0
                        block_actions = False
                        # RESET ANIMATION #
                        player_anim_roll = 3

            pygame.display.flip()

        elif items_bar:
            pygame.draw.rect(screen, "White", items_box_1)  # using the same coordinates
            pygame.draw.rect(screen, "Black", items_box_2)

            for index, item_name in enumerate(inventory):
            #What it does is create:
            #(index=0, "Item name1")
            #(index=1, "Item name2")...
                row = index // 3
                col = index % 3

                x = items_x_grid + col * (items_width + 40)
                y = items_y_grid + row * (items_height + 30)

                color = "red" if index == items_option else "white"
                text_surf = font.render(item_name, True, color)
                screen.blit(text_surf, (x,y))

            back_color = "White"
            if items_option == item_back_position:
                items1_color = "White"
                items2_color = "White"
                items3_color = "White"
                items4_color = "White"
                items5_color = "White"
                items6_color = "White"
                back_color = "Red"

            back_text_surface = font.render("Back", True, back_color)

            back_text_centralisation = back_text_surface.get_rect(center=items_box_2.center)

            screen.blit(back_text_surface, back_text_centralisation)

            if box_to_cover_visibility:
                if consumed_item.lower() == 'ok potion':
                    text = (f'You used an {consumed_item}\n'
                            f'You healed {heal} HP')
                else:
                    text = (f'You used a {consumed_item}\n'
                            f'You healed {heal} HP\n'
                            f'You cleared all Debuffs')

                pygame.draw.rect(screen, "Black", box_to_cover_bar)
                counter, time_updated, text_to_be_shown = (
                    dialogue_maker_v3(text, text_to_be_shown,
                                      time_now,
                                      time_updated,
                                      interval, counter))
                draw_text(screen, text_to_be_shown, font, "White", 110, 520)

                if time_now - time_game >= interval * (len(text)+10) * 2:
                    # END TURN#
                    swap_delay = True
                    swap_delay_time = pygame.time.get_ticks()
                    player_turn_end = True
                    text_to_be_shown = ""
                    counter = 0
                    box_to_cover_visibility = False

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":

    main()

