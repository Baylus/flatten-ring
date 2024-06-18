# flat-souls
2D Darksouls-like game that is trained via genetic algorithms

NOTE: I actually have only played like an hour of DS3, but a good amount of elden ring so I will be using terminology appropriate to this.

### Input/Output definitions

#### Tarnished

##### Inputs:
 - X Position
 - Y Position
 - Current Angle
 - Margit X
 - Margit Y
 - Margit's current action
 - Time remaining in Margit action
###### Maybe:
 - Health of Tarnished
 - Health of Margit

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
 - Time remaining in Tarnished action
###### Maybe:
 - Health of Tarnished
 - Health of Margit

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