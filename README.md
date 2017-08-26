# similarActions

## search for similar actions

* "お茶する" and "コーヒーを飲む"
* "一杯飲む" and "軽く飲む"



## Make text files from DATABASE

```
doc = Document()
# reviews
doc.make_text_file_from_database(0, './docs/tabelog/20170816/reviews.txt')
# restaurant_prs
doc.make_text_file_from_database(1, './docs/tabelog/20170816/restaurant_prs.txt')
# reviews and restaurant_prs
doc.make_text_file_from_database(2, './docs/tabelog/20170816/reviews_and_restaurant_prs.txt')
```

## Make divided document
```
doc = Document()
doc.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
# テキストファイルを読み込み分かち書きする．メンバ変数に保存．
doc.make_document('./docs/tabelog/20170816/reviews.txt')
# メンバ変数に保存された分かち書きされた文章をテキストファイルに書き出す
doc.write_document('./docs/tabelog/20170816/reviews_divided.txt')
```

## Replace experiences for symbols
```
doc = Document()
doc.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
# 分かち書きされた文章を読み込みメンバ変数に保存.
doc.read_document('./docs/tabelog/20170816/reviews_divided.txt')
# 「飲む」という語に注目．「飲む」の10語以内にある経験をなす語(actionsに含まれる語)を記号に置き換える．
doc.replace_actions('飲む', 10)
doc.write_document('./docs/tabelog/20170816/reviews_replaced_10.txt')
```

## Weight experience words

```
doc = Document()
doc.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
doc.read_document('./docs/tabelog/20170816/reviews_actions_20170607飲むcut_replaced_10.txt')
# 経験にあたる語を2つずつ増やす
doc.weight_actions(2)
doc.write_document('./docs/tabelog/20170816/reviews_actions_20170607飲むcut_replaced_10_three.txt')
```

## Get words around the target word

```
doc = Document()
doc.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
doc.read_document('./docs/tabelog/20170816/reviews_actions_20170607飲むcut_replaced_10.txt')
doc.get_words_around_actions(15)
print(sorted(doc.words_around_actions['ちょっと'].items(), key = lambda x: x[1]))
```
