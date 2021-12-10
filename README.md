# automeasurement

テンプレファイルを大量に実行するスクリプト。メンテを考えてBashで書くべし。グラフ描画などは他のリポジトリでおこなう。

## Template file

SPE\_{sustype}\_{stage}\_{doftype}\_{refnum}.xml

 * sustype : suspension type. TyepA, TypeB, TypeBp.
 * stage   : stage. IP, BF, .. , TM.
 * doftype : EUL or SENS
 * refnum  : reference number.


## Files

**./run_spectrum.sh**

　あらかじめ与えられたテンプレXMLファイルをつかって過去のスペクトルを保存するスクリプト。

メモ
 * `diag` コマンドの`set` オプションで Sync.Start に遡りたい時刻を代入すれば過去のスペクトルを xml ファイルに保存してくれる。
 * まだ `/users/ushiba/script/autoDiaggui_SPECTRUM_yuzu.sh` が実際に使っている。タイミングを見計らって `/kagra/Dropbox/Measurements/VIS/script/automeasurement/run_spectrum.sh` に移動する。


## Usage

If you measure all `Type-A` at `2021/12/1 13:53:02 UTC`, please execute like this;

```
$ run_spectrum TypeA "2021/12/1 13:53:02 UTC"
```