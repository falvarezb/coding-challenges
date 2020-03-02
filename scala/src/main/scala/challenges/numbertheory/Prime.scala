package challenges.numbertheory

import scala.annotation.tailrec
import scala.collection.mutable
import scala.math.BigInt
import scala.math.{sqrt, ceil}
import Math.floorMod

object Primes {

  def isPrime(x: BigInt): Boolean = (2 to sqrt(x.doubleValue()).toInt).forall(x%_ > 0)

  /**
    * Find prime numbers in given list
    */
  def eratosthenesSieve(l: List[Int]): List[Int] = {
    assert(l.head > 1)
    l match {
      case Nil => Nil
      case _ :: Nil => l
      case x :: xs => x :: eratosthenesSieve(xs.filter(_ % x > 0))
    }
  }

  def primeNumbersGenerator: Stream[BigInt] = {
    def oddNumbers(n: BigInt): Stream[BigInt] = n #:: oddNumbers(n + 2)
    2 #:: oddNumbers(3).filter(isPrime)
  }

  def primesLessThan(n: Int): List[Int] = {
    def isPrime(x: Int): Boolean = (2 to sqrt(x).toInt).forall(x%_ > 0)
    (2 :: (3 until n by 2).toList).filter(isPrime)
  }

  def primesLessThan_optimised(n: Int): List[Int] = {

    val primes = mutable.ListBuffer(2)
    for(x <- 3 until n by 2){
      if(primes.filter(_ <= sqrt(x).toInt).forall(x%_ > 0))
        primes += x
    }
    primes.toList
  }

  def leastPrimeFactor(i: BigInt): BigInt = {
    val iter = primeNumbersGenerator.iterator
    @tailrec
    def f(prime: BigInt): BigInt =
      if(i%prime == 0) prime
      else if(prime >= i.bigInteger.sqrt()) i
      else f(iter.next())
    f(iter.next())
  }

  /**
    * Calculates prime factorisation of n. For instance, for n=15, n = 3*5
    * @param n
    * @return
    */
  def primeFactors(n: BigInt): List[BigInt] = {
    @tailrec
    def f(m: BigInt, factors: List[BigInt]): List[BigInt] = {
      val x = leastPrimeFactor(m)
      val quotient = m / x
      if (quotient > 1)
        f(quotient, x :: factors)
      else
        x :: factors
    }

    f(n, Nil).reverse
  }


  def divisors(n: BigInt): List[BigInt] = {
    Range.BigInt.inclusive(1, n, 1).filter(n%_ == 0).toList
  }

  private[numbertheory] def count(l: Seq[BigInt]): BigInt = {
    var c: BigInt = 0
    for(_ <- l)
      c += 1
    c
  }

  /**
    * Given the prime decomposition of n
    *
    * n = p^a*q^b*r^c
    *
    * the number of divisors can be obtained as (a+1)*(b+1)*(c+1)
    */
  def numDivisors(n: BigInt): BigInt = {
    val exponents: List[BigInt] = primeFactors(n).groupBy(n => n).values.toList.map(count(_))
    exponents.map(_ + 1).product
  }

  /**
    * Euclidean algorithm to calculate the greatest common divisor of 2 numbers a and b
    * https://exploringnumbertheory.wordpress.com/2013/07/28/the-euclidean-algorithm/
    * https://en.wikipedia.org/wiki/Euclidean_algorithm
    *
    * The following two formulations are equivalent:
    * for a ≥ b, gcd(a, b) = gcd(b, a mod b) (where a mod b represents the remainder of the division a/b)
    * for a ≥ b, d|a and d|b iff d|a-b (where d|a means d divides a)
    *
    * @param a x must be equal or greater than y
    * @param b
    * @return
    */
  @tailrec
  def euclideanAlgorithm(a: Int, b: Int): Int = {
    if(b == 0) a else euclideanAlgorithm(b, a % b)
  }

  /**
    * Extended Euclidean algorithm to express the gcd of a and b as linear combination of a and b
    * for a ≥ b, if d = gcd(a, b) then there are integers x and y such that: ax + by = d (Bezout's identity)
    *
    * By the Euclidean algorithm, d = gcd(b, a mod b), so if we know how to express d as linear combination of
    * b and (a mod b), d = bp + (a mod b)q, then d as linear combination of a and b is:
    * d = aq + b(p - floor(a/b)q)
    *
    * @param a
    * @param b
    * @return (d, x, y) d = gcd(a, b), x and y are called Bezout's coefficients
    */
  def extendedEuclideanAlgorithm(a: Int, b: Int): (Int, Int, Int) = {
    if(b == 0){
      (a, 1, 0)
    }
    else{
      val (d, p, q) = extendedEuclideanAlgorithm(b, a%b)
      (d, q, p - math.floor(a/b).toInt * q)
    }
  }

  /**
    * return (x, y) such that a * x + b * y = c
    *
    * THEOREM
    * Given integers a, b, c (at least one of a and b ̸= 0), the Diophantine equation ax+by = c
    * has a solution (where x and y are integers) if and only if gcd(a, b) | c
    *
    * The proof of this theorem also provides a method to construct the solutions x and y:
    *
    * x = c/gcd(a,b) * x'
    * y = c/gcd(a,b) * y'
    *
    * where x' and y' are Bezout's coefficients given by the extended Euclid's algorithm:
    *
    * ax'+by' = gcd(a,b)
    *
    * @param a
    * @param b
    * @param c
    * @return
    */
  def diophantineEquation(a: Int, b: Int, c: Int): Option[(Int, Int)] = {
    val (d, x, y) = extendedEuclideanAlgorithm(List(a,b).max, List(a,b).min)
    if (c%d == 0) Some(if(a > b) (c/d*x, c/d*y) else (c/d*y, c/d*x)) else None
  }

