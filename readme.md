I can do a d616, save that to the users
then you run !d1 t or !d1 e to re-roll with edge


d616 will roll three dice and give you the sum as well as whether iot

!capD616

USERNAME: [d1: 1, d2: 3, dm: 5] = 9

!capD616 + 1

USERNAME: [d1: 1, d2: 3, dm: 5] + 1 = 10

!capD1 e
!capD1 t

USERNAME: [d1: [1, 2] edge 2, d2: 3, dm: 5] + 1 = 11
USERNAME: [d1: [1, 2] trouble 1, d2: 3, dm: 5] + 1 = 10
USERNAME: [d1: [1, 2], d2: 3, dm: M] + 1 = 12 fantastic
USERNAME: [d1: 6, d2: 6, dm: M] + 1 = 12 fantastic success
USERNAME: [d1: 1, d2: 1, dm: M] + 1 = 12 fantastic failure

I feel like if you want to override what you last rolled then you need to do something like

!capSet [1,2] 1 2|M K

USERNAME: [d1: [1,2], d2: 3, dm: 5] + k: 1 = 10

!capValue

USERNAME: [d1: 1, d2: 3, dm: 5] + 1 = 10

!capValue username

USERNAME: [d1: 1, d2: 3, dm: 5] + 1 = 10

I think I would want an initiative as well, but perhaps that could wait

!capInit

