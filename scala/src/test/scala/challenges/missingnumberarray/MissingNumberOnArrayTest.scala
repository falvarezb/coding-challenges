package challenges.missingnumberarray

import challenges.missingnumberarray.MissingNumberOnArray._
import org.scalacheck.Gen
import org.scalatest.FunSpec
import org.scalatest.prop.PropertyChecks

class MissingNumberOnArrayTest extends FunSpec with PropertyChecks{

  /*
    Shrinking ignores restrictions of your generator, e.g. shrinking a Gen.choose(1, 10) might try to falsify the
    property with values such as 0, and -1

    With this statement, shrinking is disabled
    */
  import org.scalacheck.Shrink.shrinkAny

  /**
    * Generator of arrays of integers "i" of length "l" such that:
    * 0 < i <= maxLength
    * 0 < l <= maxLength
    *
    * For instance, given maxLength=6:
    * + l=5 -> [1,2,3,4,5], missing value=[]
    * + l=5 -> [1,2,3,4,6], missing value=[6]
    * + l=6 -> [1,2,3,4,5,6], missing value=[]
    *
    */
  def missingNumbersOnArrayGen(maxLength: Int): Gen[Array[Int]] = for {
    l <- Gen.choose(1, maxLength)
    is <- Gen.pick(l, 1 to maxLength)
  } yield is.toArray

  val maxLength = 15
  forAll (missingNumbersOnArrayGen(maxLength)) { arr =>
    assert((arr ++ solutionN(arr, maxLength)).toList.sorted == (1 to maxLength).toList)
    assert((arr ++ solutionNOptimised(arr, maxLength)).toList.sorted == (1 to maxLength).toList)
  }

  describe("one missing element") {
    describe("given the array of integers [1,3,2,5] with elements between 1 and 5") {
      it("the missing element is 4") {
        assert(solution1(Array(1l, 3l, 2l, 5l), 5) == 4)
      }
    }
  }

  describe("two missing elements") {
    describe("given the array of integers [1,3,2,5,7,8] with elements between 1 and 8") {

      val arr = Array(1, 3, 2, 5, 7, 8)
      val max = 8
      val expectedSolution = List(4, 6)
      it("the missing elements are 4 and 6") {
        assert(solutionN(arr, max) == expectedSolution)
        assert(solutionNOptimised(arr, max) == expectedSolution)
      }
    }

    describe("given the array of integers [4,3,2,5,7,6] with elements between 1 and 8") {
      val arr = Array(4,3,2,5,7,6)
      val max = 8
      val expectedSolution = List(1,8)
      it("the missing elements are the extremes 1 and 8") {
        assert(solutionN(arr, max) == expectedSolution)
        assert(solutionNOptimised(arr, max) == expectedSolution)
      }
    }

    describe("given the array of integers [1,2,3] with elements between 1 and 10") {
      val arr = Array(1,2,3)
      val max = 10
      val expectedSolution = List(4,5,6,7,8,9,10)
      it("the missing elements are 4,5,6,7,8,9,10)") {
        assert(solutionN(arr, max) == expectedSolution)
        assert(solutionNOptimised(arr, max) == expectedSolution)
      }
    }
  }
}
