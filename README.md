# Final Project Proposal
Hui Qu<br/>
Project Name: Aircraft Wars<br/>
## Introduction
Using Python to design a game called 'EE551Spring Aircraft Wars'. This is a flying shooting game, the overall environment is mainly around space. In a simple operation, the mouse moves freely in one place. The aircraft is controled by keybord and continuously launches the bullet. When the enemy is hit by the bullet of our aircraft, it disappears. At the same time, enemy fighters will also attack our aircraft, and using keyboard to up and down can also avoid attacks. What the player has to do in the game is to drive the aircraft and attack the enemy's aircraft.

## Design Flow
### 1. Building a game framework
a. Install the framework package Pygame. Pygame is a cross-platform Python module designed for video games that includes images and sound. Built on SDL, it allows real-time video game development without being tied to low-level languages such as machine language and assembly language.<br/>
b. Search for image resources. For example, pictures of our fighters, pictures of enemy fighters, background images, and so on.<br/>
c. Search for audio files. For example, the sound of the game starts, the sound of the enemy plane being hit, and the sound of our plane being hit.<br/>

### 2. Write a game program
a. Class Bullet program. The members are mainly the image objects of the bullets and the position where the bullets appear, and of course, the speed of movement. That is, the bullet moves straight from the position to the top of the screen.<br/>
b. Class Player program. Image objects and rectangular parameters and the location of our fighters, of course, there will be moving speed and bullet collection (used to save the bullets fired by the aircraft). The method is to move up and down, left and right, but I need to make a good boundary judgment.<br/>
c. Class Enemy program. The enemy aircraft appeared in position. It should be noted that this class holds two image objects, one is the normal enemy image. One is an image of an enemy plane exploding. In order to display the impact effect when impacting.<br/>
d. Game body loop and frame rate settings.<br/>
e. Score display and ‘GameOver’ display.<br/>

### 3. Test procedure
Test and debug the program.
