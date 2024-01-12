@echo off
chcp 65001 > nul
REM 主要是防止同花顺丢失，或者自己想恢复，就是一个代码管理过程


REM拉取最新数据，丢弃当下本地库的修改
cd /d "D:\github_prj\stock_view"
git fetch --prune
git reset --hard origin/master
git push origin master --force

timeout /t 1 


set "githubFolder=D:\github_prj\stock_view\同花顺用户数据\zeroaP"
set "destinationRar=%githubFolder%.rar"  REM 文件压缩、如果不要压缩可能上传下载github有问题

REM 删除本地库原来文件
REM 使用 rmdir 命令删除文件夹及其内容，/s 表示删除子文件夹和文件，/q 表示静默模式，不提示确认
rmdir /s /q "%githubFolder%"
del /q "%destinationRar%"

timeout /t 2



 
REM 拷贝最新文件  同花顺安装目录——用户名命名的文件夹——同花顺方案    StockBlock.ini
robocopy /mir /e /z /eta "D:\ths\zeroaP\同花顺方案"  "%githubFolder%\同花顺方案"
robocopy "D:\ths\zeroaP" "D:\github_prj\stock_view\同花顺用户数据\zeroaP" StockBlock.ini /z /eta

timeout /t 1

REM 使用 WinRAR 压缩文件夹
"D:\Program Files (x86)\WinRAR\WinRAR.exe" a  -r "%destinationRar%" "%githubFolder%"

REM 如果有删除原来文件,不更新zeroaP，更新zeroaP.rar
rmdir /s /q "%githubFolder%"

REM s上传github
cd /d "D:\github_prj\stock_view"
git add .
git commit -m "更新代码"
git push -u origin master 




REM 等待用户按下任意键后关闭窗口
REM pause