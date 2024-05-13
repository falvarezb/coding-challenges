package falvarezb;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

class SortTest {

    int d = 2;
    int k = (int) (0.9 * Math.pow(10, this.d));
    InPlaceSort[] inPlaceSorters = {BubbleSort::sort, SelectionSort::sort, InsertionSort::sort, QuickSort::sort, Arrays::sort};
    NotInPlaceSort[] notInPlaceSorters = {MergeSort::sort, RadixSort.sort(d, k)};
    Sort[] sorters = mergeArrays(inPlaceSorters, notInPlaceSorters);
    String[] sorterClassNames = Arrays.stream(sorters).map(sorter -> sorter.getClass().getSimpleName()).toArray(String[]::new);
    String[] sorterNames = {"BubbleSort", "SelectionSort", "InsertionSort", "QuickSort", "Arrays.sort", "MergeSort", "RadixSort"};


    private Sort[] mergeArrays(Sort[] arr1, Sort[] arr2) {
        Sort[] arr = new Sort[arr1.length + arr2.length];
        System.arraycopy(arr1, 0, arr, 0, arr1.length);
        System.arraycopy(arr2, 0, arr, arr1.length, arr2.length);
        return arr;
    }

    private String getSorterName(Sort sorter) {
        String sorterName = sorter.getClass().getSimpleName();
        int j = 0;
        for (String s : sorterClassNames) {
            if (s.equals(sorterName))
                return sorterNames[j];
            j++;
        }
        return "Unknown sorter: " + sorterName;
    }

    private void runTest(int[] arr, int[] expected, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);

        int[] sorted = switch (sorter) {
            case InPlaceSort inPlaceSorter -> {
                inPlaceSorter.sort(temp);
                yield temp;
            }
            case NotInPlaceSort notInPlaceSorter -> notInPlaceSorter.sort(temp);
        };
        if (!Arrays.equals(expected, sorted)) {
            System.out.println(getSorterName(sorter));
            System.out.println(Arrays.toString(sorted));
        }
        assertArrayEquals(expected, sorted);
    }

    private void runPerfTest(int[] arr, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);
        long startTime = System.currentTimeMillis();
        switch (sorter) {
            case InPlaceSort inPlaceSorter -> inPlaceSorter.sort(temp);
            case NotInPlaceSort notInPlaceSorter -> notInPlaceSorter.sort(temp);
        }
        long endTime = System.currentTimeMillis();
        System.out.println(getSorterName(sorter) + ": " + (endTime - startTime) + " ms");
    }

    @Test
    public void manualTest() {
        int[] arr = {1, 3, 4, 7, 2, 6};
        int[] expected = {1, 2, 3, 4, 6, 7};

        for (Sort sorter : sorters) {
            runTest(arr, expected, sorter);
        }
    }

    @Test
    public void randomTest() {
        for (int i = 0; i < 50; i++) {
            int[] arr = RandomDataGen.generateRandomArray(1000, this.d);
            int[] expected = Arrays.copyOf(arr, arr.length);
            Arrays.sort(expected);

            for (Sort sorter : sorters) {
                runTest(arr, expected, sorter);
            }
        }
    }

    @Test
    public void perfTest() {
        //for (int i = 0; i < 50; i++) {
        int arrSize = 10000;
        int[] arr = RandomDataGen.generateRandomArray(arrSize, this.d);
        System.out.println("Array size: " + arrSize);
        for (Sort sorter : sorters) {
            runPerfTest(arr, sorter);
        }
        //}
    }


    @Test
    public void countSortTest() {
        int[] expected = {1, 2, 3, 4, 6, 7};
        int[] arr = {1, 3, 4, 7, 2, 6};
        CountingSort.sort_not_stable(arr, Arrays.stream(arr).max().getAsInt());
        assertArrayEquals(expected, arr);
    }

}