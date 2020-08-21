#Python Gravity Simulator V6
#Ezra Sitorus

import csv
import pygame
#Importing module used to provide the graphics element of the simulation
import time
#Importing module used to pause the program to give the sense of a fluid animation
import os
#Importing module used to calibrate simulation window
import math
#Importing module used for certain trigonometric functions required when dealing with vectors
import sys
#Importing module used to close the program
import colorsys
#Importing module used for representing the magnitude and argument of the vector and scalar fields
pygame.init()
#Initialised all Pygame modules

#SETTING UP THE ENVIRONMENT OF THE SIMULATION

info = pygame.display.Info()
width = info.current_w
height = info.current_h
#Gets the height and width of the screen

os.environ['SDL_VIDEO_CENTERED'] = '1'
#Centres the window

window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
#Allows the window to be resizable

pygame.display.set_caption("Simulation of Gravity")
#Sets the name of the window to Simulation of Gravity

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
#Sets the icon of the window to a custom one depicting a planet

pygame.font.init()
font = pygame.font.SysFont("Segoe UI", 30)
#Sets the default font as Segoe UI

informationScreen = pygame.image.load('InformationScreen.png')
#Loads up the information image to teach the user how to use the program

class Particle:
#This is the class Particle
#It has been defined to have the following attributes: position, velocity, acceleration, mass, valid   
   def __init__(self, position, velocity, mass, valid):
#This is the constructor of the Particle object
      self.position = position
      self.velocity = velocity
      self.acceleration = [0,0]
#Position, Velocity, Acceleration are vectors that are used to simulate the motion of the particle - they have been implemented using lists
      self.mass = mass
#Mass is a constant for the particle
      self.validity = valid
#Valid is a boolean used to check if the particle has collided with another particle and hence whether or not the particle should be used in other calculations

class Queue:
#This is the class Queue
#This is the implementation of a linear queue
#It is used to calculate the force that each particle experiences
#It has the attributes maxsize and content
    def __init__(self, maxsize):
#This is the constructor of the Queue object
        self.maxsize = maxsize
#maxsize is the maximum length of the queue
        self.content = []
#Content is a list that holds the items in the queue

    def isEmpty(self):
#isEmpty is a function that returns a boolean value, indicating if the queue is empty or not
       if self.getSize == 0:
         return True
       else:
         return False

    def getSize(self):
#getSize is a function that returns the number of items in the queue
       return len(self.content)

    def enqueue(self, item):
#enqueue is a function that adds the item into the queue as long as the queue is not full
        if (len(self.content) == self.maxsize):
            return False
        else:
            self.content.append(item)
            return True

    def dequeue(self):
#dequeue is a function that removes and returns the first item in the queue as long as the queue is not empty
        if self.isEmpty():
            return False
        else:
            return self.content.pop(0)

def createParticle(ListOfParticles, position, velocity, mass):
#This is a subroutine that calls the constructor of the Particle class and appends the particle into a list
   ListOfParticles.append(Particle(position, velocity, mass, True))

def verifyText(userString):
#This is the function verify text
#It takes in the string that the user has typed in and verifies using a recursive algorithm
#This is done by taking in the substring with the first character omitted and entering this into the function again
#This process repeats until the input is only 1 character and the characters are verified to be digits
#As this process unwinds, each previous character is verified and if every character is a digit, the function returns true
   if (userString[0]).isdigit():
      if len(userString) > 1:
         return (verifyText(userString[1:]))
      if len(userString) == 1:
         return((userString[0]).isdigit())
   else:
      return False
      
def collision(particleA, particleB, ListOfParticles):
#This function handles collisions between particles
#In this simulation, collisions are treated as a completely inelastic collision in which the particles coalesce
#Conservation of momentum is used to find the velocity of the new particle after they coalesce
   
   initialHorizontalMomentum = (particleA.mass*particleA.velocity[0]) + (particleB.mass*particleB.velocity[0])
   initialVerticalMomentum = (particleA.mass*particleA.velocity[1]) + (particleB.mass*particleB.velocity[1])
#Momentum has been resolved into horizontal and vertical components
   
   newPosition = [(particleA.position[0] + particleB.position[0])/2, (particleA.position[1] + particleB.position[1])/2]
