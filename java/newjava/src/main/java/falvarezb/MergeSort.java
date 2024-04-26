package falvarezb;

import java.util.Arrays;

public class MergeSort {

    /**
     * https://www.youtube.com/watch?v=4VqmGXwpLqc <br>
     * O(n*logn)
     * Stable and not adaptive
     */
    public static int[] sort(int[] arr) {
        if(arr.length > 1) {
            int[] left = Arrays.copyOfRange(arr, 0, arr.length / 2);
            int[] right = Arrays.copyOfRange(arr, arr.length / 2, arr.length);
            return merge(sort(left), sort(right));
        }

        return arr;
    }

    private static int[] merge(int[] left, int[] right) {
        int[] arr = new int[left.length + right.length];
        int arrIdx = 0, leftIdx = 0, rightIdx = 0;

        while (leftIdx < left.length && rightIdx < right.length) {
            if(left[leftIdx] <= right[rightIdx]) {
                arr[arrIdx++] = left[leftIdx++];
            }
            else {
                arr[arrIdx++] = right[rightIdx++];
            }
        }

        if(leftIdx == left.length) {
            for (int k = rightIdx; k < right.length; k++) {
                arr[arrIdx++] = right[k];
            }
        }
        else {
            for (int k = leftIdx; k < left.length; k++) {
                arr[arrIdx++] = left[k];
            }
        }

        return arr;
    }
}
