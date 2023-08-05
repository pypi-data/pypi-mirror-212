import os
if not os.environ.get("LOTR_API_KEY"):
    os.environ["LOTR_API_KEY"] = "1"

from lotr_sdk.sdk import LotrSdk
from .mock_data import *


def test_get_all_movies(monkeypatch):
    sdk = LotrSdk()
    monkeypatch.setattr(sdk.movie, "_get", mock_get_all_movies)
    resp = sdk.movie.get_all()
    assert len(resp.movies) == 5
    assert resp.movies[0].academyAwardNominations


def test_get_movie(monkeypatch):
    sdk = LotrSdk()
    monkeypatch.setattr(sdk.movie, "_get", mock_get_movie)
    resp = sdk.movie.get_by_id("5cd95395de30eff6ebccde5d")
    assert resp._id
    assert resp.academyAwardNominations


def test_get_all_quotes(monkeypatch):
    sdk = LotrSdk()
    monkeypatch.setattr(sdk.quote, "_get", mock_get_all_quotes)
    resp = sdk.quote.get_all()
    assert len(resp.quotes) == 183
    assert resp.quotes[0].dialog


def test_get_quote(monkeypatch):
    sdk = LotrSdk()
    monkeypatch.setattr(sdk.quote, "_get", mock_get_quote)
    resp = sdk.quote.get_by_id("5cd96e05de30eff6ebcce7e9")
    assert resp._id
    assert resp.dialog


def test_get_all_quotes_by_movie(monkeypatch):
    sdk = LotrSdk()
    monkeypatch.setattr(sdk.quote, "_get", mock_get_quotes_by_movie)
    resp = sdk.quote.get_by_movie_id("5cd95395de30eff6ebccde5d")
    assert len(resp.quotes) == 872
    assert resp.quotes[0].dialog
