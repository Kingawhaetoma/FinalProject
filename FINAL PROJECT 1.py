# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:26:41 2024

@author: kinga
"""

import pygame
import simpleGE
import random


class Guy1(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("guy1.png")
        self.setSize(50, 50)
        self.position = (50, 400)
        self.inAir = True
        
           
    def process(self):
        if self.inAir:
            self.addForce(.2, 270)
        
        if self.y > 450:
            self.inAir = False
            self.y = 450
            self.dy = 0          
        
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.x += 5
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.x -= 5   
        if self.scene.isKeyPressed(pygame.K_SPACE):
            if not self.inAir:
                self.addForce(6, 90)
                self.inAir = True

        self.inAir = True
        for platform in self.scene.platforms:
            if self.collidesWith(platform):                
                if self.dy > 0:
                        self.bottom = platform.top
                        self.dy = 0
                        self.inAir = False
        
class Platform(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        self.position = (position)
        self.setImage("platform.png")
        self.setSize(60, 30)
       
    #def update(self):
        #super().update()
        #if self.mouseDown:
         #   self.position = pygame.mouse.get_pos()
class Ghost(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("ghost.png")
        self.setSize(25, 25)
        self.reset()
        
             
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Exit(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("gate.png")
        self.setSize(60, 60)  # Adjust the size of the exit image as needed
        self.position = (600, 40)  # Adjust the position as needed
        
        
        
class StartButton(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("start_btn.png")
        self.setSize(110, 70)
        self.position = (200, 250)
    
     

class ExitButton(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("exit_btn.png")
        self.setSize(110, 70)
        self.position = (500, 250)

class IntroPage(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("plainField.png")
        self.StartButton = StartButton(self)
        self.ExitButton = ExitButton(self)
        self.sprites = [self.StartButton, self.ExitButton]

    def process(self):
        if self.StartButton.clicked:
            self.response = "play"
            self.stop()
            
        elif self.ExitButton.clicked:
             self.response = "quit"
             self.quit()
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("sky.png")
        self.guy1 = Guy1(self)
        self.ghosts = [Ghost(self) for _ in range(10)]
        
        
        
        
        
        self.platforms = [Platform(self, (130, 450)),
                          Platform(self, (200, 400)),
                          Platform(self, (250, 350)),
                          Platform(self, (200, 150)),
                          Platform(self, (350, 180)),
                          Platform(self, (400, 300)),
                          Platform(self, (300, 250)),
                          Platform(self, (550, 350)),
                          Platform(self, (450, 150)),
                          Platform(self, (400, 400)),
]
        self.exit = Exit(self)  # Instantiate the exit sprite      
        self.sprites = [self.platforms, self.guy1, self.exit] 
        # Add the exit sprite to the list of sprites

class Instruction(simpleGE.Scene):
    def __init__(self, scene):
        super().__init__()
        self.setImage("plainField.png")


def main():
    current_state = "intro"  # Initial state is "intro"
    
    while current_state != "quit":  # Run the loop until the game is set to quit
        if current_state == "intro":
            # Initialize the intro page scene
            intro_scene = IntroPage()
            intro_scene.start()
            
            # Check the user's response after the intro page
            if intro_scene.response == "play":
                current_state = "game"  # Transition to the game state
            elif intro_scene.response == "quit":
                current_state = "quit"  # Transition to the quit state
        
        elif current_state == "game":
            # Initialize the game scene
            game_scene = Game()
            game_scene.start()
            
            # Optionally handle game over or game win conditions here
            # Transition back to the intro state or quit state if needed
            # For example, you could set current_state to "intro" for restarting or "quit" to end the game

            # For now, we'll just set it back to "intro" for demonstration
            current_state = "intro"
    
    # When the loop exits, the game ends
    print("Game has exited")

if __name__ == "__main__":
    main()
