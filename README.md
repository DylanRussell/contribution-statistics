# contribution-statistics
This is a Python implementation of the [Insight Data Engineering coding challenge](https://github.com/InsightDataScience/donation-analytics). The solution can be found in a single file: `src/contribution_statistics.py`. 

The code was tested on Python v2.7. It uses the following modules from Python's standard library: `sys, collections, datetime, math, bisect` These modules are commonly included in Python distributions.

Input records are ignored if they meet any of the conditions described under the "Input file considerations" section in the coding challenge readme. I considered validating the data to ensure it conformed exactly to the data dictionary provided by the FEC, but decided that was overkill.

To identify repeat donors a dictionary that maps (name, zipcode) pairs to the earliest year that person had made a contribution is used. If a (name, zipcode) pair is already in the dictionary and the earliest contribution year is a prior year, then the donor is considered to be a repeat donor.

To group together contributions from repeat donors by recipient/zipcode/year a defaultdict that maps (recipient, zipcode, year) tuples to a list of contributions is used. A defaultdict instead of a dict was chosen so that the first time a (recipient, zipcode, year) key is used, an empty list is created - it is not necessary to first check if the grouping exists.

Each of these lists is kept in sorted order which is necessary to calculate the percentile. To maintain the sorted order I insert new records using `bisect.insort_left` which inserts the value into the sorted list in O(len(list)) time. This is faster than appending the value and then sorting the list. 

I considered installing/using the [blist package](https://pypi.python.org/pypi/blist/1.3.6) here, as it contains a data structure like a list for which the insort_left operation only takes O(log**2 N) time. Ultimately I think O(N) is good enough as any individual recipient/zipcode/year grouping is unlikely to be very large. Also I would have had to install and support a package not in the standard library.
