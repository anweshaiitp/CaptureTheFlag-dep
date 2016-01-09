#!/bin/bash
#
# @author:metastableB
# generateTestQuestion.sh
# 
# Script generates random test question files in the testQuestion directory

#mkdir ../testQuestions
for i in {1..10}
do 
	echo "Question number $i" > ../testQuestions/question$i.html
done