  /**
    * returns least common multiple of a and b
    *
    * lcm(a,b) * gcd(a,b) = a*b
    *
    * @param a
    * @param b
    * @return
    */
  def lcm(a: Int, b: Int): Int = a*b/euclideanAlgorithm(List(a,b).max, List(a,b).min)


  /**
    * Given a ̸= 0 and b, there exists x (not always) such that a * x ≡ b (mod m), therefore
    * x plays the role of modular division x = b/a (mod m)
    *
    * Example:
    *
    * 2/5 ≡ 4 (mod 6) as 4*5≡2 (mod 6)
    *
    * Modular division is not always possible. In the following example, there is no x such that:
    *
    * 3*x ≡ 1 (mod 6)
    *
    * @param a
    * @param b
    * @param m
    * @return
    */
  def modularDivisionBruteForce(a: Int, b: Int, m: Int): Option[Int] = {
    assert(a != 0)

    for(x <- 1 to m)
      if (floorMod(x*a,m) == floorMod(b,m))
        return Some(x)
    None
  }

  /**
    * A multiplicative inverse of a mod m is a' such that: a*a' ≡ 1 (mod m)
    *
    * @param a
    * @param m
    * @return
    */
  def multiplicativeInverseBruteForce(a: Int, m: Int): Option[Int] = {
    modularDivisionBruteForce(a, 1, m)
  }


  /**
    * Given that congruence is preserved under multiplication, it's easy to prove that b/a ≡ b*a' (mod m), where a' is
    * the multiplicative inverse modulo m of a
    *
    * Also, it's possible to prove that a has a multiplicative inverse modulo m iff gcd(a, m) = 1 and the
    * multiplicative inverse is given by the solution s of the Diophantine equation in the variables s and t:
    *
    * as + mt = 1
    *
    * So finally, b/a ≡ b*s (mod m)
    *
    * @param a
    * @param b
    * @param m
    * @return
    */
  def modularDivision(a: Int, b: Int, m: Int): Option[Int] = {
    assert(a != 0)

    diophantineEquation(a, m, 1).map{
      case (s, _) => floorMod(b*s,m)
    }
  }

  /**
    * Returns b^e (mod m)
    * @param b
    * @param e
    * @param m
    */
  def modularExponentiationBruteForce(b: Int, e: Int, m: Int): Int = {
    BigInt(b).pow(e) % m toInt
  }

  /**
    * Implementation based on the property that congruence is preserved under multiplication:
    * (a ⋅ b) mod m = [(a mod m) ⋅ (b mod m)] mod m
    *
    * The process takes e steps
    *
    * @param b
    * @param e
    * @param m
    * @return
    */
  def modularExponentiation(b: Int, e: Int, m: Int): Int = {

    def aux(e: Int): Int = {
      if(e == 1)
        b%m
      else
        ((b%m) * aux(e - 1))%m
    }

    aux(e)
  }

  /**
    * Similar to the previous one but using exponentiation by squaring (aka binary exponentiation)
    *
    * Useful when e is a power of 2, e=2^k, the process takes k steps
    *
    * @param b
    * @param e
    * @param m
    * @return
    */
  def fastModularExponentiation(b: Int, e: Int, m: Int): Int = {

    def aux(e: Int): Int = {
      if(e == 1)
        b%m
      else
        Math.pow(aux(e/2),2).toInt %m
    }

    aux(e)
  }

  /**
    * Similar to the previous one but using exponentiation by squaring (aka binary exponentiation)
    *
    * b^e = b^(a1*2^0 + a2*2^1 + ... aN*2*N) = b^(a1*2^0) * .... * b^(aN*2^N) where a1, a2 ... aN take the values 0 or 1
    *
    * Steps:
    * 1. Rewrite e in binary form
    * 2. Compute b^(2^k) mod m for each element of the binary representation of the exponent
    * 3. Multiply the results of previous step
    *
    * @param b
    * @param e
    * @param m
    * @return
    */
  def fastModularExponentiation2(b: Int, e: Int, m: Int): Int = {

    def aux(e: Int): Int = {
      if(e == 0)
        1
      else if(e == 1)
        b%m
      else
        Math.pow(aux(e/2),2).toInt %m
    }

    val binaryE = binaryRepresentation(e)
    binaryE.zipWithIndex.map {
      case (digit, position) => aux(digit * Math.pow(2, position).toInt)
    }.reduceLeft((acc, x) => acc * x % m)
  }

  /**
    * Leading digit is in the rightmost position
    * @param n
    * @return
    */
  def binaryRepresentation(n: Int): List[Int] = {

    val base = 2
    val q = n/base
    val r = n%base

    if(q == 0) r :: Nil
    else r :: binaryRepresentation(q)
  }

  def primesSet(n: Int): Set[BigInt] = primeNumbersGenerator take(n) toSet
  def primesList(n: Int): List[BigInt] = primeNumbersGenerator take(n) toList

}

