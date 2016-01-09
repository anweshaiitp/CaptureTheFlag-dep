#!/bin/bash
#
# @author:metastableB
# generateTestQuestion.sh
# 
# Script generates random test question files in the testQuestion directory

mkdir -p ../game_ctf/templates/testQuestions
for i in {1..10}
do 
	echo "Question number $i" > ../game_ctf/templates/testQuestions/question$i.html
done