# from flask import request, jsonify
# import firebase_admin
# from firebase_admin import credentials, auth, firestore

# # Initialize Firebase with your service account credentials
# cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
# firebase_admin.initialize_app(cred)

# # Verify Firebase Authentication tokens
# id_token = 'user-id-token'
# decoded_token = auth.verify_id_token(id_token)
# uid = decoded_token['uid']
# print(f'User ID: {uid}')


# db = firestore.client()

# # Add data to Firestore
# doc_ref = db.collection('users').document('user-id')
# doc_ref.set({
#     'name': 'John Doe',
#     'email': 'john.doe@example.com'
# })

# # Read data from Firestore
# doc = doc_ref.get()
# if doc.exists:
#     print(f'Document data: {doc.to_dict()}')
# else:
#     print('No such document!')


# @app.route('/verify_token', methods=['POST'])
# def verify_token():
#     token = request.json['token']
#     try:
#         decoded_token = auth.verify_id_token(token)
#         return jsonify({'uid': decoded_token['uid']}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 401