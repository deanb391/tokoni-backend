from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.account import Account
from appwrite.services.avatars import Avatars
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.query import Query
import urllib
from flask import Flask, request, jsonify
from flask_cors import CORS
import random


app = Flask(__name__)


CORS(app)  

appwriteConfig = { 
  'endpoint': 'https://fra.cloud.appwrite.io/v1', 
  'platform': 'com.jsm.tokoni',
  'projectId': '680691d5000568084744',
  'databaseId': '680693f6003c6ef1a190',
  'userCollectionId': '680694120032819d8799',
  'shopCollectionId': '6806941e002cccaa571f',
  'productCollectionId': '68069423003e1886bfc6',
  'reviewCollectionId': '6806943e002a7fb55dfa',
  'heartsCollectionId': '6806a2700013a4751af9',
  'storageId': '68069b5b0038042c4d12',
  'chatsCollectionId': '68069429003b9f9df7b0',
  'messagesCollectionId': '68069430000b0e94c483',
  'postCollectionId': '68069524003528fc5aa7',
  'commentCollectionId': '6806945600187f60c80d',
  'postLikesCollectionId': '6806946b00036ece1aaf',
  'notificationsCollectionId': '6806948700116a766c18',
  'settingsCollectionId': '68069496000f9beedf64',
  'shopViewsCollectionId': '6806947400158907564d',
  'notificationsSettingId': '6808828400352526c61d',
  'profileSettingId': '680882c3003e6f11ef22',

}

client = Client()

(client
 .set_endpoint(appwriteConfig["endpoint"])
 .set_project(appwriteConfig["projectId"])
 .set_key('standard_b02158e7c07adbbbfd9d5be0e6ecc59da5fac70cc540af8232e30cdb7f1deb3a4d3d16b299b60c93c524a664208deb08fe2c5b34409f7ac91bd1ab32173e777e80e7636e90f5c18f0c72a21da54f2fa500a220e0f735ade003c6aae53a069a99deeab00549feac828bb09404c77cdffa2cd7adf4ac54d834b2ab352f2925ac6f'))  

database = Databases(client)
account = Account(client)
storage = Storage(client)
avatar = Avatars(client)

@app.route('/')
def run():
    return ('This is a test')




@app.route('/database/save', methods=['POST'])
def saveData():
    try:
        data = request.get_json()
        collection = data.get('collection')
        data = data.get('data')

        print("Collection: ", collection, "Data: ", data)


        result =  database.create_document(
            appwriteConfig["databaseId"],
            appwriteConfig[collection],
            ID.unique(),
            data
        )
        return jsonify({"data": result})

        # return newData

    except Exception as e:
        print(e)


@app.route('/database/update', methods=['POST'])
def updateData():
    try:
        data = request.get_json()
        collection = data.get('collection')
        ID = data.get('ID')
        data = data.get('data')

        print("UPdating:     Collection: ", collection, "Data: ", data, "ID", ID)


        result =  database.update_document(
            appwriteConfig["databaseId"],
            appwriteConfig[collection],
            ID,
            data
        )
        return jsonify({"data": result})

        # return newData

    except Exception as e:
        print(e)



@app.route('/database/delete', methods=['POST'])
def deleteData():
    try:
        data = request.get_json()
        collection = data['collection']
        ID = data['ID']

        print("Deleting: ", collection, ID)

        database.delete_document(
            database_id=appwriteConfig['databaseId'],
            collection_id=appwriteConfig[collection],
            document_id=ID
        )
        print("Document deleted successfully.")
        return jsonify({"success": True})

    except Exception as e:
        print("Error: ", e)
        return jsonify({"success": False})



        


