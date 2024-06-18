# flatten ring
2D Darksouls-like game that is trained via genetic algorithms

NOTE: I actually have only played like an hour of DS3, but a good amount of elden ring so I will be using terminology appropriate to this.

### Input/Output definitions

#### Tarnished
It may be possible to replace the time remaining in actions with a general current tick for both parties, which may allow them to utilize that information not only for the enemy's actions but also their own.
##### Inputs:
 - X Position
 - Y Position
 - Current Angle
 - Margit X
 - Margit Y
 - Margit's current action
 - Margit's angle
 - Time remaining in Margit action
###### Maybe:
 - Health of Tarnished
 - Health of Margit

We will need Margit's current angle so that Tarnished knows whether it is in the area of margit's current attack
##### Outputs:
 - Left
 - Right
 - Forward
 - Back
 - Turn Left
 - Turn Right
 - Attack
 - Dodge


#### Margit

##### Inputs:
 - Margit X
 - Margit Y
 - Current Angle
 - Tarnished X Position
 - Tarnished Y Position
 - Tarnished's current action
 - Tarnished's Angle
 - Time remaining in Tarnished action
###### Maybe:
 - Health of Tarnished
 - Health of Margit

We will need Tarnished's current angle so that Margit knows whether it is in the area of margit's current attack, and where tarnished is dodging to.
##### Outputs:
 - Left
 - Right
 - Forward
 - Back
 - Turn Left
 - Turn Right
 - Attack
 - Retreat
###### Maybe:
 - Reverse Attack
 - Daggers

Note: Margit will have lead time on all his actions, similar to how the game works in elden ring. This is to simulate the reactions that players can have to a specific attack when they see it coming. This will be the advantage that the Tarnished has over Margit.

However, this also means that it may be critical that Margit doesn't know the Tarnished's angle, because then it could predict where it is going to be vulnerable and attack for free anytime that the tarnished dodges, but I am unsure how this will play out.
