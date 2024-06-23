# V0.1 Fitness

First experiences seeing them just stand still and swing at each other while staring.

They were prioritizing more connections than less, so they were more likely to choose a bunch of different actions, which would mean that the priority system would take over and force that attack action to take precedence.

Only seen a couple of generations, but I feel like it would be best to change the fitness earlier over later.
My ideas would be to take away the penalty from the Tarnished for taking more damage than Margit, but increase its reward from coming out on top. Also slightly incentivizing it to stay alive, but not by a ton, because I dont want it running away from a fight.

# V0.2

Turns out I am storing fitnesses not by integers, so its making these logs impossible.

So end of first huge run, got through 11 generations. Cancelling it because Tarnished just wants to keep skating off the cliff.

He is still yeeting himself. Going to up that penalty a ton.

# V0.3

Turned down the enticingness of the black void pits. Gave linear fitness points for each point of damage that
Tarnished deals to margit. Need to tune down the connectability of Margit so he doesnt just
sit there at his spawn spamming blades. Havent seen him throw a single dagger yet...

I need to give tarnished (and maybe margit as well) a lot of points for being close to the other. And possible some points for moving around, to de-incentivize just standing outside of melee range and swiping.

Some interesting and at time exciting behavior, devolved down to staring matches while swinging meat.

# V0.4

## Changes

- Incentivized Tarnished to move
    - Giving him 0.5 points every update he chooses to move
- Invectivized his proximity to margit (Just lineraly for now, but really need to do it logarithmically)
    - Initially choosing a maximum of 2 points per update to be within 100 units of Margit, will definitely have to tune it from here.

### Changes to simulation

- Reduced duration down to 300 from 1000

## Thoughts

Try to incentivize movements that yield in attacks.

# V0.5

## Changes

- Gave incentives to Margit to approach Tarnished
- Doubling population (from 150 to 300)
- Increasing generations from 50 to 150