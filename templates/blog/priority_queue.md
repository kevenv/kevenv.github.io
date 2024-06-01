# Priority Queue

The _priority queue_ is an important data structure where each element are kept in order of priority to be able to rapidly determine the element with the highest priority.

Each element of the queue will have a `value` and a `priority`.
<!-- To keep the explanation simple, we ommit the `value` of the elements. -->

Say we want to add elements with priority `3,4,1,2` to a priority queue in this order, the resulting priority queue will be `[1,2,3,4]`:
```python
#  queue | operation
[]
[3]       # add 3 (element 0 with priority 3)
[3,4]     # add 4 (element 1 with priority 4)
[1,3,4]   # add 1 (element 2 with priority 1)
[1,2,3,4] # add 2 (element 3 with priority 2)
```
The last element is always the one with the highest priority.

## Implementation
To be useful a priority queue must implement at least the following operations:

- `push()` : add an element
- `pop()` : pop the element with the highest priority
- `empty()` : check if the queue is empty

There are many ways to implement it. 
Here we show a simple toy implementation in C:
```C
#define PRIORITY_QUEUE_SIZE 5

struct element {
    int value;
    int priority;
};
struct pqueue {
    element queue[PRIORITY_QUEUE_SIZE];
    int size; // number of elements
};

void pqueue_init(pqueue* q)
{
    q->size = 0;
}
bool pqueue_empty(pqueue* q)
{
    return q->size == 0;
}
void pqueue_push(pqueue* q, element e);
element pqueue_pop(pqueue* q);
```
To keep the code short and simple we use an array of fixed size for the queue and only support `int `elements. Consider the code more as "pseudo-code" than a real implementation.

### Unsorted array
This is the simplest implementation, we use an array and we don't bother sorting it or keeping it sorted.

The `push()` simply adds to the next empty spot in the array:
```C
void pqueue_push(pqueue* q, element e)
{
    q->queue[q->size] = e;
    q->size++;
}
```

The `pop()` must search for the highest priority element in the array:
```C
element pqueue_pop(pqueue* q)
{
    // find element with highest priority
    int max_i = 0; // assume highest priority element is the first
    for (int i = 1; i < PRIORITY_QUEUE_SIZE; i++) {
        if (q->queue[i].priority > q->queue[max_i].priority) {
            max_i = i;
        }
    }
    element e = q->queue[max_i];
    // remove element from array
    q->queue[max_i].priority = 0; // lowest priority
    q->size--;
    return e;
}
```

The complexity of `push()` is O(1) but `pop()` is O(N).
Notice how similar this is to "selection sort".

### Sorted array
A better way to implement a priority queue is via a sorted array.

The `push()` adds the element to the array by making sure to keep the array sorted from the lowest priority to the highest.
The last element of the array will be the one with the highest prirority.

To figure out how to do this, let's consider an example:
```python
# add 0 to [1,2,3,_]
[1,2,3,_]
# shift whole array to the left by one
[1,2,3,_]
[_,1,2,3]
# insert the element at idx=0
[0,1,2,3]
 x
```

The implementation is then:
```C
void pqueue_push(pqueue* q, element e)
{
    // shift elements to the right
    int i = q->size;
    for (; i > 0 && element.priority < q->queue[i-1].priority; i--) {
        q->queue[i] = q->queue[i-1];
    }
    // insert element at the correct position
    q->queue[i] = element;
    q->size++;
}
```

This is very similar to "insertion sort", see [this article](http://localhost:8000/blog/sort_algos.html) for more info about sorting algorithms.

Finally `pop()` simply pops the last element of the array as it is the highest:
```C
element pqueue_pop(pqueue* q)
{
    // get element with highest priority
    element e = q->queue[q->size-1];
    // remove element from array
    q->size--;
    return e;
}
```

The complexity of `push()` is O(N) but `pop()` is O(1).

### Heap
TODO
the most efficient but also the most complex way
