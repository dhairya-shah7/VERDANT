import urllib.request
import json

payload = {
    "url": "https://sauce-demo.myshopify.com/products/grey-jacket",
    "pageTitle": "Sauce Demo - Grey Jacket",
    "domSummary": {
        "totalNodes": 620,
        "landmarks": {"header": {"tag": "header"}, "main": {"childCount": 2}},
        "stats": {"buttons": 6, "inputs": 2, "links": 14, "images": 8},
        "brokenImages": [],
        "emptyButtons": []
    },
    "domSkeleton": "<header><nav></nav></header><main><div class='product-gallery'></div><button class='add-to-cart'>Add to Cart</button></main>",
    "logs": [
        {
            "type": "console_error",
            "message": "Uncaught TypeError: Cannot read properties of undefined (reading 'variant_id') at addToCart (main.js:142:18)"
        }
    ],
    "networkEvents": [
        {
            "method": "POST",
            "url": "https://sauce-demo.myshopify.com/cart/add.js",
            "status": 422,
            "statusText": "Unprocessable Entity"
        }
    ],
    "layoutAnomalies": []
}

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/extension/ingest",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
res = urllib.request.urlopen(req)
data = json.loads(res.read().decode())
print("Action:", data.get("action_type"))
print("Summary:", data.get("spoken_summary"))
print("Root cause:", data.get("root_cause"))
print("Edits count:", len(data.get("edits", [])))
print("Model:", data.get("model_used"))
