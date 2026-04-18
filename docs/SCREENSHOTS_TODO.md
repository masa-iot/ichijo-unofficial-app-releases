# マニュアル用スクリーンショット撮影チェックリスト

`docs/manual.html` に必要なスクリーンショットの**総入れ替え版**リストです。
既存の `docs/images/` 配下は **全て撮り直し**の対象です。
placeholder（点線の枠）が画像に置き換わるよう、指定のファイル名でPNGを `docs/images/` 直下に置いてください。

---

## 撮影の指針

- **デバイス**：iPhone 実機（15 Pro 等）または Android 実機（Pixel 等）。必要な箇所はプラットフォーム別に撮る
- **モード**：既定はライトモード。ウィジェットはライト／ダーク両方
- **データ**：**デモモードで撮影推奨**。全画面にサンプルデータが揃うので効率的
- **ファイル形式**：PNG（透過不要、ステータスバー＋ホームインジケータは含めてOK）
- **解像度**：縦長1080×2400以上。ウィジェットは実サイズ
- **置き場所**：`docs/images/` 直下（サブフォルダ不可）
- **命名**：このリストのファイル名と完全一致（スネークケース、.png）

---

## 合計約 100 枚 — カテゴリ別

### ① はじめに (2セット)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `splash.png` | スプラッシュ画面。ロゴが中央に表示された瞬間 |
| `onboarding_01.png` 〜 `onboarding_05.png` | オンボーディング5ページ（書類取り込み／図面／見積り仕様書／メモ／プライバシー） |

---

### ② ホーム (5枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `home_ieduzukuri.png` | 家づくりモード10タイル（次イベントまでのカウントダウンカード付き・基本形） |
| `home_living.png` | 暮らしモード6タイル |
| `home_drawer_ieduzukuri.png` | サイドメニュー展開（家づくりモード） |
| `home_drawer_living.png` | サイドメニュー展開（暮らしモード） |
| `home_countdown_card.png` | カウントダウンカードのみ拡大（「あと ○ 日」基本表示） |

---

### ③ 取り込み (5枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `import_top.png` | 取り込み画面（空状態 or 「ファイルから選択」ボタンが目立つカット） |
| `import_share_step1.png` | iサポのPDF閲覧画面で共有メニューを呼び出す場面（共有ボタンの位置はOS・バージョンで異なる点に注意） |
| `import_share_step2.png` | OS共有シートから「ICHIJO施主手帳」を選ぶ瞬間 |
| `import_preview_list.png` | ファイル複数選択後のプレビューリスト（自動検出された図面番号・種別・日付が各行に並んだ状態） |
| `import_duplicate.png` | 重複警告「既に取り込み済み」のSnackBar or ダイアログ |

---

### ④ ドキュメント管理 (7枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `doc_list.png` | 図面番号グループ表示の一覧。最新バッジ・件数カウンタが見える状態 |
| `doc_list_empty.png` | 空状態（「まだドキュメントがありません」＋取り込み誘導ボタン） |
| `doc_group.png` | グループ詳細の2カラム種別タイル。CAD／電気／仕様書／見積りが混在 |
| `doc_file_longpress.png` | ファイル長押しのBottomSheet（編集・削除の2ボタン） |
| `doc_file_edit_dialog.png` | ファイル情報編集ダイアログ（図面番号・種別・日付・表示名） |
| `doc_delete_group.png` | 「図面番号 ${番号} を削除」確認ダイアログ（リビジョン件数表示） |
| `doc_delete_file.png` | 「${種別}を削除」確認ダイアログ（ファイル名表示） |

---

### ⑤ PDFビューア (5枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `pdf_viewer.png` | PDFビューア全体。AppBar（ページ番号タイトル＋編集＋ブックマーク）と右下オレンジFABが写るカット |
| `pdf_viewer_memo_badge.png` | 同じページにメモが複数ある時のAppBar（メモバッジに件数表示） |
| `pdf_viewer_page_memos.png` | ページメモバッジをタップして開いた、当該ページのメモ一覧ポップアップ |
| `pdf_viewer_add_memo.png` | FABタップから開いたメモ追加ダイアログ（入力中の状態） |
| `pdf_viewer_edit.png` | PDFビューアから開く「ファイル情報を編集」ダイアログ |

