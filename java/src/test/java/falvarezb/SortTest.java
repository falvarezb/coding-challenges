package falvarezb;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class SortTest {

    Sort[] sorters = {/*BubbleSort::sort, SelectionSort::sort, */InsertionSort::sort, QuickSort::sort, MergeSort::sort};
    String[] sorterNames = {/*"BubbleSort", "SelectionSort", */"InsertionSort", "QuickSort", "MergeSort"};
    String[] sorterLambdaNames = Arrays.stream(sorters).map(sorter -> sorter.getClass().getSimpleName()).toArray(String[]::new);

    private String getSorterName(Sort sorter) {
        return sorterNames[Arrays.binarySearch(sorterLambdaNames, sorter.getClass().getSimpleName())];
    }

    private int[] runTest(int[] arr, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);
        int[] sorted = sorter.sort(temp);
        return sorted;
    }

    private void runPerfTest(int[] arr, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);
        long startTime = System.currentTimeMillis();
        sorter.sort(temp);
        long endTime = System.currentTimeMillis();
        System.out.println(getSorterName(sorter) + ": " + (endTime - startTime) + " ms");
    }

    @Test
    public void manualTest() {
        int[] arr = {1,3,4,7,2,6};
        int[] expected = {1,2,3,4,6,7};

        for (Sort sorter: sorters) {
            int[] sorted = runTest(arr, sorter);
            if(!Arrays.equals(expected, sorted)) {
                System.out.println(getSorterName(sorter));
                System.out.println(Arrays.toString(sorted));
            }
            assertArrayEquals(expected, sorted);
        }
        int[] sorted = RadixSort.sort(arr, 1, 7);
        assertArrayEquals(expected, sorted);
    }

    @Test
    public void randomTest() {
        int d = 3;
        for (int i = 0; i < 50; i++) {
            int[] arr = RandomDataGen.generateRandomArray(1000, d);
            int[] expected = Arrays.copyOf(arr, arr.length);
            Arrays.sort(expected);

            for (Sort sorter : sorters) {
                int[] sorted = runTest(arr, sorter);
                if (!Arrays.equals(expected, sorted)) {
                    System.out.println(sorterNames[Arrays.binarySearch(sorterLambdaNames, sorter.getClass().getSimpleName())]);
                    System.out.println(Arrays.toString(sorted));
                }
                assertArrayEquals(expected, sorted);
            }
            int[] sorted = RadixSort.sort(arr, d, (int) (0.9 * Math.pow(10, d)));
            assertArrayEquals(expected, sorted);
        }
    }

    @Test
    public void perfTest() {
        int d = 2;
        //for (int i = 0; i < 50; i++) {
            int[] arr = RandomDataGen.generateRandomArray(400000, d);
            //Arrays.sort(arr);
            for (Sort sorter : sorters) {
                runPerfTest(arr, sorter);
            }
        long startTime = System.currentTimeMillis();
            RadixSort.sort(arr, d, (int) (0.9 * Math.pow(10, d)));
        long endTime = System.currentTimeMillis();
        System.out.println("RadixSort" + ": " + (endTime - startTime) + " ms");

        startTime = System.currentTimeMillis();
        Arrays.sort(arr);
        endTime = System.currentTimeMillis();
        System.out.println("Library sort" + ": " + (endTime - startTime) + " ms");

        startTime = System.currentTimeMillis();
        Arrays.parallelSort(arr);
        endTime = System.currentTimeMillis();
        System.out.println("Library parallel sort" + ": " + (endTime - startTime) + " ms");
        //}
    }


    @Test
    public void countSortTest() {
        int[] expected = {1,2,3,4,6,7};
        int[] arr = {1,3,4,7,2,6};
        CountingSort.sort_not_stable(arr, Arrays.stream(arr).max().getAsInt());
        assertArrayEquals(expected, arr);
    }

}