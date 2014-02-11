# Omar Rahman, andrewid: omarr

README.txt

BacSim is a bacteria simulator that allows one to observe trends of
population growth and decay. The user interface includes a petri dish
with grass on the top left, a control panel on the bottom, and a data
panel on the right hand side.

Features:

-Three types of bacteria:
    -Herbivores: only eat grass
    -Predators: only eat other bacteria
    -Omnivores: eat both grass and herbivores (but not predators)

-Each bacterium has two traits: speed and vision
    -Speed determines how fast a bacterium will travel; this affects the
     amount of food it can eat (and whether it gets food at all)
     
    -Vision allows a predator to see its prey and chase it and allows an
     herbivore to see a predator and flee
     
    -There is a tradeoff between these two traits, i.e. speed can increase
     but at the cost of reduced vision and vice versa
    
-Bacteria will divide when they eat enough food
-Bacteria will decay constantly; they must eat food faster than they decay
-Grass with 5 levels of energy available
-Adjustable rate of grass growth
-Predator/prey dynamics of chasing and fleeing
-Mutations that give rise to natural selection for certain traits (evolution)
-Relevant data variables updated live
-A scrolling plot of the populations of all species
-Reset and quit buttons

Instructions:

-Make sure pygame is installed
    -If not, visit: http://www.pygame.org/download.shtml and install
-In the BacSim directory, run the Simulation.py file with Python
-Select desired bacterium to add from the panel on the bottom
-Click anywhere on the petri dish to add one; add as many desired
-Sit back and enjoy

Items of interest:

Try letting just herbivores in the petri dish without introducing any
predators. You'll notice that their average speed will constantly increase
while their vision decreases. This makes sense in this scenario because
vision only helps when there are predators to see and flee from. Since
there are no predators, the only selecting factor is the amount of food an
herbivore can eat; thus, only the fastest ones survive since they can eat
more. Once a predator is introduced, however, herbivores must strike a
balance between speed and vision to both eat and not get eaten.

