package challenges.factorial

import scala.annotation.tailrec

object Factorial {

  def fact(n: Int): BigInt = {
    if(n == 0) 1
    else n * fact(n-1)
  }

  def factTailRec(n: Int): BigInt = {
    @tailrec
    def acc(n: Int, value: BigInt): BigInt = {
      if(n == 0) value
      else acc(n-1, n * value)
    }

    acc(n, 1)
  }

}
