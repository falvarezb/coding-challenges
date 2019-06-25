package challenges.stairs

import scala.util.Try

/**
  * Number of ways to climb 'n' stairs combining steps of different 'values' OR
  * Number of ways to provide change for an amount 'n' by using coins of different 'values'
  */
object Stairs extends App {

  /**
    * Counts all combinations, including permutations.
    * For instance, if n=5 and values=[2,3], there are 2 combinations: [2,3] and [3,2]
    */
  def countAllCombinations(n: Int, values: List[Int]): Int = n match {
    case 0 => 1
    case `n` => values.filter(_ <= n).map(step => countAllCombinations(n - step, values)).sum
  }

  /**
    * Finds all combinations, including permutations.
    * For instance, if n=5 and values=[2,3], there are 2 combinations: [2,3] and [3,2]
    *
    * If no combination exists, returns an empty list
    */
  def enumerateAllCombinations(n: Int, values: List[Int]): List[List[Int]] = n match {
    case 0 => List(Nil)
    case `n` => values.filter(_ <= n).flatMap(step => enumerateAllCombinations(n - step, values).map(comb => step :: comb))
  }

  def enumerateAllCombinationsWithoutPermutation(n: Int, values: List[Int]): List[List[Int]] = {
    enumerateAllCombinations(n, values).map(_.sorted).distinct
  }

  /**
    * Out of all possible combinations, takes the shortest ones (including permutations)
    * If no combination exists, returns an empty list
    */
  def enumerateAllOptimalCombinations(n: Int, values: List[Int]): List[List[Int]] = Try {
    enumerateAllCombinations(n, values).groupBy(l => l.length).toSeq.minBy(_._1)._2
  }.getOrElse(List())

  def enumerateAllOptimalCombinationsWithoutPermutation(n: Int, values: List[Int]): List[List[Int]] = Try {
    enumerateAllCombinationsWithoutPermutation(n, values).groupBy(l => l.length).toSeq.minBy(_._1)._2
  }.getOrElse(List())

  /**
    * Finds an optimal combination.
    * If there are more than one candidate, returns any one of them.
    * If no combination exists, returns an empty list
    */
  def enumerateAnyOptimalCombination(n: Int, values: List[Int]): List[Int] = Try {
    n match {
      case 0 => Nil
      case `n` => values.filter(_ <= n).map(step => step :: enumerateAnyOptimalCombination(n - step, values)).filter(_.sum == n).minBy(_.length)
    }
  }.getOrElse(Nil)

  /**
    * Finds the greedy combination
    * If no greedy combination exists, returns an empty list
    */
  def greedyCombination(n: Int, values: List[Int]): List[Int] = Try {
    n match {
      case 0 => Nil
      case `n` =>
        val greatestCandidate = values.filter(_ <= n).max
        greatestCandidate :: greedyCombination(n - greatestCandidate, values) match {
          case solution if solution.sum == n => solution
          case _ => Nil
        }
    }
  }.getOrElse(Nil)

}

object StairsBenchmark extends App {
  import challenges.stairs.Stairs._

  val n = 60
  val values = List(2,5,8)

  println(countAllCombinations(n, values))
  println(enumerateAllOptimalCombinations(n, values).length)
  println(enumerateAllOptimalCombinationsWithoutPermutation(n, values).length)
  println(enumerateAllOptimalCombinationsWithoutPermutation(n, values))
  //println(enumerateAnyOptimalCombination(n, values))
}
