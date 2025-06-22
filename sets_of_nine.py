import collections
import time
import itertools

print(time.strftime("%H:%M:%S", time.localtime()))

with open("all_names.txt",'r') as f:
    names = [l.strip().lower() for l in f.readlines()]

# remove duplicates
names = [n for n in names if len(set(n)) == len(n)]

# list the names by sets of letters
names_by_letters = collections.defaultdict(list)
for n in names:
    names_by_letters[frozenset(n)].append(n)

# All of the name sets that don't have an A, don't have a B, etc
# I'm using this as a global variable, because I'm lazy.
sets_excluding = collections.defaultdict(set)
for letter in "abcdefghijklmnopqrstuvwxyz":
    for s in names_by_letters:
        if letter not in s:
            sets_excluding[letter].add (s)

best = 0
nines = set()

def print_group(lst):
    for p in itertools.product(*lst):
        l = len( "".join(p))
        print( ", ".join(p), l)

def recursive_groups(current_group, possible_extensions):
    global best
    global nines
    for p in possible_extensions:
        next_poss = set(q for q in possible_extensions)
        for letter in p:
            next_poss &= sets_excluding[letter]
        if len(next_poss) == 0:

            if len(current_group) == 8: # plus [p] makes 9
                n = (names_by_letters[s] for s in current_group + [p])
                for pn in itertools.product(*n):
                    nines.add( frozenset(pn) )
                    print (len(nines), "-".join(pn))
        else:
            recursive_groups( current_group + [p], next_poss)

def is_valid(s):
    t = 0
    ss = set()
    for i in s:
        ss |= i
        t += len(i)
        if len(ss) != t:
            return False
    return True

no_vowels = sets_excluding['a']
for v in "eiou":
    no_vowels &= sets_excluding[v]
# there are only a handful of these.
for i in range(len(no_vowels), 1, -1):
    for s in itertools.combinations(no_vowels, i):
        if is_valid(s):
            pe = set(names_by_letters.keys())
            for j in s:
                for k in j:
                    pe &= sets_excluding[k]
            recursive_groups(list(s), pe)

print(time.strftime("%H:%M:%S", time.localtime()))
