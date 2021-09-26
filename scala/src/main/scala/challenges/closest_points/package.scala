package challenges

package object closest_points {

  import math._
  case class Point(x: Int, y: Int)
  case class PointDistance(p1: Point, p2: Point, d: Double)
  case class PyElement(p: Point, xPosition: Int)

  /**
    * Euclidean distance
    */
  def distance(point1: Point, point2: Point): Double = {
    sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))
  }


  /**
    * P -> Px, Py
    */
  def sortPoints(P: Seq[Point]): (Seq[Point], Seq[PyElement]) = {
    val Px = P.sortBy(_.x)
    val Py = Px.zipWithIndex.map { case (p, idx) => PyElement(p, idx) }.sortBy(_.p.y)
    (Px, Py)
  }

  def leftHalfPoints(Px: Seq[Point], Py: Seq[PyElement]): (Seq[Point], Seq[PyElement]) = {
    val leftHalfUpperBound = ceil(Px.length / 2d).toInt
    val newPx = Px.slice(0, leftHalfUpperBound)
    val newPy = Py.filter(_.xPosition < leftHalfUpperBound)
    (newPx, newPy)
  }

  def rightHalfPoints(Px: Seq[Point], Py: Seq[PyElement]): (Seq[Point], Seq[PyElement]) = {
    val n = Px.length
    val rightHalfLowerBound = n / 2
    val newPx = Px.slice(rightHalfLowerBound, n)
    val newPy = Py.filter(_.xPosition >= rightHalfLowerBound).map(p => PyElement(p.p, p.xPosition - rightHalfLowerBound))
    (newPx, newPy)
  }

  def getCandidatesFromDifferentHalves(rightmostLeftPoint: Point, Py: Seq[PyElement], minDistanceUpperBound: Double): Seq[PyElement] = {
    Py.filter(py => abs(rightmostLeftPoint.x - py.p.x) < minDistanceUpperBound)
  }

  def closestPointsFromDifferentHalves(candidates: Seq[PyElement]): PointDistance = {
    var minDistance = Double.MaxValue
    var closestPoints: (Point, Point) = (Point(0,0), Point(0,0))
    for (i <- candidates.indices) {
      for (j <- i + 1 until min(candidates.length, 16)) {
        val d = distance(candidates(i).p, candidates(j).p)
        if (d < minDistance) {
          minDistance = d
          closestPoints = (candidates(i).p, candidates(j).p)
        }
      }
    }
    PointDistance(closestPoints._1, closestPoints._2, minDistance)
  }

//  def mixedSolution(leftSolution: PointDistance, rightSolution: PointDistance)
//
//  def determineGlobalSolution(leftSolution: PointDistance, rightSolution: PointDistance, solutionFromDifferentHalves: PointDistance): PointDistance = {
//    val minLeftRightDistance = min(leftSolution.d, rightSolution.d)
//    val candidates = getCandidatesFromDifferentHalves(lx.last, Py, minLeftRightDistance)
//    val solutionFromDifferentHalves = closestPointsFromDifferentHalves(candidates)
//    List(leftSolution, rightSolution, solutionFromDifferentHalves).minBy(_.d)
//  }

  def closestPoints(Px: Seq[Point], Py: Seq[PyElement]): PointDistance = {
    if (Px.length == 2) {
      PointDistance(Px(0), Px(1), distance(Px(0), Px(1)))
    }
    else {
      //https://stackoverflow.com/questions/44713728/why-cant-we-have-capital-letters-in-tuple-variable-declaration-in-scala
      val (lx, ly) = leftHalfPoints(Px, Py)
      val (rx, ry) = rightHalfPoints(Px, Py)

      val leftSolution = closestPoints(lx, ly)
      val rightSolution = closestPoints(rx, ry)


      val minLeftRightDistance = min(leftSolution.d, rightSolution.d)
      val candidates = getCandidatesFromDifferentHalves(lx.last, Py, minLeftRightDistance)
      val solutionFromDifferentHalves = closestPointsFromDifferentHalves(candidates)
      List(leftSolution, rightSolution, solutionFromDifferentHalves).minBy(_.d)
    }
  }

}