---

### ⑥ 図面チェック（CAD差分） (13枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `diff_select.png` | 選択画面（種別セグメント＋Dropdown2つ＋履歴リスト） |
| `diff_select_single.png` | 「単独図面解析」トグルONの状態（バージョン選択が1つに変わる） |
| `diff_history.png` | 選択画面下部の比較履歴リスト拡大（メモバッジ・種別アイコンが見える） |
| `diff_computing.png` | 計算中の進捗バー＋メッセージ（「準備中…」など） |
| `diff_result.png` | 差分結果。赤青色分けがしっかり出ている差分。BottomAppBar「差分／旧／新」セグメント含む |
| `diff_result_old.png` | ビューモード「旧」表示時（旧バージョンの原画像） |
| `diff_result_new.png` | ビューモード「新」表示時（新バージョンの原画像） |
| `diff_filter_dropdown.png` | 右上フィルタDropdown展開状態（4段階が見える） |
| `diff_filter_moderate.png` | ノイズ除去フィルタ「ざっくり」適用後の差分結果 |
| `diff_adjusted_switch.png` | 「調整済／元の差分」スイッチが表示された状態（手動調整を保存したページ） |
| `diff_page_nav.png` | 複数ページPDFのBottomAppBarページナビ（←→と「X / Y」表示） |
| `diff_zoomed.png` | 8倍ズーム後の差分細部 |
| `diff_export_sheet.png` | エクスポートBottomSheet（1枚 or 3枚まとめ の選択肢） |
| `diff_align.png` | 位置合わせ画面（ドラッグ中の状態 or アンカー配置済み） |

---

### ⑦ 見積り管理 (9枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `estimate_tabs.png` | 見積り管理の「一覧／比較履歴」タブ切替UI |
| `estimate_list.png` | 見積り一覧（検算⚠マークのカードも混ぜると説明に使いやすい） |
| `estimate_list_longpress.png` | 一覧カード長押しBottomSheet（「比較対象に選択」「削除」） |
| `estimate_detail.png` | 見積り詳細の項目ツリー（①〜⑧の区分が展開されている状態） |
| `estimate_item_longpress.png` | 項目長押しBottomSheet（メモ追加・一覧・コピー） |
| `estimate_validation_warn.png` | 検算⚠️マーク付きの詳細画面の該当区分を拡大 |
| `estimate_diff.png` | 2版比較サマリー。青（追加）／赤（削除）／オレンジ（変更）が並ぶ画面 |
| `estimate_diff_filter.png` | 2版比較のフィルタ（変更ありのみ表示など） |
| `estimate_trend.png` | 推移表（3版以上のバージョンを横並び） |
| `estimate_history.png` | 比較履歴タブの内容（過去の比較実績が並んだ状態） |

---

### ⑧ 仕様書チェック (6枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `spec_list.png` | 仕様書管理 一覧タブ（取り込み済バージョンがカード表示） |
| `spec_list_longpress.png` | 一覧カード長押しBottomSheet |
| `spec_detail.png` | 仕様書詳細（セクション別カード：外部仕上表／内部仕上表／設備仕上表／…） |
| `spec_item_longpress.png` | 項目長押しのBottomSheet（メモ追加・一覧・コピー） |
| `spec_diff.png` | 2版比較（青＝追加／赤＝削除／オレンジ＝変更が同時に見える） |
| `spec_history.png` | 比較履歴タブの内容 |

---

### ⑨ ウチメモ+ (8枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `memo_on_diff.png` | CAD差分画面で位置にピンメモが立った状態 |
| `memo_on_estimate.png` | 見積り項目長押しからメモを追加する瞬間 |
| `memo_on_spec.png` | 仕様書項目長押しからメモを追加する瞬間 |
| `memo_list.png` | メモ一覧（6種の種別バッジ混在、フィルタUIも写す） |
| `memo_filter.png` | フィルタUIを展開した状態（種別／図面番号の選択肢が見える） |
| `memo_search.png` | キーワード検索の入力中（全文検索でヒット件数が絞られた状態） |
| `memo_edit.png` | メモ一覧から開くメモ編集ダイアログ |
| `memo_longpress_action.png` | 元画面（見積りやCAD差分）で既存メモを再操作するメニュー（編集／削除） |

