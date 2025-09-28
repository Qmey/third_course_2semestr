def launch_game(game_name):
    try:
        game = __import__(f"games.{game_name}.game", fromlist=["run"])
        game.run()
    except Exception as e:
        print(f"[Ошибка запуска {game_name}]:", e)
