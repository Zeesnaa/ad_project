from fastapi import HTTPException
def throwUserNotFound():
    raise HTTPException(status_code=404,detail="USER NOT FOUND")
def throwInvalidParameter(parameter : str):
    raise HTTPException(status_code=400,detail=f"{parameter.upper()} IS AN INVALID PARAMETER")
def throwNullParameter(parameter : str):
    raise HTTPException(status_code=400,detail=f"{parameter.upper()} CANNOT BE NULL")