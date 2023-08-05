from .tools_error import ToolsError
import datetime
import json
import decimal
import uuid
import functools


class Tools():
    def __init__(self):
        pass

    def json_serial(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return obj

    def make_response(self, status_code: int = 200, body: any = {}):
        return {
            'statusCode': status_code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(body, default=self.json_serial),
        }

    def load_body(self, event):
        if 'body' not in event:
            raise ToolsError.LoadBodyError()

        if event['body'] is None:
            raise ToolsError.LoadBodyError()

        return json.loads(event['body'])

    def uuidgen(self):
        return str(uuid.uuid4())

    def get_utc_time_now(self, tz=datetime.timezone.utc):
        return datetime.datetime.now(tz=tz)

    def get_timestamp(self, timespec: str = 'milliseconds'):
        now = self.get_utc_time_now()
        return now.isoformat(timespec=timespec)

    def logger_authorized_user(self, logger):
        def _logger_authorized_user(func):
            @functools.wraps(func)
            def wrapper(event, context):
                if 'requestContext' in event:
                    if 'authorizer' in event['requestContext']:
                        if 'claims' in event['requestContext']['authorizer']:
                            if 'sub' in event['requestContext']['authorizer']['claims']:
                                logger.append_keys(
                                    authorizer_claims_sub=event['requestContext']['authorizer']['claims']['sub']
                                )
                return func(event, context)
            return wrapper
        return _logger_authorized_user
