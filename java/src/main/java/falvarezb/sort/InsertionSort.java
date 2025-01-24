package falvarezb.sort;

import falvarezb.Util;

public class InsertionSort {

    /**
     * https://www.youtube.com/watch?v=JU767SDMDvA <br>
     * Best case: O(n), original array is already ordered <br>
     * Worst case: O(n^2), original array is not sorted <br>
     * Average case: O(n^2)
     * Stable and adaptive
     */
    public static void sort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            for (int j = i; j > 0 && arr[j-1] > arr[j]; j--) {
                Util.swap(arr, j, j-1);
            }
        }
    }
}
