# スクショ撮影 実施手順（撮影ワークフロー）

`SCREENSHOTS_TODO.md` を **実際に撮影する順番** に並べ替えた実施マニュアル。
100枚近くのスクショをランダムに撮ると死ぬので、**セッション単位** で「同じ画面まわりを一気に撮る」ように設計。

---

## 0. 事前準備

### 0-1. エミュレータ準備

| エミュレータ | 用途 | 設定 |
|---|---|---|
| **Android Emulator**（Pixel 7 / API 34 等） | 本体スクショの主力＋Androidウィジェット | 日本語UI、ライト／ダーク両方で起動可能 |
| **iOS Simulator**（iPhone 15 Pro / iOS 17+） | iOS固有UI＋iOSウィジェット | 日本語UI、ライト |

**エミュレータ運用のメリット**：
- 画面サイズ・OSバージョン・テーマを**固定**できる → 撮り直し時に仕上がりが揃う
- `adb` / `xcrun simctl` のCLIで**スクショを直接PCに保存**できる（AirDrop不要）
- 広告OFFビルド＋固定データセットで**完全に再現可能な撮影環境**を作れる
- ステータスバーもエミュレータ側で時刻・バッテリーを整えやすい

### 0-2. 広告OFFの専用ビルドを用意

エミュレータで撮るなら **広告OFFビルドを1本作って使い回す**のがベスト。機内モードなど気にしなくてよい。

```bash
# スクショ用ブランチを切る（本番を汚さない）
cd ~/Documents/workspace/ichijoAPP
git checkout -b screenshots-build

# ad_service.dart の _enableAds を false に変更
# lib/services/ad_service.dart:10
#   static const bool _enableAds = false;

# Android: APK ビルド → エミュレータにインストール
flutter build apk --release
adb install build/app/outputs/flutter-apk/app-release.apk

# iOS Simulator: そのまま flutter run でもOK
flutter run --release -d "iPhone 15 Pro"
```

撮影が一通り終わったら `git checkout -` で破棄、ブランチも削除。本番には一切混ざらない。

#### 広告バナーが出る画面（参考）
ホーム／ドキュメント詳細／見積り管理／仕様書管理／図面チェック／でんき通信簿 — この6画面で `_enableAds=false` により広告枠ごと畳まれる

### 0-3. エミュレータ側の調整

- **通知は全部ミュート**（エミュレータの通知バナーが混入しないように）
- **ステータスバー整え**：
  - Android: `adb shell cmd statusbar expand-notifications` や demo mode を使って時刻・電池を固定可能
    ```bash
    # Demo mode enable（固定ステータスバー）
    adb shell settings put global sysui_demo_allowed 1
    adb shell am broadcast -a com.android.systemui.demo -e command enter
    adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0930
    adb shell am broadcast -a com.android.systemui.demo -e command battery -e level 100 -e plugged false
    adb shell am broadcast -a com.android.systemui.demo -e command network -e wifi show -e level 4
    adb shell am broadcast -a com.android.systemui.demo -e command notifications -e visible false
    # 解除
    adb shell am broadcast -a com.android.systemui.demo -e command exit
    ```
  - iOS Simulator: `xcrun simctl status_bar booted override --time "9:30" --batteryState charged --batteryLevel 100 --wifiMode active --wifiBars 3 --cellularMode active --cellularBars 4 --operatorName ""`
- **テーマ切替**：
  - Android: 設定 → システム → テーマ、または `adb shell "cmd uimode night yes"` / `no`
  - iOS: シミュレータ設定、または `xcrun simctl ui booted appearance dark` / `light`

### 0-4. スクショ取得コマンド

1枚ごとに `SCREENSHOTS_TODO.md` の指定ファイル名で保存：

```bash
# Android
adb exec-out screencap -p > ~/Documents/workspace/ichijo-unofficial-app-releases/docs/images/home_ieduzukuri.png

# iOS Simulator
xcrun simctl io booted screenshot ~/Documents/workspace/ichijo-unofficial-app-releases/docs/images/home_ieduzukuri.png
```

**エイリアス化しておくと楽**：

```bash
# ~/.zshrc に追加
IMG_DIR=~/Documents/workspace/ichijo-unofficial-app-releases/docs/images
shot_a() { adb exec-out screencap -p > "$IMG_DIR/$1.png" && echo "✓ $1.png"; }
shot_i() { xcrun simctl io booted screenshot "$IMG_DIR/$1.png" && echo "✓ $1.png"; }

# 使用例
# shot_a home_ieduzukuri
# shot_i widget_ios_small
```

