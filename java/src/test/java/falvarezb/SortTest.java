package falvarezb;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SortTest {

    int d = 2;
    int k = (int) (0.9 * Math.pow(10, this.d));
    SortInPlace[] inPlaceSorters = {BubbleSort::sort, SelectionSort::sort, InsertionSort::sort, QuickSort::sort, Arrays::sort};
    SortNotInPlace[] notInPlaceSorters = {MergeSort::sort, RadixSort.sort(d, k)};
    List<Sort> sorterList = new ArrayList<>() {{
        addAll(Arrays.asList(inPlaceSorters));
        addAll(Arrays.asList(notInPlaceSorters));
    }};

    List<String> sorterNames = new ArrayList<>() {{
        add("BubbleSort");
        add("SelectionSort");
        add("InsertionSort");
        add("QuickSort");
        add("Library sort");
        add("MergeSort");
        add("RadixSort");
    }};

    List<String> sorterClassNames = sorterList.stream().map(sorter -> sorter.getClass().getSimpleName()).toList();

    private String getSorterName(Sort sorter) {
        String sorterName = sorter.getClass().getSimpleName();
        int j=0;
        for (String s: sorterClassNames) {
            if(s.equals(sorterName))
                return sorterNames.get(j);
            j++;
        }
        return "Unknown sorter: " + sorterName;
    }

    private void runTest(int[] arr, int[] expected, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);

        int[] sorted = switch (sorter) {
            case SortInPlace inPlaceSorter -> {
                inPlaceSorter.sort(temp);
                yield temp;
            }
            case SortNotInPlace notInPlaceSorter -> notInPlaceSorter.sort(temp);
        };
        if(!Arrays.equals(expected, sorted)) {
            System.out.println(getSorterName(sorter));
            System.out.println(Arrays.toString(sorted));
        }
        assertArrayEquals(expected, sorted);
    }

    private void runPerfTest(int[] arr, Sort sorter) {
        int[] temp = Arrays.copyOf(arr, arr.length);
        long startTime = System.currentTimeMillis();
        switch (sorter) {
            case SortInPlace inPlaceSorter -> inPlaceSorter.sort(temp);
            case SortNotInPlace notInPlaceSorter -> notInPlaceSorter.sort(temp);
        }
        long endTime = System.currentTimeMillis();
        System.out.println(getSorterName(sorter) + ": " + (endTime - startTime) + " ms");
    }

    @Test
    public void manualTest() {
        int[] arr = {1,3,4,7,2,6};
        int[] expected = {1,2,3,4,6,7};

        for (Sort sorter: inPlaceSorters) {
            runTest(arr, expected, sorter);
        }
        for (Sort sorter: notInPlaceSorters) {
            runTest(arr, expected, sorter);
        }
        int[] sorted = RadixSort.sort(arr, 1, 7);
        assertArrayEquals(expected, sorted);
    }

    @Test
    public void randomTest() {
        for (int i = 0; i < 50; i++) {
            int[] arr = RandomDataGen.generateRandomArray(1000, this.d);
            int[] expected = Arrays.copyOf(arr, arr.length);
            Arrays.sort(expected);

            for (Sort sorter : sorterList) {
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
            for (Sort sorter : sorterList) {
                runPerfTest(arr, sorter);
            }
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