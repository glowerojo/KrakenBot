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


def test_daily_loss_limit_blocks_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    from datetime import datetime

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 95.00,
        "trades": 5,
        "wins": 0,
        "losses": 5,
        "total_profit": -5.00,
        "position": None,
        "trades_today": 5,
        "daily_loss": 5.00,
        "last_reset": today,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    final_account = json.loads(account_path.read_text())

    assert allowed is False
    assert final_account["daily_loss"] == 5.00
    assert final_account["trades_today"] == 5
