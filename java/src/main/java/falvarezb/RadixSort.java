package falvarezb;

import java.util.Arrays;
import java.util.Objects;
import java.util.function.BiFunction;
import java.util.function.Function;

import static falvarezb.CountingSort.sort_with_satellite_data;

public class RadixSort {

    /**
     * values of the elements in the array must be in the range 0...k <br>
     * https://www.youtube.com/watch?v=OKd534EWcdk <br>
     * O(n)
     * Stable
     *
     * In the radix sort algorithm, we assume that we can think of each sort key as a d-digit number,
     * where each digit is in the range 0...k.
     *
     * Then we run a stable sort on each digit, going from right to left, from least significant digit to most significant digit.
     * If we use counting sort as the stable sort, the time complexity of radix sort is O(d*(n+k)).
     *
     */
    public static Integer[] sort(Integer[] arr, int d, int k) {
        Function<Integer, Function<Integer, Integer>> keyExtractor = currentPosition -> (t -> (t / (int) Math.pow(10, currentPosition)) % 10);
        return recursiveF(arr, d, k, 0, keyExtractor, Objects::equals, currentPosition -> currentPosition+1);
    }

    public static int[] sort(int[] arr, int d, int k) {
        Integer[] arrInteger = Arrays.stream(arr).boxed().toArray(Integer[]::new);
        Function<Integer, Function<Integer, Integer>> keyExtractor = currentPosition -> (t -> (t / (int) Math.pow(10, currentPosition)) % 10);
        Integer[] sortedInteger = recursiveF(arrInteger, d, k, 0, keyExtractor, Objects::equals, currentPosition -> currentPosition+1);
        return Arrays.stream(sortedInteger).mapToInt(Integer::intValue).toArray();
    }

    public static NotInPlaceSort sort(int d, int k) {
        return arr -> {
            Integer[] arrInteger = Arrays.stream(arr).boxed().toArray(Integer[]::new);
            Function<Integer, Function<Integer, Integer>> keyExtractor = currentPosition -> (t -> (t / (int) Math.pow(10, currentPosition)) % 10);
            Integer[] sortedInteger = recursiveF(arrInteger, d, k, 0, keyExtractor, Objects::equals, currentPosition -> currentPosition + 1);
            return Arrays.stream(sortedInteger).mapToInt(Integer::intValue).toArray();
        };
    }

    public static String[] sort(String[] arr, int d, int k) {
        // with this extractor, given two strings with the same prefix, the one with the shorter length will be considered smaller
        Function<Integer, Function<String, Integer>> keyExtractor = currentPosition -> (t -> (int) (currentPosition < t.length() ? t.charAt(currentPosition) : 0));
        return recursiveF(arr, d, k, d-1, keyExtractor, (currentPosition, _) -> currentPosition == -1, currentPosition -> currentPosition-1);
    }

    private static <T> T[] recursiveF(T[] arr, int d, int k, int currentPosition, Function<Integer, Function<T, Integer>> keyExtractor, BiFunction<Integer, Integer, Boolean> baseCaseChecker, Function<Integer, Integer> currentPositionIncrementer) {
        if (baseCaseChecker.apply(currentPosition, d)) return arr;
        return recursiveF(sort_with_satellite_data(arr, k, keyExtractor.apply(currentPosition)), d, k, currentPositionIncrementer.apply(currentPosition), keyExtractor, baseCaseChecker, currentPositionIncrementer);
    }

    public static void main(String[] args) {
        Integer[] arr = {170, 485, 775, 900, 180, 124, 1521, 666};
        Integer[] sortedArr = sort(arr, 4, 9);
        System.out.println(Arrays.toString(sortedArr));

        String[] arr2 = {"cexa","kilo","mega","giga","tera","peta","exa","zetta","yotta","cex"};
        String[] sortedArr2 = sort(arr2, 10, 255);
        System.out.println(Arrays.toString(sortedArr2));
    }
}
