# Game States

So, there are a number of reason why game states are important, but the primary one
that I am interested in is so that I can easily replay the coolest or most interesting
runs back so that I can analyze what is going on with the training and see if there is any changes that need
to enhance this project.

I also want to minimize as much as possible the chances that I will need extra information in order
to replay the game back at a later date. So a lot of stuff may be unneccessary, but I will be
storing it likely for a reason I will list here, but the main one is just for safety such that
I do not have to be concerned with future changes.

All decisions made of what to include here are going to be robust in that even if
I add more possible actions that can be taken by the entities, I will still be able to replay
the old game states as I know I will not have to remove anything such that it will brick the replay.

Just as another summary, basically all thats necessary is what is required to visually display the game state at that time, and then it will be possible for me to recreate it in a playback feature.

## Save Names

Almost certainly will change this schema once I understand better how the neural network logic works, but
thinking that it will be: "timestamp_tarnishedFitness_margitFitness_generationNumber_fitnessFunctionVersion_gamestateLoggingVersion.json"
Assuming that child/generation number will be easy to automatically get to, if not I will remove those two and deal with possible duplicates later.

## Details

As far as I can tell, the requirements for what to include would be the basic information, such as:
 - X position
 - Y position
 - Health
 - Max Health
 - Current blocking action (normally only attacks and stuff that have an animation)
 - Current angle

Since I have no intertia in my game, except for dodge if you really strain the definition, then I do not need to worry about keeping track of the current velocity, as the next tick will show me what movements were done, and any turns that were made. 

Aside from this, the action inputs will be super helpful to know what the bot was attempting to do.
Margit's bullets will need tracking, and it may be best to keep track of the current weapon if one is being used.