#The position of the new particle is the average of the positions of the two original particles

   newMass = particleA.mass + particleB.mass
#The mass of the new particle is the sum of the two particles that collided
   
   createParticle(ListOfParticles, newPosition, [initialHorizontalMomentum/newMass, initialVerticalMomentum/newMass], newMass)
#The createParticle subroutine is called again to create the new particle and add it into the list

def getMagnitude(x_0, y_0, x_1, y_1):
#This function returns the magnitude of a vector using the Pythagorean Theorem
   magnitude = ((x_1 - x_0)**2 + (y_1 - y_0)**2)**0.5
   return magnitude

def calculateForce(particleA, particleB):
#This subroutine uses vectors and Newton's Laws to determine the forces exerted on each particle
#The subroutine takes 2 particles objects as parameters
   
   displacement = [particleB.position[0] - particleA.position[0], particleB.position[1] - particleA.position[1]]
#The displacement is calculated by finding the difference between the components of position of each particle
   
   argument = math.atan2(displacement[1],displacement[0])
#The argument is the angle between the horizontal axis and the displacement vector
#This is calculated using the inverse tangent function
   
   distance = getMagnitude(particleA.position[0], particleA.position[1], particleB.position[0], particleB.position[1])
#The distance is calculated by calling the getMagnitude function

   if distance != 0:
      forceMagnitude = particleA.mass*particleB.mass*distance**-2
   else:
      forceMagnitude = 0
#The magnitude of the force is calculated by using Newton's Gravitational Law
   
   particleA.acceleration[0] += (10000*forceMagnitude*math.cos(argument)/particleA.mass)
   particleA.acceleration[1] += (10000*forceMagnitude*math.sin(argument)/particleA.mass)
   particleB.acceleration[0] += (10000*-1*forceMagnitude*math.cos(argument)/particleB.mass)
   particleB.acceleration[1] += (10000*-1*forceMagnitude*math.sin(argument)/particleB.mass)
#The acceleration of each particle is calculated using Newton's Second Law
#The acceleration is then resolved into horizontal and vertical components using trigonometric functions
#The vectors are calculated realtive to the position vector of particleA hence the vectors of particleB is negative
   
def changeAcceleration(ListOfParticles):
#This subroutine organises how the new acceleration attribute of each particles are calculated
#It uses the queue data structure to process how particles get their new acceleration values
   queueOfParticles = Queue(len(ListOfParticles))
   for particle in ListOfParticles:
      particle.acceleration = [0,0]
      queueOfParticles.enqueue(particle)
#Each particle is given a temporary acceleration of 0 and then gets transferred into a queue
   for particle in ListOfParticles:
      particleA = queueOfParticles.dequeue()
#The first item of the queue is dequeued
#Every remaining item in the queue is paired with the dequeued item and they are arguments for the calculateForce() subroutine
#This process is repeated with every unique pairing of particles
      for i in range(0, queueOfParticles.getSize()):
         particleB = queueOfParticles.dequeue()
         calculateForce(particleA, particleB)
         queueOfParticles.enqueue(particleB)

def showGravitationalField(ListOfParticles):
#This subroutine calculates the gravitational field strength at every point on the screen
#This is represented by using a method called domain colouring, often used in complex analytic functions
#Since gravitational field is a vector field, each point is a 2-Dimensional vector so it can be treated as a complex number
   for x in range(0, width + 1):
      for y in range(0, height + 1):
#Each point is given an initial vector of 0
         xForceComponent = 0
         yForceComponent = 0

         for particle in ListOfParticles:
#Each point is treated as a particle with mass 1
#The force it experiences is the gravitational field vector for that point
#This process is the same as the calculateForce() subroutine
            displacement = [particle.position[0] - x, particle.position[1] - y]
            argument = math.atan2(displacement[1],displacement[0])
            distance = getMagnitude(x, y, particle.position[0], particle.position[1])
            if (distance != 0):
               forceMagnitude = (particle.mass)*(distance**-2)
               xForceComponent += 100000*forceMagnitude*math.cos(argument)
               yForceComponent += 100000*forceMagnitude*math.sin(argument)