@app.route('/database/fetch', methods=['POST'])
def fetchAll():
    try:
        data = request.get_json()
        collection = data.get('collection')
        ID = data.get("ID")
        query = data.get('query')
        query2 = data.get("query2")
        order = data.get("order")
        limit = data.get("limit")
        offset = data.get('offset')
        print("Received", collection, ID, query, query2, order, limit, offset)

        if ID:
            result = database.list_documents(
                database_id=appwriteConfig["databaseId"],
                collection_id=appwriteConfig[collection],
                queries=[Query.equal('$id', ID)]
            ) 
        elif query: 
            if limit:
                if order: 
                    if query2:
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[
                                Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]),
                                Query.equal(query2[1], query2[2]) if query2[0] == 'equals' else Query.contains(query2[1], query2[2]),
                                Query.offset(offset),
                                Query.order_desc(order[1]) if order[0] == "descending" else Query.order_asc(order[1]),
                                Query.limit(limit)
                            ]
                        )

                    else:
                        print("YEs")
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]), 
                                     Query.offset(offset), 
                                     Query.limit(limit), 
                                     Query.order_desc(order[1]) if order[0] == "descending" else Query.order_asc(order[1])]
                        )
                else: 
                    if query2:
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]),
                                    Query.equal(query2[1], query2[2]) if query2[0] == 'equals' else Query.contains(query2[1], query2[2]),
                                    Query.offset(offset),
                                    Query.limit(limit),
                                    ]
                        )

                    else:
                        print("YEs")
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]), Query.offset(offset), Query.limit(limit)]
                        )
                   
            else: 
                print("No LIMIT")
                if order: 
                    print("YEs, Order")
                    if query2:
                        print("Yes, order 2")
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]),
                                    Query.equal(query2[1], query2[2]) if query2[0] == 'equals' else Query.contains(query2[1], query2[2]),
                                    Query.offset(offset),
                                    Query.order_desc(order[1]) if order[0] == "descending" else Query.order_asc(order[1]),
                                    ]
                        )

                    else:
                        print("YEs")
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]),
                                     Query.offset(offset), 
                                     Query.order_desc(order[1]) if order[0] == "descending" else Query.order_asc(order[1])]
                        )
                else: 
                    print("No order")
                    if query2:
                        
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]),
                                    Query.equal(query2[1], query2[2]) if query2[0] == 'equals' else Query.contains(query2[1], query2[2]),
                                    Query.offset(offset),
                                    ]
                        )

                    else:
                        print("YEs")
                        result = database.list_documents(
                            database_id=appwriteConfig["databaseId"],
                            collection_id=appwriteConfig[collection],
                            queries=[Query.equal(query[1], query[2]) if query[0] == 'equals' else Query.contains(query[1], query[2]), Query.offset(offset)]
                        )
        else: 
            result = database.list_documents(
                database_id=appwriteConfig["databaseId"],
                collection_id=appwriteConfig[collection],
            )
        return jsonify({"data": result})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})



@app.route('/feed/fetch', methods=['GET'])
def fetchFeed():
    try:
        print("⚡ Fetching feed data...")

        

        def random_ten(items):
            random.shuffle(items)
            return items[:10]

        # ---------- Fetch all shops and products ----------
        shops = database.list_documents(
            database_id=appwriteConfig["databaseId"],
            collection_id=appwriteConfig["shopCollectionId"],
        ).get('documents', [])

        products = database.list_documents(
            database_id=appwriteConfig["databaseId"],
            collection_id=appwriteConfig["productCollectionId"],
        ).get('documents', [])

        # ---------- Clean up None values ----------
        for s in shops:
            s['views'] = s.get('views') or 0
            s['isFeatured'] = bool(s.get('isFeatured'))
            s['isNew'] = bool(s.get('isNew'))
        for p in products:
            p['heart'] = p.get('heart') or 0
            p['isFeatured'] = bool(p.get('isFeatured'))
            p['isNew'] = bool(p.get('isNew'))

        # ---------- Build sections ----------
        forYouShops = random_ten(shops)
        forYouProducts = random_ten(products)

        sponsoredShops = [s for s in shops if s['isFeatured']]
        sponsoredProducts = [p for p in products if p['isFeatured']]
        sponsoredShops = random_ten(sponsoredShops)
        sponsoredProducts = random_ten(sponsoredProducts)

        popularShops = sorted(shops, key=lambda s: s['views'], reverse=True)[:10]
        popularProducts = sorted(products, key=lambda p: p['heart'], reverse=True)[:10]

        newShops = [s for s in shops if s['isNew']]
        newProducts = [p for p in products if p['isNew']]
        newShops = random_ten(newShops)
        newProducts = random_ten(newProducts)

        # ---------- Build categories ----------
        categories = {}
        all_categories = set(
            [s.get('category') for s in shops if s.get('category')] +
            [p.get('category') for p in products if p.get('category')]
        )

        for cat in all_categories:
            catShops = [s for s in shops if s.get('category') == cat]
            catProducts = [p for p in products if p.get('category') == cat]
            categories[cat] = [random_ten(catShops), random_ten(catProducts)]

        # ---------- Construct final feed ----------
        feed = {
            "forYou": [forYouShops, forYouProducts],
            "sponsored": [sponsoredShops, sponsoredProducts],
            "popular": [popularShops, popularProducts],
            "new": [newShops, newProducts],
            "categories": categories
        }


        return jsonify(feed)

    except Exception as e:
        print("❌ Error fetching feed:", e)
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(port=5000, debug=True)