@echo off
chcp 65001 > nul
REM "@echo off 是批处理文件的开头命令，它的作用是关闭命令提示符窗口的命令回显。"
REM "通过自动代码爬取文件后，执行这个脚本，自动同步stk对应下载文章目录下到github同步目录中,再执行本地文件上传github的的脚本"
REM "实现公众号文件通过软件自动爬取"
REM "然后，通过这个bat脚本同步上github上，然后可以保存管理文章链接，有道云手动保存太麻烦了"

REM "/mir 表示镜像目录树，/e 表示复制所有子目录，/z 表示使用断点续传模式，/eta 表示显示估计时间"，"C:\path\to\source\folder" 是源文件夹的路径，"\\remote-server\path\to\destination\folder" 是目标文件夹的网络路径。
REM "/mir如果没有 参数它不会删除目标文件夹中不存在源文件夹中的文件和文件夹"

REM 先拉取更新
cd /d "D:\github_prj\stock_view"
REM 丢弃为提交缓存
git reset --hard HEAD  
git pull --rebase origin master
timeout /t 1 



robocopy /mir /e /z /eta "C:\Users\DELL\Desktop\stk"  "D:\github_prj\stock_view\stk工具"
timeout /t 3  


git add .
git commit -m "更新代码"
git push -u origin master 


REM 等待用户按下任意键后关闭窗口
pause

REM 等待5秒后关闭窗口
REM timeout /t 5 /nobreak