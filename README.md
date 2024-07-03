# flatten ring
2D Darksouls-like game that is trained via genetic algorithms

NOTE: I actually have only played like an hour of DS3, but a good amount of elden ring so I will be using terminology appropriate to this.

## Parallelize

So, it has become abundantly clear that training will take far too long if making incremental adjustments and waiting literal days to train for each session. So, I am going to make it so we can train many different populations at the same time.

At first, I thought the pygame window would be a concern, but upon thinking more on it, all the processes are pretty bound together with how I laid them out. Even if the different entities exist in the same game, they should conflict, because the weapons are explicitly assigned their target, which is generated in the play_game function. I just need to make sure that theres no references to those objects on the outside and then we should be fine to simulate them. The one window should persist throughout the training just fine.

Going to be using the concurrent.futures library, specifically the ProcessPoolExecutor, which is better than ThreadPoolExecutor in our case, since our slowdown is mostly due to CPU resources, as we only ever write to the file at the end of the game.

## Input/Output definitions

#### Tarnished
It may be possible to replace the time remaining in actions with a general current tick for both parties, which may allow them to utilize that information not only for the enemy's actions but also their own.
##### Inputs:
 - X Position
 - Y Position
 - Current Angle
 - Margit X
 - Margit Y
 - Margit's angle
 - Margit's current action
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
 - Slash Attack
 - Reverse Slash
 - Daggers
###### Maybe:
 - Retreat

Note: Margit will have lead time on all his actions, similar to how the game works in elden ring. This is to simulate the reactions that players can have to a specific attack when they see it coming. This will be the advantage that the Tarnished has over Margit.

However, this also means that it may be critical that Margit doesn't know the Tarnished's angle, because then it could predict where it is going to be vulnerable and attack for free anytime that the tarnished dodges, but I am unsure how this will play out.


## Stuff to do
- Fix the TPS variable to be grabbed from a file that can be updated in the middle of a run so that I can take a better look at behavior once it starts to get farther in the run.
- Add functionality to load previous checkpoints
- Add Epsilon-Greedy Exploration to help aid the first couple of generations explore more freely
- Consider adding in functionality to save off current checkpoints incase of a keyboard interrupt, that way we don't lose 9 generations of training just because I happened to need to make a change or stop training for some reason.
- - This will require more support for picking up where we left off, by manually running training until we reach the next traditional checkpoint increment, then implementing the automated checkpointer, and running normally.
e.g. Checkpoint interval = 10, last margit checkpoint was 36. We would need to run 4 generations of training, checkpoint there, then we could add the automated checkpointer to the population and continue running.