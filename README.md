# Streamlit RedisConnection

Connect to [Redis](https://redis.io/) and other compatible databases ([KeyDB](https://docs.keydb.dev/), [DragonflyDB](https://www.dragonflydb.io/), [LedisDB](https://ledisdb.io/), [SSDB](https://github.com/ideawu/ssdb), [ARDB](https://github.com/yinqiwen/ardb)) from your [Streamlit](https://streamlit.io/) app.



## Installation

`pip install git+https://github.com/mobarski/st_redis_connection`



## Quick demonstration

```python
import streamlit as st
from st_redis_connection import RedisConnection

redis = st.experimental_connection("my_redis", type=RedisConnection)
db = redis.client()
cnt = db.incr('my-counter')
st.metric('Views', cnt)
```



## Main methods



#### client()

`connection.client() -> redis.Redis | redis.Sentinel | redis.RedisCluster`

Get Redis client object that will be used to issue commands to the server.

More info about it's methods [here](https://redis.readthedocs.io/en/latest/commands.html).



#### lock()

`connection.lock(name, timeout=None, sleep=0.1, blocking=True, blocking_timeout=None, thread_local=True) -> redis.lock.Lock`

A shared, distributed Lock using Redis.

More info [here](https://redis.readthedocs.io/en/latest/lock.html).



## Configuration

The connection configuration can be:

- passed via connection kwargs
- passed through environmental variables
- stored in Streamlit's [secrets.toml](https://docs.streamlit.io/library/advanced-features/secrets-management) file (~/.streamlit/secrets.toml on Linux)

You can find more information about managing connections in [this section](https://docs.streamlit.io/library/advanced-features/connecting-to-data#global-secrets-managing-multiple-apps-and-multiple-data-stores) of Streamlit documentation **and some examples below**.

Most important parameters:

- `host` - server host (default: 'localhost')
- `port` - server port (default: 6379)
- `username` - user name (default: default)
- `password` - user password
- `db` - numeric id of the database (default: 0)
- `from_url` - configuration passed via URL. More info [here](https://redis.readthedocs.io/en/latest/connections.html#redis.Redis.from_url)
- `type` - Redis client type used in the connection:
  - `redis` (default) - redis.Redis
  - `sentinel` - redis.Sentinel
  - `cluster` - redis.RedisCluster

You can read more about connecting to Redis [here](https://redis.readthedocs.io/en/latest/connections.html).



## Usage examples



##### simple_app.py

```python
import streamlit as st
from st_redis_connection import RedisConnection

redis = st.experimental_connection("my_redis", type=RedisConnection)
db = redis.client()

cnt = db.incr('my-counter')
st.metric('Views', cnt)
```



##### demo_app.py

You can find live demo of this app [here](https://redis-connection-demo.streamlit.app/)

```python
# NOTE: for simplicity, this is far from being a good example of *how* to use Redis.

import streamlit as st
from st_redis_connection import RedisConnection

N_CLICKS = 100 # number of clicks to enable the reset button

redis = st.experimental_connection("redis", type=RedisConnection)
db = redis.client()

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
```



## Configuration Examples



##### connection kwargs

```python
REDIS_URL = "rediss://default:this-is-my-password@my-redis-host:25061"
redis = st.experimental_connection('', type=RedisConnection, from_url=REDIS_URL)
```

```python
redis = st.experimental_connection('', type=RedisConnection, host='my-host', port=1234, password='my-password', db=2)
```



##### secrets.toml

```toml
[connections.my_redis]
from_url = "rediss://default:this-is-my-password@my-redis-host:25061/1"

[connections.redis2_db3]
host = "my-redis-host2"
port = 6379
password = "password-for-this-instance"
db = 3

[connections.redis3_sen]
type = "sentinel"
sentinels = [("localhost", 26379)]
password = "another-password"

[connections.redis_cluster]
type = "cluster"
```



##### environmental variables

```bash
my_redis_from_url = "rediss://default:this-is-my-password@my-redis-host:25061/1"

redis2_db3_host = "my-redis-host2"
redis2_db3_port = 25061
redis2_db3_password = "password-for-this-instance"
redis2_db3_db = 3

# NOTE: currently Redis sentinels cannot be configured via env. variables
# NOTE: currently Redis clusters  cannot be configured via env. variables
```