これで撮影 → 即 `docs/images/` 配下に正しいファイル名で保存完了。中間フォルダも AirDrop も不要。

### 0-5. データ状態の2パターン

本アプリのスクショは大きく2状態を使い分ける：

| 状態 | 用途 | 準備 |
|---|---|---|
| **デモON** | 機能の中身・グラフ・サンプルが必要なショット（ほぼ全部） | 設定画面でデモモードON |
| **デモOFF（データなし）** | 空状態ショット（ドキュメント空／スケジュール空 等） | デモOFFで、かつ本番側にデータがない新規状態 |

**推奨順序**：
1. デモOFFで「空状態」セッション（J）を片付ける
2. その後デモONに切り替えて他を一気に撮る

---

## セッション一覧（撮影順）

| セッション | 内容 | デモ状態 | 枚数目安 | 所要時間 |
|---|---|---|---|---|
| A | クリーンインストール＆オンボーディング | データなし | 6 | 15分 |
| B | 空状態ラッシュ | デモOFF | 8 | 20分 |
| C | ホーム＆設定まわり | デモON | 11 | 20分 |
| D | 取り込みフロー | デモON | 5 | 20分 |
| E | ドキュメント管理＋PDFビューア | デモON | 12 | 30分 |
| F | 図面チェック（CAD差分） | デモON | 14 | 40分 |
| G | 見積り管理 | デモON | 10 | 30分 |
| H | 仕様書チェック | デモON | 6 | 20分 |
| I | メモ＋ブックマーク | デモON | 11 | 30分 |
| J | スケジュール | デモON | 7 | 25分 |
| K | でんき通信簿（主力） | デモON | 22 | 60分 |
| L | 便利ツール＋設定＋開発者モード | デモON→ON | 16 | 30分 |
| M | ホームウィジェット Android | 実機 | 13 | 30分 |
| N | ホームウィジェット iOS | 実機 | 7 | 20分 |

**合計：約100枚 / 実働 6〜8時間**（分割推奨：2〜3日）

---

## セッションA：クリーンインストール＆オンボーディング（最初にやる）

**前提**：アプリをアンインストール済みの状態。

| # | 操作 | タイミング | ファイル名 |
|---|---|---|---|
| 1 | ストアからインストール → 起動 | ロゴ表示中 | `splash.png` |
| 2 | そのまま待つ | オンボ1ページ目表示 | `onboarding_01.png` |
| 3 | 右スワイプ | 2ページ目 | `onboarding_02.png` |
| 4 | 右スワイプ | 3ページ目 | `onboarding_03.png` |
| 5 | 右スワイプ | 4ページ目 | `onboarding_04.png` |
| 6 | 右スワイプ | 5ページ目（プライバシー） | `onboarding_05.png` |
| 7 | 「はじめる」をタップ | ホーム到達 | （Bで使うので撮らない or 予備） |

> ⚠️ onboardingは**初回起動でしか表示されない**。撮り逃したら `設定 → チュートリアルを再表示` で再現可能だが、最初にまとめて済ませるのが吉。

---

## セッションB：空状態ラッシュ（デモOFFのうちに一気に）

**前提**：初回インストール直後、データは一切入れていない。ホーム画面まで到達済み。

| # | 画面 | 操作 | ファイル名 |
|---|---|---|---|
| 1 | ホーム | そのまま撮影 | （Cで撮るのでスキップ） |
| 2 | ドキュメント管理 | ホーム→ドキュメント管理タイル | `doc_list_empty.png` |
| 3 | 戻る → ブックマーク | ホーム→ブックマーク | `bookmark_empty.png` |
| 4 | 戻る → スケジュール | ホーム→スケジュール | `schedule_empty.png` |
| 5 | 戻る → 設定 → 暮らしモードON | 暮らしホーム→でんき通信簿 | `electricity_empty.png` |
| 6 | 戻る → 設定 → 家づくりモードに戻す | — | — |

**追加で撮る**：
- 取り込み画面の「ファイル選択前」 → ホーム → PDF取り込みタイル → `import_top.png`

---

## セッションC：ホーム＆モード切替（デモON開始）

**前提**：設定画面へ遷移、**デモモードをON**。ホームに戻る。

