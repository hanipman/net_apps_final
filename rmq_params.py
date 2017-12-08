rmq_params = {
    "vhost": "test",
    "username": "pi",
    "password": "raspberry",
    "exchanges": {"apptoserver", "servertostorage", "servertogame", "gametoserver"},
    "queuesGame": {"player1", "player2", "board"},
    "queuesStorage": {"store"}
}
