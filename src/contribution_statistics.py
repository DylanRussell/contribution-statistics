from sys import argv
from collections import defaultdict
from datetime import datetime
from math import ceil
from bisect import insort_left


dateFmt = '%m%d%Y'


def update_stats(fields, percentile, donors={}, contributions=defaultdict(list)):
    recipient, name, zcode, transDT, amount, entity = fields
    try:
        transDT = datetime.strptime(transDT, dateFmt)
        amount = float(amount)
    except ValueError:
        return False  # malformed or empty datetime/float
    if entity or len(zcode) < 5 or not name or not recipient:
        return False  # empty name/recipient/zcode, or donation came from an entity
    zcode = zcode[:5]
    year = transDT.year
    donor = (name, zcode)
    # contribution is considered a repeat only if donor has contributed in a prior year
    if donor not in donors or donors[donor] >= year:
        donors[donor] = year
        return False
    # repeat contributions grouped by recipient, zipcode, and year
    group = contributions[(recipient, zcode, year)]
    # insert the contribution into sorted list (O(N))
    insort_left(group, amount)
    total = sum(group)
    if total.is_integer():
        total = "{0:.0f}".format(total)
    else:
        total = "{0:.2f}".format(total)
    cnt = len(group)
    nthPercentile = round(group[int(ceil(percentile * cnt)) - 1])
    return "{}|{}|{}|{:.0f}|{}|{}\n".format(recipient, zcode, year, nthPercentile, total, cnt)


def main(contributionFp, percentileFp, outputFp):
    with open(percentileFp, 'rb') as p:
        percentile = float(next(p).strip()) / 100.0
    with open(outputFp, 'wb') as out, open(contributionFp, 'rb') as f:
        for line in f:
            line = line.strip().split('|')
            try:
                fields = [line[x] for x in (0, 7, 10, 13, 14, 15)]
            except IndexError:
                continue
            stats = update_stats(fields, percentile)
            if stats:
                out.write(stats)


if __name__ == '__main__':
    main(argv[1], argv[2], argv[3])
