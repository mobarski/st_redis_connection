from streamlit.connections import ExperimentalBaseConnection
import redis
import os

# REF: https://docs.streamlit.io/library/advanced-features/connecting-to-data
# REF: https://experimental-connection.streamlit.app/Build_your_own
# REF: https://github.com/streamlit/files-connection

# REF: https://redis.readthedocs.io/en/stable/connections.html
# REF: https://redis.readthedocs.io/en/stable/commands.html
# REF: https://redis.readthedocs.io/en/stable/lua_scripting.html
# REF: https://redis.readthedocs.io/en/stable/lock.html#module-redis.lock

REDIS_OPTIONS = \
"host port db password socket_timeout socket_connect_timeout socket_keepalive socket_keepalive_options connection_pool " \
"unix_socket_path encoding encoding_errors charset errors decode_responses retry_on_timeout retry_on_error " \
"ssl ssl_keyfile ssl_certfile ssl_cert_reqs ssl_ca_certs ssl_ca_path ssl_ca_data ssl_check_hostname ssl_password " \
"ssl_validate_ocsp ssl_validate_ocsp_stapled ssl_ocsp_context ssl_ocsp_expected_cert max_connections " \
"single_connection_client health_check_interval client_name username retry redis_connect_func credential_provider".split(' ')

REDIS_CLUSTER_OPTIONS = \
"host port startup_nodes cluster_error_retry_attempts retry require_full_coverage reinitialize_steps "\
"read_from_replicas dynamic_startup_nodes url address_remap".split(' ')

REDIS_SENTINEL_OPTIONS = \
"sentinels min_other_sentinels sentinel_kwargs".split(' ') + REDIS_OPTIONS

TYPE_TO_CLIENT_CLASS = {'redis':redis.Redis, 'cluster':redis.RedisCluster, 'sentinel':redis.Sentinel}
TYPE_TO_OPTIONS = {'redis':REDIS_OPTIONS, 'cluster':REDIS_CLUSTER_OPTIONS, 'sentinel':REDIS_SENTINEL_OPTIONS}

# PARAMETERS PRIORITIES:
# 1. function kwargs
# 2. environment variables
# 3. secrets.toml


class RedisConnection(ExperimentalBaseConnection):

    def _connect(self, **kwargs):
        kw = kwargs.copy()
        
        # client type
        if 'type' in kw:
            typ = kw.pop('type')
        elif f'{self._connection_name}_type' in os.environ:
            typ = os.environ[f'{self._connection_name}_type']
        elif 'type' in self._secrets:
            typ = self._secrets['type']
        else:
            typ = 'redis'
        
        # kw parameters
        client_class = TYPE_TO_CLIENT_CLASS[typ]
        options = TYPE_TO_OPTIONS[typ]
        for k in options:
            if k in kw: continue
            k_env = f'{self._connection_name}_{k}'
            if k_env in os.environ:
                kw[k] = os.environ[k_env]
            elif k in self._secrets:
                kw[k] = self._secrets[k]
        
        # client instance
        if 'from_url' in kw:
            from_url = kw.pop('from_url')
            return client_class.from_url(from_url, **kw)
        else:
            return client_class(**kw)


    def client(self):
        "redis client object"
        return self._instance
    

    def lock(self, name, **kwargs):
        "distributed lock (https://redis.readthedocs.io/en/stable/lock.html#module-redis.lock)"
        redis.lock.Lock(self._instance, name, **kwargs)