#The vector is resolved into horizontal and vertical components
               
         argument = math.atan2(yForceComponent, xForceComponent)
         if argument < 0:
            argument += 2*math.pi
#The argument is calculated using the inverse tangent function and the angle is given between 0 and 2*pi
            
         forceMagnitude = getMagnitude(0, 0, xForceComponent, yForceComponent)
         forceMagnitude = (forceMagnitude/(forceMagnitude + 1000))
#The magnitude of the force is calculated using the getMagnitude function and then given as a ratio between 0 and 1
         
         normalised = colorsys.hsv_to_rgb(argument/(2*math.pi), 1, forceMagnitude)
#The colour is determined using the HSV colour system
#The hue is determined by the argument given as a ratio between 0 and 1
#The saturation is always 1
#The value (brightness) is determined by the force magnitude as a ratio
         
         colour = [i * 255 for i in normalised]
#A list comprehension is used to multiply each value by 255 as the conversion function returns it as a list with values between 0 and 1
         
         window.set_at((x, y), colour)
#The pixel at that point is then coloured the correct colour

def showGravitationalPotential(ListOfParticles):
   for x in range(0, width + 1):
      for y in range(0, height + 1):
#Every point on the system has a scalar value associated with it
#This value is the mass of the particle divided by the distance between the particle and the point
#For a system with multiple values, this scalar value is the sum of every potential value due to each particle
         potential = 0
         for particle in ListOfParticles:
            displacement = [particle.position[0] - x, particle.position[1] - y]
            distance = getMagnitude(0,0, displacement[0], displacement[1])
            if (distance != 0):
               potential += (100*particle.mass)/(distance)
         potential = potential/(potential + 1000)
         normalised = colorsys.hsv_to_rgb((2/3), 1, potential)
         colour = [i * 255 for i in normalised]
         window.set_at((x, y), colour)     

def showGravitationalFieldAndPotential(ListOfParticles):
   for x in range(0, width + 1, int((width+1)/20)):
      for y in range(0, height + 1, int((height + 1)/20)):
#The gravitational field is only calculated for certain points on the screen
         xForceComponent = 0
         yForceComponent = 0
         for particle in ListOfParticles:
#The process to calculate the magnitude and argument is similar to the showGravitationalField subroutine
            displacement = [particle.position[0] - x, particle.position[1] - y]
            argument = math.atan2(displacement[1],displacement[0])
            distance = getMagnitude(x, y, particle.position[0], particle.position[1])
            if (distance != 0):
               forceMagnitude = (particle.mass)*(distance**-2)
               xForceComponent += 10000*forceMagnitude*math.cos(argument)
               yForceComponent += 10000*forceMagnitude*math.sin(argument)
         forceMagnitude = getMagnitude(0, 0, xForceComponent, yForceComponent)
#Unlike the other subroutine, the vector is drawn as a line with a length determined by the magnitude and pointing in the direction of the vector
         force = [xForceComponent, yForceComponent]
         fraction = (forceMagnitude/(forceMagnitude + 10000))
         force = [i * fraction * 1000 * (forceMagnitude**-1) for i in force]
         drawArrow([x,y], force, fraction)
#The drawArrow subroutine is called to draw the arrow as it makes the code more readable
         
   potentials = []
#A 2D list is created that holds the potential value for each point on the screen
#The process to find the potential is similar to the showGravitationalPotential subroutine
   for x in range(0, width + 1):
      potentials.append([])
      for y in range(0, height + 1):
         potential = 0
         for particle in ListOfParticles:
            displacement = [particle.position[0] - x, particle.position[1] - y]
            distance = getMagnitude(0,0, displacement[0], displacement[1])
            if (distance != 0):
               potential += (100*particle.mass)/(distance)
         (potentials[x]).append(potential)

   flatList = [i for row in potentials for i in row]
#The list is flattened using a list comprehension
   frequencyDict = {}
#A dictionary is used to hold the frequencies of each unique potential value rounded to 5 decimal places
   for value in flatList:
      if round(value, 5) not in frequencyDict:
         frequencyDict[round(value, 5)] = 1
      else:
         frequencyDict[round(value, 5)] += 1

   mode_potential = max(frequencyDict, key = frequencyDict.get)
