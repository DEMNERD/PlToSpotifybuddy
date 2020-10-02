import base64
from datetime import datetime



def generate_tokens():
    now = int(datetime.now().timestamp())
    refreshToken = accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    accessToken += base64.b64encode(('{"spotify_id":"guest","iat": %s, "exp":%s}' % (now, now+600)).encode()).decode('ascii')[:-2]
    refreshToken += base64.b64encode(('{"spotify_id":"guest","iat": %s, "exp":%s}' % (now, now+86400)).encode()).decode('ascii')[-2]
    accessToken += '.Oce5LYHyuNoC0Z6LNKIjkGuU37yAa8n3-s7w1cbQPeU'
    refreshToken += '.IzIi4VMwi_yOBnZ9LVnL-tEmaniyYEdd52FWfaKmH7w'
    return '{"accessToken": "%s", "refreshToken": "%s"}' % (accessToken, refreshToken)

