import uvicorn
if __name__ == '__main__':
    uvicorn.run('ManualLoginAuth.asgi:application', reload=True)
