# similarActions

## search for similar actions

* "お茶する" and "コーヒーを飲む"
* "一杯飲む" and "軽く飲む"


## import
```
from exsim import document
```


## Make text files from DATABASE

```
# reviews
document.make_text_file_from_database(0, 'where res.pal="kyoto" limit 10', '../../data/docs/test/test_reviews.txt')
# restaurant_prs
document.make_text_file_from_database(1, 'where res.pal="kyoto" limit 10', '../../data/docs/test/test_reviews.txt')
# reviews and restaurant_prs
document.make_text_file_from_database(2, 'where res.pal="kyoto" limit 10', '../../data/docs/test/test_reviews.txt')
```

## Make texts divided
```
# テキストファイルを読み込み分かち書きして保存
document.diveide_texts('../../data/docs/test/test_reviews.txt', '../../data/docs/test/test_reviews_divided.txt')

```

## Make Documents
```
docs = document.Documents()
docs.read_documents('../../data/docs/test/test_reviews_divided.txt')
print(docs.documents[0])
# <exsim.document.Document object at 0x10f90ec50>
print(docs.documents[0].words)
# ['刺身', '美味しい', 'かす汁', '熱々', '軽い', '食べる', '嬉しい', '居酒屋', 'さん', 'ランチ', 'お出かけ', '前', '駅', '近く', '何', '食べる', '思う', '女性', '一', '人', '入れる', 'さっと', '食べる', 'られる', 'そう', '店', '例', 'イートイン', '可能', 'パン', '屋', 'あんまり', 'ない', 'よう', '本当は', 'ところ', 'いい', '思う', 'もっと', 'ゆっくり', 'したう', 'いう', 'ファストフード', '店', '入る', 'ため', '女性', '一', '人', '競馬', '場', '入る', '行く', 'の', '変', '気', 'する', '悩む', '挙句', '居酒屋', 'さん', '昼', '営業', 'やる', 'いる', '刺身', '定食', '800', '文字', '惹く', 'れる', '通りすがり', '入る', 'の', 'こちら', '文字数', '制限', 'ある', 'よう', '詳しい', 'ブログ', 'どうぞ', 'ん', '居酒屋', '淀', '駅', '昼', '総合', '点', '40', 'A', 'いい', 'コメント', 'する', 'テトラ', 'さん', '読者', 'なる', 'ブログ', '更新', '情報', '受け取れる', 'アクセス', '簡単', 'なる', '読者', 'なる', 'SNS', 'アカウント', 'TwitterFacebook', '記事', 'ある', '昨日', 'ご飯', 'たち', '～', '記事', 'ある', '次', '記事', '昨日', 'ご飯', 'たち', '～', 'ブログトップ', '記事', '一覧', '画像', '一覧']
```

## Read experiences
```
docs.read_experience_list('chie-extracted2')
print(docs.experiences.experiences[0])
<egmat.experience.Experience object at 0x10d577588>
print(docs.experiences.experiences[0].modifier)
美味しく
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
