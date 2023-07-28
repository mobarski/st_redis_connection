# NOTE: for simplicity, this is far from being a good example of *how* to use Redis.

import streamlit as st
from st_redis_connection import RedisConnection

N_CLICKS = 100 # number of clicks to enable the reset button

redis = st.experimental_connection("redis", type=RedisConnection)
db = redis.client()

# XXX
st.write(st.secrets)
import os
st.write(os.environ)
st.write(redis._secrets)
st.stop()
# /XXX

clicks1 = int(db.get('clicks1') or 0)
clicks2 = int(db.get('clicks2') or 0)
views   = int(db.get('views')   or 1)

st.markdown('# Redis connection demo')
c1,c2,c3 = st.columns(3)

b1 = c1.button('Click me.')
b2 = c2.button('No! Click me!')
b3 = c3.button('Reset stats',
               disabled = clicks1 + clicks2 < N_CLICKS,
               help = f'Reset all stats to zero. Enbled after {N_CLICKS} clicks.')

if b1: db.incr('clicks1')
if b2: db.incr('clicks2')
if b3:
    db.set('clicks1', 0)
    db.set('clicks2', 0)
    db.set('views',   1)

if b1 or b2 or b3:
    st.experimental_rerun()
else:
    db.incr('views')

c1.metric('button 1 clicks', clicks1)
c2.metric('button 2 clicks', clicks2)
c3.metric('total views', views)
