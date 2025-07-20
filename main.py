from graph import create_graph

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"ruta": "../friendly-bot"})
    print(result)
    print("README.md generado exitosamente.")