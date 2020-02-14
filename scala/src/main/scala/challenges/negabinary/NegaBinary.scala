package challenges.negabinary

import scala.annotation.tailrec

/**
  * https://en.wikipedia.org/wiki/Negative_base
  *
  * In negative base, all integers, positive and negative, can be represented without a sign.
  */
object NegaBinary {


  /**
    * Calculates base 'targetBase' expansion of a 10-based number.
    *
    * Notes:
    * - n is an integer in base 10
    * - the leading digit of the base expansion is on the leftmost position
    * - the target base may be positive or negative and its absolute value cannot be greater than 10
    */
  def fromBase10ToTargetBase(n: Int, targetBase: Int): String = {

    assert(math.abs(targetBase) > 1 && math.abs(targetBase) <= 10,
      "1 results in an infinite calculation and >10 requires defining special symbols to represent values >10")

    @tailrec
    def acc(n: Int, expansionInTargetBase: List[Int]): List[Int] = {

      if(targetBase > 0){
        assert(n >= 0, "negative number cannot be expanded in a positive base")
      }

      var q = n/targetBase
      var r = n%targetBase

      //Note: operator % in Scala is based on truncated division, thus r < 0 only when the dividend is < 0
      if (r < 0) {
        q += 1
        r -= targetBase
      }

      if(q == 0) r :: expansionInTargetBase
      else acc(q, r :: expansionInTargetBase)
    }

    def handleSign(n: Int, targetBase: Int) = if(n < 0 && targetBase > 0) ("-", -n) else ("", n)

    val (sign, magnitude) = handleSign(n, targetBase)
    sign + acc(magnitude, Nil).mkString
  }

  /**
    * Calculates 10-base representation of a number defined in base originBase
    *
    * Notes:
    * - n is the base expansion in a given origin base
    * - the leading digit of the base expansion is on the leftmost position
    * - the origin base may be positive or negative (only bases between -10 and 10 can be handled)
    */
  def fromOriginBaseToBase10(n: String, originBase: Int): Int = {

    val sign = if(n.head == '-') "-" else ""

    if(sign == "-" && originBase < 0){
      throw new IllegalArgumentException("negative bases do not have -")
    }

    val nMagnitude = if(sign == "-") n.substring(1) else n
    def applySign(i: Int) = if(sign == "-") -i else i

    val valueWithPosition: Array[(Int, Int)] = nMagnitude.reverse.toArray.map(Character.getNumericValue).zipWithIndex
    applySign(valueWithPosition.foldLeft(0) {
      case (acc, (value, position)) => acc + value * math.pow(originBase, position).toInt
    })

  }

}
