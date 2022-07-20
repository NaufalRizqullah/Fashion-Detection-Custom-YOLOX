from fastapi import APIRouter

test_router = APIRouter()

@test_router.get("/testing")
def test_return():

    return {"Mode": 'Testing'}