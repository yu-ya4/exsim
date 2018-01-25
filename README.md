# similarActions

## search for similar actions

* "お茶する" and "コーヒーを飲む"
* "一杯飲む" and "軽く飲む"


## DB connection

```
$ ssh -f -N -C -L 10000:localhost:3306 ieyasu -p 22
$ ssh -f -N -C -L 20000:localhost:3306 ieyasu-berry -p 22
'''

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
# レストランidも読み込みたい場合は以下
#docs.read_documents('../../data/docs/test/test_reviews_divided.txt', ''../../data/docs/test/test_reviews.txt.restaurant_ids.txt'')
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
docs.make_replace_dict()
# 「飲む」という語に注目．「飲む」の10語以内にある経験をなす語(experiencesに含まれる語)を記号に置き換える．
docs.replace_experiences_with_symbols('飲む', 10)
docs.write_documents('../../data/docs/test/test_divided_replaced_10.txt')
```


## Get words frequencies around the target word

```
words_frequencies, words_indexes = docs.documents[0].get_words_frequencies_around_target('食べる')
# {'軽い': 1, '熱々': 1, 'かす汁': 1, '美味しい': 1, '刺身': 1, '嬉しい': 1, '居酒屋': 1, 'さん': 1, 'ランチ': 1}
# {'5': [4, 3, 2, 1, 0, 6, 7, 8, 9]}
```

## Get words frequencies around the experiences

```
docs.get_words_frequencies_around_experiences(15)
print(docs.words_frequencies_around_experiences)
# {'美味しい飲む': {'位': 2, '思える': 4, '突き出し': 4, 'キッシュアツアツ': 2, 'キノコ': 2, '納得': 2, 'の': 7, '店': 9, '美味しい': 9, 'こちら': 4, 'それ': 4, 'そう': 5, 'いる': 5, 'れる': 4, '白': 4, 'ワイン': 4, 'experience_replace_number_0': 26, 'イタリア': 2, '産': 2, 'フィアーノ': 2, '3200': 2, '円': 14, 'シャルキュトリー': 2, '盛り合わせ': 4, '注文': 4, 'パテ': 2, '鴨': 2, '肉': 2, '燻製': 2, 'リエット': 1, '生': 1, 'ハム': 1, 'とても': 10, '馬刺し': 2, 'いつも': 2, 'どれ': 4, '品': 2, '9': 2, 'シャーベット': 2, '物': 3, '甘い': 2, '吸い物': 2, 'ご飯': 2, '筍': 1, 'ん': 4, '食べる': 10, '大騒ぎ': 2, '終': 2, 'い': 2, '女子': 2, 'スポーツ': 2, 'トレーナー': 2, 'みんな': 2, 'ハグ': 2, 'する': 13, '若干': 4, '数': 2, '人': 4, '脇': 1, '寝る': 1, '酒': 10, 'ブドウミミガー': 2, '海': 2, 'ょ': 2, 'く': 2, 'ら': 2, '島': 2, '盛り': 2, '三種': 2, '沖縄': 6, 'まず': 2, 'オススメ': 2, '良い': 7, '行く': 2, '初めて': 1, '刺身': 6, '新鮮': 2, '他': 2, 'つまむ': 2, '合う': 2, '味付け': 2, 'なる': 4, 'そば': 2, 'さっぱり': 2, '最適': 1, '僕': 1, 'コーレグス': 1, 'experience_replace_number_22': 6, 'お腹': 3, 'まあ': 2, 'つく': 2, '高い': 2, 'ちょっと': 2, '思う': 5, 'わり': 2, '中心': 1, 'メニュー': 3, '的': 1, 'キッシュ': 4, '十分': 2, '特に': 2, '金曜日': 2, '夜': 2, '全品': 2, '500': 2, '得': 2, '西大路': 2, '駅前': 1, 'あまり': 1, 'コイン': 2, 'ワン': 2, 'コンセプト': 2, '癒す': 2, '雰囲気': 2, 'ある': 8, '暖かみ': 2, 'グラス': 2, '戴く': 2, 'オーナー': 2, 'シェフ': 2, '心意気': 2, 'よう': 6, '450': 2, '数種類': 2, '中': 2, '選べる': 2, '赤': 2, 'スパーク': 1, 'リング': 1, '等': 1, '焼鳥': 4, '事': 2, '屋': 4, 'モチ': 4, '言う': 4, '旦那': 2, '珍しい': 2, '利用': 2, '頃': 1, '時': 5, '19': 1, 'experience_replace_number_86': 4, 'OK': 2, '駄目': 2, '基準': 2, '何': 2, 'アタシ': 2, '見える': 2, 'くる': 2, 'そわそわ': 2, 'てる': 2, '早々': 1, 'これ': 4, '～': 4, 'かるい': 2, '助': 2, 'とき': 2, '粒': 2, '米': 2, 'ちょこっと': 2, '寿司': 2, '締める': 2, '穴子': 1, 'ほた': 1, '２': 2, '３': 6, '安い': 2, 'ヤバイハマ': 2, 'うた': 2, '気': 2, '味': 2, '濃い': 2, 'たれる': 2, '笑': 2, '枚': 2, '一': 6, 'アグー': 2, 'だし': 3, '放題': 6, '少ない': 2, 'ジュース': 2, '豊富': 2, 'マンゴークランベリーパイン': 2, '気軽': 2, '料理': 4, '楽しめる': 2, '沢山': 6, '頼む': 4, 'とりあえず': 2, '早い': 2, 'サーブ': 2, 'さすが': 2, 'つり': 1, 'がる': 1, '空く': 1, '塩': 2, 'こんぶ': 2, '和える': 2, 'きゅうり': 2, '焼き鳥': 2, '店員': 3, 'さん': 5, '皆さん': 2, '感じ': 2, 'ついつい': 2, '長居': 2, 'しまう': 3, '意外と': 2, 'みたい': 4, '洋食': 2, 'もの': 2, '焼く': 2, '包む': 2, 'パイ': 3, 'アジ': 2, '焼き': 2, '包み': 2, '魚': 3, '結局': 2, '30': 4, '分': 5, '延長': 2, 'もらう': 2, 'かなり': 2, '飲む': 4, '4000': 2, '弱': 2, '満足': 4, '一緒': 1, '600': 2, ',': 4, '3'
```

