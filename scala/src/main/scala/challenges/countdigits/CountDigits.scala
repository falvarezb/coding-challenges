package challenges.countdigits

import challenges._

import scala.annotation.tailrec

object CountDigits {

  def countDigits(n: Int): Int = n.toString.length

  def countDigitsRecursive(n: Int): Int = {
    val x = n/10
    if (x == 0) 1
    else 1 + countDigitsRecursive(x)
  }

  def countDigitsTailRecursive(n: Int): Int = {
    @tailrec
    def acc(n: Int, counter: Int): Int = {
      val x = n/10
      if(x == 0) counter + 1
      else acc(x, counter + 1)
    }
    acc(n,0)
  }

}

object CountDigitsBenchmark extends App {

  import CountDigits._

  val amount = 1234567890

  println(s"countDigits time: ${executionTime(countDigits, amount)}")
  println(s"countDigitsRecursive time: ${executionTime(countDigitsRecursive, amount)}")
  println(s"countDigitsTailRecursive time: ${executionTime(countDigitsTailRecursive, amount)}")

  println(s"countDigits memory: ${memoryFootprint(countDigits, amount)}")
  println(s"countDigitsRecursive memory: ${memoryFootprint(countDigitsRecursive, amount)}")
  println(s"countDigitsTailRecursive memory: ${memoryFootprint(countDigitsTailRecursive, amount)}")

  println(s"countDigits gc cycles: ${gcCycles(countDigits, amount)}")
  println(s"countDigitsRecursive gc cycles: ${gcCycles(countDigitsRecursive, amount)}")
  println(s"countDigitsTailRecursive gc cycles: ${gcCycles(countDigitsTailRecursive, amount)}")

}