#The most frequent potential value is found using the max function
   
   for x in range(0, width + 1):
         for y in range(0, height + 1):
            if ((potentials[x][y] - mode_potential)**2 < 1 or (potentials[x][y] - mode_potential/2)**2 < 1.5 or (potentials[x][y] - mode_potential*2)**2 < 1.5):
                pygame.draw.circle(window, (0, 0, 255), (x, y) , 1)
#Every pixel with a potential close to the most frequent potential value (greater than or less than the most frequent value by 1) is coloured blue
#Every pixel with a potential close to half the most frequent potential value is coloured blue
#Every pixel with a potential close to double the most frequent potential value is coloured blue
#These region/line is called an equipotential line

def drawArrow(startPosition, displacement, magnitude):
   pygame.draw.line(window, (255,255,255), startPosition, [startPosition[0] + displacement[0], startPosition[1] + displacement[1]], 1)
#This is a subroutine that draws the arrow using the Pygame library
   
def main():
#THIS IS THE SUBROUTINE THAT IS CALLED FIRST IN THE PROGRAM

#CERTAIN VARIABLES ARE SET TO PROPERY CREATE THE SIMULATION ENVIRONMENT

   running = True
#Boolean used to create a while loop in which the processes of the simulation keep repeating

   fieldOn = False
#Boolean used to determine whether the gravitational field should be displayed
   
   potentialOn = False
#Boolean used to determnie whether the gravitational potential should be displayed
   
   fieldandpotentialOn = False
#Boolean used to determnie whether the gravitational field lines and equipotential lines should be displayed
   
   showText = False
#Boolean used to determine whether or not text of mass should be displayed

   mass = 1000
#Integer that represents the default mass of 1000 in some arbitrary unit

   ListOfParticles = []
#List data structure that holds all of the existing particles

   accelerationVector = False
#Boolean that determines whether or not the acceleration vector should be displayed
   
   velocityVector = False
#Boolean that determines whether or not the velocity vector should be displayed
   
   showInformation = True
#Boolean that determines whether or not the pop-up information screen should be displayed
   
   text = ''
#A blank string that will be used when the user types   

   deltaTime = 0.01
#A floating point number that represents how fast the simulation runs
   
   valid = lambda a: (a.validity == True)
#A lambda expression that is used to check whether a particle is valid or not, used in the collision checking section

#Unless the gravitational fields/potential modes are activated, the screen needs to be refreshed with a black screen so previous iterations of particles are removed   
   while running:      
      if fieldOn:
         showGravitationalField(ListOfParticles)
      elif potentialOn:
         showGravitationalPotential(ListOfParticles)
      elif fieldandpotentialOn:
         window.fill((0,0,0))
         showGravitationalFieldAndPotential(ListOfParticles)
      else:
         window.fill((0,0,0))

      deleteList = []
#List data structure that holds all particles which are going to be deleted
      
      for event in pygame.event.get(): 
         if event.type == pygame.QUIT:
#Checks if the exit button has been pressed
            running = False
#If so, the program will close
            break
         elif event.type == pygame.MOUSEBUTTONDOWN:
#Checks if the left mouse button has been pressed on the screen
            if event.button == 1:
#If so, the position of the click has been recorded
               originalPos = event.pos
         elif event.type == pygame.MOUSEBUTTONUP:
#Checks if the left mouse button has been released
            if event.button == 1:
               newPos = event.pos
               movementVector = [originalPos[0] - newPos[0], originalPos[1] - newPos[1]]
#Creates a displacement vector between the positions the screen was clicked
               createParticle(ListOfParticles, [originalPos[0], originalPos[1]], [10*movementVector[0],10*movementVector[1]], mass)
#Creates a particle whose velocity is proportional to the displacement vector created


         elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_F1:
#Toggles the velocity vector if F1 is pressed
               velocityVector = not(velocityVector)
               
            if event.key == pygame.K_F2:
#Toggles the acceleration vector if F2 is pressed
               accelerationVector = not(accelerationVector)
               
            if event.key == pygame.K_F3:
#Toggles the information screen if F3 is pressed
               showInformation = not showInformation
               
            if event.key == pygame.K_F4:
