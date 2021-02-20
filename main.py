import pygame, sys
import random

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,440))
	screen.blit(floor_surface,(floor_x_pos+288,440))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (320,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (320,random_pipe_pos-top_pipe_position))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	visible_pipes = [pipe for pipe in pipes if(pipe.right>-50)]
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 512:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	global bird_frames,pipe_surface,bg_surface
	for pipe in pipes:
		if(bird_rect.colliderect(pipe)):
			death_sound.play()
			bird_frames = random.choice(bird_choice)
			pipe_surface = random.choice([pygame.image.load('assets/pipe-green.png'),pygame.image.load('assets/pipe-red.png')])
			bg_surface = random.choice([pygame.image.load('assets/background-day.png').convert(),pygame.image.load('assets/background-night.png').convert()])
			return False
	if(bird_rect.top <= -100 or bird_rect.bottom >= 440):
		death_sound.play()
		bird_frames = random.choice(bird_choice)
		pipe_surface = random.choice([pygame.image.load('assets/pipe-green.png'),pygame.image.load('assets/pipe-red.png')])
		bg_surface = random.choice([pygame.image.load('assets/background-day.png').convert(),pygame.image.load('assets/background-night.png').convert()])
		return False
	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (80,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if(game_state == 'main_game'):
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (144,50))
		screen.blit(score_surface,score_rect)
	elif(game_state == 'game_over'):
		score_surface = game_font.render(f'Score : {(int(score))}',True,(255,255,255))
		score_rect = score_surface.get_rect(center = (144,50))
		screen.blit(score_surface,score_rect)
		high_score_surface = game_font.render(f'High Score : {(int(high_score))}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (144,409))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
	if(score>high_score):
		high_score=score
	return high_score

def set_score():
	global score, can_score 
	if pipe_list:
		for pipe in pipe_list:
			if 75 < pipe.centerx < 85 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

pygame.init()
screen = pygame.display.set_mode((288,512), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',30)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
clock_time = 50
can_score=False
top_pipe_position=180

#Background
bg_surface = random.choice([pygame.image.load('assets/background-day.png').convert(),pygame.image.load('assets/background-night.png').convert()])

#Moving Floor
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

#Bird
blue_bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
blue_bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
blue_bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()

red_bird_downflap = pygame.image.load('assets/redbird-downflap.png').convert_alpha()
red_bird_midflap = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
red_bird_upflap = pygame.image.load('assets/redbird-upflap.png').convert_alpha()

yellow_bird_downflap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
yellow_bird_midflap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
yellow_bird_upflap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()

bird_choice=[[blue_bird_downflap,blue_bird_midflap,blue_bird_upflap],
[red_bird_downflap,red_bird_midflap,red_bird_upflap],
[yellow_bird_downflap,yellow_bird_midflap,yellow_bird_upflap]]
bird_frames = random.choice(bird_choice)
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (80,256))

BIRDFLAP = pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)

#Pipes
pipe_surface = random.choice([pygame.image.load('assets/pipe-green.png'),pygame.image.load('assets/pipe-red.png')])
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,230,290,260,250,320,360]

#Default Screen
game_over_surface = pygame.image.load('assets/message.png').convert_alpha();
game_over_rect = game_over_surface.get_rect(center = (144,256))

#Sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			pygame.quit()
			sys.exit()
		if(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_SPACE and game_active):
				flap_sound.play()
				bird_movement = 0
				bird_movement -= 6
			if(event.key == pygame.K_SPACE and game_active==False):
				set_score_sound=True
				pipe_list.clear()
				bird_rect.center = (80,256)
				clock_time = 50
				bird_movement=0
				score=0
				top_pipe_position=180
				game_active=True
				can_score=True
		if(event.type == SPAWNPIPE):
			pipe_list.extend(create_pipe())
		if(event.type == BIRDFLAP):
			if(bird_index==2):
				bird_index=0
			else:
				bird_index = (bird_index+1)
			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		#Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active=check_collision(pipe_list)

		#Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		top_pipe_position-=0.1
		if(top_pipe_position<=120):
			top_pipe_position=120
		set_score()
		score_display('main_game')
	else:
		#Default Page
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')

	#Floor
	floor_x_pos -= 1
	draw_floor()
	if(floor_x_pos <= -288):
		floor_x_pos = 0

	#Clock and Display
	pygame.display.update()
	clock_time += 0.02
	if(clock_time>=70):
		clock_time=70
	clock.tick(clock_time)