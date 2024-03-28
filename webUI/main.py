from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient(f"mongodb://root:password@localhost:27778")
db = client["orders"]

categories = ["categories", "customers", "employees", "order_details", "orders", "products", "shippers", "suppliers"]


@app.get("/")
async def root():
    return {"message": "UwU"}


@app.get("/api/data/{category}")
def get_data(category: str):
    if category in categories:
        collection = db[category]
        data = list(collection.find())
        print(data)
        return dumps(data)
    else:
        raise HTTPException(status_code=404, detail="Category not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