#Deletes every particle if F4 is pressed
               for particle in ListOfParticles:
                  deleteList.append(particle)

            if event.key == pygame.K_F5:
#Toggles the gravitational field if F5 is pressed and turns off the other modes
               if not(fieldOn):
                  window.fill((0,0,0))
                  message_surface = font.render("Calculating Gravitational Field", True, (255,255,255))
                  window.blit(message_surface, (0,0))
               else:
                  message_surface = font.render("Turning Off Gravitational Field", True, (255,255,255))
                  window.blit(message_surface, (0,0))
                  pygame.display.update()
                  pygame.time.delay(3000)
               potentialOn = False
               fieldandpotentialOn = False
               fieldOn = not(fieldOn)

            if event.key == pygame.K_F6:
#Toggles the gravitational potential if F6 is pressed and turns off the other modes
               if not(potentialOn):
                  window.fill((0,0,0))
                  message_surface = font.render("Calculating Gravitational Potential", True, (255,255,255))
                  window.blit(message_surface, (0,0))
               else:
                  message_surface = font.render("Turning Off Gravitational Potential", True, (255,255,255))
                  window.blit(message_surface, (0,0))
                  pygame.display.update()
                  pygame.time.delay(3000)
               fieldandpotentialOn = False
               fieldOn = False
               potentialOn = not(potentialOn)

            if event.key == pygame.K_F7:
#Toggles the gravitational field and equipotential lines mode if F7 is pressed and turns off the other modes
               if not(fieldandpotentialOn):
                  message_surface = font.render("Turning on Gravitational Field and Equipotential Lines", True, (255,255,255))
                  window.blit(message_surface, (0,0))
                  pygame.display.update()
                  pygame.time.delay(3000)
               else:
                  window.fill((0,0,0))
                  message_surface = font.render("Turning Off Lines", True, (255,255,255))
                  window.blit(message_surface, (0,0))
                  pygame.display.update()
                  pygame.time.delay(3000)
               potentialOn = False
               fieldOn = False
               fieldandpotentialOn = not(fieldandpotentialOn)
               
            if event.key == pygame.K_RETURN:
#If the RETURN key is pressed, certain processes are done to validate the string the user has typed in
               if (text != '' and len(text) < 10 and text != "0"):
#Only allows strings to be validated by the verifyText function if it is not empty and less than 10 characters
                  if (verifyText(text)):
                     mass = int(text)
#If the text has been verified as a possible mass value, the value of mass is set to the user chosen value
                     verifiedNumber = font.render("Mass: " + text, True, (255,255,255))
                     showText = True
               text = ''
#The typed string is deleted and a string that shows the new mass is displayed
            elif event.key == pygame.K_BACKSPACE:
#If the backspace key is pressed, the string deletes the final character and displays the new string
               text = text[:-1]
            else:
               text += event.unicode
#For all other alphanumeric key presses, the character is added to the end of the string
            if event.key == pygame.K_DOWN:
#If the down arrow key is pressed, the movement of the particles slow down
               if (deltaTime == 0):
                  deltaTime = olddeltaTime
               else:
                  if deltaTime != 0.0003125:
                     deltaTime = deltaTime/2
            if event.key == pygame.K_SPACE:
#If the space key is pressed, the movement of the particles toggles between pausing and returning to the previous speed
               text = text[:-1]
               if deltaTime != 0:
                  olddeltaTime = deltaTime
                  deltaTime = 0               
               elif (deltaTime == 0):
                  deltaTime = olddeltaTime
               else:
                  olddeltaTime = deltaTime
                  deltaTime = 0
            if event.key == pygame.K_UP:
#If the down arrow key is pressed, the movement of the particles speed up
               if (deltaTime == 0):
                  deltaTime = olddeltaTime
               else:
                  if deltaTime != 0.32:
                     deltaTime = deltaTime*2
            if fieldOn or potentialOn or fieldandpotentialOn:
#If any of the modes are toggled on, the movement of the particles toggles between pausing and returning to the previous speed
#They are paused if the modes are turned on
                  if (deltaTime != 0): 
                     olddeltaTime = deltaTime
                  deltaTime = 0
 
      if (len(ListOfParticles) > 1):
