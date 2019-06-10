package challenges.missingnumberarray

import java.util

import scala.annotation.tailrec
import scala.collection.GenSeq
import scala.collection.parallel.mutable.ParArray


/**
  * Given an array 'arr' containing k distinct numbers taken from 1,2 ... n with k < n, find the n - k missing numbers
  */
object MissingNumberOnArray {


  /**
    * Solution only valid when n - k == 1
    *
    * Implementation details:
    * 1. calculate the sum of 1 ... n using the formula of the sum of the first n natural numbers
    * 2. calculate the sum of all the elements in the array
    * 3. the difference of both sums is the solution
    */
  def solution1(arr: GenSeq[Long], n: Long): Long = n*(n+1)/2 - arr.sum

  /**
    * Generic solution
    *
    * Implementation details:
    * 1. sort the elements of the array
    * 2. traverse the array and for every element a[n] check if a[n]+1 == a[n+1]: if not, the sequence of
    * numbers between a[n] and a[n+1] is the solution
    */
  def solutionN(arr: Array[Int], n: Int): List[Int] = {
    util.Arrays.parallelSort(arr) //Using Java alternative as Scala's ParArray does not have sorting methods
    val arrSorted = arr

    @tailrec
    def traverseArray(idx: Int, missingValues: List[Int]): List[Int] = {
      if(arrSorted.length-1 == idx)
        missingValues
      else
        traverseArray(idx+1, if(arrSorted(idx)+1 != arrSorted(idx+1))  ((arrSorted(idx + 1) - 1) to(arrSorted(idx) + 1,-1)).toList ::: missingValues else missingValues)

    }

    val firstMissingValues = if(arrSorted(0) != 1) (arrSorted(0)-1 to(1,-1)).toList else List()
    val missingValues = traverseArray(0, firstMissingValues)
    val lastMissingValues = if(arrSorted(arrSorted.length-1) != n)  (n to(arrSorted(arrSorted.length-1)+1,-1)).toList else List()
    (lastMissingValues ::: missingValues).reverse
  }

  /**
    * Generic solution
    *
    * Implementation details:
    * 1. create an array 'b' of n boolean elements with all elements initialised to false (such an array is a BitSet)
    * 2. map each element of the original array 'arr' to its corresponding position in the new array 'b': the value of
    * an element in 'arr' minus 1 represents the index of its position in 'b' (as 'arr' is a 1-indexed array and 'b'
    * a 0-indexed one)
    * 3. the elements in 'b' that can be mapped to an element in 'arr' are set to true
    * 4. the index plus 1 of the remaining false values in 'b' are the solution
    */
  def solutionNOptimised(arr: GenSeq[Int], n: Int): List[Int] = {

    @tailrec
    def missingValues(lastMissingIndex: Int, misses: List[Int], bitSet: util.BitSet): List[Int] = {
      val missingIndex = bitSet.nextClearBit(lastMissingIndex)
      if(missingIndex == n)
        misses
      else
        missingValues(missingIndex+1, (missingIndex+1) :: misses, bitSet)
    }

    val bitSet = new java.util.BitSet(n)
    arr.foreach(i => bitSet.set(i - 1))
    missingValues(0, Nil, bitSet).reverse
  }

}

/**
  * Benchmark, using Scalameter, to compare the performance of the 3 implementations
  */
object MissingNumberOnArrayBenchmark {

  import org.scalameter.{Key, Warmer, config}
  import MissingNumberOnArray._

  val n: Int = 10000000
  //By construction, the missing number is max/2+1
  val arr: Array[Int] = ((1 to n/2) ++ (n/2+2 to n)).toArray
  val arrPar: ParArray[Int] = arr.par
  val arrLong = arr.map(_.toLong)
  val arrLongPar = arrLong.par

  val standardConfig = config(
    Key.exec.minWarmupRuns -> 20,
    Key.exec.maxWarmupRuns -> 30,
    Key.exec.benchRuns -> 50,
    Key.verbose -> false
  ) withWarmer(new Warmer.Default)

  def main(args: Array[String]): Unit = {

    println(solution1(arrLong, n))
    println(solutionN(arr, n))
    println(solutionNOptimised(arrPar, n))

    val solution1ParTime = standardConfig.measure{
      solution1(arrLongPar, n)
    }

    val solutionNTime = standardConfig.measure{
      solutionN(arr, n)
    }

    val solutionNOptimisedParTime = standardConfig.measure{
      solutionNOptimised(arrPar, n)
    }

    println(s"solution1ParTime: $solution1ParTime") //40ms
    println(s"solutionNTime: $solutionNTime") //30ms
    println(s"solutionNOptimisedParTime: $solutionNOptimisedParTime") //14ms
  }
}


