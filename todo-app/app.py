from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import json

# Flask アプリケーションの設定
app = Flask(__name__)

# データベース接続の設定
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_NAME = os.getenv('MYSQL_DATABASE')

# データベースURLの構築とFlask設定
DATABASE_URL = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースインスタンスの作成
db = SQLAlchemy(app)

# タスクモデルの定義
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    isDone = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"

# UTF-8 で接続する設定 (データベース接続時)
@app.before_request
def set_charset():
    db.session.execute(text("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'"))

# 全タスクの取得
@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'isDone': task.isDone
    } for task in tasks]
    response = make_response(json.dumps(tasks_list, ensure_ascii=False, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# 新規タスクの作成
@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    # リクエストからデータを取得
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "無効なJSON", "message": str(e)}), 400
    
    # データが不足している場合のエラーハンドリング
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({'error': '必要なフィールドが不足しています: title, description'}), 400
    
    # タスクの作成
    new_task = Task(
        title=data['title'],
        description=data['description']
    )
    
    # タスクをデータベースに保存
    db.session.add(new_task)
    db.session.commit()

    # 作成したタスクを返す
    response = make_response(json.dumps({
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'isDone': new_task.isDone
    }, ensure_ascii=False, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 201

# 特定のタスクを取得
@app.route('/api/v1/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task is None:
        return make_response('Task not found', 404)
        
    response = make_response(json.dumps({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'isDone': task.isDone
    }, ensure_ascii=False, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# タスクの更新 
@app.route('/api/v1/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return make_response('Task not found', 404)
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "無効なJSON", "message": str(e)}), 400

    # 更新するデータの検証
    if not data or 'title' not in data or 'description' not in data or 'isDone' not in data:
        return jsonify({'error': '必要なフィールドが不足しています: title, description, isDone'}), 400

    # タスクの更新
    task.title = data['title']
    task.description = data['description']
    task.isDone = data['isDone']

    # データベースに変更を保存
    db.session.commit()

    response = make_response(json.dumps({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'isDone': task.isDone
    }, ensure_ascii=False, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# タスクの削除 
@app.route('/api/v1/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return make_response('Task not found', 404)
    
    # タスクをデータベースから削除
    db.session.delete(task)
    db.session.commit()

    return '', 204

# アプリケーションの起動
if __name__ == '__main__':
    # アプリケーションコンテキストを使用してデータベースを作成
    with app.app_context():
        if not os.path.exists('todo_app.db'):
            db.create_all()  # データベースのテーブルを作成
    print(" * Running on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
