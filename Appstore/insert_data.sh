#!/bin/sh
#数据库连接信息
#新数据库,内网
db_host='127.0.0.1'
db_user='root'
db_pw='123456'
db_name='HenryKugouComment'

source ~/.bash_profile

echo "___________________________begin load search data file_________________________"
echo [`date "+%Y-%m-%d %H:%M:%S"`] "begin"

#load 入表
data_path="./result"

cd ${data_path}
ls *|while read comment_file
do
    echo $comment_file
    mysql -h${db_host} -u${db_user} -p${db_pw} -t ${db_name} -e "LOAD DATA local INFILE '"${comment_file}"' into table KugouComment FIELDS TERMINATED BY '\t' (date,userReviewId,title,body,rating)"

    if [ $? -ne 0 ]
    then
        echo "put $comment_file error"
    fi
done

echo [`date "+%Y-%m-%d %H:%M:%S"`] 'finish update table'
