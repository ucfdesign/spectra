import base64 
import json
import zlib

class SurveyorResponse:

    def __init__(self, fpath):
        if not fpath.endswith('.tdform'):
            raise Exception('Unexpected file extension.')

        b64string = open(fpath).read()
        decoded_data = base64.b64decode(b64string)
        self.__dict__ = json.loads(decoded_data)


if __name__ == '__main__':
    import sys
    response = SurveyorResponse(sys.argv[1])
    assert type(response.__dict__) == type({})
    print(json.dumps(response.__dict__, indent=4))