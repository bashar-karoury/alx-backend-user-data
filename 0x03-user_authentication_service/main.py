#!/usr/bin/env python3
""" integration test module"""
import requests
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    form_data = {
        "email": email,
        "password": password,
    }
    response = requests.post('http://localhost:5000/users', data=form_data)
    assert (response.status_code == 200)


def log_in_wrong_password(email: str, password: str) -> None:
    form_data = {
        "email": email,
        "password": password,
    }
    response = requests.post('http://localhost:5000/sessions', data=form_data)
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    form_data = {
        "email": email,
        "password": password,
    }
    response = requests.post('http://localhost:5000/sessions', data=form_data)
    assert (response.status_code == 200)
    session_id = response.cookies.get("session_id")
    assert (session_id is not None)
    return session_id


def profile_unlogged() -> None:
    response = requests.get('http://localhost:5000/profile')
    assert (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    cookies = {
        "session_id": session_id
    }
    response = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert (response.status_code == 200)
    assert (response.json() == {"email": EMAIL})


def log_out(session_id: str) -> None:
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(
        'http://localhost:5000/sessions', cookies=cookies)
    assert (response.status_code == 200)


def reset_password_token(email: str) -> str:
    form_data = {
        "email": email
    }
    response = requests.post(
        'http://localhost:5000/reset_password', data=form_data)
    response_data = response.json()
    reset_token = response_data.get("reset_token")
    assert (response_data.get('email') == email)
    assert (response.status_code == 200)
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    form_data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(
        'http://localhost:5000/reset_password', data=form_data)
    response_data = response.json()
    reset_token = response_data.get("reset_token")
    assert (response_data.get('email') == email)
    assert (response_data.get('message') == "Password updated")
    assert (response.status_code == 200)


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
