# flatten ring
2D Darksouls-like game that is trained via genetic algorithms

NOTE: I actually have only played like an hour of DS3, but a good amount of elden ring so I will be using terminology appropriate to this.

## Usage

### Checkpoint resuming

Running the main.py file will run simulations that will resume previous checkpoints. These checkpoints will attempt to be found in the latest "run" folder of the directory for the current fitness version. To prevent resuming checkpoints, use the -r/--reset flag to start fresh model training.

### Gamestate saving

Gamestates are useful for tracking what behaviors are being rewarded most for a given generation. They do consume a lot of space though, considering our population and generation count. e.g. for our current setup we have 150 population and 500 generations. Our generations from 93 to 277 are taking up 44GB, and I am planning on increasing population count to 1000.

From these figures, we can estimate that with the current fitness function (that may still be encouraging tarnished to run off the cliff early), each gamestate file takes up about 836KB, which on its own is rather small, but adds up when running 2000 population across 500 generations.

There are ways to prevent clearing of game states, but the most guaranteed one is the `SAVE_GAMESTATES` flag in the settings.py. If this is set, no actions will be taken to remove the existing game states. This is useful for ensuring that you do not accidentally destroy records when attempting to replay previous games.

### Replay analysis

Replay's are useful for analyzing the previous games and what kind of rewards each actor is getting for different behaviors. There are a couple ways of reviewing previous games.

#### Generational bests

This is a way of collecting the best runs of a range of generations so that we can analyze what the fitness function is rewarding the models the most, in order to determine what adaptations need to be made to encourage appropriate behavior from the actors.

When viewing the replays, pressing space bar will skip the current population's replay, which can be helpful if its obvious that the trainer is repeating the same behavior and you know what it is going to be doing the whole time. NOTE: Depending on how fast your replay speed is, you may have to hold down the space bar until another "update" happens, as this is when the replay game recognizes you are attempting to skip to the next generation.

There are a couple of flags important for this.

- -b/--best: The number of best populations to show for the specified generations. Defaults to `DEFAULT_NUM_BEST_GENS` if not provided.
- -t/--trainer: Will specify which trainer to view the best of. Takes the string `tarnished` or `margit`. If not specified, will show both, but will show all of tarnished's first, then will show all of margits. You can keyboard interrupt to skip the remaining generations of tarnished if you are ready to see margit's. If flag is present but nothing provided, defaults to tarnished only.
- -g/--generations: Which generations to view. All replays will happen from the newest generation to the oldest, regardless of how the genertaions are specified. There are several use cases here:

Show the last 5 generations:
```main.py -g 5```
Show generations 23 to 42
```main.py -g 23 42```
Show generations 4 8 15 16 23 42
```main.py -g 4 8 15 16 23 42```

#### Direct replay

This is the most direct one. Simply include the -p/--replay flag, followed by the name of the replay that you want to review. Much more involved than other methods, but this does work to directly analyze behaviors.

### Input/Output definitions

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