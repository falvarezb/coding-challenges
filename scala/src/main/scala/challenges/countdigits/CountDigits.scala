package challenges.countdigits

import challenges._

import scala.annotation.tailrec
import scala.math.{ceil, log10}

object CountDigits {

  def countDigitsString(n: Int): Int = n.toString.length

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

  def countDigitsLog(n: Int): Int = ceil(log10(n.toDouble)).toInt

}

object CountDigitsBenchmark extends App {

  import CountDigits._

  val amount = 1234567890
  val n = 10000000

  def runner(n: Int, countDigits: Int => Int, digit: Int): Unit = {
    for(_ <- 1 to n)
      countDigits(digit)
  }

  val r1 = runner(n, countDigitsString, _)
  val r2 = runner(n, countDigitsRecursive, _)
  val r3 = runner(n, countDigitsTailRecursive, _)
  val r4 = runner(n, countDigitsLog, _)

  println(s"countDigitsString time: ${executionTime(r1, amount)}")
  println(s"countDigitsRecursive time: ${executionTime(r2, amount)}")
  println(s"countDigitsTailRecursive time: ${executionTime(r3, amount)}")
  println(s"countDigitsLog time: ${executionTime(r4, amount)}")
  println()
  println(s"countDigitsString memory: ${memoryFootprint(r1, amount)}")
  println(s"countDigitsRecursive memory: ${memoryFootprint(r2, amount)}")
  println(s"countDigitsTailRecursive memory: ${memoryFootprint(r3, amount)}")
  println(s"countDigitsLog memory: ${memoryFootprint(r4, amount)}")
  println()
  println(s"countDigitsString gc cycles: ${gcCycles(r1, amount)}")
  println(s"countDigitsRecursive gc cycles: ${gcCycles(r2, amount)}")
  println(s"countDigitsTailRecursive gc cycles: ${gcCycles(r3, amount)}")
  println(s"countDigitsLog gc cycles: ${gcCycles(r4, amount)}")

}
