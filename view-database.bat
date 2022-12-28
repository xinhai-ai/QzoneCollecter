@echo off
chcp 65001
echo 过滤选择后导出为csv格式
echo 选项均为默认即可
echo 导出后用命令行加载即可

"%~dp0\tool\DBViewer\DB Browser for SQLite.exe" %~dp0\archives\Data\Posts.db