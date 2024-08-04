# Sorting algorithms

Sort the array `[3,4,1,2]` in ascending order (from smallest to biggest).

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

- Simple
- Faster than selection sort and bubble sort
- Fast for very small arrays (~7-50 elements)
    - Faster than quicksort!

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

## Merge sort
Divide and conquer approach to sorting.

- Easy to understand
- Fast
- Highly parallelizable

### Intuition

```python
# given the following unsorted array
[2,8,5,3,9,4,1,7]

# split in 2 arrays until each array only has 1 element
[2,8,5,3][9,4,1,7]
[2,8][5,3][9,4][1,7]
[2][8][5][3][9][4][1][7]
# merge 2 arrays by making sure that
# the element added are in the correct order
[2,8][3,5][4,9][1,7]
# continue merging until you cannot merge anymore
# (only a single array with all the elements)
[2,3,5,8][1,4,7,9]
[1,2,3,4,5,7,8,9]
```

Note the recursivity of the algorithm which makes it easy to parallelize.

#### Splitting
How to split arrays without creating new arrays?
By using 3 indices we can view an array as 2 arrays:
```python
# 2 arrays
[2,8,5,3][9,4,1,7]

# 1 array, 3 indices
 begin   mid   end
 v       v     v
[2,8,5,3|9,4,1,7] 
```

How to merge arrays without allocating a new array every time?
Unfortunately this algortihm cannot be done _in-place_ easily, at each merging step we need a source array and a destination array:
```python
[2,3,5,8|1,4,7,9] # source array
#   \_______/
[1,2,3,4,5,7,8,9] # destination array
```

#### Merging
We thus need two arrays, we already have the input array (the original unsorted array) that we can reuse and we create another array as a temporary work array.
At each step we interchange the role of the input and work array, sometimes acting as a source and sometimes as destination.
We can do that efficiently by changing the source/destination via pointers.

Since we will overwrite the input array, we should make sure that it contains the sorted array at the end of the algorithm.
For that we first copy the input array into the work array and start sorting the work array into the input array:
```python
input array = unsorted array
work array = input array
src = work array
dst = input array
merge_sort(src, dst)
```

All together we get something like:
```python
[2,8|3,5|4,9|1,7] # input array | src
# \___/   \___/                 |
[2,3,5,8|1,4,7,9] # work array  | dst | src
#   \_______/                         |
[1,2,3,4,5,7,8,9] # input array       | dst
```

#### Merge operation
Now let's figure out how to implement the "merge" operation.
The trivial case of merging two arrays of one element can be done like this:
```python
merge(array, array_left, array_right)
    if array_left[0] < array_right[0]
        array.add( array_left[0] )
    else
        array.add( array_right[0] )
```

Generalizing to arrays of N elements is not much more complicated since we know that the left array and right array are sorted:
```python
merge(array, array_left, array_right)
    for i = 0 -> N
        if array_left[i] < array_right[i]
            array.add( array_left[i] )
        else
            array.add( array_right[i] )
```

Now we relax our assumptions that each array have the same number of elements.
To handle this we use a single array to hold the left and right array and we index each array separately:
```python
#    left         right
[0 ... mid-1][mid ... end-1]

L = 0 -> mid # index for the left array
R = mid -> end # index for the right array
```

This means that we now have two case where the arrays could get out of bounds:
```python
# left array > right array
     L      R
     v      v
[2,8,9][3,5]  
            x

# right array > left array
     L     R
     v     v
[3,5] [2,8,9]
     x
```

We modify our previous algorithm to handle the two edge cases:
```python
if L >= mid -> use array[R]
if R >= end -> use array[L]
else
    if array[L] < array[R]
        use array[L]
    else
        use array[R]
```

It is important to realize that the `L` and `R` counters should not be incremented in **lockstep**! Consider this case:
```python
 L   R
 v   v
[3,4|1,2]
[1] # 1 < 3 so add 1 to merged array
[1,3] # then add 3 to merged array
L++
R++

   L   R
   v   v
[3,4|1,2]
[1,3,2] # 2 < 4 so add 2
[1,3,2,4] # then add 4
L++
R++
# the algorithm is done but 
# the array is not sorted!
```
To sort this array correctly we must increment the counters **independently**:
```python
 L   R
 v   v
[3,4|1,2]
[1] # 1 < 3 so add 1 to merged array
R++ # increment only the choosen side (right)

 L     R
 v     v
[3,4|1,2]
[1,2] # 2 < 3 so add 2
R++

 L       R
 v       v
[3,4|1,2]
# r is out of bounds (R >= end)
# we only care about the left array from now on
[1,2,3] # add 3
L++

   L     R
   v     v
[3,4|1,2]
[1,2,3,4] # add 4
L++
```

### Implementation
```C
#include <stdlib.h> // malloc
#include <string.h> // memcpy

void sort(int* array, int n)
{
    int* tmp = (int*)malloc(n * sizeof(int));
    // copy array into tmp
    memcpy(tmp, array, n * sizeof(int));
    // merge tmp into array
    merge_sort(array, tmp, 0, n);
    free(tmp);
}

// recursively split & merge arrays (src) into (dst)
void merge_sort(int* dst, int* src, int begin, int end)
{
    if (begin == end-1) {
        // only 1 element, already sorted
        // done splitting, start merging
        return;
    }

    // split
    int mid = (begin + end) / 2;
    merge_sort(dst, src, begin, mid);
    merge_sort(dst, src, mid, end);
    // merge src into dst
    merge(dst, src, begin, mid, end);
}

// merge 2 arrays (src) into (dst) by adding element in ascending order
//   split 1 : [begin : mid-1]
//   split 2 : [mid   : end-1]
void merge(int* dst, int* src, int begin, int mid, int end)
{
    int l = begin;
    int r = mid;
    for (int i = begin; i < end; i++) {
        if (l < mid && (r >= end || src[l] <= src[r])) {
            dst[i] = src[l];
            l++;
        }
        else {
            dst[i] = src[r];
            r++;
        }
    }
}
```

### Analysis
- Best: O(N log(N)), Average: O(N log(N)), Worst: O(N log(N))
- Memory: O(N)
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
- heap sort
- quick sort
- counting sort
    - assume int only, no need comparisons, not in-place
- radix sort

## Definitions
### Best/Worst
- Best: `[1,2,3,4]` (already sorted)
- Worst: `[4,3,2,1]` (reversed)

### Stability
A sorting algorithm is said to be "stable" if identical elements keep their original position relative to each other. For example:
```python
# unstable since the two '2' have been swapped
[4,2_1,2_2,1] -> [1,2_2,2_1,4]
```
This does not matter if the elements are numbers but can matter if they are more complex objects.

### Swap
```C
inline void swap(int* a, int* b)
{
    int a_ = *a;
    *a = *b;
    *b = a_;
}
```
