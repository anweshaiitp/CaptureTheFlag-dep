#!/bin/bash
#
# @author:metastableB
# dummyQuestionJson.sh
#
# Generate a dummy question json file 

echo "["
for i in {1..7}
do
	echo "
	{
		\"model\": \"game_ctf.question\", 
		\"pk\": $i, 
		\"fields\": {
			\"valid\": true, 
			\"source_file\": \"question$i.html\", 
			\"points\": 20, 
			\"has_context\": false,
			\"answer\": \"ans$i\"
			}
		}, 	
"
val=$((i))
done
val=$((val + 1))
# TO finish of the json
echo "
	{
		\"model\": \"game_ctf.question\", 
		\"pk\": $val, 
		\"fields\": {
			\"valid\": true, 
			\"source_file\": \"question$val.html\", 
			\"points\": 0, 
			\"has_context\": false
			}
		} 	
]"