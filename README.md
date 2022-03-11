# automeasurement

VISの伝達関数測定を半自動で行うためのパッケージ。

## Usage

## 詳細

#### ディレクトリ

AutoMeasurement(ATM)のスクリプトはATM_DIRに、測定用のテンプレートファイルや測定結果はATM_SAVE_DIR以下にある。

```
ATM_DIR=/kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement
ATM_SAVE_DIR=/kagra/Dropbox/Measurements/VIS/
```

#### テンプレートファイル

テンプレートはステージごとに用意する。例えば、`PR3_BF_TEST_L` を励起したい場合は、`${ATM_SAVE_DIR}/TEMPLATES/PLANT_PR3_BF.xml` というファイルを使い、TEST_L の励起チャンネルを選んで励起する。

なお、実際のテンプレートファイルは測定用と管理用で二つ存在する。測定用ファイルは管理用ファイルから`${ATM_DIR}/bin/init_templates.sh`を使って生成される。

管理用テンプレートは、git管理するファイルを減らすために、各Typeごとにした。以下のように現在合計9ファイル存在する。

 * ${ATM_DIR}/templates/PLANT_TYPEA_IP.xml
 * ${ATM_DIR}/templates/PLANT_TYPEA_BF.xml
 * ${ATM_DIR}/templates/PLANT_TYPEA_GAS.xml
 * ${ATM_DIR}/templates/PLANT_TYPEA_IM.xml
 * ${ATM_DIR}/templates/PLANT_TYPEB_IP.xml
 * ${ATM_DIR}/templates/PLANT_TYPEB_GAS.xml 
 * ${ATM_DIR}/templates/PLANT_TYPEB_IM.xml
 * ${ATM_DIR}/templates/PLANT_TYPEBP_BF.xml
 * ${ATM_DIR}/templates/PLANT_TYPEBP_GAS.xml 
 * ${ATM_DIR}/templates/PLANT_TYPEBP_IM.xml  

#### 測定結果ファイル

測定結果はGuardianのState名と実行したタイムスタンプをファイル名に付与して保存する。例えば、2022/02/18 19:06 にSTANDBYステートのETMXのETMX_IP_TEST_Lを励起した測定結果は`${ATM_SAVE_DIR}/PLANT/ETMX/2022/02/PLANT_ETMX_STANDBY_IP_TEST_L_202202181906.xml`として保存する。なお、タイムスタンプは後述する`run_plants.sh`が実行された時刻を意味しており、個々の測定テンプレートが実行されたタイミングではないことに注意されたい。

#### 測定実行スクリプト

測定の実行は`run_plant.sh` で行う。指定したテンプレートをdiagコマンドで実行し、測定結果を指定した名前で保存するためのスクリプトである。

このdiag実行用スクリプトに適切なテンプレートファイルと保存ファイル名を与えるのが`run_plants.sh`である。このスクリプトは、連続した測定をするために使用し、一連の測定に対してGuardStateとタイムスタンプを押す。

#### Plot用スクリプト

Plot用スクリプトは任意の測定結果同士を比較するために使用する。例えば、同じ伝達関数を違う時刻で比較する場合に使用する。

### メモ, ToDo

 * 管理用テンプレファイルファイルを減らせないか