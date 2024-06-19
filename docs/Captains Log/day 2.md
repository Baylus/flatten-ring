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
