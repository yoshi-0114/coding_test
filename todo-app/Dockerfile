# ベースイメージの設定
FROM python:3.12

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナ内にコピー
COPY . /app

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# dockerize のインストール
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar -xzv -C /usr/local/bin

# ポートの設定
EXPOSE 8080

# エントリーポイントを設定
ENTRYPOINT ["dockerize", "-wait", "tcp://db:3306", "-timeout", "60s", "python", "app.py"]
