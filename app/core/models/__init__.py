import os

from ...common import read_properties_file

sql_scripts = read_properties_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mysql/sql.properties'))

from .mysql import (add_test_visitor,
                    get_test_visitor_id,
                    MySQLConnectionManager)

from .redis import (check_if_visitor_key_exists, set_session_expiry, remove_session_from_visitor,
                    get_unifonic_public_id, remove_redis_bot_channel_configuration, get_conversation_from_redis)
