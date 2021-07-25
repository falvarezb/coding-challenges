package challenges.order

import scala.util.control.Breaks.{break, breakable}

object LexicographicalOrder {

  def main(args: Array[String]): Unit = {
    println(nextElement("dkhc"))
  }

  /**
    * Given a String, find, among all possible permutations of its characters, which one is the immediately next
    * according to the lexicographical order
    */
  def nextElement(s: String): String = {
    val arr = s.toCharArray
    var changedIdx = 0
    breakable {
      for (i <- arr.length - 2 to(0, -1)) {
        for (j <- arr.length - 1 to(i+1, -1)) {
          if (arr(i) < arr(j)) {
            val temp = arr(j)
            arr(j) = arr(i)
            arr(i) = temp
            changedIdx = i
            break()
          }
        }
      }
      return "no answer"
    }
    val left = arr.take(changedIdx+1)
    val right = arr.takeRight(arr.length-changedIdx-1)
    (left ++ right.sorted).toList.mkString
  }

}
