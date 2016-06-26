#####
# Student ID: 2015-12345
# Description: makefile for Homework 1. # indicates a comment in a bash shell
# Usage:
#   * make in: run IndegreCounter.jar on Hadoop to compute the in-degree for each node
#   * make out: run OutdegreeCounter.jar on Hadoop to compute the out-degree for each node
#   * make in_dist: run DegreeDistribution.jar on Hadoop to compute the in-degree distribution
#   * make out_dist: run DegreeDistribution.jar on Hadoop to compute the out-degree distribution

all: in out in_dist out_dist

live: live_in live_out live_in_dist live_out_dist

compile:
	hadoop com.sun.tools.javac.Main IndegreeCounter.java
	hadoop com.sun.tools.javac.Main OutdegreeCounter.java
	hadoop com.sun.tools.javac.Main DegreeDistribution.java

jar:
	jar cf IndegreeCounter.jar IndegreeCounter*.class
	rm -rf IndegreeCounter*.class
	jar cf OutdegreeCounter.jar OutdegreeCounter*.class
	rm -rf OutdegreeCounter*.class
	jar cf DegreeDistribution.jar DegreeDistribution*.class
	rm -rf DegreeDistribution*.class

in:
	hadoop jar IndegreeCounter.jar IndegreeCounter ./problem.edge ./output_in
	hadoop fs -cat output_in/part-r-00000
	hadoop fs -get output_in/part-r-00000 output_in.txt

out:
	hadoop jar OutdegreeCounter.jar OutdegreeCounter ./problem.edge ./output_out
	hadoop fs -cat output_out/part-r-00000
	hadoop fs -get output_out/part-r-00000 output_out.txt

in_dist:
	hadoop jar DegreeDistribution.jar DegreeDistribution ./output_in.txt ./output_dist_in
	hadoop fs -cat output_dist_in/part-r-00000
	hadoop fs -get output_dist_in/part-r-00000 output_dist_in.txt

out_dist:
	hadoop jar DegreeDistribution.jar DegreeDistribution ./output_out.txt ./output_dist_out
	hadoop fs -cat output_dist_out/part-r-00000
	hadoop fs -get output_dist_out/part-r-00000 output_dist_out.txt

live_in:
	hadoop jar IndegreeCounter.jar IndegreeCounter ./live ./output_in
	hadoop fs -cat output_in/part-r-00000
	hadoop fs -get output_in/part-r-00000 output_in.txt

live_out:
	hadoop jar OutdegreeCounter.jar OutdegreeCounter ./live ./output_out
	hadoop fs -cat output_out/part-r-00000
	hadoop fs -get output_out/part-r-00000 output_out.txt

live_in_dist:
	hadoop jar DegreeDistribution.jar DegreeDistribution ./output_in.txt ./output_dist_in
	hadoop fs -cat output_dist_in/part-r-00000
	hadoop fs -get output_dist_in/part-r-00000 output_dist_in.txt

live_out_dist:
	hadoop jar DegreeDistribution.jar DegreeDistribution ./output_out.txt ./output_dist_out
	hadoop fs -cat output_dist_out/part-r-00000
	hadoop fs -get output_dist_out/part-r-00000 output_dist_out.txt


clean:
	rm -rf output*

cleanall:
	rm -rf output*
	rm -rf *.jar


