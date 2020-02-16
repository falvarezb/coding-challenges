package challenges.numbertheory

import org.scalatest.{FunSpec, Matchers}
import Primes._
import com.typesafe.scalalogging.LazyLogging
import org.scalatest.prop.PropertyChecks
import org.scalacheck.Gen

class PrimesTest extends FunSpec with Matchers with PropertyChecks {

  def test(f: BigInt => List[BigInt], n: BigInt, l: List[BigInt]) = assert(f(n) == l)


  describe("Prime factors of a number"){

    it("5 = [5]"){
      test(primeFactors, 5, List(5))
    }

    it("15 = [3,5]"){
      test(primeFactors, 15, List(3,5))
    }

    it("16 = [2,2,2,2]"){
      test(primeFactors, 16, List(2,2,2,2))
    }
  }

  describe("Divisors of a number"){

    it("5 = [1,5]"){
      test(divisors, 5, List(1,5))
    }

    it("15 = [1,3,5,15]"){
      test(divisors, 15, List(1,3,5,15))
    }

    it("16 = [1,2,4,8,16]"){
      test(divisors, 16, List(1,2,4,8,16))
    }

    it("28 = [1, 2, 4, 7, 14, 28]"){
      test(divisors, 28, List(1, 2, 4, 7, 14, 28))
    }

    it("63 = [1, 3, 7, 9, 21, 63]"){
      test(divisors, 63, List(1, 3, 7, 9, 21, 63))
    }
  }

  describe("Euclidean algorithm") {

    it("gcd(10,6) = 2"){
      assert(euclideanAlgorithm(10,6) == 2)
    }

    it("gcd(28,63) = 3"){
      assert(euclideanAlgorithm(63,28) == 7)
    }

    describe("Extended Euclidean algorithm") {
      it("gcd(10,6) = 2 = 10*(-1) + 6*2"){
        assert(extendedEuclideanAlgorithm(10,6) == (2,-1,2))
      }

      it("gcd(239,201) = 1 = 239*(-37) + 201*44"){
        assert(extendedEuclideanAlgorithm(239,201) == (1,-37,44))
      }
    }

  }


  //==== PROPERTY-BASED TESTING ======

  /*
  Shrinking ignores restrictions of the generator, e.g. shrinking a Gen.choose(1, 10) might try to falsify the
  property with values such as 0, and -1

  With this statement, shrinking is disabled
  */
  import org.scalacheck.Shrink.shrinkAny

  forAll{
    for {
      a <- Gen.oneOf((2 until 10000).toList)
      b <- Gen.oneOf((1 until a).toList)
    } yield (a,b)
  }{
    case (a,b) =>
      //Euclidean algorithm
      assert(divisors(a).intersect(divisors(b)).max.toInt == euclideanAlgorithm(a, b))
      //Extended Euclidean algorithm
      val (d, x, y) = extendedEuclideanAlgorithm(a, b)
      assert(a*x + b*y == d)
      //Num divisors of n as sum of exponents of the prime factorisation of n
      assert(count(divisors(a)) == numDivisors(a))
      //All common divisors of a and b are also divisors of gcd(a,b)
      assert(divisors(a).intersect(divisors(b)).forall(d % _ == 0))
  }


}
