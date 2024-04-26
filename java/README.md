# java-template
Template for Java projects: maven, junit5

https://www.geeksforgeeks.org/introduction-to-sorting-algorithm/?ref=outind

Insertion sort is a simple sorting algorithm that works similarly to the way you might sort playing cards in your hands. Here are its main characteristics:

1. **In-Place**: It requires a small constant amount of additional space beyond the input array. This makes it an in-place sorting algorithm.

2. **Stable**: It maintains the relative order of equal elements, making it a stable sort.

3. **Adaptive**: The time efficiency improves if the input array is partially sorted. In the best case scenario (when the array is already sorted), the complexity is O(n).

4. **Online**: It can sort a list as it receives it. This means that it can deal with dynamic data, where the complete input is not known in advance.

5. **Time Complexity**: The worst-case and average time complexity is O(n^2), where n is the number of elements in the array. This makes it less efficient on large lists compared to more advanced algorithms like quicksort, heapsort, or merge sort.

6. **Usage**: Due to its simplicity and the fact that it performs well on small or mostly sorted lists, it is often used as a building block in more advanced algorithms. It's also used when memory write is a costly operation, as it has fewer writes compared to other sorting algorithms like quicksort or mergesort.




Bubble Sort is a simple sorting algorithm that works by repeatedly swapping the adjacent elements if they are in the wrong order. Here are its main characteristics:

1. **In-Place**: It requires a small constant amount of additional space beyond the input array. This makes it an in-place sorting algorithm.

2. **Stable**: It maintains the relative order of equal elements, making it a stable sort. This is because Bubble Sort can be optimized to stop early if it makes a pass through the list without having to swap any elements. This means that if the list is already sorted, Bubble Sort will only need to make one pass through the list to confirm this, resulting in a best-case time complexity of O(n)

3. **Adaptive**: The time efficiency improves if the input array is partially sorted. In the best case scenario (when the array is already sorted), the complexity is O(n).

4. **Time Complexity**: The worst-case and average time complexity is O(n^2), where n is the number of elements in the array. This makes it less efficient on large lists compared to more advanced algorithms like quicksort, heapsort, or merge sort.

5. **Usage**: Due to its simplicity, it is often used in educational contexts for teaching the basics of algorithm design and analysis.

6. **Performance**: Bubble sort performs poorly on large datasets. It's not used in practice for large arrays because of its high time complexity.

7. **Mechanism**: Bubble sort works by repeatedly swapping adjacent elements if they are in the wrong order. This gives it the property that after each pass through the list, the largest element "bubbles" to the end.

8. **Optimization**: The algorithm can be optimized by stopping the algorithm if inner loop didn’t cause any swap in last pass. This makes the best case time complexity of Bubble Sort to O(n).



Selection Sort is a simple sorting algorithm that works by repeatedly finding the minimum element from the unsorted part of the array and putting it at the beginning. Here are its main characteristics:

1. **In-Place**: It requires a small constant amount of additional space beyond the input array. This makes it an in-place sorting algorithm.

2. **Not Stable**: It does not maintain the relative order of equal elements, making it an unstable sort.

3. **Time Complexity**: The worst-case, average-case, and best-case time complexity is O(n^2), where n is the number of elements in the array. This is because it always performs n(n-1)/2 comparisons, regardless of the input order.

4. **Usage**: Due to its simplicity, it is often used in educational contexts for teaching the basics of algorithm design and analysis. However, it is not efficient on large lists.

5. **Mechanism**: Selection sort works by dividing the input into a sorted and an unsorted region. The sorted region is built up from left to right at the front of the array. Each step selects the smallest (or largest, depending on sorting order) element from the unsorted array and swaps it with the leftmost unsorted element, moving the boundary between these two regions one element to the right.

6. **Performance**: Selection sort performs poorly on large datasets. It's not used in practice for large arrays because of its high time complexity.

7. **Not Adaptive**: The time efficiency does not improve even if the input array is partially sorted. The algorithm does not take into account the order of the array, and will perform the same number of operations regardless.


Stable Sorting Algorithms: Stable sorting algorithms maintain the relative order of records with equal keys (i.e., values). In other words, a sorting algorithm is stable if whenever there are two records R and S with the same key and with R appearing before S in the original list, R will appear before S in the sorted list.

Adaptive Sorting Algorithms: Adaptive sorting algorithms are those that take into account the initial order of the input and try to capitalize on any existing order. In other words, an adaptive sorting algorithm is one that performs better (i.e., sorts faster) when given a partially ordered list than when given a list in random order.


