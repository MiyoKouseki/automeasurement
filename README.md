# automeasurement

VISの伝達関数測定を半自動で行うためのパッケージ

## Install

## Usage

## 詳細

### ディレクトリ

AutoMeasurement(ATM)のスクリプトはATM_DIRに、測定用のテンプレートファイルや測定結果はSAVE_DIR以下にある。

```
ATM_DIR=/kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement
SAVE_DIR=/kagra/Dropbox/Measurements/VIS/
```

### テンプレートファイル

テンプレートはステージごとに用意する。例えば、`PR3_BF_TEST_L` を励起したい場合は、`${SAVE_DIR}/TEMPLATES/PLANT_PR3_BF.xml` というファイルを使い、TEST_L の励起チャンネルを選んで励起する。

実際のテンプレートファイルは測定用と管理用で二つ存在する。測定用ファイルは管理用ファイルから`${ATM_DIR}/bin/init_templates.sh`を使って生成される。

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

### 結果ファイル

測定結果は

### メモ, ToDo

 * 管理用テンプレファイルファイルを減らせないか