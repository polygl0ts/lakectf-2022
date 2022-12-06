# Challenge
To try the challenge, you only need `challenge.tex`, maybe the associated `chall_description.txt` and the python file `server.py` is what remote was running

The rest of this is an author point of view write up of the `tex-up` challenge from the 2022 LakeCTF. If you are interested by the behind the scenes or just want the solved versions, look into the corresponding directories.

Here I will explain how to approach this challenge in a way that can (hopefully) also extend to other revs, and hopefully help out any beginners. I will also explain some design decisions as well as the intended solve. But first of all I would suggest you give it a try if you haven't already ^^

# General design decisions
My aim was to make an accesible challenge, something that didn't require a lot reversing knowledge/experience, that you could just grind through little by little, not really getting stuck. This meant a pure logic puzzle (instead of any more complex state machine) was what a chose.

The feedback I have gotten indicates this aim was acheived (and if you have any feedback of your own to give, please do contact me!)

This is also the reason only one (very common) package is used, to try to make sure anyone can attempt the challenge and limited myself only to tex/latex primitives. Latex has the advantage that it isn't (supposed to be) a programming language. So the set of primitives I used are simple: if-else and interger "variables" with only addition, multiplication and division. This means anyone attempting it shouldn't be unfamiliar with the operations being done (although the sytax might be harder to grab)


# How to start

Here I decribe how one mighr approach a rev like this

## Starting out
One of the first thing you see when opening the file is 
```latex
\newcount\uni
```
These count are the main tool of this challenge. They are 32 bit signed integers, in which we can store values and do comparisons, addition and multiplication.

One of the informations I should have given in hindsight is that you can print the value in a count named `\x` by doing `\the\x` (if the file compiles of course)

But the rest of the file might seem daunting (1300+ lines), so let's start at the beginning: the end of the file! (aka the main body) Here we see
```latex
\begin{document}
    \prep
	
	%Enter the work you need to send should be written here in the following format (character then eval). This would be the work "wtf" 

	\textw
	\eval

	\textt
	\eval

	\textf
	\eval

	\verify
	
	\flag
\end{document}
```
Now this is an incredibly common scheme, and `eval`, `verify` and `flag` should immediatly raise some flags (pun intended). 

Indeed, having a initial state (set in `\prep` here), a set of inputs that are evaluated (in `\eval` here) and then a verify (`\verify`) that you have to pass in one form or another is the core of an incountable number of revs (and also all of debugging). 

## Verify this
Each of these lines call a command defined by a `\newcommand`, which can be thought of the tex way of defining a function or macro. We continue our exploration by looking into the key part of the file :`\verify` (only 30 lines)

```latex
\newcommand{\verify}{
	\ifnum\p=2075748138 
	\else \err \fi
	
	\ifnum\ucount=7
	\else \err \fi
	
	\ifnum\c=4
	\else \err \fi
	
	\ifnum\mmema<0 \err \fi
	\ifnum\mmemb<0 \err \fi
	%... 
	\ifnum\mmemo<0 \err \fi
	\ifnum\mmemp<0 \err \fi

	\ifnum\musts=17
	\else \err \fi
	
	\ifnum\e>0 \errmessage \fi
}
```

Immediately we can look at the last line. If you had tried to comiple this file, you would had an error message saying something about "missing }". No such } exists and just removing the `\errmessage` is sufficient to make the file compile (although this does not directly give us the flag sadly T_T). Thus we see that `\e` must stay at 0. Where does `\e` appear? Well in very few places actually (4 I believe). Once at the start to create it with `\newcount\e` (l.4), once where it is set to 0 with `\e=0` in `\prep`, once in the `\verify` we are looking at and finally once in  
```latex
\newcommand{\err}{
	\advance\e by 1
}
```
Ahah! Suddenly `\verify` (and the rest of the programm) makes more sense. We can rephrase the challenge as "finding the input that makes us dodge all the `\err`"

