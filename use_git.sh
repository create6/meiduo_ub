#!/bin/bash

git add .
git commit -m 'udpate'
git push

echo -e "\033[33m push success! \033[0m"
echo -e "\033[35m begin sendEmail \033[0m"


# 调用python send Email 同时向sys传入相关参数
~/Desktop/myshell/source/sendEmail_1.py success push by $(pwd),In $(date)

echo -e “\033[35m CODE:200 \033[0m”
