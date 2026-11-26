# LYNX: Lines, Yields and Nodes eXamined

Formerly `graph-sketch-checker`.

Checks a student's claimed sketch of a polynomial graph against its exact features: y-intercept, x-intercepts, end behaviour and points on the curve.

## What it solves
Marking a sketch means checking intercepts and ends by hand. Give the polynomial and what the sketch claims, and the tool lists every inconsistency in words. Coefficients are exact fractions. Pure Python 3.10+, standard library only.

## Example
```bash
python -m sketchcheck '[1,-3,2]' '{"y_intercept":-2,"roots":[1],"end":["down","down"],"points":[[0,0]]}'
```
```
y-intercept should be 2, not -2
missing the x-intercept x = 2
ends should go ('up', 'up'), not ('down', 'down')
(0, 0) is not on the graph; f(0) = 2
```
(Output pasted from a real run.)

## The maths behind it
A polynomial is a list of coefficients, highest power first, so [1, -3, 2] is x^2 - 3x + 2. The y-intercept is the constant term. Rational x-intercepts come from the rational root theorem: any root p/q has p dividing the constant term and q dividing the leading coefficient (after clearing denominators), and each candidate is tested exactly by Horner's rule. For x^2 - 3x + 2 the roots are 1 and 2. End behaviour depends on the sign of the leading coefficient and on whether the degree is odd or even. A cubic has two turning points exactly when the discriminant of its derivative 3ax^2 + 2bx + c is positive. Irrational roots are not listed, so only rational x-intercepts can be reported as missing.

## Install and run
```bash
python -m pip install -e .
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
