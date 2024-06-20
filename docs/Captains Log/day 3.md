# V0.7 Notes

So woke up this morning to the run. Again, really unimpressive since the bots keep doing the same action over and over and over again. Tarnished is just dashing through Margit and bashing his head against the wall behind him. Going to have to punish repeated moves even harder.

# V0.8 Notes

## Changes

- Change how we are punishing repeat actions to ensure it is being identified correctly
- More seriously punish repeat actions, with increasing penalty everytime it is done.
- Punish Margit anytime his primary action is attack two updates in a row.
- Adding checkpointing functionality, so I can possibly show off the growth of the algorithm later
- Add directories for each generation's population for the game states
- Fixed the output for Margit so he is allowed to cast daggers now. May change later if this just makes him spam daggers all day long, but hopefully a mix of complex tarnished movement will make it harder for him to get consistent points from spamming it. Might need to add back the penalties for taking damage so tarnished recognizes these daggers as a danger.
- !!!!!!!!!!!!! Fixed it so that they are co-evolving where they will take turns training, instead of spending 50+ generations with tarnished training until margit can finally start to learn.