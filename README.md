# ランニングシューズ 3Dマップ

速さ・反発・年代の3軸でランニングシューズの立ち位置を比べる 3D マップです。
ビルド不要の静的サイトなので、GitHub Pages にそのまま置けます。

```
shoe-map-3d/
├── index.html   アプリ本体（three.js は CDN から読み込み）
├── data.js      ブランドとシューズのデータ
└── images/      シューズ画像を置くフォルダ
```

## 手元で開く

画像を 3D 上に表示するには、ローカルサーバー経由で開いてください
（`index.html` をダブルクリックで開くと、ブラウザの制限で画像だけ仮のイラストになります）。

```powershell
cd shoe-map-3d
npx serve .            # Node.js がある場合 → 表示された http://localhost:3000 を開く
# または
python -m http.server 8000   # → http://localhost:8000
```

## GitHub Pages で公開する

1. GitHub で新しいリポジトリを作る（例：`shoe-map-3d`）
2. このフォルダをプッシュする

   ```powershell
   cd shoe-map-3d
   git init
   git add .
   git commit -m "Add running shoe 3D map"
   git branch -M main
   git remote add origin https://github.com/<ユーザー名>/shoe-map-3d.git
   git push -u origin main
   ```

3. リポジトリの **Settings → Pages** を開き、**Source** を「Deploy from a branch」、
   **Branch** を `main` / `/(root)` にして **Save**
4. 1〜2分後に `https://<ユーザー名>.github.io/shoe-map-3d/` で公開される

以降は `data.js` や `images/` を更新してプッシュするたびに、自動で公開ページに反映されます。

## データを更新する

### A. ブラウザの編集モードで更新する

1. 公開ページ（または手元のローカルサーバー）の URL の末尾に `?edit` を付けて開く
   例：`https://<ユーザー名>.github.io/shoe-map-3d/?edit`
2. 「カードを追加」「ブランドを管理」「編集」で内容を変える
   （変更はそのブラウザに下書きとして保存されるだけで、まだ公開ページには出ません）
3. 右下の「data.js を書き出す」→「data.js をダウンロード」
4. リポジトリの `data.js` をダウンロードしたファイルで置き換えて、コミット・プッシュ
5. 反映を確認したら、編集モードの「下書きを破棄」で下書きを消す

`?edit` を付けない URL は閲覧専用です。編集ボタンは表示されません。

### B. data.js を直接編集する

```js
{
  "id": "s20",            // 重複しない ID
  "brandId": "b-asics",   // brands の id
  "name": "METASPEED Edge",
  "year": 2024,           // 発売年
  "speed": 4.3,           // -5（遅い）〜 +5（速い）
  "rebound": 3.5,         // -5（低反発・安定）〜 +5（高反発）
  "image": "images/metaspeed-edge.webp",
  "note": "メモ（グラフ上の詳細に表示）"
}
```

新しいブランドは `brands` に `{ "id": "b-on", "name": "On", "color": "#0e7490" }` のように追加します。

## 画像について

- `images/` に置いて、`data.js` の `image` にパスを書くのがおすすめです（背景を切り抜いた透過 PNG / WebP がきれいに見えます）
- 編集モードで「画像を選ぶ」から入れた画像は、`data.js` の中に埋め込まれます。手軽ですが、枚数が多いと `data.js` が重くなります

## 注意

- GitHub Pages のサイトは、URL を知っていれば誰でも見られる公開ページになります。
  メーカーの製品画像を使う場合は、各社の利用条件を確認してください。
- 軸の範囲（年代の 1970〜2030 など）は `index.html` 内の `CONFIG` で変えられます。
