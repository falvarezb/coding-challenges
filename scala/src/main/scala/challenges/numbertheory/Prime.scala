package challenges.numbertheory

import scala.annotation.tailrec
import scala.collection.mutable
import scala.math.BigInt
import scala.math.{sqrt, ceil}

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
    assert(a >= b)
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
    assert(a >= b)
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
  def diophantineEquation(a: Int, b: Int, c: Int): (Int, Int) = {
    val (d, x, y) = extendedEuclideanAlgorithm(List(a,b).max, List(a,b).min)
    assert(c%d == 0)
    if(a > b) (c/d*x, c/d*y)
    else (c/d*y, c/d*x)
  }

  def primesSet(n: Int): Set[BigInt] = primeNumbersGenerator take(n) toSet
  def primesList(n: Int): List[BigInt] = primeNumbersGenerator take(n) toList

}

