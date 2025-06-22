import collections
from functools import cmp_to_key

# import all of the names in lower case
with open("all_names.txt",'r') as f:
    names = [l.strip().lower().replace("-", "") for l in f.readlines()]

# remove names with duplicate letters
names = [n for n in names if len(n) == len(set(n))]

# vowel density function
VOWELS = "aeiouy"
def rho_v(name):
    v = len([i for i in name if i in VOWELS])
    return v/max(len(name),1)

# density for each name
densities = collections.defaultdict(set)
for n in names:
    densities[rho_v(n)].add(n)

vowels_available = 6
letters_needed = 25 # we can't do 26, but 25 works

# are two sets disjoint?
def valid(s1, s2):
    return s1 & s2 == set()

# ordering comparison function
def comp(name, other):
    if other == 0:
        return -1
    if name == other:
        return 0
    r1 = rho_v(name) - rho_v(other)
    if r1 < 0 or r1==0 and name < other:
        return -1
    return 1


L_MAX = 26
# list the possible names that can be added to a set
def candidates_to_add(letters_used, vowels_available, letters_needed, peers, last=""):
    current_rho = (6-vowels_available)/max(1,L_MAX-letters_needed)
    rho_max = vowels_available / max(letters_needed,1)
    candidates = [n for n in peers if valid(set(n), letters_used) and comp(n, last) == 1]
    for rho, names in densities.items():
        if current_rho < rho <= rho_max:
            candidates.extend( [n for n in names if valid(set(n), letters_used)])
    return sorted(candidates, key=cmp_to_key(comp))

# start with an empty set to handle
# the elements are (letters used, vowels needed, letters needed, candidate extensions)
queue = [(set(),6,L_MAX, [n for n in names if not (set(n) & set("aeiouy"))], "")]

possibles = {} # 25-letter families
handled = set() # we don't want to handle a set more than once

while queue:
    c, v, l, peers, names = queue.pop()
    nn = frozenset(names.split("-"))
    if nn in handled:
        continue
    else:
        handled.add(nn)
    last = names.split("-")[-1]
    candidates = candidates_to_add(c, v, l, peers, last=last)
    if len(candidates)==0:
        nc = names.count("-")
        lc = len(names) - nc
        #if nc >= 8 or lc >= 24:
        if lc == 25:
            possibles[ frozenset(names.split("-"))] = (nc, lc)
    for i, ci in enumerate(candidates):
        cn = c | set(ci)
        vi = 6 - len(cn & set("aeiouy"))
        li = L_MAX - len(cn)
        peers_i = [j for j in candidates[i+1:]]
        queue.append((cn, vi, li, peers_i, names+"-" + ci))

for p, v in possibles.items():
    ps = "-".join(p)
    lc = len(ps) - ps.count("-")
    print(f"{ps[1:]}")
