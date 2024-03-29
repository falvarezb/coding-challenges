package chiefhopper;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.List;

public class ChiefHopperJava {
    public static void main(String[] args) {
        List<Integer> testCase2 = Arrays.asList(1401,2019,1748,3785,3236,3177,3443,3772,2138,1049,353,908,310,2388,1322,88,2160,2783,435,2248,1471,706,2468,2319,3156,3506,2794,1999,1983,2519,2597,3735,537,344,3519,3772,3872,2961,3895,2010,10,247,3269,671,2986,942,758,1146,77,1545,3745,1547,2250,2565,217,1406,2070,3010,3404,404,1528,2352,138,2065,3047,3656,2188,2919,2616,2083,1280,2977,2681,548,4000,1667,1489,1109,3164,1565,2653,3260,3463,903,1824,3679,2308,245,2689,2063,648,568,766,785,2984,3812,440,1172,2730);
        List<Integer> testCase12 = Arrays.asList(4,4);
        System.out.println(chiefHopper(Arrays.asList(3,4,3,2,4)));//expected 4
        System.out.println(chiefHopper(testCase2));//expected 1859
        System.out.println(chiefHopper(testCase12));//expected 3
    }

    /**
     * Key facts
     * ----------
     *
     * 1. in all cases:
     * newEnergy = 2*botEnergy - height
     *
     * 2. if we write newEnergy as a function 'f' of botEnergy
     * f(botEnergy-1) = fot(botEnergy) - 2^(length of arr)
     */
    public static BigInteger finalEnergy(BigInteger initialEnergy, List<Integer> list)  {
        return list.stream()
                .map(BigInteger::valueOf)
                .reduce(initialEnergy, (energy, height) -> energy.multiply(BigInteger.valueOf(2)).subtract(BigInteger.valueOf(height.intValue())));
    }

    public static int chiefHopper(List<Integer> list) {
        int max = list.stream().max(Integer::compareTo).get();
        BigInteger energy = finalEnergy(BigInteger.valueOf(max), list);
        return max-energy.divide(BigInteger.valueOf(2).pow(list.size())).intValue();
    }
}
