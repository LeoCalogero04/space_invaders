import pygame, random
class Player(pygame.sprite.Sprite):  #inherits from sprite class
    def __init__(self,position):
        super().__init__()  #inherits sprite attributes into class
        self.score=0
        self.hp=3
        self.sprites=[]
        self.sprites.append(pygame.image.load('pilots.png'))
        self.sprites.append(pygame.image.load('invader_explosion.png'))
        
        self.shoot_noise=pygame.mixer.Sound('player_shoot.wav') #loads gunshot sound
        self.death_noise=pygame.mixer.Sound('player_death.wav')
        self.cooldown_count= 0
        self.last_hit_time=0 #last time hit
        self.current_sprite=0
        self.image=self.sprites[self.current_sprite]
        self.rect=self.image.get_rect()
        self.rect.center=position
        self.last_shot=0 #last time cannon shot a laser

    
    def move(self):  #when used on a group, method is called for each sprite in group
        x=2
        key=pygame.key.get_pressed()
        if key[pygame.K_RIGHT]==True:
            self.rect.move_ip(x,0)
            
        if key[pygame.K_LEFT]==True:
            self.rect.move_ip(-x,0)
  
  
    def update(self,current_time):
        self.move()
        self.shoot(current_time)


        self.select_image(current_time)
        if self.hp<=0:
            self.kill
            global run
            run=False 

    def shoot(self,current_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.on_cooldown(current_time) != True:
                         if self.current_sprite == 0:
                            vertical_gap=5
                            self.shoot_noise.play() #plays sound
                            x=self.rect.centerx
                            y=self.rect.top-vertical_gap
                            laser=Laser(pilot,x,y)  #creates laser at center of cannon a set distance above cannon
                            self.last_shot=current_time
                            lasers.add(laser)

    def got_hit(self,current_time):
        if self.current_sprite!=1:
            self.death_noise.play()
            self.hp-=1
            self.last_hit_time=current_time
    def select_image(self,current_time):
        timer=1
        difference= (current_time-self.last_hit_time)/1000 #time since hit in seconds
        if current_time/1000>timer: #avoid image being set to explosion at start
            if difference>timer: # 1 second since last death
                self.current_sprite=0 # pilot image appears 1 second has passed since hit
            else:
                self.current_sprite=1
        self.image=self.sprites[self.current_sprite]

    def get_position(self):
        return self.position

    def add_score(self,amount): #add functionality based on type of alien
        self.score+=amount
    
    def on_cooldown(self,current_time): 
        if (current_time-self.last_shot)/1000>0.6: #if it has been 0.5 seconds, return False
            return False
        else:
            return True
    def get_score(self):
        return self.score
    
    def get_hp(self):
        return self.hp
    




   
class Laser(pygame.sprite.Sprite): #finish
    def __init__(self,creator,x,y): #creator is sprite group spawing lazer
            super().__init__()
            self.creator=creator
            if creator==pilot:
                self.image=pygame.image.load('lazer.png')
            elif creator == invaders:
                self.image=pygame.image.load('red lazer.png')
            self.rect=self.image.get_rect()
            self.rect.bottom=y
            self.rect.centerx=x
    def collision(self,current_time):
        if self.creator == pilot:
            invaders_collided= pygame.sprite.spritecollide(self,invaders,False,pygame.sprite.collide_mask) #list of all sprites that collided with laser
            ufo_collided= pygame.sprite.spritecollide(self,ufo,False,pygame.sprite.collide_mask)
            for invader in invaders_collided:
                invader.kill()
                invader.death_sound()
                self.kill()           #self.kill prevents laser from hitting multiple targets
            for ufos in ufo_collided:
                ufos.kill()
                ufos.death_sound()
                self.kill()
        if self.creator == invaders:
            collided=pygame.sprite.spritecollide(self,pilot,False,pygame.sprite.collide_mask)
            for player in collided:
                player.got_hit(current_time) #update hp down by 1,plays death sound, handles explosion animation
                self.kill()
   

    def update(self,current_time): #will move lazer down screen
        y_update=5
        if self.creator==pilot:
            self.rect.move_ip(0,-y_update) 
        elif self.creator==invaders:
            self.rect.move_ip(0,y_update)
        if self.rect.top >= Screen_height or self.rect.bottom < 0:
            self.kill()
        self.collision(current_time) #deals with any collisions that have occured


class Invader(pygame.sprite.Sprite):
    def __init__(self,row,x,y):
        super().__init__()
        
        self.sprites=[] #attributes corresponding to animation
        self.current_sprite=0
        self.last_animate=0
        self.move_sound=[]
        for i in range(1,5):
            self.move_sound.append(pygame.mixer.Sound('fastinvader'+str(i)+'.wav'))
        self.death=pygame.mixer.Sound('invaderkilled.wav')
        self.shoot_sound=pygame.mixer.Sound('invader shoot_sound.mp3')

        if row <=1:
            self.sprites.append(pygame.image.load('front 2 row invader.png'))
            self.sprites.append(pygame.image.load('front row part 2.png'))

        elif row <=3:
            self.sprites.append(pygame.image.load('row 3 4 invader.png'))
            self.sprites.append(pygame.image.load('row 3 4 p2.png'))
        elif row==4:
            self.sprites.append(pygame.image.load('row 5 invader.png'))
            self.sprites.append(pygame.image.load('row 5 invader p2.png'))
        
        self.image=self.sprites[self.current_sprite]
        self.rect=self.image.get_rect()
        self.rect.bottomleft=(x,y)
        self.row=row+1
        self.direction='right'
    def current_direction(self):
        return self.direction
    def animation_cooldown(self,current_time):
        time=current_time/1000
        if (current_time-self.last_animate)/1000 >= 1-time/80: #if 1 second has passed
            self.last_animate=current_time  
            return False
        else:
            return True
    def get_x(self): #returns x cord of left side or right side of rectangle
        if self.direction == 'right':
            return self.rect.right
        elif self.direction == 'left':
            return self.rect.left
    def get_y(self): #returns y cord of bottom of sprite
        return self.rect.bottom
    def death_sound(self):
        self.death.play()

    def shoot(self):
        vertical_gap=5
        self.shoot_sound.play() #plays sound
        x=self.rect.centerx
        y=self.rect.top+vertical_gap
        laser=Laser(invaders,x,y)  #creates laser at center of invader a set distance above invader
        return laser
        
    def update(self,current_time,border_check):
        x_move=10
        y_move=26
        if self.animation_cooldown(current_time) == False: # when off cooldown
            self.current_sprite+=1 #cycle image
            for sound in self.move_sound:
                sound.play() #plays sound
            

            if border_check == True: #if at end of screen
                self.rect.move_ip(0,y_move)  #move down and change direction
                if self.direction=='right':
                    self.direction='left'
                elif self.direction=='left':
                    self.direction='right'

            elif border_check==False: #if not at border
                if self.direction == 'right':
                    self.rect.move_ip(x_move,0)
                elif self.direction == 'left':
                    self.rect.move_ip(-x_move,0)
            

            if self.current_sprite >= len(self.sprites): #resets sprite back to original png if cycle is complete
                self.current_sprite=0
            self.image=self.sprites[self.current_sprite]

            roll=random.randint(1,25)
            if roll == 3:
                lasers.add(self.shoot()) 
                   
class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('ufo.png')
        self.rect=self.image.get_rect()
        self.rect.centery=Screen_height/12
        self.rect.left=0
        self.sound=pygame.mixer.Sound('ufo_highpitch.wav')
        self.last_sound=0
        self.sound.play()
        self.death_sound_effect=pygame.mixer.Sound('invaderkilled.wav')
    def update(self,current_time):
        self.sound_player(current_time)
        self.rect.x+=2
        if self.rect.left>Screen_width:
            self.kill()
    def sound_player(self,current_time):
        if (current_time-self.last_sound)/1000>=0.1:
            self.sound.play()
            self.last_sound=current_time
    def death_sound(self):
        self.death_sound_effect.play()
        
        



def create_invaders():
    invaders=pygame.sprite.Group()
    for i in range(5):
        y=350-50*i
        for j in range(11):
            x=120+j*52
            invader=Invader(i,x,y)
            invaders.add(invader)
    return invaders

def invader_border_check(invader_group): #returns True if any invader at border of screen, else false
    x_move=10
    list=[]
    for invader in invader_group:
        if invader.current_direction()=='right':
            if invader.get_x()+x_move>=Screen_width:
                list.append('down')
        elif invader.current_direction()=='left':
            if invader.get_x()-x_move<=0:
                list.append('down')
    if 'down' in list:
        return True  
    else:
        return False


def ufo_create(current_time):
    global last_ufospawn
    if (current_time-last_ufospawn)/1000>=20:
        roll=random.randint(1,21)
        if roll==2:
            flyer=UFO()
            ufo.add(flyer)
            last_ufospawn=current_time
        




pygame.init()
Screen_width=800
Screen_height=700
screen=pygame.display.set_mode((Screen_width,Screen_height))
black=(0,0,0)
run=True
last_ufospawn=0
#clock initialization
clock=pygame.time.Clock()
current_time=0
#pilot group setup
player1=Player((Screen_width/2,Screen_height-72))
pilot=pygame.sprite.Group()
pilot.add(player1)
#invaders setup
invaders=create_invaders()
last_shots=0
lasers=pygame.sprite.Group()
ufo=pygame.sprite.Group()
  

while run:
    movement_list=[]
    screen.fill(black)
    pilot.draw(screen)
    pilot.update(current_time)
    lasers.draw(screen)
    invaders.draw(screen)
    ufo_create(current_time)
    ufo.draw(screen)
    ufo.update(current_time)
    
    current_time=pygame.time.get_ticks() #time in milliseconds since game started
    border_check=invader_border_check(invaders) #T/F bool indicating if at border
    invaders.update(current_time,border_check)
    lasers.update(current_time)
    
                
    for invader in invaders:
        if invader.get_y()>=640:
            run=False
    pygame.display.update()
    clock.tick(60)

pygame.quit()

