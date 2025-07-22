from config.graph import create_graph

repository_location = "../friendly-bot"

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"route": repository_location})
    print(result)
    print("README.md generado exitosamente.")