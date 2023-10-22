# Debts payment network

Another small graph-theory related project.

Imagine you have a network of people debts:
```
A B {'debt': 5}
A E {'debt': 2}
B C {'debt': 6}
B D {'debt': 3}
C D {'debt': 3}
D E {'debt': 2}
E A {'debt': 6}
```
Explanation: `A` owns 5 money to `B`

So you need to compute optimal way for these people to exchange money with each other
to pay off all debts.

This program solves this problem:

Output:
```
-----------------
These people have cycle debt of 2 money - they simply forget this much debt
[('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')]
----------------------
['E']
Gives 2 money trough people they debts to
['D']
----------------------
['A']
Gives 1 money trough people they debts to
['D']
----------------------
['B']
Gives 1 money trough people they debts to
['D']
----------------------
['B']
Gives 3 money trough people they debts to
['C']
If you follow these instructions you will pay off debts of all people
```