| # | 操作 | タイミング | ファイル名 |
|---|---|---|---|
| 1 | ホーム画面（家づくりモード） | 全10タイル見える | `home_ieduzukuri.png` |
| 2 | 左上☰アイコンタップ | ドロワー展開 | `home_drawer_ieduzukuri.png` |
| 3 | ドロワー閉じる → カウントダウンカードの位置 | カード部分を中心にスクショ | `home_countdown_card.png` |
| 4 | 設定 → モード切替で暮らしモードへ | 設定画面のトグル拡大 | `settings_mode_toggle.png` |
| 5 | ホームに戻る | 暮らしモード6タイル | `home_living.png` |
| 6 | 左上☰アイコンタップ | ドロワー（暮らし） | `home_drawer_living.png` |
| 7 | 暮らしホームの「家づくり記録」タイルタップ | 家づくり記録画面 | `iedukuri_record.png` |
| 8 | 暮らしホームの「便利ツール」タイルタップ | ツール一覧 | `tools_list.png` |
| 9 | 湿度計算ツールタップ → 値入力 | 値入力済み | `humidity_calc.png` |
| 10 | 設定 → 家づくりモードに戻す | — | — |

---

## セッションD：取り込みフロー

**前提**：デモON（デモONでも取り込み動作自体は可）。家づくりモードのホームから開始。

| # | 操作 | タイミング | ファイル名 |
|---|---|---|---|
| 1 | iサポ（or テスト用PDFアプリ）でPDFを開いて共有メニューを呼び出す | **iサポ側画面** | `import_share_step1.png` |
| 2 | 共有シートで「ICHIJO施主手帳」を選ぶ | **OS共有シート** | `import_share_step2.png` |
| 3 | アプリ側に戻る → 取り込み画面が開いた状態 | プレビューリスト | `import_preview_list.png` |
| 4 | 同じPDFをもう一度取り込み実行 | 重複警告が出る | `import_duplicate.png` |

> **Tips**：step1・step2はスクショが自然に撮りやすいように、**iサポ／ダミーPDFアプリの準備**を先にしておく。撮影用ダミーPDFは `docs/images/samples/dummy.pdf` のようなプレースホルダを使っても良い。

---

## セッションE：ドキュメント管理＋PDFビューア

**前提**：デモONでデータあり（複数の図面番号グループが揃っている状態）。

### E-1. 一覧 → グループ詳細

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → ドキュメント管理 | `doc_list.png` |
| 2 | いずれかの図面番号カードを長押し | `doc_delete_group.png`（ダイアログ出たところで撮影→**キャンセル**） |
| 3 | カードをタップ | `doc_group.png` |

### E-2. ファイル長押しメニュー

| # | 操作 | ファイル名 |
|---|---|---|
| 4 | グループ内のファイルタイルを長押し | `doc_file_longpress.png` |
| 5 | 「ファイル情報を編集」をタップ | `doc_file_edit_dialog.png`（編集せずキャンセル） |
| 6 | もう一度タイル長押し → 「削除」をタップ | `doc_delete_file.png`（キャンセル） |

### E-3. PDFビューア

| # | 操作 | ファイル名 |
|---|---|---|
| 7 | タイルタップでPDFビューアを開く | `pdf_viewer.png` |
| 8 | 右下FABタップ | `pdf_viewer_add_memo.png`（入力途中で撮影→キャンセル or 保存） |
| 9 | メモを2〜3件同ページに追加（事前に仕込む） | `pdf_viewer_memo_badge.png`（バッジ付きAppBar） |
| 10 | バッジをタップ | `pdf_viewer_page_memos.png` |
| 11 | 右上 編集アイコンをタップ | `pdf_viewer_edit.png`（キャンセル） |

> **仕込み**：E-3 の#9 用に、該当PDFの同一ページにメモを複数件追加しておく。E-4メモセッション後にまとめて撮るのも可。

---

## セッションF：図面チェック（CAD差分）

**前提**：デモONで複数バージョンのCAD／電気図面が揃っている。

### F-1. 選択画面まわり

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → 図面チェック | `diff_select.png` |
| 2 | 画面下部の比較履歴エリアに近寄って撮る | `diff_history.png` |
| 3 | 単独図面解析トグルをON | `diff_select_single.png` |
| 4 | トグルをOFFに戻す | — |

### F-2. 差分結果画面

| # | 操作 | ファイル名 |
|---|---|---|
| 5 | 旧・新を選んで「比較する」タップ → 計算中 | `diff_computing.png`（シャッター素早く） |
| 6 | 計算完了 → 差分画面 | `diff_result.png` |
| 7 | BottomAppBarで「旧」に切替 | `diff_result_old.png` |
| 8 | 「新」に切替 | `diff_result_new.png` |
| 9 | 「差分」に戻す | — |

