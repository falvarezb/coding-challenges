package challenges.combinatorics

import scala.util.control.Breaks.{break, breakable}

object Permutation {

  def main(args: Array[String]): Unit = {
    println(List("1452", "dkhc").map(nextPermutation))
    println(permutations("1234"))
  }

  /**
    * Given a String, find, among all possible permutations of its characters, which one is the immediately next
    * according to the lexicographical order
    *
    * Algorithm
    * ---------
    *
    * iterate backwards over the chars of the String, and for each char, find if there is any char greatest than it
    * among the chars after it. If so, swap the chars and stop the iteration
    *
    * Now, sort the chars after it in ascending order (in reality, it's enough to reverse its order)
    *
    * Examples
    * --------
    *
    * "1452" -> "1524"
    * "dkhc" -> "hcdk"
    */
  def nextPermutation(s: String): String = {
    val arr = s.toCharArray
    var pivot = 0
    breakable {
      for (i <- arr.length - 2 to(0, -1)) {
        for (j <- arr.length - 1 to(i+1, -1)) {
          if (arr(i) < arr(j)) {
            val temp = arr(j)
            arr(j) = arr(i)
            arr(i) = temp
            pivot = i
            break()
          }
        }
      }
      return "" //the provided String is already the last permutation so there is no "next"
    }
    val left = arr.take(pivot+1)
    val right = arr.takeRight(arr.length-pivot-1)
    (left ++ right.reverse).toList.mkString
  }

  /**
    * Given the lowest permutation, calculate all possible permutations
    */
  def permutations(s: String): List[String] = {
    def helper(permutation: String): List[String] = {
      val next = nextPermutation(permutation)
      if (next.isEmpty) Nil
      else next :: helper(next)
    }
    s :: helper(s)
  }

}