## Calc words weght
```
docs.calc_words_weight()
print(docs.all_documents_weight)
# {0: {'今日': 0.73436916155120424, 'は': 0.57898508202353927, 'いい': 1.0, '天気': 1.0, 'です': 0.73436916155120424, 'も': 0.0, '頑張る': 0.0, '昨日': 0.0, '雨': 0.0, 'が': 0.0, '振った': 0.0, '私は': 0.0, '嫌い': 0.0, '曇り': 0.0, '晴れ': 0.0}, 1: {'今日': 0.73436916155120424, 'は': 0.0, 'いい': 0.0, '天気': 0.0, 'です': 0.0, 'も': 1.0, '頑張る': 1.0, '昨日': 0.0, '雨': 0.0, 'が': 0.0, '振った': 0.0, '私は': 0.0, '嫌い': 0.0, '曇り': 0.0, '晴れ': 0.0}, 2: {'今日': 0.0, 'は': 0.57898508202353927, 'いい': 0.0, '天気': 0.0, 'です': 0.0, 'も': 0.0, '頑張る': 0.0, '昨日': 1.0, '雨': 0.73436916155120424, 'が': 0.73436916155120424, '振った': 1.0, '私は': 0.0, '嫌い': 0.0, '曇り': 0.0, '晴れ': 0.0}, 3: {'今日': 0.0, 'は': 0.57898508202353927, 'いい': 0.0, '天気': 0.0, 'です': 0.73436916155120424, 'も': 0.0, '頑張る': 0.0, '昨日': 0.0, '雨': 0.73436916155120424, 'が': 0.73436916155120424, '振った': 0.0, '私は': 1.0, '嫌い': 1.0, '曇り': 0.0, '晴れ': 0.0}, 4: {'今日': 0.0, 'は': 0.0, 'いい': 0.0, '天気': 0.0, 'です': 0.0, 'も': 0.0, '頑張る': 0.0, '昨日': 0.0, '雨': 0.0, 'が': 0.0, '振った': 0.0, '私は': 0.0, '嫌い': 0.0, '曇り': 1.0, '晴れ': 0.33333333333333331}}
```

## Make Documents for each experience
```
exp_docs = docs.make_documents_for_each_experience()
```
