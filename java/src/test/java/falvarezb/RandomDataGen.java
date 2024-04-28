package falvarezb;

public class RandomDataGen {
    public static int[] generateRandomArray(int size, int digits) {
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = (int) (Math.random() * Math.pow(10, digits));
        }
        return arr;
    }
}
