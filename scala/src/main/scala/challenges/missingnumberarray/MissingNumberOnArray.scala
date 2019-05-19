package challenges.missingnumberarray

import java.util
import scala.annotation.tailrec
import scala.collection.GenSeq
import scala.collection.parallel.mutable.ParArray


object MissingNumberOnArray {


  /**
    * Given an array 'arr' of all except one integers between 1 and 'max', find the missing one
    */
  def solution1(arr: GenSeq[Long], max: Long): Long = max*(max+1)/2 - arr.sum

  /**
    * Given an array 'arr' of all except n integers between 1 and 'max', find the n missing ones
    */
  def solutionN(arr: Array[Int], max: Int): List[Int] = {
    val arrSorted = arr.sorted

    @tailrec
    def traverseArray(idx: Int, misses: List[Int]): List[Int] = {
      if(arrSorted.length-1 == idx)
        misses
      else
        traverseArray(idx+1, if(arrSorted(idx)+1 != arrSorted(idx+1)) (arrSorted(idx) + 1 until arrSorted(idx + 1)).toList ++ misses else misses)

    }

    val isFirstValueMissing = if(arrSorted(0) != 1) (arrSorted(0)-1 to(1,-1)).toList else List()
    val missingValues = traverseArray(0, isFirstValueMissing)
    val isLastValueMissing = if(arrSorted(arrSorted.length-1) != max)  (max to(arrSorted(arrSorted.length-1)+1,-1)).toList else List()
    (isLastValueMissing ++ missingValues).reverse
  }

  /**
    * Given an array 'arr' of all except n integers between 1 and 'max', find the n missing ones
    */
  def solutionNOptimised(arr: GenSeq[Int], max: Int): List[Int] = {

    @tailrec
    def missingValues(max: Int, lastMissingIndex: Int, misses: List[Int], bitSet: util.BitSet): List[Int] = {
      val missingIndex = bitSet.nextClearBit(lastMissingIndex)
      if(missingIndex == max)
        misses
      else
        missingValues(max, missingIndex+1, (missingIndex+1) :: misses, bitSet)
    }

    val bitSet = new java.util.BitSet(max)
    arr.foreach(i => bitSet.set(i - 1))
    missingValues(max, 0, Nil, bitSet).reverse
  }

}

object MissingNumberOnArrayBenchmark {

  import org.scalameter.{Key, Warmer, config}
  import MissingNumberOnArray._

  val max: Int = 10000000
  val arr: Array[Int] = ((1 to max/2) ++ (max/2+2 to max)).toArray
  val arrPar: ParArray[Int] = arr.par
  val arrLong = arr.map(_.toLong)
  val arrLongPar = arrLong.par

  val standardConfig = config(
    Key.exec.minWarmupRuns -> 10,
    Key.exec.maxWarmupRuns -> 20,
    Key.exec.benchRuns -> 50,
    Key.verbose -> true
  ) withWarmer(new Warmer.Default)

  def main(args: Array[String]): Unit = {

    println(solution1(arrLong, max))
    println(solution1(arrLongPar, max))
    println(solutionN(arr, max))
    println(solutionNOptimised(arr, max))
    println(solutionNOptimised(arrPar, max))

    val parallelTime = standardConfig.measure{
      arr.par
    }

    val reverseTime = standardConfig.measure{
      arr.reverse
    }

    val solution1Time = standardConfig.measure{
      solution1(arrLong, max)
    }
    val solution1ParTime = standardConfig.measure{
      solution1(arrLongPar, max)
    }

    val solutionNTime = standardConfig.measure{
      solutionN(arr, max)
    }

    val solutionNOptimisedTime = standardConfig.measure{
      solutionNOptimised(arr, max)
    }
    val solutionNOptimisedParTime = standardConfig.measure{
      solutionNOptimised(arrPar, max)
    }

    println(s"parallelTime: $parallelTime")
    println(s"reverseTime: $reverseTime")
    println(s"solution1Time: $solution1Time")
    println(s"solution1ParTime: $solution1ParTime")
    println(s"solutionNTime: $solutionNTime")
    println(s"solutionNOptimisedTime: $solutionNOptimisedTime")
    println(s"solutionNOptimisedParTime: $solutionNOptimisedParTime")
  }
}


