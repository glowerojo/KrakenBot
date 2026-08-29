import json


def test_daily_trade_limit_blocks_sixth_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    account = {
        "balance": 100.00,
        "trades": 0,
        "wins": 0,
        "losses": 0,
        "total_profit": 0.00,
        "position": None,
        "trades_today": 4,
        "daily_loss": 0.00,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    fifth_trade = risk_manager.record_trade()
    sixth_trade = risk_manager.record_trade()

    final_account = json.loads(account_path.read_text())

    assert fifth_trade is True
    assert sixth_trade is False
    assert final_account["trades_today"] == 5
