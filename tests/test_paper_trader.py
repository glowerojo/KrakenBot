import importlib
import json


def test_stop_loss(tmp_path, monkeypatch):
    account_path = tmp_path / "account.json"

    account = {
        "balance": 100.00,
        "trades": 0,
        "wins": 0,
        "losses": 0,
        "total_profit": 0.00,
        "position": None,
        "daily_loss": 0.00,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import paper_trader
    importlib.reload(paper_trader)

    paper_trader.open_trade("ETHUSD", 2500.00)
    paper_trader.check_trade(2475.00)

    final_account = json.loads(account_path.read_text())

    assert final_account["balance"] == 99.50
    assert final_account["trades"] == 1
    assert final_account["wins"] == 0
    assert final_account["losses"] == 1
    assert final_account["total_profit"] == -0.50
    assert final_account["daily_loss"] == 0.50
    assert final_account["position"] is None


def test_take_profit(tmp_path, monkeypatch):
    account_path = tmp_path / "account.json"

    account = {
        "balance": 100.00,
        "trades": 0,
        "wins": 0,
        "losses": 0,
        "total_profit": 0.00,
        "position": None,
        "daily_loss": 0.00,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import paper_trader
    importlib.reload(paper_trader)

    paper_trader.open_trade("ETHUSD", 2500.00)
    paper_trader.check_trade(2550.00)

    final_account = json.loads(account_path.read_text())

    assert final_account["balance"] == 101.00
    assert final_account["trades"] == 1
    assert final_account["wins"] == 1
    assert final_account["losses"] == 0
    assert final_account["total_profit"] == 1.00
    assert final_account["position"] is None
