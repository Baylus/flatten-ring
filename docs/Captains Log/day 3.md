# V0.7 Notes

So woke up this morning to the run. Again, really unimpressive since the bots keep doing the same action over and over and over again. Tarnished is just dashing through Margit and bashing his head against the wall behind him. Going to have to punish repeated moves even harder.

# V0.8 Notes

### Changes

- Change how we are punishing repeat actions to ensure it is being identified correctly
- More seriously punish repeat actions, with increasing penalty everytime it is done.
- Punish Margit anytime his primary action is attack two updates in a row.
- Adding checkpointing functionality, so I can possibly show off the growth of the algorithm later
- Add directories for each generation's population for the game states
- Fixed the output for Margit so he is allowed to cast daggers now. May change later if this just makes him spam daggers all day long, but hopefully a mix of complex tarnished movement will make it harder for him to get consistent points from spamming it. Might need to add back the penalties for taking damage so tarnished recognizes these daggers as a danger.
- !!!!!!!!!!!!! Fixed it so that they are co-evolving where they will take turns training, instead of spending 50+ generations with tarnished training until margit can finally start to learn.
- Huge punish for doing nothing

### Results

So, we got to generation 62 of the co training, and both were exhibiting signs of preferring to do nothing. I think I realized what the problem was, when I setup the no-action penalty, I wasn't actually subtracting from their penalty. Which meant that they were only punished more severely from not doing anything if they then started doing the same actions over and over. So essentially they elected to do nothing rather than risk attempting new moves and repeating one.

I might change it where I only punish repeated moves if they had done that move the last 3 turns, but im not sure. Maybe even be specific enough and define numbered rules that say that certain action types can only be done X number of times, but actions of another kind can be done Y times before incurring a penalty.

For now, I am just going to update the fitness function to include that behavior of penalizing no actions, and up the amount of fitness points that damaging gives. I am also considering the value of Margit's daggers right now. They are long enough range to destroy tarnished, so when margit spams them, tarnished dies insanely quickly. I dont want to have to move them farther apart, but the daggers arent in a healthy state so I am going to remove them again until I decide if I want them enough to just lower their range. I want to encourage them to get closer to each other for right now.

## V0.8.1

### Changes
- Fixed penalty for no action where it will correctly decrement fitness when this condition is found.
- Removed daggers from NEAT output
- Increased reward for dealing damage