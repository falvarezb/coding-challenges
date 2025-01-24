package falvarezb.sort;

import falvarezb.TestUtil;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

class SortTest {

    // ** PARAMETERS TO CREATE THE RADIX SORTER **
    // In the radix sort algorithm, each sort key is regarded as a d-digit number, where each digit is in the range 0...k.
    private int d = 2;
    private int k = 9;
    private Map<Sort, String> sorters = getSorters();

    private Map<Sort, String> getSorters() {
        InPlaceSort[] inPlaceSorters = {BubbleSort::sort, SelectionSort::sort, InsertionSort::sort, QuickSort::sort, Arrays::sort};
        NotInPlaceSort[] notInPlaceSorters = {MergeSort::sort, RadixSort.sort(d, k)};
        Sort[] sorters = mergeArrays(inPlaceSorters, notInPlaceSorters);
        String[] sorterNames = {"BubbleSort", "SelectionSort", "InsertionSort", "QuickSort", "Arrays.sort", "MergeSort", "RadixSort"};
        return IntStream.range(0, sorters.length)
                .boxed()
                .collect(Collectors.toMap(i -> sorters[i], i -> sorterNames[i]));
    }

    private Sort[] mergeArrays(Sort[] arr1, Sort[] arr2) {
        Sort[] arr = new Sort[arr1.length + arr2.length];
        System.arraycopy(arr1, 0, arr, 0, arr1.length);
        System.arraycopy(arr2, 0, arr, arr1.length, arr2.length);
        return arr;
    }

    private String getSorterName(Sort sorter) {
        String sorterName = sorter.getClass().getSimpleName();
        for (Sort s : sorters.keySet()) {
            if (s.getClass().getSimpleName().equals(sorterName))
                return sorters.get(s);
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

        for (Sort sorter : sorters.keySet()) {
            runTest(arr, expected, sorter);
        }
    }

    @Test
    public void randomTest() {
        for (int i = 0; i < 50; i++) {
            int[] arr = TestUtil.generateRandomArray(1000, this.d);
            int[] expected = Arrays.copyOf(arr, arr.length);
            Arrays.sort(expected);

            for (Sort sorter : sorters.keySet()) {
                runTest(arr, expected, sorter);
            }
        }
    }

    @Test
    public void perfTest() {
        //for (int i = 0; i < 50; i++) {
        int arrSize = 10000;
        int[] arr = TestUtil.generateRandomArray(arrSize, this.d);
        System.out.println("Array size: " + arrSize);
        for (Sort sorter : sorters.keySet()) {
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