### F-3. フィルタ・ズーム・位置合わせ・エクスポート

| # | 操作 | ファイル名 |
|---|---|---|
| 10 | 右上フィルタDropdown タップ（開いた瞬間） | `diff_filter_dropdown.png` |
| 11 | 「ざっくり」を選択 → 再計算後 | `diff_filter_moderate.png` |
| 12 | 「しっかり」に戻す → 位置合わせアイコン | 位置合わせ画面 `diff_align.png` |
| 13 | 手動で調整 → 保存して戻る | 「調整済／元の差分」スイッチが表示 `diff_adjusted_switch.png` |
| 14 | ピンチで最大までズーム | `diff_zoomed.png` |
| 15 | 次のページに送る（複数ページPDFで） | `diff_page_nav.png`（BottomAppBar中心） |
| 16 | 右上エクスポートアイコンタップ | `diff_export_sheet.png` |

---

## セッションG：見積り管理

**前提**：デモONで3版以上の見積り、検算⚠付きも含まれている状態。

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → 見積り管理 | `estimate_list.png` |
| 2 | AppBar下のタブバーにフォーカス | `estimate_tabs.png` |
| 3 | 一覧カードを長押し | `estimate_list_longpress.png`（キャンセル） |
| 4 | カードをタップ → 詳細 | `estimate_detail.png` |
| 5 | 検算⚠が付いている区分までスクロール | `estimate_validation_warn.png` |
| 6 | 任意の項目を長押し | `estimate_item_longpress.png` |
| 7 | 戻る → 比較ボタンから2版比較 | `estimate_diff.png` |
| 8 | 比較画面のフィルタUIを開く | `estimate_diff_filter.png` |
| 9 | 戻って推移表を開く | `estimate_trend.png` |
| 10 | 戻って比較履歴タブを開く | `estimate_history.png` |

---

## セッションH：仕様書チェック

**前提**：デモONで2版以上の仕様書。

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → 仕様書チェック | `spec_list.png` |
| 2 | 一覧カード長押し | `spec_list_longpress.png`（キャンセル） |
| 3 | カードタップ → 詳細 | `spec_detail.png` |
| 4 | 項目長押し | `spec_item_longpress.png` |
| 5 | 戻る → 比較ボタンから2版比較 | `spec_diff.png` |
| 6 | 戻って比較履歴タブ | `spec_history.png` |

---

## セッションI：メモ＋ブックマーク

**前提**：デモONで各種データあり。CAD差分は一度計算済みで即表示できる状態。

### I-1. メモの追加（4種類＋フィルタ）

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | CAD差分画面で気になる位置を長押し → ピンメモ入力 | `memo_on_diff.png` |
| 2 | 見積り詳細で項目長押し → メモ追加 | `memo_on_estimate.png` |
| 3 | 仕様書詳細で項目長押し → メモ追加 | `memo_on_spec.png` |
| 4 | 既存メモを元画面で長押し | `memo_longpress_action.png` |

### I-2. メモ一覧

| # | 操作 | ファイル名 |
|---|---|---|
| 5 | ホーム → ウチメモ+ | `memo_list.png` |
| 6 | フィルタアイコンタップ | `memo_filter.png` |
| 7 | 検索欄に文字入力 | `memo_search.png` |
| 8 | カードタップ → 編集ダイアログ | `memo_edit.png`（キャンセル） |

### I-3. ブックマーク

| # | 操作 | ファイル名 |
|---|---|---|
| 9 | 事前に6種（PDF／図面差分／見積り詳細・比較／仕様書詳細・比較）をブックマーク登録 | — |
| 10 | ホーム → ブックマーク | `bookmark_list.png` |
| 11 | カード長押し | `bookmark_delete.png`（キャンセル） |

---

## セッションJ：スケジュール

**前提**：デモON（サンプルイベントが入っている状態）。ピン留め操作に注意（撮影順大事）。

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → スケジュール | `schedule_timeline.png` |
| 2 | アイテムのピンアイコンを片方だけ塗りつぶしに | `schedule_pin_state.png`（ピン済と未ピンが同時に見える構図） |
| 3 | アイテムタップ → 編集ダイアログ | `schedule_edit.png`（キャンセル） |
| 4 | アイテム長押し → 削除確認 | `schedule_delete.png`（キャンセル） |
| 5 | 右下FABタップ → 追加ダイアログ | `schedule_add_preset.png` |
| 6 | 「自由入力」チップ選択 | `schedule_add_custom.png` |
| 7 | キャンセル → 右上ヘルプアイコン | `schedule_help.png` |

