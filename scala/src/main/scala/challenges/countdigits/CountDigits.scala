package challenges.countdigits

import org.scalameter.{Aggregator, Measurer, Quantity}

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
    Key.exec.benchRuns -> 50
  )

  val amount = 1234567890

  def executionTime(f: Int => Int): Quantity[Double] = standardConfig withWarmer new Warmer.Default measure {
    f(amount)
  }

  def memoryFootprint(f: Int => Int): Quantity[Double] = standardConfig withWarmer new Warmer.Default withMeasurer new Measurer.MemoryFootprint measure {
    f(amount)
  }

  def gcCycles(f: Int => Int): Quantity[Int] = standardConfig withWarmer new Warmer.Default withMeasurer(new Measurer.GarbageCollectionCycles, Aggregator.median[Int]) measure {
    f(amount)
  }

  println(s"countDigits time: ${executionTime(countDigits)}")
  println(s"countDigitsRecursive time: ${executionTime(countDigitsRecursive)}")
  println(s"countDigitsTailRecursive time: ${executionTime(countDigitsTailRecursive)}")

  println(s"countDigits memory: ${memoryFootprint(countDigits)}")
  println(s"countDigitsRecursive memory: ${memoryFootprint(countDigitsRecursive)}")
  println(s"countDigitsTailRecursive memory: ${memoryFootprint(countDigitsTailRecursive)}")

  println(s"countDigits gc cycles: ${gcCycles(countDigits)}")
  println(s"countDigitsRecursive gc cycles: ${gcCycles(countDigitsRecursive)}")
  println(s"countDigitsTailRecursive gc cycles: ${gcCycles(countDigitsTailRecursive)}")



}