### Other counts
Now let us look into the counts we see in the `\verify`. `\p` is set to 1 (not 0!) in `\prep` but also in `\eval`, and the only other time it appears is at the very beginning of `\eval`: 
```latex 
\multiply\p by \np
```
So `\p` is the result of a multiplication of `\np` it seems, with value 2075748138. 

`\ucount` starts at 0 and is only incremented once in `\eval`, so we need to pass at that spot 7 times it seems (since `\ifnum\ucount=7 \else \err \fi`)

The `\musts` variable starts at 0 and is only incremented once, in the `\must`. Each time this happens, it seems like one of the `\mmemX` counts could be decremented, and we know these must never be under 0 (see the `\verify` posted above)

Finally `\c` appears everywhere. So it must be an important value, especially since it most of them are comparisons. It is also set to a seemingly arbitry value: 725258376. Also these comparisons are for other just as random values. But if we look closely, it is actually modified only in one spot 
```latex
\newcommand{\step}{	
	\ifodd\c
		\multiply\c by 3
		\advance\c by 1
	\else
		\divide\c by 2
	\fi
}
```
This is the Collatz conjecture, also known as 3x+1. And the name `\step` and the fact it is only called once at the very end of `\eval` gives us a reasonable guess: `\c` is the value used to know how many times `\eval` has been called (similar to a loop counter)

## Before we continue

After this I will explain the solve path in much less detail, so if you didn't know where to start or just gave up before getting this far, I would encourage you to give the challenge (or should I aŝay puzzle) another attempt with all this extra knowledge in your pocket, before it gets "spoiled" by the full solution

I put this image here to both encourage people and prevent them from getting inadvertently spoiled by the solution below
![](motivation.webp)

# Solve path

Here I will explain the solve path I set out

## Starting out

We know that we need to end up with `\c` equal to 4, and since calling eval with any value `\c` lower then 5 creates an error (l.133), we know the final work is of length 55.

If we look into where `\ucount` is incremented, we can see it only happens if `\np`is 1, which happens iff the character is `'_'`. Also we get an error if the `\c` is not a given value for every value of `\ucount`. This gives us the positions of the seven `_` in the password.

l.232 tells us the first character is a 'w'

