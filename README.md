## Count projections ##
I made this to sooth my anxiety over a tight race in battleground states.
It pulls data from the NYT, who are nice enough to pause their paywall for
election business.

It then looks at each county in the states currently supported (GA, PA, NV).
Based on the current margin and percent counted, it allocates the estimated
number of remaining votes to Biden or Trump. It then tallies those up and
checks the margin of remaining votes. If the percent counted is something 
like ">98%", it sees the ">" and adds a random percentage of 1 percent. I
could average out that variance by just adding 0.005, but that feels 
arbitrary and cheap. It needs the flavor of random draw.

RE: build and stuff, just make a venv, `pip install -r requirements.txt`,
and run it from there if you want.