from sanic import Sanic, response

app = Sanic(name="contacts_app")

# Test data

contacts = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "a@a.com",
    },
    {
        "id": 2,
        "name": "Jane Doe",
        "email": "b@b.com",
    },
    {
        "id": 3,
        "name": "Jim Doe",
        "email": "c@c.com",
    }
]

@app.route("/", methods=["GET"])
async def home(request):
    return response.html('''<h1>Creating Contacts API</h1>''')

@app.route("/api/v1/contacts/all", methods=["GET"])
async def api_all(request):
    return response.json(contacts)

@app.route("/api/v1/contacts", methods=["GET"])
async def api_username(request):
    if 'name' in request.args:
        name = str(request.args['name'])[0]
    else:
        return response.text("No username provided. Especify one")

    results = []

    for contact in contacts:
        if contact['name'] == name:
            results.append(contact)

    return response.json(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)