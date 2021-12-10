# automeasurement

テンプレファイルを大量に実行するスクリプト。メンテを考えてBashで書くべし。グラフ描画などは他のリポジトリでおこなう。

## Files

**./run_spectrum.sh**

　あらかじめ与えられたテンプレXMLファイルをつかって過去のスペクトルを保存するスクリプト。

メモ
 * `diag` コマンドの`set` オプションで Sync.Start に遡りたい時刻を代入すれば過去のスペクトルを xml ファイルに保存してくれる。
 * まだ `/users/ushiba/script/autoDiaggui_SPECTRUM_yuzu.sh` が実際に使っている。タイミングを見計らって `/kagra/Dropbox/Measurements/VIS/script/automeasurement/run_spectrum.sh` に移動する。