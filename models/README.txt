test1: data=data1, size=200, window=15
	50 actions use natural w2v
test2: data=data2, size=200, window=15
	50 actions regard an action as one word

0_0_drink.model: フレーズ検索 60行動(action.txt drink) window=15 use mydict
0_1_drink.model: フレーズ検索 60行動(action.txt drink) window=15 use default dict
1_0_drink.model: 通常検索 60行動(action.txt drink) window=15 use mydict
1_1_drink.model: 通常検索 60行動(action.txt drink) window=15 use default dict
