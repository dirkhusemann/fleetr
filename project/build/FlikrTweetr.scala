import sbt._

class LiftProject(info: ProjectInfo) extends DefaultProject(info) {

    val liftVersion = "2.2"
    val liftWebkit = "net.liftweb" %% "lift-webkit" % liftVersion
    val liftMapper = "net.liftweb" %% "lift-common" % liftVersion

    val twitter4jVersion = "[2.1,)"
    val twitter4j = "org.twitter4j" % "twitter4j-core" % twitter4jVersion

    val logback = "ch.qos.logback" % "logback-classic" % "0.9.26"

    val junit = "junit" % "junit" % "4.5" % "test->default"
    val specs = "org.scala-tools.testing" %% "specs" % "1.6.7" % "test->default"

}
