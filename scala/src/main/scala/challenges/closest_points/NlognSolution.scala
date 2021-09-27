package challenges.closest_points

object NlognSolution {

  def solution(P: Seq[Point]): PointDistance = {
    (closestPoints _).tupled(sortPoints(P))
  }

  def main(args: Array[String]): Unit = {
    val P = readTestFile(args(0))
    println(solution(P))
  }

}
