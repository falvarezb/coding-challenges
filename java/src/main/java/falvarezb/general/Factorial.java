package falvarezb.general;

import java.math.BigInteger;
import java.util.stream.IntStream;

public class Factorial {

    static int factorial(int n) {
        return recImpl(n);
    }

    static int loopImpl(int n) {
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    static int funcImpl(int n) {
        return IntStream.rangeClosed(2,n).reduce(1, (x,y) -> x*y);
    }

    static int recImpl(int n) {
        if(n == 0 || n==1) return 1;
        return n * recImpl(n-1);
    }

    static BigInteger factorialBigInt(BigInteger n) {
        if(n == BigInteger.ZERO || n == BigInteger.ONE) return BigInteger.ONE;
        return n.multiply(factorialBigInt(n.subtract(BigInteger.ONE)));
    }

    static BigInteger factorialTailRecursive(BigInteger n) {
        return aux(n, BigInteger.ONE);
    }

    private static BigInteger aux(BigInteger n, BigInteger acc) {
        if(n == BigInteger.ZERO || n == BigInteger.ONE) return acc;
        return aux(n.subtract(BigInteger.ONE), acc.multiply(n));
    }
}
