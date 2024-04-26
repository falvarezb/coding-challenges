package falvarezb;

public class SelectionSort {

    /**
     * https://www.youtube.com/watch?v=g-PGLbMth_g <br>
     * O(n^2) <br>
     * Not stable and not adaptive
     * It's not stable because it swaps non-adjacent elements, e.g. 5, 5, 2
     */
    public static void sort(int[] arr) {
        for (int i = 0; i < arr.length-1; i++) {
            int minIndex = i;
            for (int j = i+1; j < arr.length; j++) {
                if(arr[j] < arr[minIndex])
                    minIndex = j;
            }
            Util.swap(arr, i, minIndex);
        }
    }
}
