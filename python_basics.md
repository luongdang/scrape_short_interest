# Python Basics

This document provides a quick overview of Python in case you are not familiar with the language.

## String

String literals in Python can be specified with single-quotes (`'`) or double-quotes (`"`). For consistency, I will use double-quotes through this document and the `scape.py` script.

### str as variable name

Avoid naming your variable `str`, as `str` refers to the string data type in Python. If you do, you redefine a built-in data type as a variable.

### Multi-line literals

If you need to specify a string literal that spans multiple lines, enclose it within a pair of tripple quotes:

```python
string = """Hello,
And goodbye
"""

# is the same as...
string = "Hello\nAnd goodbye"
```

### String interpolation

When you need to include variables a string, use *string interpolation*, also known in Python as f-strings:

```python
string = f"Hello {name}, you are {age} years old"

# is the same as...
string = "Hello " + name ", you are " + str(age) + " years old"     # for amateurs
string = "Hello {0}, you are {1} years old".format(name, age)       # minium exceptable on an interview
```

## Functions

### Default arguments

You can specify default arguments to Python functions:

```python
def add(a, b=42):
    return a + b

add(1)      # returns 43
add(1,2)    # returns 3
```

### Named arguments

You can pass arguments to Python functions using the argument's position or its name. Specifying the argument name is highly recommended when you want to add clarity to the function call. And they are also indispensible when you specify values for optional arguments.

```python
def greet(name, year=2018, car="Tesla"):
    return f"Hello {name}, you are driving a {year} {car}"

greet("John")               # Hello John, you are driving a 2018 Tesla
greet("John", 2018, "BMW")  # Hello John, you are driving a 2018 BMW
greet("John", car="Honda")  # Hello John, you are driving a 2018 Honda

# And since the `year` and `car` parameters are optionals, you can specify
# them in arbitrary order if you specify the argument's name
greet("Jack", car="Mercedes", year=2005)    # Hello Jack, you are driving a 2005 Mercedes
```

### Documentation

Visual Studio Code parses a string literal immediately following a function's definition as its documentation:

```python
def add(a, b):
    "Return the sum of two numbers"
    return a + b

add(1,2)
```

Now every time you hover your mouse over the `add` function, a tooltip will popup with the documentation you wrote.

## Loops

You should think every `for` loop in Python as a for-each loop:

```python
for item in a_list:
    # do things with `item`
```

The magic is in specifying `item` and `a_list`.

### Enumerate with index

You can get both the index and the element of the list when you wrap the list in `enumerate()` function:

```python
names = ["Mary", "Bill", "Alexis"]
greetings = []
for index, name in enumerate(names):
    greetings.append(f"Hello {name}, you are employee #{index}")

# greetings = [
#    "Hello Mary, you are employee #0",
#    "Hello Bill, you are employee #1",
#    "Hello Alexis, you are employee #2"
# ]
```

### List comprehension

List commprehension is a faster way to transform the elements of one list to another:

```python
names = ["Mary", "Bill", "Alexis"]
greetings = [f"Hello {name}, you are employee #{index}" for index, name in enumerate(names)]
```

You can also apply a condition to filter elements of the original list. Let's say you want to select only the even numbers and double them:

```python
numbers = [1,2,3,4,5,6]
results = [n * 2 for n in numbers if n % 2 == 0]

# results = [4,8,12]
```