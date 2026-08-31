import json
from datetime import datetime, timedelta


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

    from datetime import datetime, timedelta

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


def test_cooldown_blocks_recent_trade_and_allows_expired_cooldown(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    from datetime import datetime, timedelta, timedelta

    today = datetime.now().strftime("%Y-%m-%d")

    recent_account = {
        "balance": 100.00,
        "trades": 1,
        "wins": 1,
        "losses": 0,
        "total_profit": 1.00,
        "position": None,
        "trades_today": 1,
        "daily_loss": 0.00,
        "last_reset": today,
        "last_trade_time": (datetime.now() - timedelta(minutes=10)).isoformat(),
    }

    account_path.write_text(json.dumps(recent_account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    blocked = risk_manager.can_trade()

    assert blocked is False

    expired_account = {
        **recent_account,
        "last_trade_time": (datetime.now() - timedelta(minutes=31)).isoformat(),
    }

    account_path.write_text(json.dumps(expired_account))

    allowed = risk_manager.can_trade()

    assert allowed is True


def test_daily_stats_reset_on_new_day(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    from datetime import datetime, timedelta, timedelta

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    account = {
        "balance": 95.00,
        "trades": 5,
        "wins": 0,
        "losses": 5,
        "total_profit": -5.00,
        "position": None,
        "trades_today": 5,
        "daily_loss": 5.00,
        "last_reset": yesterday,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    reset_account = risk_manager.reset_daily_stats(account)

    today = datetime.now().strftime("%Y-%m-%d")

    saved_account = json.loads(account_path.read_text())

    assert reset_account["trades_today"] == 0
    assert reset_account["daily_loss"] == 0
    assert reset_account["last_reset"] == today
    assert saved_account["trades_today"] == 0
    assert saved_account["daily_loss"] == 0
    assert saved_account["last_reset"] == today


def test_can_trade_allows_valid_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    from datetime import datetime, timedelta, timedelta

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 100.00,
        "trades": 2,
        "wins": 2,
        "losses": 0,
        "total_profit": 2.00,
        "position": None,
        "trades_today": 2,
        "daily_loss": 1.00,
        "last_reset": today,
        "last_trade_time": (datetime.now() - timedelta(minutes=31)).isoformat(),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    assert allowed is True

    final_account = json.loads(account_path.read_text())

    assert final_account["trades_today"] == 2
    assert final_account["daily_loss"] == 1.00


def test_record_trade_updates_trade_count_and_timestamp(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    account = {
        "balance": 100.00,
        "trades": 2,
        "wins": 2,
        "losses": 0,
        "total_profit": 2.00,
        "position": None,
        "trades_today": 2,
        "daily_loss": 0.00,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    recorded = risk_manager.record_trade()

    final_account = json.loads(account_path.read_text())

    assert recorded is True
    assert final_account["trades_today"] == 3
    assert final_account["balance"] == 100.00
    assert final_account["daily_loss"] == 0.00
    assert final_account["last_trade_time"]




def test_recorded_trade_starts_cooldown(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    account = {
        "balance": 100.00,
        "trades": 2,
        "wins": 2,
        "losses": 0,
        "total_profit": 2.00,
        "position": None,
        "trades_today": 2,
        "daily_loss": 0.00,
        "last_reset": datetime.now().strftime("%Y-%m-%d"),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    recorded = risk_manager.record_trade()

    assert recorded is True

    blocked = risk_manager.can_trade()

    assert blocked is False

    final_account = json.loads(account_path.read_text())

    assert final_account["trades_today"] == 3
    assert final_account["last_trade_time"]




def test_new_day_resets_daily_limits_but_preserves_active_cooldown(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    recent_trade = (datetime.now() - timedelta(minutes=10)).isoformat()

    account = {
        "balance": 95.00,
        "trades": 5,
        "wins": 0,
        "losses": 5,
        "total_profit": -5.00,
        "position": None,
        "trades_today": 5,
        "daily_loss": 5.00,
        "last_reset": yesterday,
        "last_trade_time": recent_trade,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    final_account = json.loads(account_path.read_text())

    assert allowed is False
    assert final_account["trades_today"] == 0
    assert final_account["daily_loss"] == 0
    assert final_account["last_reset"] == datetime.now().strftime("%Y-%m-%d")
    assert final_account["last_trade_time"] == recent_trade




def test_can_trade_allows_account_with_no_previous_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 100.00,
        "trades": 0,
        "wins": 0,
        "losses": 0,
        "total_profit": 0.00,
        "position": None,
        "trades_today": 0,
        "daily_loss": 0.00,
        "last_reset": today,
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    assert allowed is True

    final_account = json.loads(account_path.read_text())

    assert final_account["trades_today"] == 0
    assert final_account["daily_loss"] == 0.00
    assert "last_trade_time" not in final_account




def test_daily_loss_just_below_limit_allows_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 95.01,
        "trades": 4,
        "wins": 0,
        "losses": 4,
        "total_profit": -4.99,
        "position": None,
        "trades_today": 4,
        "daily_loss": 4.99,
        "last_reset": today,
        "last_trade_time": (
            datetime.now() - timedelta(minutes=31)
        ).isoformat(),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    assert allowed is True

    final_account = json.loads(account_path.read_text())

    assert final_account["daily_loss"] == 4.99
    assert final_account["trades_today"] == 4




def test_daily_loss_just_above_limit_blocks_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 94.99,
        "trades": 4,
        "wins": 0,
        "losses": 4,
        "total_profit": -5.01,
        "position": None,
        "trades_today": 4,
        "daily_loss": 5.01,
        "last_reset": today,
        "last_trade_time": (
            datetime.now() - timedelta(minutes=31)
        ).isoformat(),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    assert allowed is False

    final_account = json.loads(account_path.read_text())

    assert final_account["daily_loss"] == 5.01
    assert final_account["trades_today"] == 4




def test_daily_trade_limit_just_below_limit_allows_trade(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 100.00,
        "trades": 4,
        "wins": 4,
        "losses": 0,
        "total_profit": 4.00,
        "position": None,
        "trades_today": 4,
        "daily_loss": 0.00,
        "last_reset": today,
        "last_trade_time": (
            datetime.now() - timedelta(minutes=31)
        ).isoformat(),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    allowed = risk_manager.can_trade()

    assert allowed is True

    final_account = json.loads(account_path.read_text())

    assert final_account["trades_today"] == 4
    assert final_account["daily_loss"] == 0.00




def test_record_trade_blocks_at_daily_trade_limit(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 100.00,
        "trades": 5,
        "wins": 5,
        "losses": 0,
        "total_profit": 5.00,
        "position": None,
        "trades_today": 5,
        "daily_loss": 0.00,
        "last_reset": today,
        "last_trade_time": (
            datetime.now() - timedelta(minutes=31)
        ).isoformat(),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    recorded = risk_manager.record_trade()

    assert recorded is False

    final_account = json.loads(account_path.read_text())

    assert final_account["trades_today"] == 5
    assert final_account["last_trade_time"] == account["last_trade_time"]




def test_record_trade_allows_trade_just_below_daily_limit(tmp_path, monkeypatch):

    account_path = tmp_path / "account.json"

    today = datetime.now().strftime("%Y-%m-%d")

    account = {
        "balance": 100.00,
        "trades": 4,
        "wins": 4,
        "losses": 0,
        "total_profit": 4.00,
        "position": None,
        "trades_today": 4,
        "daily_loss": 0.00,
        "last_reset": today,
        "last_trade_time": (
            datetime.now() - timedelta(minutes=31)
        ).isoformat(),
    }

    account_path.write_text(json.dumps(account))

    monkeypatch.chdir(tmp_path)

    import risk_manager

    recorded = risk_manager.record_trade()

    assert recorded is True

    final_account = json.loads(account_path.read_text())

    assert final_account["trades_today"] == 5
    assert final_account["last_trade_time"] != account["last_trade_time"]