---

## セッションK：でんき通信簿（ボリューム最大）

**前提**：**デモON＋でんき通信簿のダミーCSVが取り込まれている**状態。1年分以上のデータがあると年間・通算まで撮れる。

### K-1. 設定・取り込みまわり

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → でんき通信簿（空状態は B で撮ったのでスキップ） | — |
| 2 | 右上メニュー展開 | `electricity_menu.png` |
| 3 | 「CSV取り込み」 → ピッカー → 進捗画面 | `electricity_csv.png` |
| 4 | 不正なCSVを投入してエラー画面 | `electricity_csv_error.png` |
| 5 | 「プラン設定」 → プリセットリスト | `electricity_plan_preset.png` |
| 6 | カスタムプラン作成画面 | `electricity_plan_custom.png` |
| 7 | 祝日管理 | `electricity_holidays.png` |
| 8 | 特別日管理 | `electricity_special_days.png` |
| 9 | 燃料費調整 | `electricity_fuel.png` |
| 10 | 再エネ賦課金 | `electricity_renewable.png` |
| 11 | 補助金管理 | `electricity_subsidy.png` |

### K-2. 月次レポート

| # | 操作 | ファイル名 |
|---|---|---|
| 12 | でんき通信簿メイン → 月次セグメント選択 | `electricity_monthly.png` |
| 13 | 内訳カード部分まで寄る | `electricity_monthly_breakdown.png` |
| 14 | スクロール → 日別ヒートマップ | `electricity_monthly_heatmap.png` |
| 15 | 日別TOP5カード | `electricity_monthly_top5.png` |
| 16 | 月内ハイライト | `electricity_monthly_highlights.png` |
| 17 | 画面全体（縦長スクロール） | `electricity_monthly_full.png` |

### K-3. 年間・通算

| # | 操作 | ファイル名 |
|---|---|---|
| 18 | 年間セグメント | `electricity_annual.png` |
| 19 | 棒グラフ部分拡大 | `electricity_annual_chart.png` |
| 20 | 通算セグメント | `electricity_total.png` |
| 21 | 投資回収ゴール＋予測グラフ拡大 | `electricity_recovery_chart.png` |
| 22 | ベスト記録セクション | `electricity_best_records.png` |
| 23 | 実績バッジ | `electricity_badges.png` |

### K-4. SNS共有

| # | 操作 | ファイル名 |
|---|---|---|
| 24 | 月次レポートから「画像として共有」 | `electricity_share_card.png` |

---

## セッションL：設定＆開発者モード

**前提**：デモON。最後に開発者モードをON→撮影。

| # | 操作 | ファイル名 |
|---|---|---|
| 1 | ホーム → 設定 | `settings.png` |
| 2 | バックアップセクションに寄る | `settings_backup.png` |
| 3 | 「バックアップ復元」タップ → 確認ダイアログ | `settings_restore_confirm.png`（キャンセル） |
| 4 | （事前に小さなZipを用意しておき）復元完了画面を撮る | `settings_restore_done.png` |
| 5 | データ管理セクション | `settings_data.png` |
| 6 | モード切替セクション | `settings_mode.png` |
| 7 | テーマ選択展開 | `settings_theme.png` |
| 8 | デモモードセクション | `settings_demo.png` |
| 9 | デモモードOFFにする瞬間（or ONにする瞬間） | `settings_demo_confirm.png` |
| 10 | アプリ情報セクション | `settings_info.png` |
| 11 | **バージョン行を7回連続タップ** → SnackBar | 撮り逃さない |
| 12 | 開発者モードONの設定画面 | `settings_devmode.png` |
| 13 | パース失敗ダンプ項目をタップ → 内容ダイアログ | `settings_parse_dump.png` |
| 14 | （撮影後）開発者モードOFFに戻す | — |

---

## セッションM：ホームウィジェット Android（エミュレータ）

**前提**：Android Emulator（Pixel_7等）にアプリをインストール＋スケジュールにデモデータが入っている。

### M-1. 各サイズ × ライト／ダーク（8枚）