Although the sytax is obscure, `a gives the ordinal of the character 'a', so line 246-255 tell us that position 45 and 46 are 'a' and 'b' respectively.

Now we can see that the last eight characters obey special rules:
 -  they can't contribute to `\musts` 
 -  they must be in increasing `\np` order
 -  they can only be alphabetic characters
 -  their `\np` multiply to 2075748138 

An observation that all alphabetical characters have prime `\np` values yields us 'noolwbvf' as the last eight characters.

## A bit a flags

Before we continue I will discuss several "flags"  that characters may have set to 1, and that do not affect the last eight characters:
- `\rX` may be set to 1. This means that it can only come right after a character with the same `\np` as the character's `\rValue` (that is set at the same time as `\rX`)
- `\nX` may be set to 1. This means that it can only come right before a character with the same `\np` as the character's `\nValue` (that is set at the same time as `\nX`)
- `\even` or `\odd` gives the necessary parity of `\c` when this character is. (Note: we can see that since 'r' has both of these, it cdannot appear in the work)
- `\eq` says the same `\np` is before it as is after it

I will also mention the `\isOn` count, that is set to 1 at every '_'. It will be put to 0 unless the character has the `\cOn` flag. The `\aOn` flag neccesitates `\isOn` be 1.

Finally before we can continue we can observe that the `\mmemX` give us the exact count of certain characters, so if you see that "we know that '8' appears exactly once", this is how.

## Continuing wording this out

Now let us focus on the 3rd word. l.162 tells us they multiply to 360, and there is only a few sequences of charcter that multiply to that number, and all contain an '8'. Now '8' can only come after '_' (with `\rX`) and must be at postion 12. 

Now l.138 to 144 tell us that postion 13 to 15 must be numbers, telling us the characters there must be a permuatiation of '357'. Now `\rX` tells us '5' must come right after '3' and since 3 has the `\aOn` flag, and only '8' has the `\cOn` flag, 3 must be after '8', giving us '8357' as the 3rd word.

Now l257 to 328 give us a number of postions that share `\np`. One of them is position 13. Since '3' has `\even` and 'e' has `\odd`, this allows us to place them at the correct positions giving us:

```w3????e_??e_8357_?3?_???????????_?3???????e?_ab_noolwbvf```

Now another position is position 14, that gives us 'n'/'5'. Now we know '5' appears twice and always after '3'/'e', and there is only one postion left for this allowing us to place them all. We thus get 

```w3????e_??e_8357_n3?_??????n??n?_?3?n?????e5_ab_noolwbvf```

Since `\sum`, that gives the sum of the `\np` of the last 3 characters allows us to place 'w' in position 19 and 'i' in position 41, impliying also 'i' in position 29. This (using `\sum`) in turn gives us 9 in postion 31.

'x' must appear and is between a '3'/'e' and a 'n'/'5', which can only be position 35. '1' must also appear right after an '3'/'e' and the only possibility is position 3. 

`\sum` tells us the second word must start with either 'jj', 'bq', 'ht' or 'rw' (or their opposite).
We know that 'r' cannot appear, and l.331 tells us 2 identical characters can never follow each other. We can also know that `\nX` tells us that 'q' must be followed by 'p'.
Since 't' must follow '_', the know the second word is 'the'.

To resume we now have 

```w31???e_the_8357_n3w_??????n?in9_?3xn????ie5_ab_noolwbvf```

## Mustering a finsih
We can get that 'c0me' must appear, and positions 4 to 7 are the only ones possible, giving us 'w31c0me' as the first word.

The fact that 'ogi' appears gives us positions 39 to 41. 
The fact that '74n' appears with only one 'n' fitting the bill allows us to obtain

```w31come_the_8357_n3w_????74n?in9_?3xn??ogie5_ab_noolwbvf```

The different strings '7s7', 'ou7' and 'olo' must appear. The fact only 3 'o' appear, and no space for 'olou7' allows us to place all of these giving us 

```w31come_the_8357_n3w_ou7s74n?in9_?3xnologie5_ab_noolwbvf```

Finally 't' must appear a second time after '_' giving us 't3xnologie5' as the sixth word. The final unknown character is obtained by the fact anny other character make `\p` overflow, and is 'd' giving us the work 

```w31come_the_8357_n3w_ou7s74ndin9_t3xnologie5_ab_noolwbvf```

After giving this to remote, we obtain a 
```latex 
\newcommand{\flag}{

            Well done!\\

    \resizebox{\textwidth}{!}{%
    \begin{tikzpicture}
		
\draw[ultra thick] (0.0, -7.1729) -- (0.0,-0.0);
\draw[ultra thick] (0.0, -0.0) -- (5.229500000000001,-0.0);
\draw[ultra thick] (5.229500000000001, -0.0) -- (5.229500000000001,-0.8789);
%...
\draw[ultra thick] (94.1583, -4.5567) arc (-1.8909555217035716 r: -2.7147868648818556 r:1.2791000000000001);
\draw[ultra thick] (93.3965, -3.8720999999999997) .. controls (93.2158,-3.4814000000000003) .. (93.2158,-2.7441);

        	
	\end{tikzpicture}
    }
}
```
We can replace the `\flag` with it, compile and see `EPFL{on9feev7ctu8nk}` get printed out

The solve path I give is by far not the only one, some things can be guessed, bruteforced or simply done in a different order. I simply want to show that doing it purely logically **is** possible.

## Final words


I would like to give my most heartfelt thanks to my challenge tester syn, who suffered and fell into every hole my challenge had just so I could patch them up. Without this, my challenge would have been a much worst experience, if even playable at all! 

I would also like to thank all the players who took the time to try my challenge, give me feedback or simply read this write up. I wish you all the best.