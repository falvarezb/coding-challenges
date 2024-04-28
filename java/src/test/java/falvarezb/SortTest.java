package falvarezb;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class SortTest {

    //int[] expected = {1,2,3,4,6,7};
    Sort[] sorters = {BubbleSort::sort, SelectionSort::sort, InsertionSort::sort, QuickSort::sort, MergeSort::sort};
    String[] sorterNames = {"BubbleSort", "SelectionSort", "InsertionSort", "QuickSort", "MergeSort"};
    String[] sorterLambdaNames = Arrays.stream(sorters).map(sorter -> sorter.getClass().getSimpleName()).toArray(String[]::new);

    private int[] runTest(int[] arr, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);
        int[] sorted = sorter.sort(temp);
        return sorted;
    }

    @Test
    public void manualTest() {
        int[] arr = {1,3,4,7,2,6};
        int[] expected = {1,2,3,4,6,7};

        for (Sort sorter: sorters) {
            int[] sorted = runTest(arr, sorter);
            if(!Arrays.equals(expected, sorted)) {
                System.out.println(sorterNames[Arrays.binarySearch(sorterLambdaNames, sorter.getClass().getSimpleName())]);
                System.out.println(Arrays.toString(sorted));
            }
            assertArrayEquals(expected, sorted);
        }
        int[] sorted = RadixSort.sort(arr, 1, 7);
        assertArrayEquals(expected, sorted);
    }


    @Test
    public void quickSortTestRepeat() {
        int[] arr = {1,4,3,4,2,1,7,6};
        QuickSort.sort(arr);
        assertArrayEquals(new int[] {1,1,2,3,4,4,6,7}, arr);
    }

    @Test
    public void quickSortTest2Elem() {
        int[] arr = {1,2};
        QuickSort.sort(arr);
        assertArrayEquals(new int[]{1,2}, arr);
    }

    @Test
    public void countSortTest() {
        int[] expected = {1,2,3,4,6,7};
        int[] arr = {1,3,4,7,2,6};
        CountingSort.sort_not_stable(arr, Arrays.stream(arr).max().getAsInt());
        assertArrayEquals(expected, arr);
    }

}