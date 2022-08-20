from pymongo import MongoClient

# 实例化mongo，建立连接
client = MongoClient(host='127.0.0.1', port=27017)
collection = client['pymongo_test']['t1000']

# 插入1000条数据
# data_list = [{'name': 'py{}'.format(i), 'my_id': i} for i in range(1000)]
# collection.insert_many(data_list)

# 查询my_id为100的倍数，同时显示name，不显示_id
# data_list = list(collection.find())
# data_list = [i for i in data_list if i['my_id']%100==0]
# print(data_list)
# 用聚合函数(多个管道放在聚合函数里)
# result = collection.aggregate([{'$group': {'_id': 'name', 'count': {'$sum': 1}}}])
result = collection.aggregate([{'$match': {'my_id': {'$lte': 10}}}, {'$project': {'_id': 0}}])
print(list(result))
