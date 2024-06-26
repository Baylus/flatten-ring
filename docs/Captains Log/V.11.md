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