package util

import java.io.File
import java.nio.charset.StandardCharsets
import java.nio.file.StandardOpenOption.{APPEND, CREATE, TRUNCATE_EXISTING, WRITE}
import java.nio.file.{Files, Path, Paths, StandardCopyOption}

import scala.annotation.tailrec
import scala.collection.immutable
import scala.io.Source
import scala.util.Try

object FileOps {

  /*
    Starting in "originPath", walks through all subfolders looking for files whose name matches the given regex and
    copies them into "destinationPath"
  */
  def copyFilesRecursively(originPath: String, destinationPath: String, fileNameRegex: String): Unit = {
    if (Files.notExists(new File(destinationPath).toPath)) {
      Files.createDirectory(new File(destinationPath).toPath)
    }

    listFilesRecursively(originPath, fileNameRegex)
      .foreach { file =>
        val origin = file.toPath
        val destination = new File(destinationPath + file.getName).toPath.toAbsolutePath
        println(s"copying ${origin} to ${destination}")
        Files.copy(origin, destination, StandardCopyOption.REPLACE_EXISTING)
      }
  }

  def listFilesRecursively(originPath: String, fileNameRegex: String): IndexedSeq[File] = {
    os.walk(os.Path(originPath))
      .map(_.toIO)
      .filter(file => fileNameRegex.r.findFirstIn(file.toString).isDefined && !file.isDirectory)
  }

  def listFilesRecursivelySlow(originPath: String, fileNameRegex: String): List[File] = {

    @tailrec
    def nextStep(files: List[File]): List[File] =
      if(!files.exists(_.isDirectory)) files
      else nextStep(files.flatMap{file =>
        if(file.isDirectory) file.listFiles()
        else List(file)
      })

    nextStep(List(new File(originPath)))
      .filter(file => fileNameRegex.r.findFirstIn(file.toString).isDefined)
  }

  def writeToFile(fileName: String, content: String, overwrite: Boolean = false): Unit = {
    Try{
      Files.write(Paths.get(fileName), content.getBytes(StandardCharsets.UTF_8), CREATE, if(overwrite) TRUNCATE_EXISTING else APPEND, WRITE)
    }.recover{
      case t => t.printStackTrace()
    }
    ()
  }

  /**
   * [(1,"a",3), (2,"b",4)] =>
   * """
   * 1,a,3
   * 2,b,4
   *
   * """
   */
  def toCsv[T,U,V](x: List[(T, U, V)]): String = {
    x.map{ s =>
      val str = s.toString
      str.slice(1, str.length-1)
    } match {
      case Nil => ""
      case xs => xs.mkString("\n") + "\n"
    }
  }

  def main(args: Array[String]): Unit = {

    val t0 = System.currentTimeMillis()
    val originPath = "/Users/franciscoalvarez/MyProjects"
    val destinationPath = "./intellij_backup/"
    val fileNameRegex = """.idea/runConfiguration"""
    copyFilesRecursively(originPath, destinationPath, fileNameRegex)

    //listFilesRecursively(originPath, fileNameRegex)
    println(s"total time: ${(System.currentTimeMillis() - t0) / 1000} sec")

  }

  def readFromFile(filePath: String): immutable.Seq[String] = Source.fromFile(new File(filePath)).getLines().toList
}

