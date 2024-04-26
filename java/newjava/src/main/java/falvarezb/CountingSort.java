package falvarezb;

import java.lang.reflect.Array;
import java.util.Comparator;
import java.util.function.Function;

public class CountingSort {

    /**
     * values of the elements in the array must be in the range 0...k <br>
     * https://www.youtube.com/watch?v=OKd534EWcdk <br>
     * O(n)
     * Stable
     *
     * Elements are never compared between them but used to index an array containing the number of occurrences
     * of each element in the original array.
     */
    public static int[] sort_stable(int[] arr, int k) {
        // count[j] contains the number of occurrences of j (where j=0...k) in the original array
        int[] count = new int[k+1];
        for (int e: arr) {
            count[e]++;
        }

        // accummulatedCount[j] contains the number of elements less than j in the original array
        // thus accummulatedCount[j] is the index where the first occurrence of j should be placed in the sorted array
        int[] accummulatedCount = new int[k+1];
        accummulatedCount[0] = 0;
        for (int i = 1; i < accummulatedCount.length; i++) {
            accummulatedCount[i] = accummulatedCount[i-1] + count[i-1];
        }

        int[] sorted = new int[arr.length];
        for (int e: arr) {
            sorted[accummulatedCount[e]++] = e;
        }
        return sorted;
    }

    public static <T> T[] sort_with_satellite_data(T[] arr, int k, Function<T, Integer> keyExtractor) {
        int[] count = new int[k+1];
        for (T e: arr) {
            count[keyExtractor.apply(e)]++;
        }

        int[] accummulatedCount = new int[k+1];
        accummulatedCount[0] = 0;
        for (int i = 1; i < accummulatedCount.length; i++) {
            accummulatedCount[i] = accummulatedCount[i-1] + count[i-1];
        }

        @SuppressWarnings("unchecked")
        T[] sortedArr = (T[]) Array.newInstance(arr.getClass().getComponentType(), arr.length);
        for (T e: arr) {
            sortedArr[accummulatedCount[keyExtractor.apply(e)]++] = e;
        }
        return sortedArr;
    }


    public static void sort_not_stable(int[] arr, int k) {
        int[] count = new int[k+1];
        for (int e: arr) {
            count[e]++;
        }

        int l = 0;
        // this nested loop has a time-complexity of O(arr.length)
        for (int i = 0; i < count.length; i++) {
            for (int j = 0; j < count[i]; j++) {
                arr[l++] = i;
            }
        }
    }

    public static void main(String[] args) {
        int[] arr = {0, 5, 5, 0, 2, 4, 2, 6};
        int[] sortedArr = sort_stable(arr, 8);
        for (int i = 0; i < sortedArr.length; i++) {
            System.out.print(sortedArr[i] + " ");
        }
    }
}
