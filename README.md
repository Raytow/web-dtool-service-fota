# web-dtool-service

合宙差分包生成服务

代码使用flask框架
用uwsgi直接起http服务。也可以自行配置，放在nginx之后。
运行在linux系统

---

src包含代码

python3_8_3_dtool_app.df为镜像描述(dockerfile)

python3_8_3_dtool_app_requirements.txt为代码所需的python库，会在dockerfile中进行安装。

docker-compose.yaml是docker-compose配置。

dtool_uwsgi.ini是uwsgi配置

---

用户可以自行安装python库，自己运行服务。
安装环境参考上述配置文件。

pip3 install -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com -r python3_8_3_dtool_app_requirements.txt

安装完后运行
uwsgi --ini web-dtool-service/dtool_uwsgi.ini

---

用户也可以在docker环境中运行服务。推荐用docker运行。

进入web-dtool-service目录

1. 生成镜像  
sudo docker build -f python3_8_3_dtool_app.df -t python3_8_3_dtool_app .

2. dtool启动  
sudo docker compose up -d dtool

3. log查看  
sudo docker compose logs dtool

4. 查看状态  
sudo docker compose ps

如果state是UP说明已经跑起来了。

---

接口地址
http://你的ip:7882/api/site/dfota_diff_image
30030可在docker-compose.yaml改为其他端口比如常用的80。

form参数
两个文件。文件名为f1和f2。

返回
若成功返回http 200。附带文件。
若失败返回http 400等。带错误信息msg。


---

差分工具可执行文件在/web-dtool-service/src/app/third_party/dfota/。
需要设置为可执行。

---
  ## 更新日志

  ### 2025-10-28
  - 新增：添加自动清理机制，防止差分文件无限增长
    - 每次请求时自动检查并清理旧文件
    - 只保留最新的20个版本
    - 按时间顺序删除最早的文件，避免服务器存储空间耗尽

  保存后提交：
  git add README.md
  git commit -m "更新README：添加清理机制说明"
  git push github master

  ---