| # | 手順 |
|---|---|
| 1 | エミュレータのテーマをライトに切替：`adb shell "cmd uimode night no"` |
| 2 | ホーム画面長押し → ウィジェット → ICHIJO施主手帳 |
| 3 | 2×1 ウィジェットを設置 → `shot_a widget_android_2x1_light` |
| 4 | 2×2 設置 → `shot_a widget_android_2x2_light` |
| 5 | 4×1 設置 → `shot_a widget_android_4x1_light` |
| 6 | 4×2 設置 → `shot_a widget_android_4x2_light` |
| 7 | テーマをダークに切替：`adb shell "cmd uimode night yes"` |
| 8 | 同じ4サイズを撮る → `widget_android_2x1_dark.png` 〜 `4x2_dark.png` |

> 💡 **ウィジェットは画面全体ではなくウィジェット部分だけをトリミングするのが綺麗**。エミュレータ画面全体を `screencap` で撮ってから、画像編集でウィジェット枠だけ切り出す。

### M-2. 状態別（5枚）

各状態を作るためのスケジュール調整例：

| 状態 | 作り方 | ファイル名 |
|---|---|---|
| カウントダウン | 近めの未来日付でピン留め | `widget_countdown.png` |
| 今日 | 今日の日付でピン留め | `widget_today.png` |
| 新居生活カウンター | 引き渡しを過去日付でピン留め | `widget_life_counter.png` |
| 過去イベント | 過去イベントをピン留め（引き渡し等がない状態） | `widget_past.png` |
| 空状態 | 全スケジュールを削除 or ピン無し | `widget_empty.png` |

**💡 撮影は状態切替の度にウィジェットが再描画されるのを待つ**（Androidは即時、数秒待ってから撮ると安心）。

---

## セッションN：ホームウィジェット iOS（Simulator）

**前提**：iOS Simulator にアプリインストール済み、スケジュールにデータが入っている。

### N-1. サイズ別（2枚）

| # | 手順 | ファイル名 |
|---|---|---|
| 1 | ホーム画面長押し → ＋ → ICHIJO施主手帳 | — |
| 2 | Small サイズ設置 → 数秒待つ | `shot_i widget_ios_small` |
| 3 | Medium サイズ設置 | `shot_i widget_ios_medium` |

### N-2. 状態別（5枚）

Android と同じパターンで5状態。エミュレータ側データを切り替えつつ撮影。

> 💡 **iOSウィジェットはWidgetKitのTimelineで更新されるため、スケジュール変更が即反映されない場合あり**。アプリを一度フォアグラウンドに持っていくと強制更新される（Simulator でも同じ挙動）。

> 💡 iOSウィジェットもトリミング前提でOK。`xcrun simctl io booted screenshot` でホーム画面全体を撮って後から切り出し。

---

## 🎁 撮影 **しない** ショット

サプライズ温存のため、以下は意図的に撮影対象外：

- ホーム画面のねぎらいメッセージカード／記念日メッセージカード
- 新居生活カウンターへの切替表示（ウィジェット版の `widget_life_counter.png` は撮ってOKですが、ホーム画面本体は「節目で変わる」として匂わせ止まりにしています）
- ウィジェット版の記念日お祝い表示

---

## 最終チェックリスト

撮影が一巡したら以下を確認：

- [ ] `docs/images/` 配下に全ファイルが揃っている
- [ ] `manual.html` をブラウザで開き、placeholder が全部画像に置き換わっている
- [ ] placeholder が残っているファイル名 = 撮り逃し。`SCREENSHOTS_TODO.md` と突き合わせて埋める
- [ ] 開発者モードは**OFF**に戻した
- [ ] デモモードは**OFF**に戻した
- [ ] 撮影用端末上の個人情報（実名・住所が含まれる見積りPDF等）が残っていないか確認

### 置き換わり確認コマンド（Mac）

```bash
# placeholder に記載されている想定ファイル名一覧
grep -oE '[a-z_0-9]+\.png' docs/SCREENSHOTS_TODO.md | sort -u > /tmp/expected.txt

# 実際にあるファイル名一覧
ls docs/images/*.png | xargs -n1 basename | sort -u > /tmp/actual.txt

# 撮り逃しを洗い出す
comm -23 /tmp/expected.txt /tmp/actual.txt
```

---

## 運用メモ

- アプリUIに変更が入ったら、このファイルの該当セクションも更新
- 新機能追加時は `SCREENSHOTS_TODO.md` と連動して撮影手順もここに追記
- 撮影2回目以降はセッションC〜Lを同じ流れで回せば、1〜2時間で差し替えが完了する