---

### ⑩ ブックマーク (3枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `bookmark_list.png` | ブックマーク一覧（6種混在が理想：PDF・図面差分・見積り詳細／比較・仕様書詳細／比較） |
| `bookmark_empty.png` | 空状態のメッセージ |
| `bookmark_delete.png` | 削除確認ダイアログ（「「${ラベル}」を削除してよいですか？」） |

---

### ⑪ スケジュール (7枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `schedule_timeline.png` | タイムライン。過去・今日ライン・未来・ピン留めが1枚で見える |
| `schedule_empty.png` | 空状態（「まだスケジュールがありません」＋ヒントカード） |
| `schedule_pin_state.png` | ピン留め中（塗りつぶし）と未ピン（アウトライン）のアイコン比較が見える構図 |
| `schedule_add_preset.png` | 追加ダイアログ（プリセットチップが並んだ状態） |
| `schedule_add_custom.png` | 追加ダイアログ（自由入力チップ選択中） |
| `schedule_edit.png` | 既存アイテムタップから開く編集ダイアログ（種別は変更不可で表示） |
| `schedule_delete.png` | 長押しからの削除確認ダイアログ |
| `schedule_help.png` | 右上ヘルプアイコンからのBottomSheet |

---

### ⑫ ホームウィジェット (15枚)

#### Android — 全8種

| ファイル名 |
|---|
| `widget_android_2x1_light.png` |
| `widget_android_2x1_dark.png` |
| `widget_android_2x2_light.png` |
| `widget_android_2x2_dark.png` |
| `widget_android_4x1_light.png` |
| `widget_android_4x1_dark.png` |
| `widget_android_4x2_light.png` |
| `widget_android_4x2_dark.png` |

#### iOS — 2種（ライトのみ / システムテーマ追従）

| ファイル名 |
|---|
| `widget_ios_small.png` |
| `widget_ios_medium.png` |

#### 状態別 — 5種

| ファイル名 | 状態 |
|---|---|
| `widget_countdown.png` | カウントダウン（あと○日） |
| `widget_today.png` | 当日（ゴールド） |
| `widget_life_counter.png` | 新居生活カウンター |
| `widget_past.png` | 過去イベント（グレー） |
| `widget_empty.png` | 空状態 |

> 🎁 **記念日お祝い・ねぎらい等の特殊表示パターンはサプライズのため撮影対象外**。

---

### ⑬ でんき通信簿 (22枚)

#### メイン画面

| ファイル名 | 用途 |
|---|---|
| `electricity_empty.png` | 初回・データ未取り込み状態（CSV取り込み誘導） |
| `electricity_monthly.png` | セグメント「月次」メイン（トータル収支カード＋内訳） |
| `electricity_monthly_breakdown.png` | 収支の内訳カード拡大（売電収入／自家消費／蓄電池／基本料金／買電コスト） |
| `electricity_monthly_heatmap.png` | 日別収支ヒートマップのクローズアップ |
| `electricity_monthly_top5.png` | 日別収支TOP5 カード |
| `electricity_monthly_highlights.png` | 月内ハイライト（最高発電日・買電ゼロ日数等） |
| `electricity_monthly_full.png` | 月次ページのスクロール全体像（縦長スクリーンショット） |
| `electricity_annual.png` | セグメント「年間」メイン（年サマリー＋棒グラフ） |
| `electricity_annual_chart.png` | 年間レポートの積み上げ棒グラフ拡大（緑／赤の対比） |
| `electricity_total.png` | セグメント「通算（マイベスト）」メイン |
| `electricity_recovery_chart.png` | 投資回収ゴール＋回収予測LineChart |
| `electricity_best_records.png` | ベスト記録セクション（8項目×3粒度のグリッド） |
| `electricity_badges.png` | 実績バッジ（買電ゼロ日数・黒字日数・黒字月数） |

#### 取り込み／設定まわり

