package challenges.countdigits

import org.scalameter.{Key, Warmer}

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
  import org.scalameter.{Key, Warmer, config}
  val standardConfig = config(
    Key.exec.minWarmupRuns -> 10,
    Key.exec.maxWarmupRuns -> 20,
    Key.exec.benchRuns -> 50,
    Key.verbose -> true
  ) withWarmer(new Warmer.Default)

  val figure = 1234567890

  val countDigitsTime = standardConfig.measure {
    countDigits(figure)
  }

  val countDigitsRecursiveTime = standardConfig.measure {
    countDigitsRecursive(figure)
  }

  val countDigitsTailRecursiveTime = standardConfig.measure {
    countDigitsTailRecursive(figure)
  }

  println(s"countDigitsTime: $countDigitsTime")
  println(s"countDigitsRecursiveTime: $countDigitsRecursiveTime")
  println(s"countDigitsTailRecursiveTime: $countDigitsTailRecursiveTime")

}
