package challenges.negabinary

import scala.annotation.tailrec

/**
  * https://en.wikipedia.org/wiki/Negative_base
  *
  * In negative base, all integers, positive and negative, can be represented without a sign.
  */
object NegaBinary {


  /**
    * Calculates base expansion of n in the base targetBase.
    *
    * Notes:
    * - n is 10-base number
    * - the leading digit of the base expansion is on the leftmost position
    * - the target base may be positive or negative and its absolute value cannot be greater than 10
    */
  def from10(n: Int, targetBase: Int): String = {

    assert(math.abs(targetBase) > 1 && math.abs(targetBase) <= 10,
      "1 results in an infinite calculation and >10 requires defining special symbols to represent values >10")

    @tailrec
    def acc(n: Int, targetRepresentation: List[Int]): List[Int] = {
      var q = n/targetBase
      var r = n%targetBase

      if(targetBase < 0) {
        if (r < 0) {
          q += 1
          r -= targetBase
        }
      }

      if(q == 0) r :: targetRepresentation
      else acc(q, r :: targetRepresentation)
    }

    if(n < 0 && targetBase > 0){
      "-" + acc(-n, Nil).mkString
    }
    else {
      acc(n, Nil).mkString
    }
  }

  /**
    * Calculates 10-base representation of n
    *
    * Notes:
    * - n is the base expansion in a given origin base
    * - the leading digit of the base expansion is on the leftmost position
    * - the origin base may be positive or negative (only bases between -10 and 10 can be handled)
    */
  def to10(n: String, originBase: Int): Int = {

    val isNegative = n.head == '-'

    if(isNegative && originBase < 0){
      throw new IllegalArgumentException("negative bases do not have -")
    }

    def negateString(s: String) = if(isNegative) s.substring(1) else s
    def negate(i: Int) = if(isNegative) -i else i

    val valueWithPosition: Array[(Int, Int)] = negateString(n).reverse.toArray.map(Character.getNumericValue).zipWithIndex
    negate(valueWithPosition.foldLeft(0) {
      case (acc, (value, position)) => acc + value * math.pow(originBase, position).toInt
    })

  }

}
