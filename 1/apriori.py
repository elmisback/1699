"""apriori.py: a simplified A Priori Algorithm implementation."""
__author__ = 'elm139'

import sys

def combinations(iterable, r):
    """Courtesy of the itertools documentation.

    Note: swapped tuple() for frozenset()
    """
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield frozenset(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield frozenset(pool[i] for i in indices)

def all_items(i_set_iter):
    """Returns a set of all items in an iterable containing itemsets.
    """
    s = set()
    [s.update(i_set) for i_set in i_set_iter]
    return s

def singletons(i_set):
    """Returns a frozenset of singletons from i_set.
    """
    return frozenset([frozenset([item]) for item in i_set])

def gen_rules(i_set):
    """Returns a set of rules that could be constructed from an itemset.

    A rule is a tuple of two itemsets.
    """
    # Strategy: generate all combinations up to half the size of our itemset.
    # Use each combination as a premise and its complement as an implication.
    return set([(frozenset(p), frozenset(i_set - p)) 
                    for i in xrange(1, len(i_set)/2 + 1) 
                    for p in map(frozenset, combinations(i_set, i))])

def main():
    infile, outfile, msp, min_con = sys.argv[1:]
    msp = float(msp)/100 # minimum support percentage
    min_con = float(min_con)/100 # minimum confidence
    
    f = open(infile, 'r')
    transactions = [frozenset(map(int, t.strip().rstrip(', ').split(',')[1:])) 
                    for t in f.readlines()]
    f.close()

    if not transactions: 
        raise Exception("Problem reading input: no transactions found.")
    
    CFI = set() # Candidate Frequent Itemset Set (initialized to all items)
    CFI = singletons(all_items(transactions))
    print "Found %d items." % len(CFI) 

    def support(i_set, _memo={}):
        """Returns the support percentage for an itemset.
        """
        assert isinstance(i_set, frozenset)
        try:
            # memoized 
            return _memo[i_set]
        except KeyError:
            count = len(filter(lambda s: s >= i_set, transactions))
            ret = float(count)/len(transactions)
            _memo[i_set] = ret
            return ret

    def confidence((X, Y), _memo={}):
        """Takes a rule and returns the confidence percentage.
        """
        assert isinstance(X, frozenset)
        assert isinstance(Y, frozenset)
        try:
            return _memo[(X, Y)]
        except:
            ret = support(frozenset(X | Y)) / support(X)
            _memo[(X, Y)] = ret
            return ret

    VFI_L = [] # Verified Frequent Itemset list of (support, Itemset) tuples
    rules = [] # List of (support, confidence, (X, Y)) tuples, 
               # where X and Y are itemsets and X => Y
    i = 1
    while CFI: # there exist candidates
        print "%d candidate itemsets." % len(CFI)
        VFI = frozenset([i_set for i_set in CFI 
                            if support(i_set) >= msp])
        print "Verified %d itemsets." % len(VFI)
        # get all sets of size (i + 1) composed of the remaining items 
        # add each set if all subsets of size (i) are verified
        CFI = set()
        [CFI.add(frozenset(i_set)) 
                for i_set in combinations(all_items(VFI), i + 1)
                    if set(combinations(i_set, i)) <= VFI]

        print "%d new candidates." % len(CFI)
        VFI_L += list(VFI)
        rules += [r for i_set in VFI for r in gen_rules(i_set) 
                    if confidence(r) >= min_con]
        print "%d rules found so far." % len(rules)
        i += 1

    def i_set_str(i_set):
        i_L = map(str, sorted(i_set))
        return "'set', %f, %s" % (support(i_set), ', '.join(i_L))
    
    def rule_str((X, Y)):
        X_L = map(str, sorted(X))
        Y_L = map(str, sorted(Y))
        return "'rule', %f, %f, %s, '=>', %s" % (
                    support(X | Y), confidence((X, Y)), 
                    ', '.join(X_L), ', '.join(Y_L))

    f = open(outfile, 'w')
    f.writelines([i_set_str(i_set) + '\n' for i_set in VFI_L 
                    if len(i_set) > 1])
    f.writelines([rule_str(r) + '\n' for r in rules])
    f.close()

if __name__ == "__main__":
    main()