| ファイル名 | 用途 |
|---|---|
| `electricity_menu.png` | 右上 PopupMenuButton 展開（CSV取り込み／プラン設定／再計算／画像共有） |
| `electricity_csv.png` | CSV取り込み画面（進捗バー表示中） |
| `electricity_csv_error.png` | CSV取り込みバリデーションエラー（ヘッダー不一致など） |
| `electricity_plan_preset.png` | 料金プラン設定（プリセット9社リスト） |
| `electricity_plan_custom.png` | 料金プラン設定（カスタム作成入力中・3種の計算方式チップが見える） |
| `electricity_holidays.png` | 祝日管理画面（3ソース：API／計算／手動のマーク付き） |
| `electricity_special_days.png` | 特別日管理画面 |
| `electricity_fuel.png` | 燃料費調整管理画面（月別テーブル） |
| `electricity_renewable.png` | 再エネ賦課金管理画面（年度別） |
| `electricity_subsidy.png` | 補助金管理画面 |

#### 共有

| ファイル名 | 用途 |
|---|---|
| `electricity_share_card.png` | SNS共有カードのプレビュー画面 |

---

### ⑭ 便利ツール・家づくり記録 (3枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `tools_list.png` | 便利ツール一覧 |
| `humidity_calc.png` | 湿度計算ツール（値入力済） |
| `iedukuri_record.png` | 家づくり記録（暮らしモード専用、集計カードが見える） |

---

### ⑮ 設定 (13枚)

| ファイル名 | 用途・推奨ショット |
|---|---|
| `settings.png` | 設定画面全体（縦に長い場合は上半分と下半分に分けてもOK） |
| `settings_backup.png` | バックアップセクション拡大 |
| `settings_restore_confirm.png` | 復元前の警告ダイアログ（赤色、「既存データを完全に上書きします」） |
| `settings_restore_done.png` | バックアップ復元完了ダイアログ（再起動案内） |
| `settings_data.png` | データ管理セクション（再構築ボタン2つ） |
| `settings_mode.png` | モード切替セクション |
| `settings_mode_toggle.png` | モード切替トグルのみ拡大 |
| `settings_theme.png` | テーマ選択（ライト／ダーク／システム追従） |
| `settings_demo.png` | デモモードトグル |
| `settings_demo_confirm.png` | デモモードON時の確認ダイアログ |
| `settings_info.png` | アプリ情報セクション（バージョン行含む） |
| `settings_devmode.png` | 開発者モード有効化後のメニュー項目 |
| `settings_parse_dump.png` | パース失敗ダンプ内容ダイアログ（開発者モードから開いた状態） |

---

## 優先順（Phase 分け）

撮りやすい順＋ユーザー動線の起点から埋めていくのがおすすめ。数字は合計約100枚。

1. **Phase 1（実用最小 = 20枚）** — ①②③④⑤ の基本ショット  
   splash, onboarding5, home×5, import_top/share1/share2, doc_list/group/longpress, pdf_viewer（主要のみ）
2. **Phase 2（家づくりメイン機能 = 30枚）** — ⑥⑦⑧⑨⑩  
   図面チェック13 + 見積り9 + 仕様書6 + メモ8 + ブックマーク3（空状態・確認ダイアログは次Phase）
3. **Phase 3（スケジュール + ウィジェット + 設定 + ツール = 35枚）**  
   スケジュール7 + ウィジェット15 + 便利3 + 設定13
4. **Phase 4（でんき通信簿 = 22枚）** — 入居済みオーナー向け。デモデータで撮影可能
5. **Phase 5（状態・ダイアログ補完）** — 空状態／確認ダイアログ類を埋める仕上げ作業

---

## サプライズ温存のお願い 🎁

以下は **意図的にマニュアルから除外**しています。撮影もスキップしてください：

- ホーム画面のねぎらいメッセージカード（予定日翌日表示）
- ホーム画面の記念日メッセージカード（年記念日表示）
- 新居生活カウンターへの切替表示（ユーザーが育ててから見つける体験）
- ウィジェット版の記念日お祝い表示・ねぎらい表示
- その他、予定日翌日・年記念日・節目にだけ出る特殊表示パターン全般

マニュアルではこれらを「育てていく楽しみ」として温存しています。スクショで先出ししないようご注意ください。

---

## 運用ルール

- マニュアルに新しい機能が追加されたら、このリストを**必ず**同期更新する
- 機能改修でUIが変わったら既存スクショも撮り直して差し替え（ファイル名据え置き）
- 撮影済みで不要になったファイルはPRで削除
