package challenges.missingnumberarray

import challenges.missingnumberarray.MissingNumberOnArray._
import org.scalacheck.Gen
import org.scalatest.FunSpec
import org.scalatest.prop.PropertyChecks

class MissingNumberOnArrayTest extends FunSpec with PropertyChecks{


  //==== PROPERTY-BASED TESTING ======

  /*
    Shrinking ignores restrictions of the generator, e.g. shrinking a Gen.choose(1, 10) might try to falsify the
    property with values such as 0, and -1

    With this statement, shrinking is disabled
    */
  import org.scalacheck.Shrink.shrinkAny

  /**
    * Generator of arrays of integers "i" of length "k" such that:
    * 0 < k <= n
    * 0 < i <= n
    *
    * For instance, given n=6:
    * + k=5 -> [1,2,3,4,5], missing value=[6]
    * + k=5 -> [1,2,3,4,6], missing value=[5]
    * + k=6 -> [1,2,3,4,5,6], missing value=[]
    *
    */
  def missingNumbersOnArrayGen(n: Int): Gen[Array[Int]] = for {
    k <- Gen.choose(1, n)
    is <- Gen.pick(k, 1 to n)
  } yield is.toArray

  val n = 15
  forAll (missingNumbersOnArrayGen(n)) { arr =>
    assert((arr ++ solutionN(arr, n)).toList.sorted == (1 to n).toList)
    assert(solutionNOptimised(arr, n) == solutionN(arr, n))
  }


  //==== FUNCTIONAL TESTING ======

  describe("one missing element") {
    describe("given the array of integers [1,3,2,5] with elements between 1 and 5") {
      it("the missing element is 4") {
        assert(solution1(Array(1L, 3L, 2L, 5L), 5) == 4)
      }
    }
  }

  describe("multiple missing elements") {
    describe("given the array of integers [1,3,2,5,7,8] with elements between 1 and 8") {

      val arr = Array(1, 3, 2, 5, 7, 8)
      val n = 8
      val expectedSolution = List(4, 6)
      it("the missing elements are 4 and 6") {
        assert(solutionN(arr, n) == expectedSolution)
        assert(solutionNOptimised(arr, n) == expectedSolution)
      }
    }

    describe("given the array of integers [4,3,2,5,7,6] with elements between 1 and 8") {
      val arr = Array(4,3,2,5,7,6)
      val n = 8
      val expectedSolution = List(1,8)
      it("the missing elements are the extremes 1 and 8") {
        assert(solutionN(arr, n) == expectedSolution)
        assert(solutionNOptimised(arr, n) == expectedSolution)
      }
    }

    describe("given the array of integers [1,2,3] with elements between 1 and 10") {
      val arr = Array(1,2,3)
      val n = 10
      val expectedSolution = List(4,5,6,7,8,9,10)
      it("the missing elements are 4,5,6,7,8,9,10") {
        assert(solutionN(arr, n) == expectedSolution)
        assert(solutionNOptimised(arr, n) == expectedSolution)
      }
    }
  }
}
