package challenges.stairs

import org.scalatest.FunSpec
import Stairs._
import org.scalacheck.Gen
import org.scalatest.prop.PropertyChecks

class StairsTest extends FunSpec with PropertyChecks{


  //==== FUNCTIONAL TESTING ======

  describe("step values: 1, 4, 5") {
    val values = List(1, 4, 5)

    describe("4 stairs") {
      val n = 4

      it("countAllCombinations") {
        assert(countAllCombinations(n, values) == 2)
      }

      it("enumerateAllCombinations") {
        assert(enumerateAllCombinations(n, values) == List(List(1,1,1,1), List(4)))
      }

      it("enumerateAllOptimalCombinations") {
        assert(enumerateAllOptimalCombinations(n, values) == List(List(4)))
      }

      it("enumerateAllOptimalCombinationsWithoutPermutation") {
        assert(enumerateAllOptimalCombinationsWithoutPermutation(n, values) == List(List(4)))
      }

      it("enumerateAnyOptimalCombination") {
        assert(enumerateAnyOptimalCombination(n, values) == List(4))
      }

      it("greedyCombination") {
        assert(greedyCombination(n, values) == List(4))
      }
    }

    describe("8 stairs") {
      val n = 8

      it("countAllCombinations") {
        assert(countAllCombinations(n, values) == 11)
      }

      it("enumerateAllCombinations") {
        assert(enumerateAllCombinations(n, values) == List(List(1,1,1,1,1,1,1,1), List(1,1,1,1,4), List(1,1,1,4,1), List(1,1,1,5), List(1,1,4,1,1), List(1,1,5,1), List(1,4,1,1,1), List(1,5,1,1), List(4,1,1,1,1), List(4,4), List(5,1,1,1)))
      }

      it("enumerateAllOptimalCombinations") {
        assert(enumerateAllOptimalCombinations(n, values) == List(List(4,4)))
      }

      it("enumerateAllOptimalCombinationsWithoutPermutation") {
        assert(enumerateAllOptimalCombinationsWithoutPermutation(n, values) == List(List(4,4)))
      }

      it("enumerateAnyOptimalCombination") {
        assert(enumerateAnyOptimalCombination(n, values) == List(4,4))
      }

      it("greedyCombination") {
        assert(greedyCombination(n, values) == List(5,1,1,1))
      }
    }

  }

  describe("step values: 5") {
    val values = List(5)

    describe("6 stairs") {
      val n = 6

      it("should countAllCombinations") {
        assert(countAllCombinations(n, values) == 0)
      }

      it("should enumerateAllCombinations") {
        assert(enumerateAllCombinations(n, values) == List())
      }

      it("should enumerateAllOptimalCombinations") {
        assert(enumerateAllOptimalCombinations(n, values) == List())
      }

      it("should enumerateAnyOptimalCombination") {
        assert(enumerateAnyOptimalCombination(n, values) == List())
      }

      it("should enumerateAnyOptimalCombinationGreedy") {
        assert(greedyCombination(n, values) == List())
      }
    }

    describe("2 stairs") {
      val n = 2

      it("should countAllCombinations") {
        assert(countAllCombinations(n, values) == 0)
      }

      it("should enumerateAllCombinations") {
        assert(enumerateAllCombinations(n, values) == List())
      }

      it("should enumerateAllOptimalCombinations") {
        assert(enumerateAllOptimalCombinations(n, values) == List())
      }

      it("should enumerateAnyOptimalCombination") {
        assert(enumerateAnyOptimalCombination(n, values) == List())
      }

      it("should enumerateAnyOptimalCombinationGreedy") {
        assert(greedyCombination(n, values) == List())
      }
    }

  }

  describe("step values: 1, 2, 3") {
    val values = List(1,2,3)

    describe("8 stairs") {
      val n = 8

      it("should countAllCombinations") {
        assert(countAllCombinations(n, values) == 81)
      }

      it("should enumerateAllOptimalCombinations") {
        assert(enumerateAllOptimalCombinations(n, values) == List(List(2, 3, 3), List(3, 2, 3), List(3, 3, 2)))
      }

      it("enumerateAllOptimalCombinationsWithoutPermutation") {
        assert(enumerateAllOptimalCombinationsWithoutPermutation(n, values) == List(List(2,3,3)))
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

  /**
    * Generator of tuples of number of stairs 'n' and list of steps 'values':
    * - 'n' is a value such that 0 < n <= maxStairs
    * - values[i] is value such that 0 < values[i] <= n for all 0 < i <= n
    *
    */
  def stairsGenerator(maxStairs: Int): Gen[(Int, List[Int])] = for{
    n <- Gen.choose(1, maxStairs)
    length <- Gen.choose(1, n)
    values <- Gen.pick(length, 1 to n)
  } yield (n, values.toList)

  val maxStairs = 22
  forAll(stairsGenerator(maxStairs)){
    case (stairs, steps) =>
      val allCombinations: List[List[Int]] = enumerateAllCombinations(stairs, steps)
      val allOptimalCombinations = enumerateAllOptimalCombinations(stairs, steps)
      val anyOptimalCombination: List[Int] = enumerateAnyOptimalCombination(stairs, steps)
      val gCombination = greedyCombination(stairs, steps)
      assert(allCombinations.length == countAllCombinations(stairs, steps))
      assert(allCombinations.forall(_.isEmpty) && allOptimalCombinations.forall(_.isEmpty) || allOptimalCombinations.forall(allCombinations.contains(_)))
      assert(allOptimalCombinations.forall(_.isEmpty) && anyOptimalCombination.isEmpty || allOptimalCombinations.contains(anyOptimalCombination))
      assert(allOptimalCombinations.forall(_.isEmpty) || gCombination.isEmpty || allOptimalCombinations.forall(_.length <= gCombination.length))
  }

}
