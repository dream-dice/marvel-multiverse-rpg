DESCRIPTIONS = {
"d": """Captain Dice here, helping you to activate my power `d616`
This is how you roll your dice, the D1, D2 and DM dice to be precise.
You can run `!cap d616` or `!cap d` and I will create a new Pool of dice for you.

I you already have a Pool, then you might be looking for more info on my pool power `!cap help pool` or on the `!cap trouble` power to apply trouble.

You can combine this with your Ability score, amount of Trouble, and your VS Target.
This does not change the values in your Pool.
`!cap d616 ability 3` or `!cap d a 3` to add an Ability score of `3`.
`!cap d616 trouble 2` or `!cap d t 2` to roll with 2 Trouble.
`!cap d616 vs_target 12` or `!cap d v 12` to compare your total with a VS Target.

You can combine these extra parameters in any order.
`!cap d616 ability 3 trouble 2 vs_target 12` will combine all three.""",
"p": """Captain Dice here, helping you to activate my power `pool`
If you already have a Pool of dice, then you can see it with this power.

If you were looking to apply trouble you can use the trouble power, learn more with `!cap help trouble`.

You can combine this with your Ability score and your VS Target.
This does not change the values in your Pool.
`!cap pool ability 3` or `!cap p a 3` to add an Ability score of `3`.
`!cap pool vs_target 12` or `!cap p v 12` to compare your total with a VS Target.

You can combine these extra parameters in any order.
`!cap pool ability 3 vs_target 12` will combine all three.""",
"t": """Captain Dice here, helping you to activate my power `trouble`
If you forgot to apply all your Trouble then use this command to reroll for Trouble.
If you are totally lost and want to use a certain set of dice, use my set power, for more info `!cap help set`.

You can reroll with Trouble by doing the following.
`!cap trouble 2` or `!cap t 2` which will roll 2 lots of Trouble.

You can combine this with your Ability score and your VS Target.
This does not change the values in your Pool.
`!cap trouble ability 3` or `!cap t a 3` to add an Ability score of `3`.
`!cap trouble vs_target 12` or `!cap t v 12` to compare your total with a VS Target.

You can combine these extra parameters in any order.
`!cap trouble ability 3 vs_target 12` will combine all three.""",
"e": """Captain Dice here, helping you to activate my power `edge`

Amazing you have Edge! You can reroll a specific die with Edge by doing the following
`!cap edge d1|1|d2|2|dm|m`

For example you could reroll your DM with
`!cap edge dm` or `!cap e m`

You can combine this with your Ability score and your VS Target.
This does not change the values in your Pool.
`!cap edge ability 3` or `!cap p a 3` to add an Ability score of `3`.
`!cap edge vs_target 12` or `!cap p v 12` to compare your total with a VS Target.

You can combine these extra parameters in any order.
`!cap edge ability 3 vs_target 12` will combine all three.""",
"s": """Captain Dice here, helping you to activate my power `set`

Sometimes people need to reset their Pool to a certain value, Captain Dice gets it (you villainous cheater!) we all make mistakes.
You can use this to set your Pool's value with the following
`!cap set d1 1|2|3|4|5|6 d2 1|2|3|4|5|6 dm M|1|2|3|4|5|6` on a dm `m`, `M`, and `1` are all treated the same

For example
`!cap set d1 1 d2 2 dm 3` or `!cap s 1 1 2 2 m 3` will set your dice to **D1** 1 **D2** 2 **DM** 3

You can combine this with your Ability score and your VS Target.
This does not change the values in your Pool.
`!cap set ability 3` or `!cap p a 3` to add an Ability score of `3`.
`!cap set vs_target 12` or `!cap p v 12` to compare your total with a VS Target.

You can combine these extra parameters in any order.
`!cap set ability 3 vs_target 12` will combine all three.""",
"i": """Captain Dice here, helping you to activate my power `init`
This will generate a URL for you so you can play in the browser.
I will send you a link via DM.
This link identifies you as a player.
""",
"h": """Captain Dice here, helping you to activate my power `help`
Did you do this to see if you could get help on help? One of Captain Dice's mortal enemies are Trolls!
Simply run `!cap help d616|d|pool|p|trouble|t|edge|e|set|s|init|i` to get more info on one of my powers.

Have you noticed my powers can be invoked in strange ways?
Captain Dice is am illiterate and can only read the first letter of a word (ignoring casing).
For example `d616` will also be interpreted when reading `d` or `dice`"""
}