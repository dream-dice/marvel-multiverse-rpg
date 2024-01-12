# Captain Dice

[!Captain Dice](https://th.bing.com/th/id/OIG.pLqHEwrlDGh7ZXTyHuTM?pid=ImgGn)

A Discord bot to help you roll dice for the Marvel Multiverse RPG game

## Introduction

Hey there, it's Captain Dice here 
Let me tell you about my powers
My powers follow a similar pattern

`!cap POWER PARAMETER_1 VALUE PARAMETER_2 VALUE`

Most powers and parameters can be abbreviated, and the parameters can be in any order
The following is a list of my powers, just call on my and I will help you enjoy your game

## Help

Captain Dice can help any time you need it
Pick the power you need more info about

`!cap help|h d616|d|pool|p|trouble|t|edge|e|set|s|init|i`

### Examples

* You want to know about rolling a `d616` just ask Captain Dice `!cap help d616`
* Are you having trouble with trouble? `!cap h t`

## d616

I can roll dice for you and store them in your dice pool
I will remember those for you so you can use them for later
There are some convinces as well
* You can also compare to a target
* If you are experiencing trouble I can apply that for you
* I can do some quick maths and add your abilities scores as well

You will roll your edge separately, if you tried to let me do it I might do it wrong!

`!cap d616|d trouble|t <trouble count:number> vs_target|v <vs target:number> ability|a <ability:number>`
`trouble`, `vs_target`, and `ability` are optional

### Examples

* You are trying to sneak into a dark building, it is hard to see giving you a single trouble, you have to beat a target of 12, but you have a decent agility adding 2 to the score, simply run `!cap d616 trouble 1 vs_target 12 ability 2`
* You are going to knock out a guard who isn't looking your direction, you have to beat a low target of 8 and your melee allows you to add 9. Is your Narrator actually going to make you roll? You should join my table instead! I got your back, you could do this `!cap d a 9 v 8`

## Pool

If you want to check your current dice pool just ask
Remember all those other convinces for `d616`? You can use some of those here and they won't alter the dice you rolled
`!cap pool|p vs_target|v <vs target:number> ability|a <ability:number>`

### Examples

* You rolled a `d616` already, and just want to see your current dice before deciding if you want to use your Karma to add some edge. Easy `!cap pool`
* Did you forget your calculator and want to add your ability score? Never fear for Captain Dice brought his! `!cap p a 3`
* Are you wanting to double check someone else's dice because you forgot to write it down and don't want to scroll back? Easy `!cap p n @Ms Marvel`
* Can't be bothered working out if you have beat the target value, or you just want to confirm that it was sucess because your Narrator is not good at those sort of things? Why didn't you say so!? `!cap p v 12 a -1`

## Trouble

Did you roll and forgot that you had some trouble? Or did you try to cheat and "forget", you filthy villain!
Fret not, I can help by updating your pool with trouble
Those conveniences can be used here as well

`!cap trouble|t <trouble count:number> vs_target|v <vs target:number> ability|a <ability:number>`
`vs_target`, and `ability` are optional

### Examples

* You rolled, but your Narrator forgot to mention you have trouble because the bats in the cave keep squawking (sounds like the wrong universe, but oh well). Say no more `!cap trouble 1`
* Wait, the cave also collapsed and your butler is knocked out cold! Your Narrator sounds like a nasty person! `!cap trouble 2` don't apply the one from before again!

## Edge

So you want to apply edge to one of your dice in your pool.
That's fine! I know how to do that and can help you.
You will want to run edge for each edge you have available, assuming your Narrator will let you stack edge.

`!cap edge|e <die:[d1, 1, d2, 2, dm, m]> vs_target|v <vs target:number> ability|a <ability:number>`
`vs_target`, and `ability` are optional

### Examples

* You rolled a 2 on your `DM` dice and wish to try getting a better score, maybe even a fantastic one, using your Karma! `!cap edge dm v 12 a 2`
* Another hero has come to help you give you their magnifying glass to find clues, and you have great hearing. That sounds like you will need to roll 2 edges. You will need to roll one edge for your `D1` with `!cap e d1` and another for your `DM` with `!cap e dm 16 a 1` no need to check the target and add ability on the first edge roll.

## Set

Even Captain Dice makes mistakes or perhaps you are a villain and cheated!
Sometimes Captain Dice forgets things, usually due to his universe getting wiped and upgraded and forgets to back up his memory
Only a server admin can set the dice for someone else, Captain Dice doesn't condone cheaters and trolls in his server
Whatever the case Captain Dice is here to correct any evil wrong doings

`!cap set|s d1|1 <value:number> d2|2 <value:number> dm|m <value:number or m> trouble|t <trouble count:number> vs_target|v <vs target:number> ability|a <ability:number>`
`trouble`, `vs_target`, and `ability` are optional

### Examples

* I had a whoopsie and lost your dice pool, sorry about that, even Captain Dice isn't infallible. You can put your values back into the pool with `!cap set d1 3 d2 5 dm m`
* Your Narrator didn't tell you to roll d616, just roll trouble! Narrator, you can reset it for them `!cap set n Dr Doom d1 2 d2 3 dm 2`

## Initiative

Captain Dice is a little tired now, but this is the general idea

`!cap init|i start|s`
`!cap init|i join|j ability|a <ability:number> edge|e`
`!cap init|i leave|l ability|a <ability:number> edge|e`
`!cap init|i next|n`
`!cap init|i previous|p`
`!cap init|i turn|t <name or username:string>`
`!cap init|i view|v`
`!cap init|i end|e`

## My Narrator

My Narrator, Luke, would like to say a few words.

This is a small project and has been fun to make. If you find any issues with it then please let me know by raising a GH issue.
If you want to have a go at fixing some of this yourself then follow these instructions and raise a PR.

```bash
# Create the heros data
echo "{}" > heros.json

# To install dependencies
pip install -r requirements.txt

# To run the tests
python captain_dice_test.py
python power_test.py
```

This project has a loose definition for tests, if you want to have a stab at making something with pytest, or similar, feel free to add those.
Everything is themed super hero style, instead of users we have heros, and instead of commands they are powers. It adds some flavour to the code and is both enjoyable and readable (sort of), with that, try to keep to the spirit of the code. Not enough code bases have fun anymore!

## Copyright and License

MIT License

Copyright (c) 2014 Luke Preston

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Marvel Copyright

This is an implementation for the [Marvel Multiverse RPG](https://www.marvel.com/rpg) to run in Discord.
The rules are owned by Marvel (or Disney I guess) and can be found on their website (buy the book like I did, it is gorgeous!).
I would like to add a `!cap power name` and other rule searching tools, but you should buy the book to find the rules because they put so much hard work into it. This and I don't know whether I'd get in trouble, what are the rules on something like a wiki?

## Captain Dice

This version of Captain Dice is an invention by me and the image was generated using Dall-E. If he is original awesome, but I doubt it. If you would like to use him in your games or works of fiction please do and let me know, I'd love to hear about it.

### Who is Captain Dice?

Captain Dice is a mortal given the powers of the Dice Gods.

Murphy Steel was playing D&D, and at the same time so was the Dice God Alea. Both of them were on a terrible nat 1 streak.
Alea screamed in anger,

> Are you kidding me! A Nat 1 for the third time in a row!

Alea hurled their dice across the room, to the Dice Jail dimension where Murphy Steel lives. One of the d6's landed under the unsuspecting hand of Murph. As they picked up this dice to roll, they felt a power surge through their veins. They threw the dice and it landed... On another nat 1! Everything went dark. As the world came back into focus Murph had changed, their head became a d6, that when rolled, gives a different power depending on the score (with 1 being fantastic). Murph was now hell bent on reclaiming the freedom for all dice-kind living in Dice Jail, with a mission to exact revenge on the Dice Gods that cast aside so many dice before.
