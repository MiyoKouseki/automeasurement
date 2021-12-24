# automeasurement

Diag の xml テンプレファイルをもとに各サスペンションの伝達関数やスペクトルを測定する。

## Usage
### Transfer Function Measurement

#### Euler basis
オイラー自由度でプラントの応答を図りたい場合は以下の通り。たとえば、`ITMX`の`IM`段の`L`自由度を`TEST`で励起して、同じく`IM`段の`OSEM`でその応答を図りたい場合、以下のコマンドを入力。

```
$ run_plant ITMX IM TEST L 0.1
```

0.1 は測定のバンド幅。（Bashで`-bw 0.1` 綺麗に引数をとりたい。デフォルト値は0.1）

#### Sensor basis
もしセンサー自由度で応答を図りたい場合は以下の通り。

```
$ run_plant ITMX IM COILOUTF H1 0.1
```


### Spectrum Measurement
#### Past data
過去のスペクトルを測定したい場合は以下の通り。たとえば、`2021/12/1 13:53:02 UTC` でのすべての`Type-A` サスペンションのセンサーの値を図りたい場合、以下のコマンドを入力。

```
$ run_spectrum TypeA "2021/12/1 13:53:02 UTC"
```

なお、実際に使用するテンプレートファイルは`templates.txt`で与える。（これはそのうち使わないようにしたい。）

#### Template file

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


