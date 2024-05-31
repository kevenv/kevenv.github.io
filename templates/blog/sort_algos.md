# Sorting algorithms

Sort the array `[3,4,1,2]` in ascending order (from smallest to biggest).

- Best: `[1,2,3,4]` (already sorted)
- Worst: `[4,3,2,1]` (reversed)

## Bubble sort
Bruteforce way to sort.

### Intuition
Swap each pair of elements until the array is sorted.
The max element "bubbles up" at the end of the array.

```python
[3,4,1,2]

# pass 0

 v v
[3,4,1,2] # swap if 4 < 3

[3,4,1,2]

# ---

   v v
[3,4,1,2] # swap if 1 < 4

[3,1,4,2] 

# ---

     v v
[3,1,4,2]

[3,1,2,4]

# pass 1

 v v
[3,1,2,4]

[1,3,2,4]

# ---

   v v
[1,3,2,4]

[1,2,3,4]

# ---

     v v
[1,2,3,4]

[1,2,3,4]

# pass 2
# continue until didn't need to swap during a whole pass
```

### Implementation
```C
void sort(int* array, int n)
{
    bool swapped = true;
    while (swapped) {
        swapped = false;
        for (int i = 0; i < n-1; i++) {
            if (array[i+1] < array[i]) {
                swap(&array[i+1], &array[i]);
                swapped = true;
            }
        }
        n--; // optim: at the end of a pass the last element is sorted
    }
}
```

### Analysis
- Best: O(N), Average: O(N<sup>2</sup>), Worst: O(N<sup>2</sup>)
- Memory: O(1)
- Stable: yes

## Selection sort
An easy & intuitive way to sort.

### Intuition
```python
min = None
unsorted_array = [3,4,1,2] # start with input
sorted_array = [] # start empty

min = 1 # find minimum of unsorted_array
unsorted_array = [3,4,2] # remove element at idx
sorted_array = [1] # append element to end

min = 2
unsorted_array = [3,4]
sorted_array = [1,2]

min = 3
unsorted_array = [4]
sorted_array = [1,2,3]

min = 4
unsorted_array = [] # end when empty
sorted_array = [1,2,3,4]
```

We need to allocate a second array, this can be avoided by doing it in-place with swaps:
```python
# imagine dividing the input array in 2 sections: [sorted|unsorted]

# initially:
# the sorted section is empty
# the unsorted section contains the initial array
[|3,4,1,2]

# ---

# find min element of unsorted section
      v
[|3,4,1,2]

# remove element from unsorted section 
#               + 
# append element to sorted section
#               = 
# swap element to last sorted section
  v   v
[|3,4,1,2]

[|1,4,3,2]

# increment the section divider
[1|4,3,2]

# ---

       v
[1|4,3,2] # min element or unsorted section

   v   v
[1|4,3,2] # swap

[1|2,3,4]

[1,2|3,4] # increment divider

# ---

     v
[1,2|3,4]

     vv
[1,2|3,4]

[1,2|3,4]

[1,2,3|4] # we could stop early here

# ---

       v
[1,2,3|4]

       vv
[1,2,3|4]

[1,2,3|4]

[1,2,3,4|] # stop when unsorted section is empty
```

### Implementation
```C
void sort(int* array, int n)
{
    int divider_idx = 0;
    while (divider_idx < n) {
        // find min of array from divider_idx
        int min_val = INT_MAX;
        int min_idx = 0;
        for (int i = divider_idx; i < n; i++) {
            if (array[i] <= min_val) {
                min_val = array[i];
                min_idx = i;
            }
        }

        // if (min_idx != divider_idx), avoid swap vs avoid branching
        swap(&array[divider_idx], &array[min_idx]);

        divider_idx++;
    }
}

// can simplify by:
// - assuming that the first element of the unsorted section is the min
// - we don't need to swap the last element at the end of the sort
void sort(int* array, int n)
{
    for (int divider_idx = 0; divider_idx < n-1; divider_idx++) {
        // find min of array from divider_idx
        // assume min=first
        int min_idx = divider_idx;
        for (int i = divider_idx+1; i < n; i++) {
            if (array[i] < array[min_idx]) {
                min_idx = i;
            }
        }
        swap(&array[divider_idx], &array[min_idx]);
    }
}
```

### Analysis
- Best: O(N<sup>2</sup>), Average: O(N<sup>2</sup>), Worst: O(N<sup>2</sup>)
- Memory: O(1)
- Stable: no

## Insertion sort
Same as sorting cards.

- simple
- faster than selection sort and bubble sort
- fast for very small arrays (~7-50 elements)
    - faster than quicksort!

### Intuition
```python
[3,4,1,2]

# ---

   v
[3,4,1,2] # start at idx 1, check where element should go

# 4 < 3? no
# no more element to the left -> element is already at the correct position

[3,4,1,2]

# ---

     v
[3,4,1,2] # check where element should go

# 1 < 4 yes
# 1 < 3 yes
# no more element to the left -> element goes to idx=0

[1,3,4,2] # insert element to correct position
 x

# ---

       v
[1,3,4,2]

# 2 < 4 yes
# 2 < 3 yes
# 2 < 1 no -> element goes to idx=1

[1,2,3,4]
   x

# stop after each element have been moved to the correct position
```

Since we want to insert and remove an element of the array at the same time, we really just want to move the element to a specific position. This can be easily accomplished by swapping it to the left until it gets to the desired position, we don't need to reallocate the array at all.

To find where an element should go, 
we need to compare it with every element at its left, which will be already done by the moving operation.

In summary, we move each element by swapping it to the left until we shouldn't swap anymore, meaning that it is at the correct position.

### Implementation
```C
void sort(int* array, int n)
{
    // for each element
    for (int i = 1; i < n; i++) {
        // swap it to the left until it gets to the correct position.
        for (int j = i; j > 0 && array[j] < array[j-1]; j--) {
            swap(&array[j], &array[j-1]);
        }
    }
}
```

We can also optimize it by moving each element to the right place in one go.
```python

# say we have:
     v
[4,3,1,2]

# we need to move 1 to idx=0
# to make some room for 1 we shift 4,3 one position to the right
[_,4,3,2]
# this overwrites 1, so make sure to save it before shifting

# we can then copy 1 to the correct position
[1,4,3,2]
```

The optimized implementation is then:
```C
void sort(int* array, int n)
{
    // for each element
    for (int i = 1; i < n; i++) {
        int x = array[i]; // save element to move
        // shift elements to the right
        int j = i;
        for (; j > 0 && x < array[j-1]; j--) {
            array[j] = array[j-1];
        }
        // j will be the correct position of x at this point
        array[j] = x; // copy element to the right place
    }
}
```

### Analysis
- Best: O(N), Average: O(N<sup>2</sup>), Worst: O(N<sup>2</sup>)
- Memory: O(1)
- Stable: yes

## Sorting networks
TODO:

- for fixed N
- always same time
- can be optimal
- implemented as a network of swaps
- not obvious how to find the network
- many algos exists
    - odd-even sort = parallel bubble sort

## TODO:
- merge sort
- heap sort
- quick sort
- counting sort
    - assume int only, no need comparisons, not in-place
- radix sort

## Shared code
```C
inline void swap(int* a, int* b)
{
    int a_ = *a;
    *a = *b;
    *b = a_;
}
```
