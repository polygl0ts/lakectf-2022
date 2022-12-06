Here you will find the cogs and wheels behind the challenge `tex-up`. Discalimer: this is not meant to be high quality code, so ... sorry

Interestingly, the challenge was designed with giving each team a sleightly different file, where the last eight characters as well as the final flag are completly different. This wasn't able to be used, lack of time/infra, so everyone got the group 1 version (random seed 1) and thus the `server.py` that was running on remote was simplified (see `diff server.py ../server.py`) although they give the same thing for the group 1 flag.

There three parts, the challenge generation, the server validation as well as flag drawing generation which are done on the server side and the utilities, which where used when designing the challenge.

## Generation

The `template.tex` file is the base template that is then filled up by `generator.py`, the true core of this challenge. This produces a `filled_template.tex` (which I renamed and moved into `challenge.tex`, limiting damage if I mess up ^^")


If you look into `generator.py`, you will find several structures that are encoded in the final challenge, like `weights` and `flags`. The main function (and only main) is

```python
generate_file(group_num:int, solved:bool=False, flagged:bool=False)
``` 

The group number defines the random seed, solved and flagged allow us to generated the solved and flagged version of the challenge (see solve folder).

## Server 
The `run.sh` is what was running on remote, a simple socat to lauch `server.py`, which is what was actually doing all th work. In it, the work validation shares code with the generator, to check the password is correct. Then is needs to generate the drawing for the flag which happens in `fonter.py`

`fonter.py` is the bane of my existance
<details>
  <summary>Find out why</summary>
  This file needs to generate the tikz \draw from a font. After looking into it for a bit, the simplest way was to transforme the font into svg's using a website and copiy them into the font directory (by hand for each letter).

  Then we parse the svg and generate the tikz equivalent. This is simple to do for lines and bezier curves (you would assume not) but not for circular arcs. The problem is that svg's use the start point, end point and radius along with 2 flags to indicate which of the possible arcs to use. Tikz on the other hand, uses start point, radius along with **the start and end angles** along the curve. And although these two set of informations are equivalent, getting prom one to the other is a PITA, involving a bunch of math.

  Did I mention all of this was self-inflicted pain, as I could have just given the flag normally, and it wouldn't have changed the challenge at all? Yeah I'm dumb. The reason I stuck to it is that the challenge started out with the flag getting drawn, so removing this kindof made the challenge moot in my eyes. It also ties together all of the challenge nicely with the \\data you drag along the whole program
</details>  
  
This takes a string and generates the corresponding tikz equivalent starting from the svg representation of the font. 

## Utilities

We also have `utils.py` which has various custom functions that I used to tune the challenge, amongst which `value(str)` which calulates the total \\p (multiple of \\np) the string will produce (useful to know if it will overflow)

Finally we have `steps.py` whose only purpose was to find the initial value of \\c, which is quite constrained if you think about it.

