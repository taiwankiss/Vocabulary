#!/bin/sh
# 把要上線的檔案複製到 cf-dist/（Cloudflare 部署的資料夾），再執行 npx wrangler deploy
cd "$(dirname "$0")"
mkdir -p cf-dist/data
cp flashcard_app.html cf-dist/index.html
cp flashcard_app.html cf-dist/flashcard_app.html
cp toeic_vocabulary.csv toeic_vocabulary.json icon.png apple-touch-icon.png cf-dist/
cp data/*.json cf-dist/data/
echo "cf-dist ready"
