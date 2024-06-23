# V0.5

Waking up this morning, the run had stopped, not sure if it was because my monitors turned off or if
it was the fact that VScode had reset somewhat. Not sure what causes it, but it reset the command line and probably cancelled
the run because of it.

Rerunning this morning, on gen 6, the tarnished is just constantly spinning, and Margit will only ever do one action
on any given population. I need to try to change my fitness function and possibly my configuration in order to get them
to try to do new stuff. Ideally they wouldnt do the same action two updates in a row, which would encourage them to try
stuff that would yield them better results.

## Maybe consider for future

Giving better fitness for actions taken that are not the same as the one that was done previously
- This may have issues since we are still asking the network for actions even on updates where it is locked into a specific action.
Change the fitness function to only give points for movement if the opponent got closer during that update.
- Consider whether it matters if points should be awarded in this scenario if the character did not participate in movement that yielded in that distance shrinking. e.g. margit getting points for tarnished running up to him when margit was spamming attacks.

# V0.6

## Changes

### Fitness

- Decreasing reward for just moving around.
- - Giving Margit this reward too
- Increasing the linear multiplier for damage dealt to opponent (not %, just flat)
- - Giving Margit this fitness score improvement that wasn't there before.
- Decreasing the population back to normal levels while actively testing

### Configuration

I gave the details to ChatGPT to help explain some changes I can make to my configuration file, and these were the changes made and reasons why

- activation_mutate_rate  = 0.1 -> 0.2 # Slightly increased to encourage variety
- bias_mutate_power       = 0.5 -> 0.8  # Increased to encourage meaningful changes
- conn_add_prob           = 0.5 -> 0.1  # Reduced to ensure fewer connections initially
- conn_delete_prob        = 0.5 -> 0.1  # Reduced to prevent excessive deletion
- node_delete_prob        = 0.2 -> 0.1  # Reduced to prevent excessive node removal
- weight_mutate_power     = 0.5 -> 0.8  # Increased to encourage meaningful changes
- weight_mutate_rate      = 0.8 -> 0.6  # Balanced for exploration

## Notes

They are changing their behavior somewhat, which is a good sign. Tarnished seems to be doing a better job with getting closer to margit, and has even shown signs that he can alternate actions and not just hold down the same buttons to simulate complex movement.

Thinking itd be best at this point to let it go a little longer to see if letting things run their course this long could be beneficial, and then plan on changing the movement reward to only happen if they were moving towards the other.

# V0.7

## Changes

- Rewarding them for choosing a different move than the previous update.
- Increasing the points of dealing damage to each other again.
- Upping the reward from moving by a lot more, but it only rewards when they are moving closer to each other


### Misc

I realized that I was not pruning the outputs of the natworks for the duplicate bad actions, like holding left and right at the same time, so I am fixing that so that it no longer duplicates it, to lead to unexpected behavior

- Pruning out the actions before I am storing it in the game state, so there will be no record of them
