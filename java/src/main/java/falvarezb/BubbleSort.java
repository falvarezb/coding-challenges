package falvarezb;

public class BubbleSort {

    /**
     * https://www.youtube.com/watch?v=xli_FI7CuzA <br>
     * Best case: O(n), original array is already ordered <br>
     * Worst case: O(n^2), original array is not sorted <br>
     * Average case: O(n^2)
     * Stable and not adaptive
     */
    public static void auxSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            boolean swapped = false; //optimization to achieve O(n) for best case
            for (int j = 0; j < arr.length-1; j++) {
                if (arr[j] > arr[j+1]) {
                    Util.swap(arr, j, j+1);
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }

    public static int[] sort(int[] arr) {
        auxSort(arr);
        return arr;
    }
}
