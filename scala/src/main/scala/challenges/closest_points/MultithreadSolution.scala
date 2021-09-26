package challenges.closest_points

import java.util.concurrent.{ForkJoinPool, ForkJoinTask, RecursiveTask}
import scala.math.min


class ClosestPointTask(Px: Seq[Point], Py: Seq[PyElement], parThreshold: Int) extends RecursiveTask[PointDistance] {
  override def compute(): PointDistance = {
    if(Px.length == 2) {
      PointDistance(Px(0), Px(1), distance(Px(0), Px(1)))
    }
    else if(Px.length > parThreshold) {
      val (lx, ly) = leftHalfPoints(Px, Py)
      val (rx,ry) = rightHalfPoints(Px, Py)

      val leftClosestPointsTask: ForkJoinTask[PointDistance] = new ClosestPointTask(lx, ly, parThreshold).fork()
      val rightSolution: PointDistance = new ClosestPointTask(rx, ry, parThreshold).compute()
      val leftSolution: PointDistance = leftClosestPointsTask.join()

      val minLeftRightDistance = min(leftSolution.d, rightSolution.d)
      val candidates = getCandidatesFromDifferentHalves(lx.last, Py, minLeftRightDistance)
      val solutionFromDifferentHalves = closestPointsFromDifferentHalves(candidates)
      List(leftSolution, rightSolution, solutionFromDifferentHalves).minBy(_.d)
    }
    else {
      closestPoints(Px, Py)
    }
  }
}

object MultithreadSolution {
  def nlognSolution(P: Seq[Point], numProcesses: Int): PointDistance = {
    val (px, py) = sortPoints(P)
    val parThreshold = P.length / numProcesses
    val task = new ClosestPointTask(px, py, parThreshold)
    val pool = new ForkJoinPool(numProcesses)
    pool.invoke(task)
  }
}
