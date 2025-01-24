package falvarezb;

import java.lang.reflect.Array;

public class TestUtil {

    public static int[] generateRandomArray(int size, int digits) {
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = (int) (Math.random() * Math.pow(10, digits));
        }
        return arr;
    }

    public static <T> T[] mergeArrays(T[] arr1, T[] arr2) {
        @SuppressWarnings("unchecked")
        T[] arr = (T[]) Array.newInstance(arr1.getClass().getComponentType(), arr1.length + arr2.length);
        System.arraycopy(arr1, 0, arr, 0, arr1.length);
        System.arraycopy(arr2, 0, arr, arr1.length, arr2.length);
        return arr;
    }
}
