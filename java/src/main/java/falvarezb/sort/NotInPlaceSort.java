package falvarezb.sort;

@FunctionalInterface
public non-sealed interface NotInPlaceSort extends Sort {
    int[] sort(int[] arr);
}
