# similarActions

## search for similar actions

* "お茶する" and "コーヒーを飲む"
* "一杯飲む" and "軽く飲む"



## Make text files from DATABASE

```
doc = Document()
# reviews
doc.make_text_file_from_database(0, '../../data/docs/tabelog/20170816/reviews.txt')
# restaurant_prs
doc.make_text_file_from_database(1, '../../data/docs/tabelog/20170816/restaurant_prs.txt')
# reviews and restaurant_prs
doc.make_text_file_from_database(2, '../../data/docs/tabelog/20170816/reviews_and_restaurant_prs.txt')
```

## Make divided document
```
doc = Document()
# テキストファイルを読み込み分かち書きする．メンバ変数に保存．
doc.make_document('../../data/docs/tabelog/20170816/reviews.txt')
# メンバ変数に保存された分かち書きされた文章をテキストファイルに書き出す
doc.write_document('../../data/docs/tabelog/20170816/reviews_divided.txt')
```

## Replace experiences for symbols
```
doc = Document()
doc.read_experience_list('chie-extracted2')
# 分かち書きされた文章を読み込みメンバ変数に保存.
doc.read_document('../../data/docs/tabelog/20170816/reviews_divided.txt')
# 「飲む」という語に注目．「飲む」の10語以内にある経験をなす語(experiencesに含まれる語)を記号に置き換える．
doc.replace_experiences('飲む', 10)
doc.write_document('../../data/docs/tabelog/20170816/reviews_replaced_10.txt')
```

## Weight experience words

```
doc = Document()
doc.read_experience_list('chie-extracted2')
doc.read_document('../../data/docs/tabelog/20170816/reviews_actions_20170607飲むcut_replaced_10.txt')
# 経験にあたる語を2つずつ増やす
doc.weight_experiences(2)
doc.write_document('../../data/docs/tabelog/20170816/reviews_actions_20170607飲むcut_replaced_10_three.txt')
```

## Get words around the target word

```
doc = Document()
doc.read_experience_list('chie-extracted2')
doc.read_document('../../data/docs/test/test-divided-replaced-10.txt')
doc.get_words_around_experiences(15)
doc.show_words_around_experience('ちょっと')
```
