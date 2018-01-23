#!/usr/bin/env python3

RULE = [86 >> i & 1 for i in range(8)]
N_BYTES = 32
N = 8 * N_BYTES

def next(x,n=N):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= RULE[(x >> i) & 7] << i
  return y


def reverse(y):
  valid = []                            # declare a valid array since the preimage of a value according
                                        # to the rule can be the result of 4 different input
  
  ycell = y & 0b1                       # get the last bit
  for j in range(len(RULE)):            # for every rule 
    if RULE[j] == ycell:                # check if the result match our expected value
      valid.append(j)                   # add the value as valid
  
  for i in range(1, N):                 # for every bit in y (should be 256/258 bit)
    newvalid = []
    for v in valid:                     # for every previous valid value
      ycell = (y >> i) & 0b1            # get the y target cell (1 bit)
      xcell = (v >> i) & 0b011          # get the x target cell (2 bit out of 3) from the previous valid
      for j in range(len(RULE)):        
        if RULE[j] == ycell:
          if (j & 0b011) == xcell:      # check if the result match our target one
            v |= (j << i)               # "add" our match to the already valid one
            newvalid.append(v)          # update the valid list
    valid = newvalid

  x = None
  for v in valid:                       # for every valid 256 bit value
    if (v >> 256) == (v & 0b11):        # check if the 2 msb are equals to the 2 lsb
      x = v                             # we found our previous x 

  if x is None:
    print("Error no valid integer!")
    exit(1)
          
  x = (x >> 1) & ((1 << N)-1)           # fix our x accordingly
  return x


#values from the keystream
l = [37450399269036614778703305999225837723915454186067915626747458322635448226786,
100622653914913501834016856771730649612864879431221716975620828032766397709367,
30565965598786057661696410930164890805958057693583615925316094177133280560720,
103573567656710023306192266386049368645675636074643938780342918703636500548568,
28509515191943075455625810763252620824333983857860790449437105502768741406797,
87537284303558144156631836069957764733725337398790274426598731583572530580725,
44716782229954850790645591045965014941901610454109696374926338641251779999508,
82447195088123999846117257332504341489187184956851468679950679621555020370358,
66901809945344917781374326984783824023739095925450107364519045210557505092242,
114067135427233025222698564170101622975443616062287263643297019211756836637438,
2884516673931260333907001189797696957250433333677043264446344069828816140802,
5289872070696193140037770894656341630909797897334877860267293814493245082375,
69023781971677661808035522723190242410127104903614192265146189107040377117065,
107613775284599791185420266567845597101440592435618453390961765397563059875550,
16357066489843479901612193664610011889060446509506296924636891723597443981890,
57186523063755103597333412726627151956381596060761612487300750841069890516967]


# try to reverse the keystream
for i in range(len(l)-1,0,-1):
  next(l[i-1])
  a = reverse(l[i])

  if a != l[i-1]:
    print('Error in keystream')
    exit()
  print('OK ---',i)
  
print("YOU ROCK! Keystream reversed.\nReversing 128 bootstrap rounds...")

# after this you should go 128 block reverse and get the PRNG seed aka FLAG
curr = l[1]
for i in range(0,129):
  curr = reverse(curr)

print("128 rounds done.\nPrinting flag...\n")
print(curr.to_bytes(N_BYTES,'little').decode())
