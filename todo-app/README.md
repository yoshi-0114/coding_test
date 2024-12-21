# TODOアプリ

## 前提条件
・Docker  
・Docker Compose

## 起動方法
1. Dockerデーモンが起動していることを確認  
Windows/Macの場合：  
Docker Desktopが起動していることを確認  
Linuxの場合：  
sudo systemctl status docker  
もし起動していない場合は以下のコマンドで起動：  
sudo systemctl start docker  

2. リポジトリのクローン  
git clone https://github.com/yoshi-0114/coding_test  
カレントディレクトリをtodo-appに変更  
cd coding_test/todo-app  

3. 環境変数の設定  
アプリケーションの環境変数は docker-compose.yml ファイルで設定されています。必要に応じて以下を編集してください。  
MYSQL_HOST: db  
MYSQL_PORT: 3306  
MYSQL_USER: root  
MYSQL_PASSWORD: password  
MYSQL_DATABASE: todo_app  

4. アプリケーションの起動  
初回起動時：  
docker-compose up --build  
2回目以降：  
docker-compose up  

5. アプリケーションの停止  
アプリケーションを停止するには：  
docker-compose down  
データベースの永続化データを完全に削除する場合：  
docker-compose down -v  
