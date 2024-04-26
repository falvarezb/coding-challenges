package falvarezb;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class SortTest {

    int[] expected = {1,2,3,4,6,7};

    @Test
    public void bubbleSortTest() {
        int[] arr = {1,3,4,7,2,6};
        BubbleSort.sort(arr);
        assertArrayEquals(expected, arr);
    }

    @Test
    public void selectionSortTest() {
        int[] arr = {1,3,4,7,2,6};
        SelectionSort.sort(arr);
        assertArrayEquals(expected, arr);
    }

    @Test
    public void insertionSortTest() {
        int[] arr = {1,3,4,7,2,6};
        InsertionSort.sort(arr);
        assertArrayEquals(expected, arr);
    }

    @Test
    public void mergeSortTest() {
        int[] arr = {1,3,4,7,2,6};
        assertArrayEquals(expected, MergeSort.sort(arr));
    }

    @Test
    public void quickSortTest() {
        int[] arr = {1,3,4,7,2,6};
        QuickSort.sort(arr);
        assertArrayEquals(expected, arr);
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
        int[] arr = {1,3,4,7,2,6};
        CountingSort.sort_not_stable(arr, Arrays.stream(arr).max().getAsInt());
        assertArrayEquals(expected, arr);
    }

}