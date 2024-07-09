# V.11

A lot of annoyances with the network have led me here, but I am currently working more with the configuration files to ensure that I am correctly balancing work on the fitness function and on the neat network configuration. I do not want to be overtuning the fitness function when my real problem was the network wasn't configured properly to being with.

## Changes

We are now:
- Cutting the repeated action penalty in half, or incrementing depending on what is more beneficial, whenever a new action is made
- Giving a flat reward for the number of unique actions made in the game.

As for the configurations. I am actually going to be changing the neat configurations for both. Those changes are:
- changing the species elitism to encourage more types of species to guarantee survive, that way we dont only have pit fallers.
- Add some hidden nodes to the initial connections. This will significantly aid in complex behavior learning. I am annoyed that I didnt noticed we had no hidden nodes to begin with. This makes a ton more sense.
- Make our initial connections be connected to those hidden nodes. This will also increase our likelihood of choosing many
- Increase our population to 1000 to encourage early exploration and make sure our fitness function is the issue

## Results

For some reason, it didnt update the population number. It was only doing 150 like it was before... Maybe because margit was still set to 150? Checking to see if I can make out why it stopped... It might have been because it resumed a previous checkpoint. It would have assumed all the previous checkpoint's configurations and junk. Will have to restart the simulation.

Sigh... Same stuff I have seen a hundred times now. Tarnished is now straight backing up, and praying that Margit will run straight at him too. Worried that increasing the repeated action penalty is going to make him jump off cliffs again. Think that the only answer is to bump up reward for moving closer to margit. Its just pretty hard to get a good idea of how to make sure that its Tarnished's actions that resulted in closer proximity to Margit.

I am just going to crank up the falling punishment so that he couldnt possibly think its worth running off it to avoid repeated actions. He is going to have to learn to do something eventually. Maybe I will crank up the repeated action penalty too, and have the falling scale off of the remaining moves as though he did just stand there for the entire remaining duration.

I am going to give it another chance, since I cannot quite pin point when my checkpoints were generated, so I want to see if I just cached some bad settings or something...