#For a system with multiple particles, forces from each particle causes acceleration
         changeAcceleration(ListOfParticles)

      for particle in ListOfParticles:                
#This for loop evaluates the particles in the system
         if (((particle.position[0])**2 > 1000000) and ((particle.position[1])**2 > 1000000)):
            if not(particle in deleteList):
               deleteList.append(particle)
#For particles that are at a position far enough, they are added to the deletion list wherer they will be deleted lated
         pygame.draw.circle(window, (255, 255, 255), (int(particle.position[0]), int(particle.position[1])) , 10)    #FOR EVERY PARTICLE, A BALL IS DRAWN IN THEIR POSITION
         if velocityVector:
#If the velocity vector is turned on, a line is drawn to represent the magnitude and direction of the particle's velocity
            magnitude = getMagnitude(0, 0, particle.velocity[0] ,particle.velocity[1])
            intensity = magnitude/(magnitude+1)
            if (magnitude != 0):
#The line is only drawn if the magnitude of the vector is not equal to zero
               pygame.draw.line(window, (intensity*255,0,0), particle.position, [particle.position[0] + int(35*particle.velocity[0]/(magnitude)), particle.position[1] + int(25*particle.velocity[1]/(magnitude))], 7)
         if accelerationVector:
#If the acceleration vector is turned on, a line is drawn to represent the magnitude and direction of the particle's acceleration
            magnitude = getMagnitude(0, 0, particle.acceleration[0] ,particle.acceleration[1])
            intensity = magnitude/(magnitude+1)
            if (magnitude != 0):
#The line is only drawn if the magnitude of the vector is not equal to zero
               pygame.draw.line(window, (0,intensity*255,0), particle.position, [particle.position[0] + int(35*particle.acceleration[0]/magnitude), particle.position[1] + int(25*particle.acceleration[1]/magnitude)], 7)

         particle.velocity[0] += particle.acceleration[0]*(deltaTime)
#Using a non-analytical method, we get the new position and velocity of the particle by multiplying by some arbitrarily small number
         particle.velocity[1] += particle.acceleration[1]*(deltaTime)
#This small number is the change in time and can be altered by pressing the arrow keys
         particle.position[0] += particle.velocity[0]*(deltaTime)
#This gives an approximation to the integral as position is the integral of velcoity with respect to time and velocity is the integral of acceleration with respect to time
         particle.position[1] += particle.velocity[1]*(deltaTime)

      for particleA in filter(valid, ListOfParticles):
#This subroutine checks every particle to see if they have collided with another particle
         for particleB in filter(valid, ListOfParticles[(ListOfParticles.index(particleA)+1):]):
#The conditions for collision are that the particles must be valid and have a distance of 20 units between the centres
            if (getMagnitude(particleA.position[0], particleA.position[1], particleB.position[0], particleB.position[1]) < 20):
                  collision(particleA, particleB, ListOfParticles)
#If they have collided, the collision subroutine is called and the two particles are not considered valid anymore to prevent further collisions from happening as this for loop occurs
                  particleA.validity = False
                  particleB.validity = False
                  if not(particleA in deleteList):
                     deleteList.append(particleA)
#The two particles are then appended onto the deletion list
                  if not(particleB in deleteList):
                     deleteList.append(particleB)

      for particle in deleteList:
         ListOfParticles.remove(particle)
#The particles in the deletion list are removed from the list of particles
         
      if showText:
         window.blit(verifiedNumber, (0,40))
#If the showText boolean is on, the value of mass is displayed
         
      if showInformation:
         window.blit(informationScreen, (int(width/2) - 300, int(height/2) - 300))
#If the information screen has been toggled on, the pop-up information is displayed in the middle of the screen
         
      txt_surface = font.render(text, True, (255,255,255))
#Every alphanumeric key the user has pressed is added onto the string which is displayed at all times
      window.blit(txt_surface, (0,0))

      pygame.time.delay(10)
#A short interval of 10 milliseconds between screen updates is done to provide a fluid animation
      pygame.display.update()
      
main();
#The main subroutine is called here
pygame.quit()
#When the user presses the exit button, the pygame processes are closed and the program is then able to be closed afterwards
sys.exit()
