package challenges.numbertheory

import org.scalatest.{FunSpec, Matchers}
import Primes._
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

    it("gcd(10,6) = gcd(6,10)"){
      assert(euclideanAlgorithm(10,6) == euclideanAlgorithm(6,10))
    }

    it("gcd(63,28) = 7"){
      assert(euclideanAlgorithm(63,28) == 7)
    }

    describe("Extended Euclidean algorithm") {
      it("gcd(10,6) = 2 = 10*(-1) + 6*2"){
        assert(extendedEuclideanAlgorithm(10,6) == (2,-1,2))
      }

      it("gcd(6,10) = 2 = 6*2 + 10*(-1)"){
        assert(extendedEuclideanAlgorithm(6,10) == (2,2,-1))
      }

      it("gcd(239,201) = 1 = 239*(-37) + 201*44"){
        assert(extendedEuclideanAlgorithm(239,201) == (1,-37,44))
      }
    }

    describe("Diophantine equation") {
      it("10x+6y=14, x=-7,y=14"){
        assert(diophantineEquation(10,6,14).contains(-7,14))
      }

      it("6x+10y=14, x=14,y=-7"){
        assert(diophantineEquation(6,10,14).contains(14,-7))
      }

      it("8x+4y=7 has no solution"){
        assert(diophantineEquation(8,4,7).isEmpty)
      }
    }

    describe("least common multiple") {
      it("lcm(2,3)=6"){
        assert(lcm(2,3) == 6)
      }
    }

    describe("Modular division"){
      it("2/5 ≡ 4 (mod 6)"){
        assert(modularDivisionBruteForce(5, 2, 6).contains(4))
        assert(modularDivision(5, 2, 6).contains(4))
      }

      it("1/3 (mod 6) does not exist"){
        assert(multiplicativeInverseBruteForce(3, 6).isEmpty)
        assert(modularDivision(3, 1, 6).isEmpty)
      }

      it("7/2 ≡ 8 (mod 9) "){
        assert(modularDivisionBruteForce(2, 7, 9).contains(8))
        assert(modularDivision(2, 7, 9).contains(8))
      }

      it("1/7 ≡ 1 (mod 6) "){
        assert(multiplicativeInverseBruteForce(7, 6).contains(1))
        assert(modularDivision(7, 1, 6).contains(1))
      }

      it("1/5 ≡ 5 (mod 6)"){
        assert(multiplicativeInverseBruteForce(5, 6).contains(5))
        assert(modularDivision(5, 1, 6).contains(5))
      }

      it("1/2 (mod 6) does not exist"){
        assert(multiplicativeInverseBruteForce(2, 6).isEmpty)
        assert(modularDivision(2, 1, 6).isEmpty)
      }

      it("6/4 ≡ 5 (mod 7)"){
        assert(modularDivisionBruteForce(4, 6, 7).contains(5))
        assert(modularDivision(4, 6, 7).contains(5))
      }
    }

  }

  describe("Modular exponentiation"){
    it("7^4 (mod 11) = 3"){
      assert(modularExponentiationBruteForce(7, 4, 11) == 3)
      assert(modularExponentiation(7, 4, 11) == 3)
      assert(fastModularExponentiation(7, 4, 11) == 3)
      assert(fastModularExponentiation2(7, 4, 11) == 3)
    }

    it("7^128 (mod 11) = 9"){
      assert(modularExponentiationBruteForce(7, 128, 11) == 9)
      assert(modularExponentiation(7, 128, 11) == 9)
      assert(fastModularExponentiation(7, 128, 11) == 9)
      assert(fastModularExponentiation2(7, 128, 11) == 9)
    }

    it("7^13 (mod 11) = 2"){
      assert(modularExponentiationBruteForce(7, 13, 11) == 2)
      assert(modularExponentiation(7, 13, 11) == 2)
      assert(fastModularExponentiation2(7, 13, 11) == 2)
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
