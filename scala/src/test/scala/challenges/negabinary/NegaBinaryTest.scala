package challenges.negabinary

import org.scalatest.FunSpec
import NegaBinary._
import org.scalatest.prop.PropertyChecks
import org.scalacheck.Gen

class NegaBinaryTest extends FunSpec with PropertyChecks{


  describe("from base 10"){

    describe("to base 10"){
      it("-12 == -12"){
        assert(fromBase10ToTargetBase(-12, 10) == "-12")
      }
    }

    describe("to base -10"){

      val targetBase = -10
      it("0 -> 0"){
        assert(fromBase10ToTargetBase(0, targetBase) == "0")
      }

      it("1 -> 1"){
        assert(fromBase10ToTargetBase(1, targetBase) == "1")
      }

      it("-15 -> 25"){
        assert(fromBase10ToTargetBase(-15, targetBase) == "25")
      }

      it("10 -> 190"){
        assert(fromBase10ToTargetBase(10, targetBase) == "190")
      }
    }

    describe("to base -2"){
      val targetBase = -2
      it("0 -> 0"){
        assert(fromBase10ToTargetBase(0, targetBase) == "0")
      }

      it("1 -> 1"){
        assert(fromBase10ToTargetBase(1, targetBase) == "1")
      }

      it("-1 -> 11"){
        assert(fromBase10ToTargetBase(-1, targetBase) == "11")
      }

      it("-9 -> 1011"){
        assert(fromBase10ToTargetBase(-9, targetBase) == "1011")
      }

      it("9 -> 11001"){
        assert(fromBase10ToTargetBase(9, targetBase) == "11001")
      }
    }
  }


  describe("to base 10"){

    describe("from base -10"){
      val originBase = -10
      it("0 -> 0"){
        assert(fromOriginBaseToBase10("0", originBase) == 0)
      }

      it("1 -> 1"){
        assert(fromOriginBaseToBase10("1", originBase) == 1)
      }

      it("25 -> -15"){
        assert(fromOriginBaseToBase10("25", originBase) == -15)
      }

      it("190 -> 10"){
        assert(fromOriginBaseToBase10("190", originBase) == 10)
      }
    }

    describe("from base -2"){
      val originBase = -2
      it("0 -> 0"){
        assert(fromOriginBaseToBase10("0", originBase) == 0)
      }

      it("1 -> 1"){
        assert(fromOriginBaseToBase10("1", originBase) == 1)
      }

      it("11 -> -1"){
        assert(fromOriginBaseToBase10("11", originBase) == -1)
      }

      it("1011 -> -9"){
        assert(fromOriginBaseToBase10("1011", originBase) == -9)
      }

      it("11001 -> 9"){
        assert(fromOriginBaseToBase10("11001", originBase) == 9)
      }
    }

    describe("from base 2"){
      it("110 -> 6"){
        assert(fromOriginBaseToBase10("110", 2) == 6)
      }

      it("-110 -> -6"){
        assert(fromOriginBaseToBase10("-110", 2) == -6)
      }
    }
  }


  // ==== PROPERTY BASED TEST ====

  /*
    Shrinking ignores restrictions of the generator, e.g. shrinking a Gen.choose(1, 10) might try to falsify the
    property with values such as 0, and -1

    With this statement, shrinking is disabled
    */
  import org.scalacheck.Shrink.shrinkAny

  def positiveTargetBaseGenerator(maxN: Int): Gen[(Int, Int)] =  for {
    n <- Gen.chooseNum(-maxN, maxN)
    targetBase <- Gen.chooseNum(2, 10)
  } yield (n, targetBase)

  def negativeTargetBaseGenerator(maxN: Int): Gen[(Int, Int)] =  for {
    n <- Gen.chooseNum(1, maxN)
    targetBase <- Gen.chooseNum(-10, -2)
  } yield (n, targetBase)

  forAll(positiveTargetBaseGenerator(100)) {
    case (n, targetBase) =>
      assert(fromOriginBaseToBase10(fromBase10ToTargetBase(n, targetBase), targetBase) == n)
  }

  forAll(negativeTargetBaseGenerator(100)) {
    case (n, targetBase) =>
      assert(fromOriginBaseToBase10(fromBase10ToTargetBase(n, targetBase), targetBase) == n)
  }


}
