package falvarezb.sort;

import falvarezb.Util;

public class QuickSort {

    /**
     *  https://www.youtube.com/watch?v=Hoixgm4-P4M <br>
     *  https://algorithmist.com/wiki/Quicksort <br>
     *  Best case: O(n*logn) <br>
     *  Worst case: O(n^2) when list is sorted <br>
     *  Average case: O(n*logn) when pivot is selected correctly
     *
     *  The worst-case scenario for QuickSort occurs when the partitioning routine produces one subproblem
     *  with n-1 elements and one with 0 elements, leading to the most unbalanced partitions possible, 'logn' becomes 'n'.
     *
     *  This can happen if the "pivot" element is the smallest or largest element in the array (the array is already
     *  sorted in ascending or descending order).
     */
    public static void sort(int[] arr) {
        quicksort(arr, 0, arr.length-1);
    }

    static void quicksort(int[] arr, int left, int right) {
        if (left < right) {
            int pivotIdx = partition(arr, left, right);
            quicksort(arr, left, pivotIdx - 1);
            quicksort(arr, pivotIdx + 1, right);
        }
    }
    /**
     * <p>The {@code partition} function in the QuickSort algorithm is responsible for dividing the array into two halves around a selected pivot element.</p>
     *
     * <p>The goal of the partition function is to rearrange the array in such a way that all elements less than the pivot are moved to the left of the pivot
     * and all elements greater than the pivot are moved to the right of the pivot.</p>
     *
     * <p>In this implementation, the pivot is selected as the last element of the array.</p>
     */
    private static int partition(int[] arr, int left, int right) {
        int pivot = arr[right];
        int pivotIndex = left;
        for (int i = left; i < right; i++) {
            if (arr[i] < pivot) {
                Util.swap(arr, i, pivotIndex);
                pivotIndex++;
            }
        }
        Util.swap(arr, pivotIndex, right);
        return pivotIndex;
    }
}
