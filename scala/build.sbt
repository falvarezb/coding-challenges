name := "scala"
version := "0.1"
scalaVersion := "2.12.8"

libraryDependencies ++= Seq(
  "org.scalatest" %% "scalatest" % "3.0.3" % "test",
  "com.storm-enroute" %% "scalameter" % "0.17",
  "org.scalacheck" %% "scalacheck" % "1.14.0" % "test"
)