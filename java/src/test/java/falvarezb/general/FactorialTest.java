package falvarezb.general;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigInteger;

import static org.junit.jupiter.api.Assertions.*;

public class FactorialTest {

    @Test
    @DisplayName("0! = 1")
    public void test0() {
         assertEquals(1, Factorial.factorial(0));
    }

    @Test
    @DisplayName("1! = 1")
    public void test1() {
        assertEquals(1, Factorial.factorial(1));
    }

    @Test
    @DisplayName("2! = 2")
    public void test2() {
        assertEquals(2, Factorial.factorial(2));
    }

    @Test
    @DisplayName("5! = 120")
    public void test5() {
        assertEquals(120, Factorial.factorial(5));
    }

    @Test
    @DisplayName("1000! = big")
    public void testBig() {
        assertEquals(BigInteger.valueOf(120), Factorial.factorialTailRecursive(BigInteger.valueOf(10000000)));
    }
}
